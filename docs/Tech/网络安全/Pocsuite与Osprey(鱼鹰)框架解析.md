---
order: 1534831469
---
# Pocsuite与Osprey(鱼鹰)框架解析

## Pocsuite框架简介以及功能

Pocsuite框架是由知道创宇开发的远程漏洞测试框架，基于pocsuite的SDK进行POC/EXP的开发，可以很方便的检验或者攻击。  


### Pocsuite目录结构
```bash
Pocsuite.
│  pcs-attack.py   Attack 模式
│  pcs-console.py  交互式控制台模式(console)
│  pcs-verify.py   Verify 模式
│  pocsuite.py     命令行模式(cli)
│  README.md
│  setup.py
│
├─.github
│      ISSUE_TEMPLATE.md
│
├─docs
│  │  CHANGELOG.md
│  │  CODING.md
│  │  COPYING
│  │  INTEGRATE.md
│  │  THANKS.md
│  │  USAGE.md
│  │
│  ├─images
│  │      poc_json_attack.png
│  │      poc_json_verify.png
│  │
│  └─translations
│          README-zh.md
│          USAGE-zh.md
│
├─modules   Pocsuit demo poc
│      detect_doublepulsar.py
│      dlink_command_php_exec_noauth.py
│      wordpress_core_4_6_rce.py
│
└─pocsuite
    │  pocsuite_attack.py  Attack 模式
    │  pocsuite_cli.py     命令行模式(cli)
    │  pocsuite_console.py 交互式控制台模式(console)
    │  pocsuite_verify.py  Verify 模式
    │  __init__.py
    │
    ├─api
    │      cannon.py   Class pocsuite.api.cannon.Cannon returns details of  error and failure of a PoC 
    │      packet.py   内置接口API
    │      poc.py      内置接口API
    │      rcGen.py    存储seebug token
    │      request.py  内置接口API
    │      seebug.py   登陆seebug API
    │      utils.py    内置utils接口API
    │      webshell.py 生成webshell后门
    │      x.py        Zoomeye Seebug相关API
    │      zoomeye.py  
    │      __init__.py
    │
    ├─data
    │      password-top100.txt  弱密码 Top100
    │      password-top1000.txt
    │      token.conf
    │      user-agents.txt
    │
    ├─lib
    │  │  __init__.py
    │  │
    │  ├─controller
    │  │      check.py       检测POC参数相关信息以及需要安装的python库
    │  │      controller.py  线程并发控制
    │  │      setpoc.py      设置POC文件
    │  │      __init__.py
    │  │
    │  ├─core
    │  │      common.py      公共函数库
    │  │      consoles.py    console模式
    │  │      convert.py     替换print输出模式
    │  │      data.py        全局变量存放
    │  │      datatype.py    
    │  │      defaults.py
    │  │      enums.py       枚举类型
    │  │      exception.py   异常类型
    │  │      handlejson.py  
    │  │      log.py         log输出
    │  │      option.py      解析选项
    │  │      poc.py         POC基类 OUPUT基类
    │  │      register.py    注册POC
    │  │      revision.py    
    │  │      settings.py    设置信息
    │  │      threads.py     线程设置信息
    │  │      update.py
    │  │      __init__.py
    │  │
    │  ├─parse
    │  │      parser.py      选项解析
    │  │      __init__.py
    │  │
    │  ├─request
    │  │      basic.py
    │  │      requestspatch.py
    │  │      __init__.py
    │  │
    │  └─utils
    │          funs.py          function函数     
    │          packet.py        socket相关模块
    │          parseopener.py   
    │          password.py      获取弱密码Top100
    │          randoms.py       生成随机字符串/数字
    │          require.py       检测必须参数等
    │          requirescheck.py
    │          seebug.py        Seebug相关接口
    │          versioncheck.py  Python版本相关验证
    │          zoomeye.py       zoomeye相关接口
    │          __init__.py
    │
    ├─tests
    │      test_pocsuite.py
    │      __init__.py
    │
    └─thirdparty
        │  __init__.py
        │
        ├─ansistrm
        │      ansistrm.py
        │      __init__.py
        │
        ├─argparse
        │      argparse.py
        │      __init__.py
        │
        ├─colorama
        │      ansi.py
        │      ansitowin32.py
        │      initialise.py
        │      win32.py
        │      winterm.py
        │      __init__.py
        │
        ├─odict
        │      odict.py
        │      __init__.py
        │
        ├─oset
        │      LICENSE.txt
        │      pyoset.py
        │      _abc.py
        │      __init__.py
        │
        ├─prettytable
        │      CHANGELOG
        │      COPYING
        │      MANIFEST.in
        │      PKG-INFO
        │      prettytable.py
        │      README
        │      __init__.py
        │
        ├─pyparsing
        │  │  CHANGES
        │  │  HowToUsePyparsing.html
        │  │  LICENSE
        │  │  PKG-INFO
        │  │  pyparsing.py
        │  │  pyparsingClassDiagram.JPG
        │  │  pyparsingClassDiagram.PNG
        │  │  README
        │  │  robots.txt
        │  │  setup.py
        │  │  __init__.py
        │  │
        │  └─htmldoc
        │          api-objects.txt
        │          class-tree.html
        │          crarr.png
        │          epydoc.css
        │          epydoc.js
        │          frames.html
        │          help.html
        │          identifier-index.html
        │          index.html
        │          module-tree.html
        │          pyparsing.pyparsing-module.html
        │          pyparsing.pyparsing-pysrc.html
        │          pyparsing.pyparsing.And-class.html
        │          pyparsing.pyparsing.CaselessKeyword-class.html
        │          pyparsing.pyparsing.CaselessLiteral-class.html
        │          pyparsing.pyparsing.CharsNotIn-class.html
        │          pyparsing.pyparsing.Combine-class.html
        │          pyparsing.pyparsing.Dict-class.html
        │          pyparsing.pyparsing.Each-class.html
        │          pyparsing.pyparsing.Empty-class.html
        │          pyparsing.pyparsing.FollowedBy-class.html
        │          pyparsing.pyparsing.Forward-class.html
        │          pyparsing.pyparsing.GoToColumn-class.html
        │          pyparsing.pyparsing.Group-class.html
        │          pyparsing.pyparsing.Keyword-class.html
        │          pyparsing.pyparsing.LineEnd-class.html
        │          pyparsing.pyparsing.LineStart-class.html
        │          pyparsing.pyparsing.Literal-class.html
        │          pyparsing.pyparsing.MatchFirst-class.html
        │          pyparsing.pyparsing.NoMatch-class.html
        │          pyparsing.pyparsing.NotAny-class.html
        │          pyparsing.pyparsing.OneOrMore-class.html
        │          pyparsing.pyparsing.OnlyOnce-class.html
        │          pyparsing.pyparsing.Optional-class.html
        │          pyparsing.pyparsing.Or-class.html
        │          pyparsing.pyparsing.ParseBaseException-class.html
        │          pyparsing.pyparsing.ParseElementEnhance-class.html
        │          pyparsing.pyparsing.ParseException-class.html
        │          pyparsing.pyparsing.ParseExpression-class.html
        │          pyparsing.pyparsing.ParseFatalException-class.html
        │          pyparsing.pyparsing.ParserElement-class.html
        │          pyparsing.pyparsing.ParseResults-class.html
        │          pyparsing.pyparsing.ParseSyntaxException-class.html
        │          pyparsing.pyparsing.QuotedString-class.html
        │          pyparsing.pyparsing.RecursiveGrammarException-class.html
        │          pyparsing.pyparsing.Regex-class.html
        │          pyparsing.pyparsing.Regex.compiledREtype-class.html
        │          pyparsing.pyparsing.SkipTo-class.html
        │          pyparsing.pyparsing.StringEnd-class.html
        │          pyparsing.pyparsing.StringStart-class.html
        │          pyparsing.pyparsing.Suppress-class.html
        │          pyparsing.pyparsing.Token-class.html
        │          pyparsing.pyparsing.TokenConverter-class.html
        │          pyparsing.pyparsing.Upcase-class.html
        │          pyparsing.pyparsing.White-class.html
        │          pyparsing.pyparsing.Word-class.html
        │          pyparsing.pyparsing.WordEnd-class.html
        │          pyparsing.pyparsing.WordStart-class.html
        │          pyparsing.pyparsing.ZeroOrMore-class.html
        │          pyparsing_2.0.2_docs.zip
        │          redirect.html
        │          toc-everything.html
        │          toc-pyparsing.pyparsing-module.html
        │          toc.html
        │
        ├─requests
        │  │  adapters.py
        │  │  api.py
        │  │  auth.py
        │  │  cacert.pem
        │  │  certs.py
        │  │  compat.py
        │  │  cookies.py
        │  │  exceptions.py
        │  │  hooks.py
        │  │  models.py
        │  │  sessions.py
        │  │  status_codes.py
        │  │  structures.py
        │  │  utils.py
        │  │  __init__.py
        │  │
        │  └─packages
        │      │  __init__.py
        │      │
        │      ├─chardet
        │      │      big5freq.py
        │      │      big5prober.py
        │      │      chardetect.py
        │      │      chardistribution.py
        │      │      charsetgroupprober.py
        │      │      charsetprober.py
        │      │      codingstatemachine.py
        │      │      compat.py
        │      │      constants.py
        │      │      cp949prober.py
        │      │      escprober.py
        │      │      escsm.py
        │      │      eucjpprober.py
        │      │      euckrfreq.py
        │      │      euckrprober.py
        │      │      euctwfreq.py
        │      │      euctwprober.py
        │      │      gb2312freq.py
        │      │      gb2312prober.py
        │      │      hebrewprober.py
        │      │      jisfreq.py
        │      │      jpcntx.py
        │      │      langbulgarianmodel.py
        │      │      langcyrillicmodel.py
        │      │      langgreekmodel.py
        │      │      langhebrewmodel.py
        │      │      langhungarianmodel.py
        │      │      langthaimodel.py
        │      │      latin1prober.py
        │      │      mbcharsetprober.py
        │      │      mbcsgroupprober.py
        │      │      mbcssm.py
        │      │      sbcharsetprober.py
        │      │      sbcsgroupprober.py
        │      │      sjisprober.py
        │      │      universaldetector.py
        │      │      utf8prober.py
        │      │      __init__.py
        │      │
        │      └─urllib3
        │          │  connection.py
        │          │  connectionpool.py
        │          │  exceptions.py
        │          │  fields.py
        │          │  filepost.py
        │          │  poolmanager.py
        │          │  request.py
        │          │  response.py
        │          │  _collections.py
        │          │  __init__.py
        │          │
        │          ├─contrib
        │          │      ntlmpool.py
        │          │      pyopenssl.py
        │          │      __init__.py
        │          │
        │          ├─packages
        │          │  │  ordered_dict.py
        │          │  │  six.py
        │          │  │  six.pyc
        │          │  │  __init__.py
        │          │  │
        │          │  └─ssl_match_hostname
        │          │          _implementation.py
        │          │          __init__.py
        │          │
        │          └─util
        │                  connection.py
        │                  request.py
        │                  response.py
        │                  retry.py
        │                  ssl_.py
        │                  timeout.py
        │                  url.py
        │                  __init__.py
        │
        ├─socks     socket代理相关
        │      PKG-INFO
        │      setup.py
        │      socks.py
        │      sockshandler.py
        │      __init__.py
        │
        └─termcolor
                termcolor.py
                __init__.py

```

## Pocsuite模块(payload)加载

### 远程加载

pocsuite远程加载poc，通过访问seebug API，API返回seebug SSV-ID以及源、POC代码，程序保存文件到模块目录命名为{ssv-id}.py，然后通过本地加载加载模块执行

### 本地加载

pocsuite通过对命令中pocFile参数解析，pocFile可以为一个文件或者一个目录，通过loadPoc加载pocFile。  
`pocsuite\lib\controller\setpoc.py`中`loadPoc`定义如下
```python 
def loadPoc(pocFile):
    if pocFile.endswith(".pyc"):
        conf.isPycFile = True

    if conf.isPocString:
        poc = conf.pocFile
        if not conf.pocname:
            if conf.pocFile:
                conf.pocname = os.path.split(conf.pocFile)[1]
            else:
                errMsg = "Use pocString must provide pocname"
                logger.log(CUSTOM_LOGGING.ERROR, errMsg)
        pocname = conf.pocname
    else:
        pocname = os.path.split(pocFile)[1]
        poc = readFile(pocFile)

    if not conf.isPycFile:
        if not re.search(POC_REGISTER_REGEX, poc):
            warnMsg = "poc: %s register is missing" % pocname
            logger.log(CUSTOM_LOGGING.WARNING, warnMsg)
            className = getPocClassName(poc)
            poc += POC_REGISTER_STRING.format(className)

        retVal = multipleReplace(poc, POC_IMPORTDICT)
    else:
        retVal = poc
    return {pocname: retVal}

```

loadPoc对poc代码进行检测，以正则`register\(.*\)`检测代码,如果失败则使用下列代码format  
`POC_REGISTER_STRING = "\nfrom pocsuite.api.poc import register\nregister({})"`  

```python 
POC_IMPORTDICT = {
    "from pocsuite.net import": "from pocsuite.lib.request.basic import",
    "from pocsuite.poc import": "from pocsuite.lib.core.poc import",
    "from pocsuite.utils import register": "from pocsuite.lib.core.register import registerPoc as register",
}

```

进行替换  
所有poc代码最后都存入了kb.pocs字典。执行模块，调用模块内的`registerPoc`将pocname,以及poc函数注册到kb.registeredPocs中。  
对`kb.registeredPocs`检测是否存在下列接口
```python 
POC_ATTRS = ("vulID", "version", "author", "vulDate", "name", "appVersion", "desc", "createDate", "updateDate", "references", "appPowerLink", "vulType", "appName")

```

最后将url与poc函数以`url,pocFunction,pocName`的形式组合到kb.targets
``` 
kb.targets.put((url, copy.copy(poc), pocname))

```

## Pocsuite并发控制

pocsuite并发控制比较简单，主要以多线程为主，位于`pocsuite\lib\core\threads.py` `runThreads`函数，函数简化后如下：
```python 
def runThreads(numThreads, threadFunction):
    threads = []

    try:
        if numThreads > 1:
            if startThreadMsg:
                infoMsg = "starting %d threads" % numThreads
                logger.log(CUSTOM_LOGGING.SYSINFO, infoMsg)

        else:
            threadFunction()
            return

        for numThread in xrange(numThreads):
            thread = threading.Thread(target=threadFunction, name=str(numThread))
            setDaemon(thread)

            try:
                thread.start()
            except threadError, errMsg:
                pass

            threads.append(thread)

        # And wait for them to all finish
        alive = True
        while alive:
            alive = False
            for thread in threads:
                if thread.isAlive():
                    alive = True
                    time.sleep(0.1)

    except KeyboardInterrupt:
        pass

    except (PocsuiteConnectionException, PocsuiteValueException), errMsg:
        pass

    except:
        pass

```

`pocThreads`函数意思为从kb.targets取出目标执行,然后通过runThreads(numThreads, pocThreads)执行并发 

## Pocsuite 内置接口

Pocsuite POC开发需要以POCBase为基类，填写poc相关信息变量`("vulID", "version", "author", "vulDate", "name", "appVersion", "desc", "createDate", "updateDate", "references", "appPowerLink", "vulType", "appName")`

重写其中的 `_attack`以及 `_verify`方法。最后调用`register(TestPOC)`。  


## Pocsuite优点以及缺点

Pocsuite优点为强制性要求填写poc相关的所有参数，所有POC需要规范代码，方便扫描器统一处理和调度。支持console模式  


## Osprey 简介以及功能

> 「Osprey」是TCC研发的一款开源漏洞检测框架，应用在斗象科技旗下产品网藤CRS（www.riskivy.com/product/crs），并已同步到Github开源社区。 

Osprey是一个可扩展的开源漏洞检测与利用框架(Python3开发)，Osprey框架可供使用者在渗透测试、漏洞检测、漏洞扫描等场景中应用。  


## Osprey 编写规范和要求说明

osprey使用Python3开发，PoC脚本也应使用py3.

### 目录结构
```
Osprey.
│  BasePoc.py                  POC模板基类
│  config.yaml                 配置文件
│  osprey.py                启动文件
│  README.md
│  requirements.txt
│  settings.py                程序相关设置文件
│  setup.py
│  utils.py                    POC插件常用函数
│
├─console
│      osprey-console.py    osprey-console 控制命令模式
│      __init__.py
│
├─core
│      PocManager.py        POC插件加载运行相关控制
│      RunPoc.py            POC插件运行机制
│      __init__.py
│
├─doc
│      PoC_specification.md
│      web_api_tutorial.md
│
├─docker
│      docker-compose.yml
│      dockerfile-osprey
│      osprey-web.png
│      start-osprey.sh
│
├─lib
│  │  log.py
│  │  payload.py            header头
│  │  requests.py            封装requests
│  │  __init__.py
│  │
│  └─core
│          cmdparser.py        命令行解析
│          config.py        config加载
│          datatype.py        AttribDict字典类
│          db.py            数据库相关
│          display.py        展示结果相关类
│          gevent.py        gevent协程类
│          prepare.py        命令行预处理
│          req.py            requests更上层封装
│          __init__.py
│
├─pocs
│      vb_2017_0060_Metinfo_5_3_17_X_Rewrite_url_Sql_Injection.py
│      __init__.py
│
├─thirdparty
│  │  __init__.py
│  │
│  └─requests_toolbelt
│      │  exceptions.py
│      │  sessions.py
│      │  streaming_iterator.py
│      │  _compat.py
│      │  __init__.py
│      │
│      ├─adapters
│      │      appengine.py
│      │      fingerprint.py
│      │      host_header_ssl.py
│      │      socket_options.py
│      │      source.py
│      │      ssl.py
│      │      __init__.py
│      │
│      ├─auth
│      │      guess.py
│      │      handler.py
│      │      http_proxy_digest.py
│      │      _digest_auth_compat.py
│      │      __init__.py
│      │
│      ├─cookies
│      │      forgetful.py
│      │      __init__.py
│      │
│      ├─downloadutils
│      │      stream.py
│      │      tee.py
│      │      __init__.py
│      │
│      ├─multipart
│      │      decoder.py
│      │      encoder.py
│      │      __init__.py
│      │
│      ├─threaded
│      │      pool.py
│      │      thread.py
│      │      __init__.py
│      │
│      └─utils
│              deprecated.py
│              dump.py
│              formdata.py
│              user_agent.py
│              __init__.py
│
└─web
    │  check.py                check_task_id 检测任务id
    │  osprey-web.py        osprey-web WEB接口
    │  requirements.txt
    │  SubProcess.py        封装SUBPROCESS
    │  task.py                命令行模式执行命令
    │  __init__.py
    │
    └─static
            index.html

```

### PoC脚本命名规范

文件名称由VID和英文描述两部分组成，VID号以“vb _year_xxxx”为格式，英文描述需遵循驼峰命名法，使用“_ ”连接，尽量体现存在漏洞的组建、版本、路径、漏洞类型等信息。

由于osprey调用PoC脚本时是通过–v参数指定选用某个PoC的，因此文件名格式必须正确包含VID号且唯一。

命名示例：vb_2017_0060_Metinfo_5_3_17_X_Rewrite_url_Sql_Injection.py

### POC编写Demo
```python
from BasePoc import BasePoc               # 导入BasePoc，是PoC脚本实现的类中必须继承的基类
from utils import tree, highlight, req    # utils实现了一些常用函数，可以直接导入方便使用
from urllib.parse import urljoin          # 导入其他的脚本需要用到的模块


POC_NAME = "MetinfoXRewriteurlSQLInjection"    # PoC脚本中实现的类名，osprey架将根据POC_NAME去实例化类以达到调用的效果，因此类名应与该变量名保持相同


class MetinfoXRewriteurlSQLInjection(BasePoc):

    # PoC实现类，需继承BasePoc
    # 为PoC填充poc_info、scan_info、test_case三个字典中的基本信息

    poc_info = {
        'poc': {
            'Id': 'vb_2017_0060',    # PoC的VID编号
            'vbid': '',
            'Name': 'Metinfo 5.3.17 X-Rewrite-url SQL Injection',    # PoC名称
            'Author': 'ice.liao',    # PoC作者
            'Create_date': '2017-08-15',    # PoC创建时间
            },

        'vul': {
            'Product': 'Metinfo',    # 漏洞所在产品名称
            'Version': '5.3.17',    # 产品的版本号
            'Type': 'SQL Injection',    # 漏洞类型
            'Severity': 'critical',    # 漏洞危害等级low/medium/high/critical
            'isWeb' : True,    # 是否Web漏洞
            'Description': '''
                MetInfo是中国长沙米拓信息技术有限公司的一套使用PHP和Mysql开发的内容管理系统（CMS）
                危害: 网站数据库信息可造成泄漏，管理员密码可被远程攻击者获得
                修复建议： 前往http://www.metinfo.cn/download/下载最新版本
            ''',    # 漏洞简要描述
            'DisclosureDate': '2017-08-11',    # PoC公布时间
        }
    }

    # scan_info信息可以保持默认，相关参数如target/mode/verbose在osprey中都可以通过命令行参数设置
    scan_info = {
        'Target': '',    # 目标网站域名
        'Mode': 'verify',    # verify或exploit
        'Verbose': True,    # 是否打印详细信息
        'Error': '',    # 检测失败时可用于记录相关信息
        'Success': False,    # 是否检出漏洞，若检出请更新该值为True
        'risk_category': 'sec_vul',
        'Ret': tree()    # 可用于记录额外的一些信息
    }

    test_case = {
        'Need_fb': False,
        'Vuln': [],    # 列表格式的测试URL
        'Not_vuln': [],    # 同上
    }


    def verify(self, first=False):
        # 漏洞验证方法（mode=verify）
        target = self.scan_info.get("Target", "")    # 获取测试目标
        verbose = self.scan_info.get("Verbose", False)   # 是否打印详细信息

        # 以下是PoC的检测逻辑
        url = urljoin(target,'index.php?lang=Cn&index=1')
        payload = "1/2/zxxza' union select 1,2,3,md5(0x11),5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29#/index.php"
        headers = {
            "X-Rewrite-Url": payload
        }

        location = ""
        # 使用req做HTTP请求的发送和响应的处理，req是TCC框架将requests的HTTP请求方法封装成统一的req函数，使用req(url, method, **kwargs)，参数传递同requests
        resp = req(url, 'get', headers=headers, allow_redirects=False)
        if resp is not None:
            location = resp.headers.get("Location", "")

        if "47ed733b8d10be225eceba344d533586" in location:
            self.scan_info['Success'] = True    # 漏洞存在，必须将该字段更新为True（必须）
            self.scan_info['Ret']['VerifyInfo']['URL'] = url    # 记录漏洞相关的一些额外信息（可选）
            self.scan_info['Ret']['VerifyInfo']['DATA'] = "X-Rewrite-Url:" + payload
            if verbose:
                highlight('[*] Metinfo 5.3.17 X-Rewrite-url SQL Injection found')    # 打印高亮信息发现漏洞，其他可用方法包括info()/warn()/error()/highlight()方法分别打印不同等级的信息


    def exploit(self, first=False):
        # 漏洞利用方法（mode=verify）
        self.verify(first=first)

```

class继承自`BasePoc.py`的`BasePoc` Class.重写其中的`verify`方法和`attack`方法。

### utils.py提供内置函数调用
```python
from utils import *

now()    # 返回当前时间，格式为：“YYYY-MM-DD HH:MM:SS,MS”，逗号后为毫秒

is_same_domain(url1, url2)    # 判断2个URL是否为同域，此处并非严格的同源。端口不同或协议不同均判断为同域

get_absolute_url(base, url)    # 获取URL的绝对路径

retrieve_url_from_page(p_url, keyword, depth)    # 从p_url页面中查找获取含指定关键字的URL链接

retrieve_url_from_spider(spider)   # 从爬虫URL文件中获取URL链接

normalize_url(url)    # 格式化不规范的URL为http://xxx/

valid_status_code(status_code)    # 判断HTTP请求的返回状态码，当状态码为4XX-5XX时返回False

target_handler(target, port, payload)    # 对url进行port和payload的拼接,返回一个列表

get_scan_info(scan_info)    # 返回scan_info中的Target和Verbose数据

isIP(target)    # 判断输入数据是否是IP

get_html(url, **kwargs)    # 发起GET请求取回Response body，注意返回的数据格式为bytes类型

url_join(base, url)    # 对两个路径进行拼接

info(message)    # 打印info日志

warn(message)    # 打印warn日志

error(message)    # 打印error日志

highlight(message)    # 打印highlight日志

```

## Osprey 插件加载机制

`Osprey\core\PocManager.py` `PoCManager`定义了POC插件加载以及运行的相关机制`_load_poc`
```python 
def _load_poc(self, poc_vid):
    specify_pocs = {}
    poc_names = [name for name in os.listdir(self.fb.poc_setting.dir_name) if name.startswith("vb_") and name.endswith(".py")]
    # 遍历出目录内的插件
    if poc_vid == ["all"]:
        for poc_name in poc_names:
            vid = "_".join(poc_name.split("_")[:3])
            specify_pocs[vid] = poc_name
    else:
        for vid in poc_vid:
            for poc_name in poc_names:
                if vid in poc_name:
                    specify_pocs[vid] = poc_name
                    break
    # poc_vid 为all时，加载全部插件，否则加载制定vid插件

    poc_classes = collections.defaultdict(list)
    # poc_classes = {vid1: [name1, class1], vid2: [name2, class2], vid3: [name3, class3]}
    for vid, poc in specify_pocs.items():
        try:
            module_name = "{}.{}".format(self.fb.poc_setting.dir_name, poc)[:-3].split("/")[-1]
            __import__(module_name)
            # 动态引入模块
            tmp = sys.modules[module_name]
            # 获得模块实例
            poc_classes[vid] = [module_name, getattr(tmp, getattr(tmp, "POC_NAME"))]
            # 存储模块实例和类实例
        except ImportError as e:
            log.warn("Failed to import PoC {}. {}".format(poc, e))
            continue
        except Exception as e:
            log.warn("Failed to load PoC {}. {}".format(poc, e))
            continue
    return poc_classes

```

之后将target和poc_classes组合加入协程队列
```python 
poc_classes = self._load_poc(vids)
result_queue = queue.Queue()

task_queue = queue.Queue()
for target in targets:
    for poc_class in poc_classes.items():
        task_queue.put_nowait([target, poc_class])
        # [target, (vid1, [name1, class1])]

```

## Osprey 并发机制

Osprey的并发使用协程。
```python 
run_poc = [RunPoc(task_queue, task_info, result_queue, self.fb) for i in range(self.fb.poc_setting.thread_num)]
def task():
    p = run_poc.pop()
    try:
        p.start()
    finally:
        run_poc.append(p)
    # 保持不中断
start_gevent_pool_skip_empty(self.fb.poc_setting.thread_num, task)

```

`Osprey\lib\core\gevent.py`
``` 
def start_gevent_pool_skip_empty(thread_num, func, *args, **kwargs):
    gevent_pool = Pool(thread_num)
    for i in range(thread_num):
        gevent_pool.spawn(partial(gevent_skip_empty_func, func, *args, **kwargs))
    gevent_pool.join()

def gevent_skip_empty_func(func, *args, **kwargs):
    while True:
        try:
            func(*args, **kwargs)
        except queue.Empty:
            break
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            log.warn(e)
        except Exception:
            log.error(traceback.format_exc())
            continue

```

后面结果结果处理加入到result队列
```python 
results_list = []
results = {task_id: collections.defaultdict(dict)}
while not result_queue.empty():
    # tmp = [poc_name, poc.poc_info, poc.scan_info]
    tmp = result_queue.get_nowait()
    results_list.append(tmp)
    results[task_id][tmp[0]] = {"poc_info": {}, "scan_info": []}
for result in results_list:
    results[task_id][result[0]]["scan_info"].append(result[2])
    if results[task_id][result[0]]["poc_info"]:
        continue
    results[task_id][result[0]]["poc_info"] = result[1]

if task_flag:
    _now = now()[:-4]
    self.db.save_result(task_id, results[task_id], _now)
    self.db.save_basic(task_id, _now)
else:
    return results[task_id]
# 写入数据库或者返回

```

## Osprey WEB接口

osprey-web使用Flask提供Web Service，使用Celery以任务队列的形式调度和下发检测任务。数据库存储使用mongodb,消息队列使用amqp，分布式使用celery
```bash 
$ curl http://127.0.0.1:5000/api/start -d '{"task_id": "TASK_ID", "vid": "vb_ID", "target": "http://x.com/"}'
$ curl http://127.0.0.1:5000/api/result -d '{"task_id": "TASK_ID"}'

```

### Osprey WEB下发任务

web调用任务会调用celery任务`start_task_func`

start_task_func作用为启动子进程填写参数运行`osprey.py`

`Osprey\web\task.py`
```python 
import os
import psutil
import signal
from core.PocManager import PoCManager
from lib.log import logger as log
from settings import PROGRAM, DST_FILE
from web.SubProcess import SubProcess


def start_poc_task(task_data):
    def kill_child_processes(parent_pid, sig=signal.SIGTERM):
        try:
            p = psutil.Process(parent_pid)
        except psutil.NoSuchProcess:
            return
        child_pid = p.children(recursive=True)
        for pid in child_pid:
            os.kill(pid.pid, sig)

    cmd_list = [PROGRAM, DST_FILE]
    cmd_list.extend(['''--target={}'''.format(task_data.get("target", ""))])
    cmd_list.extend(['''--vid={}'''.format(task_data.get("vid", ""))])
    cmd_list.extend(['''--task_id={}'''.format(task_data.get("task_id", ""))])
    cmd_list.extend(['''--mode={}'''.format(task_data.get("mode", "verify"))])
    cmd_list.extend(['''--quiet''' if not task_data.get("verbose", True) else ""])
    cmd_list.extend(['''--cookies={}'''.format(task_data.get("cookies", "x"))])
    cmd_list.extend(['''--proxy={}'''.format(task_data.get("proxy", "x"))])
    cmd_list.extend(['''--headers={}'''.format(task_data.get("headers", "x"))])
    if task_data.get("poc_dir"):
        cmd_list.extend(['''--poc-dir={}'''.format(task_data.get("poc_dir"))])

    manager_process = SubProcess(cmd_list).run()

    # Process timeout
    if manager_process['status'] == 1:
        process = manager_process['proc']
        log.info("process {} is timeout when scanning [{}]-[{}]-[{}],terminating...".format(
            process.pid, task_data.get("task_id"), task_data.get("vid", ""), task_data.get("target", "")))
        PoCManager.exit_write2db(task_data.get("task_id", ""))

        kill_child_processes(process.pid)
        process.kill()
        process.wait()

    if manager_process['status'] == -1:
        process = manager_process['proc']
        log.info("process {} is been revoked when scanning [{}]-[{}].".format(
            process.pid, task_data.get("vid", ""), task_data.get("target", "")))

```

### Osprey WEB获取结果

WEB获取结果通过task_id查询数据库获得。

## Osprey Celery 分布式调度系统

osprey-web中定义了Celery task  
`Osprey\web\osprey-web.py`
```python 
@celery.task(queue="poc-queue")
def start_task_func(task_data):
    start_poc_task(task_data)

```

start_poc_task用于下发任务

## Osprey与Pocsuite异同

两者的POC接口需要按照指定格式编写，插件加载方式上Osprey与Pocsuite都是本地加载(Pocsuite远程加载也是下载到本地再加载)在调用，并发控制上Pocsuite使用多线程，而Osprey使用协程。二者都提供交互式Console接口。  

