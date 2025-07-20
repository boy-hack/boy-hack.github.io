---
order: 1551881646
---
# 花两天时间的docker踩坑记录

要被docker折腾吐血的我，“带着伤”写下这次记录…

## 起因

在复现openmrs漏洞时候，日常的工作之一就是搭建该漏洞的docker靶场，但是由于docker靶场平台统一的缘故，需要将靶机的所有环境安装在一个docker里面，无形之中增加了很大的复杂性，而我的踩坑之旅就此开始。

## 第一天

openmrs需要jre运行环境和tomcat，但我java的这套不是很熟，第一天大部分时间都浪费在了这里。openmrs主要需要tomcat，jre和mysql，在复现漏洞的时候，我是直接用的官方docker，官方docker是docker-compose的形式，tomcat一个容器，mysql一个容器，复现漏洞很简单，填好payload就可以打了，但是最后的shell反连模式无论如何也回连不了，最终放弃了。

接下来就是靶场的搭建环节，官方镜像太复杂了，于是想在dockerhub或者github上找找有没有人写过，找到几个，看了下dockerfile，但感觉都太复杂了，最后还是决定，从openmrs官方tomcat镜像构建，想法很简单，在它镜像上面加个mysql就好了。于是就花了一下午的时间，但也没有成功，主要是alpine启动mysql太难了，启动也各种报错，和我想到`apk add`之后就能用，差别太大了。看了下其他人基于alpine安装mysql的方案，都感觉太麻烦了。

而且，很重要的一点是，大多数mysql启动都是独立写在一个sh文件里面，这样意味着我要将官方的docker镜像重新编译，我试了试，可能基础镜像太老了，网速也慢，等了半天最后等到一个错误，也不知道怎么解决，于是放弃了基于官方镜像构建。

然而我又在dockerhub上找到一个别人做好的镜像，一个docker里面包含包裹了openmrs中所有的组件，正好满足我的要求，`docker pull`下来运行，完美。

但，世上巧合的事情很多很多，这个漏洞有一个唯一不受影响的版本，好像是`1.1x`，而，这个docker就是基于这个版本构建的，刚好在不受影响的范围。。我也是在搭建完后，用poc测试一阵才明白的…

看一下时间，还有半个小时下班，于是放下了这个事情，做点其他事。

## 第二天

昨天和大佬@BadCode交流了一下，确定了几个事情，openmrs安装很简单，只需要将`openmrs.war`这个包放到tomcat的`webapps`里面就行了。

还是先从昨天未完成的开始，昨天的版本有点低，那么我更新一下不就好了，顺着这个思路，我在其镜像的基础上加了一层copy，但是总是出现404。很奇怪的原因，找了老半天，最后查看了tomcat的日志，找到的原因，日志是个好东西~原因是当前镜像是jre7，而我copy上去的war需要运行到jre8上，找了些版本更低的war包copy上去做测试，倒是不404了，但是poc打过去也没反应。。

最后，我必须面对一个残忍的事实，我要在一个docker里面同时构建出tomcat和加mysql，然后部署war包。说的很容易，但是这是我最不愿做的，因为它们并不是直接下载下来就能安装好，它们也不能直接在docker里面执行，它们需要很多shell脚本来执行，这些都是我最不愿意做的，我的想法是，能在dockerfile’里写好就在里面写好。

于是我花了一个下午的时间来研究如何从别人构造好的tomcat+mysql中部署war包运行openmrs，但是没有一个是能够真正build完后直接运行的，都或多或少存在问题。我总结有以下：

  * 别人构造好的镜像，Mysql的root密码是由环境变量传递的，但是我们的docker靶场平台并没有额外运行参数的概念，我尝试基于此镜像，编写dockerfile中加入env来设置环境变量，但似乎没有效果。
  * 读不好环境变量中的root密码，那root密码就为空咯，按理来说确实不错，但是openmrs竟然说root密码不能为空？？好气
  * 如何在dockerfile里面修改mysql的root密码，这是个难点
  * 在我费尽心思重构完了tomcat+mysql的dockerfile文件，终于可以跑起来docker+tomcat，也能修改root的密码了，却在安装openmrs时候提示我不能创建用户？wtf？？root用户都不能创建吗？？



那么时间这么一流逝就到了晚上，最后我只得按照我最不愿意的思路去做了，从基于官方tomcat的包上安装mysql和openmrs环境。

做到一半，@Badcode说它已经做好了tomcat+mysql的基础dockerfile
```dockerfile 
FROM tomcat:8.5
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN sed -i "s/security.debian.org/mirrors.ustc.edu.cn/g" /etc/apt/sources.list
#RUN sed -i 's/security.debian.org/mirrors.ustc.edu.cn\/debian-security/g' /etc/apt/sources.list
RUN apt-get update
RUN echo "mysql-server mysql-server/root_password password password" | debconf-set-selections
RUN echo 'mysql-server mysql-server/root_password_again password password' | debconf-set-selections
RUN apt-get -yq install mysql-server
#ENV MYSQL_PASS =root
RUN apt-get install -y openssh-server curl dnsutils
RUN sed -i "s/.*PermitRootLogin.*/PermitRootLogin yes/" /etc/ssh/sshd_config
RUN /etc/init.d/ssh start 
#RUN service mysql start && mysql_secure_installation 
#RUN mysqladmin -u root  password root
RUN service mysql start && mysql -u root -e "update mysql.user set password=PASSWORD('root'),plugin = 'mysql_native_password' where user='root';flush privileges; "
#RUN service mysql restart

```

真的太厉害了，这就是我喜欢的dockerfile方式，没有其他杂杂质，“纯洁的”dockerfile… 不过有些构建顺序可以调整，然后在测试时发现`service mysql start`写在dockerfile里面是执行不成功的，那么我明天再去公司的docker靶机平台尝试一下~

## 第三天

但是你们以为这样就结束了？too young too simple…

最后我得到一个信息，dockerfile里面entrypoint只能存在一个，且只有最后一个有效，于是，就很简单了..
```dockerfile 
FROM tomcat:8.5
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && \
    sed -i "s/security.debian.org/mirrors.ustc.edu.cn/g" /etc/apt/sources.list && \
    echo "mysql-server mysql-server/root_password password password" | debconf-set-selections && \
    echo 'mysql-server mysql-server/root_password_again password password' | debconf-set-selections
RUN apt-get update && apt-get -yq install mysql-server && apt install openssh-server curl dnsutils -y
RUN sed -i "s/.*PermitRootLogin.*/PermitRootLogin yes/" /etc/ssh/sshd_config
RUN /etc/init.d/ssh start &
COPY openmrs2.war /usr/local/tomcat/webapps/openmrs.war

ADD start.sh /root/start.sh
RUN chmod +x /root/start.sh
ENTRYPOINT [ "/root/start.sh" ]

```

start.sh
```bash 
#!/bin/bash
service mysql start 
mysql -u root -e "update mysql.user set password=PASSWORD('root'),plugin = 'mysql_native_password' where user='root';flush privileges; "
service mysql restart
/usr/local/tomcat/bin/catalina.sh run

```

最后又得到一条信息： debian中安装的mysql默认配置文件`/etc/mysql/debian.cnf`在里面修改密码即可。

## End

花了三天时间折腾这个，总算稍微弄清楚了一点docker的运行流程，以及如何手动安装数据库的…
