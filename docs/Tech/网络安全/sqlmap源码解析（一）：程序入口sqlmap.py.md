---
order: 1504428814
---
# sqlmap源码解析（一）：程序入口sqlmap.py

sqlmap源码很详细了，慢慢看，将一些英文翻译成中文。 

这是sqlmap.py中的main入口函数，一系列的处理都是从这里开始的 

  

```py 
def main():
    """
    Main function of sqlmap when running from command line.
    """

    try:
        checkEnvironment() # 检测环境
        setPaths(modulePath()) # 为一些目录和文件设置了绝对路径
        banner() # 打印sqlmap banner信息

        # Store original command line options for possible later restoration
        # 先初始化命令信息，等会还要进行设置
        cmdLineOptions.update(cmdLineParser().__dict__)
        initOptions(cmdLineOptions)

        if conf.get("api"):
            # heavy imports
            from lib.utils.api import StdDbOut
            from lib.utils.api import setRestAPILog

            # Overwrite system standard output and standard error to write
            # to an IPC database
            sys.stdout = StdDbOut(conf.taskid, messagetype="stdout")
            sys.stderr = StdDbOut(conf.taskid, messagetype="stderr")
            setRestAPILog()

        conf.showTime = True
        dataToStdout("[!] legal disclaimer: %s\n\n" % LEGAL_DISCLAIMER, forceOutput=True)
        dataToStdout("[*] starting at %s\n\n" % time.strftime("%X"), forceOutput=True)
        # 打印文本 法律免责申明和开始时间

        init() # 初始化信息，根据输入的命令初始化

        if conf.profile:
            profile() # 将在一个非常nice的图表上显示数据 需要安装这些库 python-pydot python-pyparsing python-profiler graphviz
        elif conf.smokeTest:
            smokeTest() # 测试sqlmap能否运行
        elif conf.liveTest:
            liveTest()  # 测试sqlmap的注入功能
        else:
            try:
                start() # 前面一系列的设置完毕后，现在开始进行注入攻击了
            except thread.error as ex:
                if "can't start new thread" in getSafeExString(ex):
                    errMsg = "unable to start new threads. Please check OS (u)limits"
                    logger.critical(errMsg)
                    raise SystemExit
                else:
                    raise

    except SqlmapUserQuitException:
        # sqlmap自定义的用户退出异常处理
        errMsg = "user quit"
        try:
            logger.error(errMsg)
        except KeyboardInterrupt:
            pass

    except (SqlmapSilentQuitException, bdb.BdbQuit):
        pass

    except SqlmapShellQuitException:
        cmdLineOptions.sqlmapShell = False

    except SqlmapBaseException as ex:
        errMsg = getSafeExString(ex)
        try:
            logger.critical(errMsg)
        except KeyboardInterrupt:
            pass
        raise SystemExit

    except KeyboardInterrupt:
        print

        errMsg = "user aborted"
        try:
            logger.error(errMsg)
        except KeyboardInterrupt:
            pass

    except EOFError:
        print
        errMsg = "exit"

        try:
            logger.error(errMsg)
        except KeyboardInterrupt:
            pass

    except SystemExit:
        pass

    except:
        print
        errMsg = unhandledExceptionMessage()
        excMsg = traceback.format_exc()
        valid = checkIntegrity() #在未处理的文件中检测代码的完整性

        try:
            if valid is False:
                errMsg = "code integrity check failed (turning off automatic issue creation). "
                errMsg += "You should retrieve the latest development version from official GitHub "
                errMsg += "repository at '%s'" % GIT_PAGE
                logger.critical(errMsg)
                print
                dataToStdout(excMsg)
                raise SystemExit

            elif any(_ in excMsg for _ in ("tamper/", "waf/")):
                logger.critical(errMsg)
                print
                dataToStdout(excMsg)
                raise SystemExit

            elif "MemoryError" in excMsg:
                errMsg = "memory exhaustion detected"
                logger.error(errMsg)
                raise SystemExit

            elif any(_ in excMsg for _ in ("No space left", "Disk quota exceeded")):
                errMsg = "no space left on output device"
                logger.error(errMsg)
                raise SystemExit

            elif all(_ in excMsg for _ in ("No such file", "_'", "self.get_prog_name()")):
                errMsg = "corrupted installation detected ('%s'). " % excMsg.strip().split('\n')[-1]
                errMsg += "You should retrieve the latest development version from official GitHub "
                errMsg += "repository at '%s'" % GIT_PAGE
                logger.error(errMsg)
                raise SystemExit

            elif "Read-only file system" in excMsg:
                errMsg = "output device is mounted as read-only"
                logger.error(errMsg)
                raise SystemExit

            elif "OperationalError: disk I/O error" in excMsg:
                errMsg = "I/O error on output device"
                logger.error(errMsg)
                raise SystemExit

            elif "_mkstemp_inner" in excMsg:
                errMsg = "there has been a problem while accessing temporary files"
                logger.error(errMsg)
                raise SystemExit

            elif "can't start new thread" in excMsg:
                errMsg = "there has been a problem while creating new thread instance. "
                errMsg += "Please make sure that you are not running too many processes"
                if not IS_WIN:
                    errMsg += " (or increase the 'ulimit -u' value)"
                logger.error(errMsg)
                raise SystemExit

            elif "'DictObject' object has no attribute '" in excMsg and all(_ in errMsg for _ in ("(fingerprinted)", "(identified)")):
                errMsg = "there has been a problem in enumeration. "
                errMsg += "Because of a considerable chance of false-positive case "
                errMsg += "you are advised to rerun with switch '--flush-session'"
                logger.error(errMsg)
                raise SystemExit

            elif all(_ in excMsg for _ in ("pymysql", "configparser")):
                errMsg = "wrong initialization of pymsql detected (using Python3 dependencies)"
                logger.error(errMsg)
                raise SystemExit

            elif "bad marshal data (unknown type code)" in excMsg:
                match = re.search(r"\s*(.+)\s+ValueError", excMsg)
                errMsg = "one of your .pyc files are corrupted%s" % (" ('%s')" % match.group(1) if match else "")
                errMsg += ". Please delete .pyc files on your system to fix the problem"
                logger.error(errMsg)
                raise SystemExit

            elif "valueStack.pop" in excMsg and kb.get("dumpKeyboardInterrupt"):
                raise SystemExit

            elif any(_ in excMsg for _ in ("Broken pipe",)):
                raise SystemExit

            for match in re.finditer(r'File "(.+?)", line', excMsg):
                file_ = match.group(1)
                file_ = os.path.relpath(file_, os.path.dirname(__file__))
                file_ = file_.replace("\\", '/')
                file_ = re.sub(r"\.\./", '/', file_).lstrip('/')
                excMsg = excMsg.replace(match.group(1), file_)

            errMsg = maskSensitiveData(errMsg)
            excMsg = maskSensitiveData(excMsg)

            if conf.get("api") or not valid:
                logger.critical("%s\n%s" % (errMsg, excMsg))
            else:
                logger.critical(errMsg)
                kb.stickyLevel = logging.CRITICAL
                dataToStdout(excMsg)
                createGithubIssue(errMsg, excMsg)
                # 输出不知道的异常情况并且创建Issue自动上报给github
        except KeyboardInterrupt:
            pass

    finally:
        # 结尾处理，各种收尾工作
        kb.threadContinue = False

        if conf.get("showTime"):
            dataToStdout("\n[*] shutting down at %s\n\n" % time.strftime("%X"), forceOutput=True)

        kb.threadException = True

        if kb.get("tempDir"):
            for prefix in (MKSTEMP_PREFIX.IPC, MKSTEMP_PREFIX.TESTING, MKSTEMP_PREFIX.COOKIE_JAR, MKSTEMP_PREFIX.BIG_ARRAY):
                for filepath in glob.glob(os.path.join(kb.tempDir, "%s*" % prefix)):
                    try:
                        os.remove(filepath)
                    except OSError:
                        pass
            if not filter(None, (filepath for filepath in glob.glob(os.path.join(kb.tempDir, '*')) if not any(filepath.endswith(_) for _ in ('.lock', '.exe', '_')))):
                shutil.rmtree(kb.tempDir, ignore_errors=True)

        if conf.get("hashDB"):
            try:
                conf.hashDB.flush(True)
            except KeyboardInterrupt:
                pass

        if conf.get("harFile"):
            with openFile(conf.harFile, "w+b") as f:
                json.dump(conf.httpCollector.obtain(), fp=f, indent=4, separators=(',', ': '))

        if cmdLineOptions.get("sqlmapShell"):
            cmdLineOptions.clear()
            conf.clear()
            kb.clear()
            main()

        if conf.get("api"):
            try:
                conf.databaseCursor.disconnect()
            except KeyboardInterrupt:
                pass

        if conf.get("dumper"):
            conf.dumper.flush()

        # short delay for thread finalization
        try:
            _ = time.time()
            while threading.activeCount() > 1 and (time.time() - _) > THREAD_FINALIZATION_TIMEOUT:
                time.sleep(0.01)
        except KeyboardInterrupt:
            pass
        finally:
            # Reference: http://stackoverflow.com/questions/1635080/terminate-a-multi-thread-python-program
            if threading.activeCount() > 1:
                os._exit(0)
```

  

