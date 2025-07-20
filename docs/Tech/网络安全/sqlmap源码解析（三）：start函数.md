---
order: 1504567938
---
# sqlmap源码解析（三）：start函数

在init()函数中调用了start()函数，如果说Init函数是初始化一些环境信息，那么start函数的作用就是初始和解析HTTP相关的内容，最后由 
```js 
injection = checkSqlInjection(place, parameter, value)
```

检测是否存在sql注入，存在则会返回payload。 

详细分析如下： 
```js 
def start():
    """
    This function calls a function that performs checks on both URL
    stability and all GET, POST, Cookie and User-Agent parameters to
    check if they are dynamic and SQL injection affected
    """
    # 这个函数调用一个功能用于检测是否有sql注入
    if conf.direct:
        initTargetEnv()
        setupTargetEnv()
        action()
        return True

    if conf.url and not any((conf.forms, conf.crawlDepth)):
        kb.targets.add((conf.url, conf.method, conf.data, conf.cookie, None))
        # 添加到目标

    if conf.configFile and not kb.targets:
        # 判断，没有目标就会报错
        errMsg = "you did not edit the configuration file properly, set "
        errMsg += "the target URL, list of targets or google dork"
        logger.error(errMsg)
        return False

    if kb.targets and len(kb.targets) > 1:
        infoMsg = "sqlmap got a total of %d targets" % len(kb.targets)
        logger.info(infoMsg)
        # 打印出目标个数

    hostCount = 0
    initialHeaders = list(conf.httpHeaders)

    for targetUrl, targetMethod, targetData, targetCookie, targetHeaders in kb.targets:
        try:
            # 下面这个判断看网络是否能连接
            if conf.checkInternet:
                infoMsg = "[INFO] checking for Internet connection"
                logger.info(infoMsg)

                if not checkInternet():
                    warnMsg = "[%s] [WARNING] no connection detected" % time.strftime("%X")
                    dataToStdout(warnMsg)

                    while not checkInternet():
                        dataToStdout('.')
                        time.sleep(5)

                    dataToStdout("\n")

            conf.url = targetUrl
            conf.method = targetMethod.upper() if targetMethod else targetMethod
            conf.data = targetData
            conf.cookie = targetCookie
            conf.httpHeaders = list(initialHeaders)
            conf.httpHeaders.extend(targetHeaders or [])
            # 配置HTTP连接的相关参数

            initTargetEnv() # 函数主要就是完成全局变量conf和kb的初始化工作
            parseTargetUrl() # 函数主要完成针对目标网址的解析工作，如获取协议名、路径、端口、请求参数等信息

            testSqlInj = False
            # 测试过的url参数信息会保存到kb.testedParams中，所以在进行test之前，会先判断当前的url是否已经test过
            # 如果没test过的话，则testSqlInj = True，否则testSqlInj = False。
            # 当testSqlInj = False的时候，就不会执行 injection = checkSqlInjection(place, parameter, value)这句代码了。
            if PLACE.GET in conf.parameters and not any([conf.data, conf.testParameter]):
                for parameter in re.findall(r"([^=]+)=([^%s]+%s?|\Z)" % (re.escape(conf.paramDel or "") or DEFAULT_GET_POST_DELIMITER, re.escape(conf.paramDel or "") or DEFAULT_GET_POST_DELIMITER), conf.parameters[PLACE.GET]):
                    paramKey = (conf.hostname, conf.path, PLACE.GET, parameter[0])

                    if paramKey not in kb.testedParams:
                        testSqlInj = True
                        break
            else:
                paramKey = (conf.hostname, conf.path, None, None)
                if paramKey not in kb.testedParams:
                    testSqlInj = True

            if testSqlInj and conf.hostname in kb.vulnHosts:
                if kb.skipVulnHost is None:
                    message = "SQL injection vulnerability has already been detected "
                    message += "against '%s'. Do you want to skip " % conf.hostname
                    message += "further tests involving it? [Y/n]"

                    kb.skipVulnHost = readInput(message, default='Y', boolean=True)

                testSqlInj = not kb.skipVulnHost

            if not testSqlInj:
                infoMsg = "skipping '%s'" % targetUrl
                logger.info(infoMsg)
                continue

            if conf.multipleTargets:
                hostCount += 1

                if conf.forms and conf.method:
                    message = "[#%d] form:\n%s %s" % (hostCount, conf.method, targetUrl)
                else:
                    message = "URL %d:\n%s %s" % (hostCount, HTTPMETHOD.GET, targetUrl)

                if conf.cookie:
                    message += "\nCookie: %s" % conf.cookie

                if conf.data is not None:
                    message += "\n%s data: %s" % ((conf.method if conf.method != HTTPMETHOD.GET else conf.method) or HTTPMETHOD.POST, urlencode(conf.data) if conf.data else "")

                if conf.forms and conf.method:
                    if conf.method == HTTPMETHOD.GET and targetUrl.find("?") == -1:
                        continue

                    message += "\ndo you want to test this form? [Y/n/q] "
                    choice = readInput(message, default='Y').upper()

                    if choice == 'N':
                        continue
                    elif choice == 'Q':
                        break
                    else:
                        if conf.method != HTTPMETHOD.GET:
                            message = "Edit %s data [default: %s]%s: " % (conf.method, urlencode(conf.data) if conf.data else "None", " (Warning: blank fields detected)" if conf.data and extractRegexResult(EMPTY_FORM_FIELDS_REGEX, conf.data) else "")
                            conf.data = readInput(message, default=conf.data)
                            conf.data = _randomFillBlankFields(conf.data)
                            conf.data = urldecode(conf.data) if conf.data and urlencode(DEFAULT_GET_POST_DELIMITER, None) not in conf.data else conf.data

                        else:
                            if targetUrl.find("?") > -1:
                                firstPart = targetUrl[:targetUrl.find("?")]
                                secondPart = targetUrl[targetUrl.find("?") + 1:]
                                message = "Edit GET data [default: %s]: " % secondPart
                                test = readInput(message, default=secondPart)
                                test = _randomFillBlankFields(test)
                                conf.url = "%s?%s" % (firstPart, test)

                        parseTargetUrl()

                else:
                    message += "\ndo you want to test this URL? [Y/n/q]"
                    choice = readInput(message, default='Y').upper()

                    if choice == 'N':
                        dataToStdout(os.linesep)
                        continue
                    elif choice == 'Q':
                        break

                    infoMsg = "testing URL '%s'" % targetUrl
                    logger.info(infoMsg)

            # 该函数主要包含3个子功能：
            # 1.创建保存目标执行结果的目录和文件
            # 2.将get或post发送的数据解析成字典形式，并保存到conf.paramDict中
            # 3.读取session文件（如果存在的话），并提起文件中的数据，保存到kb变量中
            setupTargetEnv()

            if not checkConnection(suppressOutput=conf.forms) or not checkString() or not checkRegexp():
                continue

            checkWaf() # 检测waf，以后在详细分析

            if conf.identifyWaf:
                identifyWaf() # 识别waf

            if conf.nullConnection:
                checkNullConnection()

            if (len(kb.injections) == 0 or (len(kb.injections) == 1 and kb.injections[0].place is None)) \
                and (kb.injection.place is None or kb.injection.parameter is None):

                if not any((conf.string, conf.notString, conf.regexp)) and PAYLOAD.TECHNIQUE.BOOLEAN in conf.tech:
                    # NOTE: this is not needed anymore, leaving only to display
                    # a warning message to the user in case the page is not stable
                    checkStability() # 检测页面是否稳定

                # Do a little prioritization reorder of a testable parameter list
                parameters = conf.parameters.keys()

                # Order of testing list (first to last)
                orderList = (PLACE.CUSTOM_POST, PLACE.CUSTOM_HEADER, PLACE.URI, PLACE.POST, PLACE.GET)

                for place in orderList[::-1]:
                    if place in parameters:
                        parameters.remove(place)
                        parameters.insert(0, place)

                proceed = True
                for place in parameters:
                    # 根据参数level等级是否注入cookie referer user_agent

                    # Test User-Agent and Referer headers only if
                    # --level >= 3
                    skip = (place == PLACE.USER_AGENT and conf.level < 3)
                    skip |= (place == PLACE.REFERER and conf.level < 3)

                    # Test Host header only if
                    # --level >= 5
                    skip |= (place == PLACE.HOST and conf.level < 5)

                    # Test Cookie header only if --level >= 2
                    skip |= (place == PLACE.COOKIE and conf.level < 2)

                    skip |= (place == PLACE.USER_AGENT and intersect(USER_AGENT_ALIASES, conf.skip, True) not in ([], None))
                    skip |= (place == PLACE.REFERER and intersect(REFERER_ALIASES, conf.skip, True) not in ([], None))
                    skip |= (place == PLACE.COOKIE and intersect(PLACE.COOKIE, conf.skip, True) not in ([], None))
                    skip |= (place == PLACE.HOST and intersect(PLACE.HOST, conf.skip, True) not in ([], None))

                    skip &= not (place == PLACE.USER_AGENT and intersect(USER_AGENT_ALIASES, conf.testParameter, True))
                    skip &= not (place == PLACE.REFERER and intersect(REFERER_ALIASES, conf.testParameter, True))
                    skip &= not (place == PLACE.HOST and intersect(HOST_ALIASES, conf.testParameter, True))
                    skip &= not (place == PLACE.COOKIE and intersect((PLACE.COOKIE,), conf.testParameter, True))

                    if skip:
                        continue

                    if kb.testOnlyCustom and place not in (PLACE.URI, PLACE.CUSTOM_POST, PLACE.CUSTOM_HEADER):
                        continue

                    if place not in conf.paramDict:
                        continue

                    paramDict = conf.paramDict[place]

                    paramType = conf.method if conf.method not in (None, HTTPMETHOD.GET, HTTPMETHOD.POST) else place

                    for parameter, value in paramDict.items():
                        if not proceed:
                            break

                        kb.vainRun = False
                        testSqlInj = True
                        paramKey = (conf.hostname, conf.path, place, parameter)

                        if paramKey in kb.testedParams:
                            testSqlInj = False

                            infoMsg = "skipping previously processed %s parameter '%s'" % (paramType, parameter)
                            logger.info(infoMsg)

                        elif parameter in conf.testParameter:
                            pass

                        elif parameter == conf.rParam:
                            testSqlInj = False

                            infoMsg = "skipping randomizing %s parameter '%s'" % (paramType, parameter)
                            logger.info(infoMsg)

                        elif parameter in conf.skip or kb.postHint and parameter.split(' ')[-1] in conf.skip:
                            testSqlInj = False

                            infoMsg = "skipping %s parameter '%s'" % (paramType, parameter)
                            logger.info(infoMsg)

                        elif conf.paramExclude and (re.search(conf.paramExclude, parameter, re.I) or kb.postHint and re.search(conf.paramExclude, parameter.split(' ')[-1], re.I)):
                            testSqlInj = False

                            infoMsg = "skipping %s parameter '%s'" % (paramType, parameter)
                            logger.info(infoMsg)

                        elif parameter == conf.csrfToken:
                            testSqlInj = False

                            infoMsg = "skipping anti-CSRF token parameter '%s'" % parameter
                            logger.info(infoMsg)

                        # Ignore session-like parameters for --level < 4
                        elif conf.level < 4 and (parameter.upper() in IGNORE_PARAMETERS or parameter.upper().startswith(GOOGLE_ANALYTICS_COOKIE_PREFIX)):
                            testSqlInj = False

                            infoMsg = "ignoring %s parameter '%s'" % (paramType, parameter)
                            logger.info(infoMsg)

                        elif PAYLOAD.TECHNIQUE.BOOLEAN in conf.tech or conf.skipStatic:
                            check = checkDynParam(place, parameter, value)

                            if not check:
                                warnMsg = "%s parameter '%s' does not appear to be dynamic" % (paramType, parameter)
                                logger.warn(warnMsg)

                                if conf.skipStatic:
                                    infoMsg = "skipping static %s parameter '%s'" % (paramType, parameter)
                                    logger.info(infoMsg)

                                    testSqlInj = False
                            else:
                                infoMsg = "%s parameter '%s' is dynamic" % (paramType, parameter)
                                logger.info(infoMsg)

                        kb.testedParams.add(paramKey)

                        if testSqlInj:
                            try:
                                if place == PLACE.COOKIE:
                                    pushValue(kb.mergeCookies)
                                    kb.mergeCookies = False

                                check = heuristicCheckSqlInjection(place, parameter)

                                if check != HEURISTIC_TEST.POSITIVE:
                                    if conf.smart or (kb.ignoreCasted and check == HEURISTIC_TEST.CASTED):
                                        infoMsg = "skipping %s parameter '%s'" % (paramType, parameter)
                                        logger.info(infoMsg)
                                        continue

                                infoMsg = "testing for SQL injection on %s " % paramType
                                infoMsg += "parameter '%s'" % parameter
                                logger.info(infoMsg)

                                # 传入参数 开始检测是否有注入 checkSqlInjection
                                injection = checkSqlInjection(place, parameter, value)
                                proceed = not kb.endDetection
                                injectable = False

                                if getattr(injection, "place", None) is not None:
                                    if NOTE.FALSE_POSITIVE_OR_UNEXPLOITABLE in injection.notes:
                                        kb.falsePositives.append(injection)
                                    else:
                                        injectable = True

                                        kb.injections.append(injection)

                                        # In case when user wants to end detection phase (Ctrl+C)
                                        if not proceed:
                                            break

                                        msg = "%s parameter '%s' " % (injection.place, injection.parameter)
                                        msg += "is vulnerable. Do you want to keep testing the others (if any)? [y/N] "

                                        if not readInput(msg, default='N', boolean=True):
                                            proceed = False
                                            paramKey = (conf.hostname, conf.path, None, None)
                                            kb.testedParams.add(paramKey)

                                if not injectable:
                                    warnMsg = "%s parameter '%s' does not seem to be " % (paramType, parameter)
                                    warnMsg += "injectable"
                                    logger.warn(warnMsg)

                            finally:
                                if place == PLACE.COOKIE:
                                    kb.mergeCookies = popValue()

            if len(kb.injections) == 0 or (len(kb.injections) == 1 and kb.injections[0].place is None):
                if kb.vainRun and not conf.multipleTargets:
                    errMsg = "no parameter(s) found for testing in the provided data "
                    errMsg += "(e.g. GET parameter 'id' in 'www.site.com/index.php?id=1')"
                    raise SqlmapNoneDataException(errMsg)
                else:
                    errMsg = "all tested parameters appear to be not injectable."

                    if conf.level < 5 or conf.risk < 3:
                        errMsg += " Try to increase '--level'/'--risk' values "
                        errMsg += "to perform more tests."

                    if isinstance(conf.tech, list) and len(conf.tech) < 5:
                        errMsg += " Rerun without providing the option '--technique'."

                    if not conf.textOnly and kb.originalPage:
                        percent = (100.0 * len(getFilteredPageContent(kb.originalPage)) / len(kb.originalPage))

                        if kb.dynamicMarkings:
                            errMsg += " You can give it a go with the switch '--text-only' "
                            errMsg += "if the target page has a low percentage "
                            errMsg += "of textual content (~%.2f%% of " % percent
                            errMsg += "page content is text)."
                        elif percent < LOW_TEXT_PERCENT and not kb.errorIsNone:
                            errMsg += " Please retry with the switch '--text-only' "
                            errMsg += "(along with --technique=BU) as this case "
                            errMsg += "looks like a perfect candidate "
                            errMsg += "(low textual content along with inability "
                            errMsg += "of comparison engine to detect at least "
                            errMsg += "one dynamic parameter)."

                    if kb.heuristicTest == HEURISTIC_TEST.POSITIVE:
                        errMsg += " As heuristic test turned out positive you are "
                        errMsg += "strongly advised to continue on with the tests. "
                        errMsg += "Please, consider usage of tampering scripts as "
                        errMsg += "your target might filter the queries."

                    if not conf.string and not conf.notString and not conf.regexp:
                        errMsg += " Also, you can try to rerun by providing "
                        errMsg += "either a valid value for option '--string' "
                        errMsg += "(or '--regexp')."
                    elif conf.string:
                        errMsg += " Also, you can try to rerun by providing a "
                        errMsg += "valid value for option '--string' as perhaps the string you "
                        errMsg += "have chosen does not match "
                        errMsg += "exclusively True responses."
                    elif conf.regexp:
                        errMsg += " Also, you can try to rerun by providing a "
                        errMsg += "valid value for option '--regexp' as perhaps the regular "
                        errMsg += "expression that you have chosen "
                        errMsg += "does not match exclusively True responses."

                    if not conf.tamper:
                        errMsg += " If you suspect that there is some kind of protection mechanism "
                        errMsg += "involved (e.g. WAF) maybe you could retry "
                        errMsg += "with an option '--tamper' (e.g. '--tamper=space2comment')"

                    raise SqlmapNotVulnerableException(errMsg.rstrip('.'))
            else:
                # Flush the flag
                kb.testMode = False

                _saveToResultsFile()
                _saveToHashDB()
                _showInjections()
                _selectInjection()

            if kb.injection.place is not None and kb.injection.parameter is not None:
                if conf.multipleTargets:
                    message = "do you want to exploit this SQL injection? [Y/n] "
                    condition = readInput(message, default='Y', boolean=True)
                else:
                    condition = True

                if condition:
                    action() # 如果存在注入，action函数将继续检测其他信息

        except KeyboardInterrupt:
            if conf.multipleTargets:
                warnMsg = "user aborted in multiple target mode"
                logger.warn(warnMsg)

                message = "do you want to skip to the next target in list? [Y/n/q]"
                choice = readInput(message, default='Y').upper()

                if choice == 'N':
                    return False
                elif choice == 'Q':
                    raise SqlmapUserQuitException
            else:
                raise

        except SqlmapSkipTargetException:
            pass

        except SqlmapUserQuitException:
            raise

        except SqlmapSilentQuitException:
            raise

        except SqlmapBaseException, ex:
            errMsg = getSafeExString(ex)

            if conf.multipleTargets:
                _saveToResultsFile()

                errMsg += ", skipping to the next %s" % ("form" if conf.forms else "URL")
                logger.error(errMsg.lstrip(", "))
            else:
                logger.critical(errMsg)
                return False

        finally:
            showHttpErrorCodes()

            if kb.maxConnectionsFlag:
                warnMsg = "it appears that the target "
                warnMsg += "has a maximum connections "
                warnMsg += "constraint"
                logger.warn(warnMsg)

    if kb.dataOutputFlag and not conf.multipleTargets:
        logger.info("fetched data logged to text files under '%s'" % conf.outputPath)

    if conf.multipleTargets:
        if conf.resultsFilename:
            infoMsg = "you can find results of scanning in multiple targets "
            infoMsg += "mode inside the CSV file '%s'" % conf.resultsFilename
            logger.info(infoMsg)

    return True
```
