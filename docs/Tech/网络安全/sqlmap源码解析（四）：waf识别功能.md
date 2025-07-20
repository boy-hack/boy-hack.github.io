---
order: 1504593794
---
# sqlmap源码解析（四）：waf识别功能

前面三节主要分析了sqlmap的初始化工作和一些配置工作。现在来看看sqlmap其中一个waf识别功能是怎么实现的。

## waf识别流程

sqlmap源码读了几天，发现大量的工作并不在sql注入上面，而是在一些小地方，细节方面处理的很好。我觉得这样一个优秀的软件很值得我学习。看了waf识别的代码，心中稍微有些概念了，凭我的理解列一下。

  * 初始化载入脚本，这个是在`init()`方法中的`_setWafFunctions()`函数，载入的脚本存放在一个list 列表中调用
  * 执行`checkWaf()`函数开始识别。先使用payload


```python 
# Payload used for checking of existence of IDS/IPS/WAF (dummier the better)
IDS_WAF_CHECK_PAYLOAD = "AND 1=1 UNION ALL SELECT 1,NULL,'<script>alert(\"XSS\")</script>',table_name FROM information_schema.tables WHERE 2>1--/**/; EXEC xp_cmdshell('cat ../../../etc/passwd')#"

```

探测一下，然后根据响应时间来判断是否存在waf

  * 使用`identifyWaf()`函数识别waf，这个函数里面用了python的装饰器和语法糖，不是很看得懂代码。。但是大概功能就是动态调用之前的脚本列表中的模块
  * 初始化脚本中加载的脚本，一个列子：


```python 
#!/usr/bin/env python

"""
Copyright (c) 2006-2017 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""

import re

from lib.core.settings import WAF_ATTACK_VECTORS

__product__ = "360 Web Application Firewall (360)"

def detect(get_page):
    retval = False

    for vector in WAF_ATTACK_VECTORS:
        page, headers, code = get_page(get=vector)
        retval = re.search(r"wangzhan\.360\.cn", headers.get("X-Powered-By-360wzb", ""), re.I) is not None
        retval |= code == 493 and "/wzws-waf-cgi/" in (page or "")
        if retval:
            break

    return retval

```

可以看出，这个脚本是通过识别服务器返回的header来识别waf的

## 代码解读

找到那几个关键函数，大致的框架就已经知道了。然后写了几个注释

### 初始化部分

在`lib\core\option.py`的`init()`函数中，调用了`_setWafFunctions()`函数进行相关初始化的操作。
```python 
def _setWafFunctions():
    """
    Loads WAF/IPS/IDS detecting functions from script(s)
    """

    if conf.identifyWaf:
        for found in glob.glob(os.path.join(paths.SQLMAP_WAF_PATH, "*.py")):
            dirname, filename = os.path.split(found)
            dirname = os.path.abspath(dirname)
            # 取出waf目录中.py结尾的文件，获取目录与文件名
            # 目录取绝对路径目录
            # 排除 __init__.py 文件
            if filename == "__init__.py":
                continue

            debugMsg = "loading WAF script '%s'" % filename[:-3]
            logger.debug(debugMsg)

            if dirname not in sys.path:
                sys.path.insert(0, dirname)
            # 如果目录不在python的搜索环境中就加入进来

            try:
                # 如果系统环境中模块和此模块重名了，则删除
                if filename[:-3] in sys.modules:
                    del sys.modules[filename[:-3]]
                module = __import__(filename[:-3].encode(sys.getfilesystemencoding() or UNICODE_ENCODING))
                # 然后动态的引入该模块
                # __import__() 函数用于动态加载类和函数
            except ImportError, msg:
                raise SqlmapSyntaxException("cannot import WAF script '%s' (%s)" % (filename[:-3], msg))

            _ = dict(inspect.getmembers(module))
            # inspect.getmembers获取模块所有成员。返回的是元组，用dict转换为字典的形式
            if "detect" not in _:
                # 如果模块中没有detect函数则抛出错误
                errMsg = "missing function 'detect(get_page)' "
                errMsg += "in WAF script '%s'" % found
                raise SqlmapGenericException(errMsg)
            else:
                kb.wafFunctions.append((_["detect"], _.get("__product__", filename[:-3])))
                # 加入detect方法 和 描述__product__
        kb.wafFunctions = sorted(kb.wafFunctions, key=lambda _: "generic" in _[1].lower())

```

### 识别部分

在`lib\controller\controller.py`的`start()`中调用了识别waf相关的代码
``` 
checkWaf() # 检测waf，以后在详细分析

if conf.identifyWaf:
    identifyWaf() # 识别waf

```

先看`checkWaf()`函数，用于分析是否是waf
```python 
def checkWaf():
    """
    Reference: http://seclists.org/nmap-dev/2011/q2/att-1005/http-waf-detect.nse
    """

    if any((conf.string, conf.notString, conf.regexp, conf.dummy, conf.offline, conf.skipWaf)):
        return None

    _ = hashDBRetrieve(HASHDB_KEYS.CHECK_WAF_RESULT, True)
    if _ is not None:
        if _:
            warnMsg = "previous heuristics detected that the target "
            warnMsg += "is protected by some kind of WAF/IPS/IDS"
            logger.critical(warnMsg)
        return _

    # 如果之前数据库有数据就取出返回

    if not kb.originalPage:
        return None

    infoMsg = "checking if the target is protected by "
    infoMsg += "some kind of WAF/IPS/IDS"
    logger.info(infoMsg)

    retVal = False
    payload = "%d %s" % (randomInt(), IDS_WAF_CHECK_PAYLOAD)
    # payload是一个随机数字 和一个专门用于检测waf的payload

    value = "" if not conf.parameters.get(PLACE.GET) else conf.parameters[PLACE.GET] + DEFAULT_GET_POST_DELIMITER
    value += agent.addPayloadDelimiters("%s=%s" % (randomStr(), payload))

    pushValue(conf.timeout)
    conf.timeout = IDS_WAF_CHECK_TIMEOUT

    try:
        retVal = Request.queryPage(place=PLACE.GET, value=value, getRatioValue=True, noteResponseTime=False, silent=True)[1] < IDS_WAF_CHECK_RATIO
        # 响应时间如果小于设置阈值，则可以判断是有waf
        # 美名其曰：启发式检测
    except SqlmapConnectionException:
        retVal = True
    finally:
        kb.matchRatio = None
        conf.timeout = popValue()

    if retVal:
        warnMsg = "heuristics detected that the target "
        warnMsg += "is protected by some kind of WAF/IPS/IDS"
        logger.critical(warnMsg)

        if not conf.identifyWaf:
            message = "do you want sqlmap to try to detect backend "
            message += "WAF/IPS/IDS? [y/N] "

            if readInput(message, default='N', boolean=True):
                conf.identifyWaf = True

        if conf.timeout == defaults.timeout:
            logger.warning("dropping timeout to %d seconds (i.e. '--timeout=%d')" % (IDS_WAF_CHECK_TIMEOUT, IDS_WAF_CHECK_TIMEOUT))
            conf.timeout = IDS_WAF_CHECK_TIMEOUT

    hashDBWrite(HASHDB_KEYS.CHECK_WAF_RESULT, retVal, True)

    return retVal

```

如果判断是waf的话会调用`identifyWaf()`来识别这个waf。
```python 
def identifyWaf():

    # 判断是否进行waf识别
    if not conf.identifyWaf:
        return None

    # 看有没有初始化中加载的脚本，没有就报错
    if not kb.wafFunctions:
        setWafFunctions()

    kb.testMode = True

    infoMsg = "using WAF scripts to detect "
    infoMsg += "backend WAF/IPS/IDS protection"
    logger.info(infoMsg)

    # 这里用了python的装饰器，主要起的作用是是可以让python调用getPage函数，并且可以设定多个参数
    @cachedmethod
    def _(*args, **kwargs):
        page, headers, code = None, None, None
        try:
            pushValue(kb.redirectChoice)
            kb.redirectChoice = REDIRECTION.NO
            if kwargs.get("get"):
                kwargs["get"] = urlencode(kwargs["get"])
            kwargs["raise404"] = False
            kwargs["silent"] = True
            page, headers, code = Request.getPage(*args, **kwargs)
        except Exception:
            pass
        finally:
            kb.redirectChoice = popValue()
        return page or "", headers or {}, code

    retVal = []

    # 从函数表中调用函数
    for function, product in kb.wafFunctions:
        try:
            logger.debug("checking for WAF/IPS/IDS product '%s'" % product)
            found = function(_)
            # 调用函数处理
        except Exception, ex:
            errMsg = "exception occurred while running "
            errMsg += "WAF script for '%s' ('%s')" % (product, getSafeExString(ex))
            logger.critical(errMsg)

            found = False

        if found:
            errMsg = "WAF/IPS/IDS identified as '%s'" % product
            logger.critical(errMsg)

            retVal.append(product)

    if retVal:
        # 如果未发现，一些报告收尾工作
        if kb.wafSpecificResponse and len(retVal) == 1 and "unknown" in retVal[0].lower():
            handle, filename = tempfile.mkstemp(prefix=MKSTEMP_PREFIX.SPECIFIC_RESPONSE)
            os.close(handle)
            with openFile(filename, "w+b") as f:
                f.write(kb.wafSpecificResponse)

            message = "WAF/IPS/IDS specific response can be found in '%s'. " % filename
            message += "If you know the details on used protection please "
            message += "report it along with specific response "
            message += "to 'dev@sqlmap.org'"
            logger.warn(message)

        message = "are you sure that you want to "
        message += "continue with further target testing? [y/N] "
        choice = readInput(message, default='N', boolean=True)

        if not conf.tamper:
            warnMsg = "please consider usage of tamper scripts (option '--tamper')"
            singleTimeWarnMessage(warnMsg)

        if not choice:
            raise SqlmapUserQuitException
    else:
        warnMsg = "WAF/IPS/IDS product hasn't been identified"
        logger.warn(warnMsg)

    kb.testType = None
    kb.testMode = False

    return retVal

```

## 总结

在函数`identifyWaf()`中使用的python装饰器`@cachedmethod`，没有看懂，后来结合着waf的脚本一起看，才稍微明白的它的大概功能。大概就是就是将参数装入字典然后在后面传入给脚本一个函数来实现功能。因为传入的这个函数可能会有多个参数，所以这个装饰器大概处理参数的把。

总之，看了sqlmap源代码后感觉自己还需要很大的提升啊，什么时候我的`w8scan`能写的像sqlmap一样就好了。
