---
order: 1561475557
---
# w3af爬虫攻击规则

前几天用了下长亭的xray扫描器，用代理扫描的功能，测试的内网环境的一些网站，效果还不错，也激发了我的灵感，我也要造一个被动扫描器的轮子！下面是整理的w3af的爬虫相关的插件功能，w3af的爬虫攻击分为两类，一类是基于爬虫获取更多地址，一类是一个具体地址进行的攻击。因为太多了，先把对应目录列出来，需要的时候在详细看。 

## 根据url生成对应的fuzz参数
```
_appendables = ('~', '.tar.gz', '.gz', '.7z', '.cab', '.tgz',
                    '.gzip', '.bzip2', '.inc', '.zip', '.rar', '.jar', '.java',
                    '.class', '.properties', '.bak', '.bak1', '.bkp', '.back',
                    '.backup', '.backup1', '.old', '.old1', '.$$$'
                    )
    _backup_exts = ('tar.gz', '7z', 'gz', 'cab', 'tgz', 'gzip',
                    'bzip2', 'zip', 'rar')
    _file_types = (
        'inc', 'fla', 'jar', 'war', 'java', 'class', 'properties',
        'bak', 'bak1', 'backup', 'backup1', 'old', 'old1', 'c', 'cpp',
        'cs', 'vb', 'phps', 'disco', 'ori', 'orig', 'original'
    )

```

/w3af/plugins/crawl/url_fuzzer.py

## 通过～枚举目录

w3af/plugins/crawl/user_dir.py

## wsdl接口

w3af/plugins/crawl/wsdl_finder.py

## crossdomain.xml

w3af/plugins/crawl/ria_enumerator.py

## phpinfo枚举

w3af/plugins/crawl/phpinfo.py

## 寻找支付接口

w3af/plugins/crawl/payment_webhook_finder.py

## 寻找oracel程序

w3af/plugins/crawl/oracle_discovery.py

## Open API接口探测

w3af/plugins/crawl/open_api.py

## 寻找.git .svn .sg .csv等服务

w3af/plugins/crawl/find_dvcs.py

## dwsync.xml

w3af/plugins/crawl/dwsync_xml.py

## 搜索.DS_Store文件并检查包含的文件

w3af/plugins/crawl/dot_ds_store.py

## 获取index1等

w3af/plugins/crawl/digit_sum.py

## Wordpress 指纹识别

w3af/plugins/crawl/wordpress_fingerprint.py

## XXE漏洞

w3af/plugins/audit/xxe.py

## XXS漏洞

w3af/plugins/audit/xss.py

## XPATH注入

w3af/plugins/audit/xss.py

## websocket_hijacking

w3af/plugins/audit/websocket_hijacking.py

## SSI

Find server side inclusion vulnerabilities.

w3af/plugins/audit/ssi.py

## SQL注入

w3af/plugins/audit/sqli.py

## shell shock

w3af/plugins/audit/shell_shock.py

## remote file inclusion

w3af/plugins/audit/rfi.py

## 反射下载

w3af/plugins/audit/rfd.py

## preg_replace

寻找php不安全的preg_replace

w3af/plugins/audit/preg_replace.py

## 系统命令执行

w3af/plugins/audit/os_commanding.py

## 本地文件包含

w3af/plugins/audit/lfi.py

## LDAP injection

w3af/plugins/audit/ldapi.py

## .htaccess

w3af/plugins/audit/htaccess_methods.py

## 查找将浏览器重定向到任何站点的脚本

w3af/plugins/audit/global_redirect.py

## 查找格式字符串漏洞

w3af/plugins/audit/format_string.py

## 寻找eval脚本

w3af/plugins/audit/eval.py

## 反序列化漏洞

w3af/plugins/audit/deserialization.py

## CSRF漏洞

w3af/plugins/audit/csrf.py

## 缓存溢出

w3af/plugins/audit/buffer_overflow.py

## SQL盲注

w3af/plugins/audit/blind_sqli.py
