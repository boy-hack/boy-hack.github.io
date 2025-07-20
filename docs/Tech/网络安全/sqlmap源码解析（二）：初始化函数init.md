---
order: 1504435081
---
# sqlmap源码解析（二）：初始化函数init

上一贴：sqlmap源码解析（一）：程序入口sqlmap.py

现在看看初始化函数init的内部构造&作了哪些工作 

函数位于 `lib/core/option.py`
```js 
def init():
    """
    Set attributes into both configuration and knowledge base singletons
    based upon command line and configuration file options.
    """
    # 设置属性，基于命令行和配置文件选项。

    _useWizardInterface() # 用户向导程序
    setVerbosity() # 设置debug等级
    _saveConfig() # 将命令行选项保存到sqlmap配置INI文件中
    _setRequestFromFile() # 设置http请求从文件中
    _cleanupOptions() # 清理配置选项
    _cleanupEnvironment() # 清理环境
    _dirtyPatches() # 补丁相关
    _purgeOutput() # 安全删除(purges)输出目录。
    _checkDependencies() # 检测丢失的依赖
    _createTemporaryDirectory() # 创建运行的临时目录
    _basicOptionValidation() # 检测选项是否有效
    _setProxyList() # 设置代理列表
    _setTorProxySettings() # 设置Tor代理
    _setDNSServer() # 设置DNS服务器
    _adjustLoggingFormatter() # 调整日志格式
    _setMultipleTargets() # 如果在多个目标中运行，只定义一种参数
    _setTamperingFunctions() # 设置tamper脚本
    _setWafFunctions() # 载入waf检测脚本
    _setTrafficOutputFP() # 设置记录http日志文件
    _setupHTTPCollector() # 清理http收集
    _resolveCrossReferences()
    _checkWebSocket() # 检测websocket-client模块调用

    parseTargetUrl() # 解析目标url
    parseTargetDirect() # 解析目标DBMS

    if any((conf.url, conf.logFile, conf.bulkFile, conf.sitemapUrl, conf.requestFile, conf.googleDork, conf.liveTest)):
        # 如果设置了上述选项，配置相关http
        _setHTTPTimeout() # 设置超时
        _setHTTPExtraHeaders() # 设置Headers
        _setHTTPCookies() # 设置Cookies
        _setHTTPReferer() # 设置Referer
        _setHTTPHost() # 设置Host
        _setHTTPUserAgent() # 设置UserAgent
        _setHTTPAuthentication() # 设置HTTPAuthentication
        _setHTTPHandlers() # 检查并设置所有HTTP请求的HTTP / SOCKS代理。
        _setDNSCache() # 设置DNS缓存
        _setSocketPreConnect()
        _setSafeVisit() # 检查并设置安全访问选项。
        _doSearch() # 使用搜索平台搜索结果并存储
        _setBulkMultipleTargets()
        _setSitemapTargets() # 解析SitemapTargets中的目标
        _checkTor() # 检测Tor
        _setCrawler() # 设置爬虫
        _findPageForms() # 寻找网页的表单
        _setDBMS() # 强制DBMS选项 
        _setTechnique()

    _setThreads() # 设置现场
    _setOS() # 强制OS
    _setWriteFile() # 写入文件
    _setMetasploit() # Metasploit相关设置
    _setDBMSAuthentication()
    loadBoundaries() # 载入Boundaries
    loadPayloads() # 载入Payloads
    _setPrefixSuffix() # 设置前后缀
    update() # 更新sqlmap
    _loadQueries() # 加载查询的xml /查询
```

  

