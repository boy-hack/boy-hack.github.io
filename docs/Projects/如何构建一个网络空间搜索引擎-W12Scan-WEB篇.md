---
order: 1556813576
---
# 如何构建一个网络空间搜索引擎-W12Scan-WEB篇

当黑客们不羁的灵魂受够了那些受到限制的空间搜索引擎，是否有想过使用自己搭建的网络空间搜索引擎呢？你只需要一台独立的服务器(配置取决于你想象的扫描速度，最低1G1H)即可拥有它，并且允许分布式搭建。搭建简单，使用简单，你还在等什么呢？趁着51的假期余温，简单写一篇说明文档。

## 说明

这是W12Scan官方的安装搭建说明文档，将包含大部分w12scan使用过程中的问题以及解决方案。但是你需要注意的是，在写下这篇官方说明文档的时间，w12scan当前的发行版本是0.2，若之后在更高的版本遇到了问题，请以GitHub上说明为准！

## 简介

W12Scan是一款网络空间搜索引擎，最早的概念是基于W10Scan的全自动漏洞扫描，但是它也会帮你自动分析企业的资产，分析出相关资产段的详细信息，无论是刷SRC还是管理企业资产，又或者单纯想批量测试漏洞范围(W12Scan提供搜索API)，W12Scan都能实现，甚至W12Scan的功能还在不停的完善（具体看GitHub介绍）。

一个演示视频：
<video controls src="./assert/uper_video_1556034118929372.mp4" title="Title"></video>

## 搭建&安装

W12Scan整套又分为交互的WEB端和提供扫描client端，这篇文章主要讲的是WEB端，但是只需要一句docker命令就能将W12Scan整套搭建起来。
``` 
git clone https://github.com/boy-hack/w12scan
cd w12scan
docker-compose up -d

```

默认账号密码boyhack

运行环境默认配置是需要 内存 > 2G 且是安装了docker的Linux系统。我也说过1G1H也能跑起来，Windows系统搭建需要踩些坑都在会后面说道。

下面说一下一些常见的问题与解决方案，这些问题都是统计字github以及telefgram。

### 1G1H如何配置

根据服务器配置修改`docker-compose.yml`参数，设置elasticsearch内存占用大小，默认设置是521M，如果你是1G内存可以设置为128M。

具体，在W12Scan跟目下，`docker-compose.yml`找到`ES_JAVA_OPTS=-Xms512m -Xmx512m`修改为`ES_JAVA_OPTS=-Xms128m -Xmx128m`,但是代价是在搜索和分析时可能会报内存不足的错误。所以内存还是越高越好。

### Windows安装问题

在Windows上，由于sh文件的格式问题，需要转换下格式才能构建。

> 因为windows上git pull的代码，w12scan\dockerconf\start.sh的脚本格式是dos的，需要转换下,我是上传的linux服务器，用dos2unix转换的，转换完替换windows上的脚本，docker rmi之前构建的镜像，再一次运行docker-compose up就ok了

refer:https://github.com/boy-hack/w12scan/issues/12

### 搜索数为0

搜索目标需要自行添加，在dashboard中`添加扫描目标`

### 如何分布式部署

W12Scan的启动都是通过读环境变量进行的，意味着你不需要修改一行代码，通过docker即可进行分布式的部署。相关部署文档参考https://github.com/boy-hack/w12scan/blob/master/doc/DEPLOYMENT1.md

### 访问8000端口失败

参考https://github.com/boy-hack/w12scan/issues/17

访问8000端口失败，先确认docker是否都运行成功，在w12scan根目录下，运行`docker ps -a`来查看容器的运行状态，一般会有四个容器，如果容器出现exit，则说明有容器运行失败。一般都是配置问题或者服务器自身问题，使用`docker logs + 容器对应id`来查看日志，报告错误时请连log日志错误一同报告。

### 创建任务后运行无反应

创建任务后需要等待1~5分钟节点获得任务，若节点管理中有日志，则说明运行正常，若节点管理显示节点挂了，你需要详细排查挂掉的原因

### 最高能扫描多少主机？

无限，但是看你配置

### 扫描速度多少？

w12scan使用masscan+nmap扫描，速度一般比较慢，但主要看配置，以及分布式的节点。

### 显示插件库为 - ？

这是正常情况，因为这里还没有写。但是插件的调用是有的，会自动调用airbug，只是显示的代码没有写。

### 运行节点名称不显示

删掉w12scan相关镜像，重新运行一遍，遇到这种问题大部分是没有按照要求运行的。

### issue 模板

在使用过程中遇到的问题可以到 https://github.com/w-digital-scanner/w12scan/issues/new 提问，但是在提问时候，务必将以下信息贴上，方便排查。

  * 服务器操作系统名称（eg:windows or linux ubuntu,centos?），位数(32 or 64)，操作系统版本信息
  * 服务器配置(内存的大小，CPU核心数量)
  * docker-compose ps，所有docker是否启动？如果有docker exit请贴出docker logs 信息
  * 详细描述复现步骤



## 最后

目前扫描端已经优化得比较稳定了，保持最新的client镜像即可。
