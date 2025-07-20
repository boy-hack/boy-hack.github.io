---
order: 1710850507
---
# Hacking8自动化就是好玩 知识星球-公众号2023年终总结
![](assert/VI7sX_image_whLPxf7skK.png)

> 很多黑客和安全工具的构造是那么巧妙，我看了很多安全工具的代码，将它们值得学习的地方记录了下来。持续更新星球中的精华文章和补全安全知识，记录笔记，对自己对他人都是一种收获。付费加入是我更新的动力。

星球我把他当作整理总结学习内容的地方，平时看到好玩的东西，项目代码，觉得未来有用的东西，会随手分析一下发到星球，方便后面检索。

如果要给我的星球打上标签，我觉得是`自动化`，`安全开发`。23年换了一份工作，开始做大模型与网络安全垂类的研究，星球也可以多加一个标签：`大模型`

## 网络安全大模型 SecGPT

在23年2月就发了一个想法，用安全文章来训练GPT3，当时只是一个想法，离实现还很遥远

![](assert/6xdC7_image_A534FQywIv.png)

其实在此以前就开始关注AI能做什么了。

比如yolo模型做目标检测，cnn做通用验证码识别

![](assert/fykXb_image_rEUURbGME7.png)

3月开始，研究chatgpt和hacking8知识库的打通

![](assert/iJd6E_image_iPiy6VUHb3.png)

然后，开始玩stable diffusion图像微调，用自己的头像做训练。

![](assert/mOnw1_image_j9bMYruh_3.png)

打通公众号和知识库搜索，但是公众号有超时机制，所以失败了

![](assert/Cy24l_image_-6Ggxom9Mh.png)

四个月后，2023.7.6 开始研究大模型了，由于训练资源有限，先复现了GPT2小模型

![](assert/RWXHU_image_HgeIyDaXut.png)

两个月后，训练了第一个网络安全大模型

![](assert/A53gZ_image_IZ0gAI1Qh8.png)

1个月后，星球开始内测

![](assert/fp6Sj_image_QSC_kUPR1D.png)

开源预训练数据

![](assert/ADa1J_image_SajdEIjlZ-.png)

模型开源

![](assert/TbPHO_image_iAKV09uEJZ.png)

完整开源训练代码

![](assert/zXeos_image_-p3b8N8sqj.png)

2024.2.14基于小参数模型训练，开源了SecGPT-Mini模型

![](assert/wHDCQ_image_Z40ZvdGLrD.png)

训练模型这一块有很多细节，开始总结经验文档

![](assert/4WIyl_image_HToNbjY1bi.png)

![](assert/ysN2n_image_pQEXVSg2qC.png)

## XSCAN

2023年，开始总结之前的自动化经验，编写自动化的xss扫描器。幻想是全自动挖掘xss漏洞赏金。

![](assert/mzdfo_image_NgOOzVl9uO.png)

3月6日发布了第一个版本

![](assert/qTl2r_image_NuBE8cvquj.png)

用向量相似度的方法解决了爬虫重复的问题

![](assert/v4fGE_image_9SznF9c82i.png)

3月19日正式发布

![](assert/yUts8_image_8JFpjKB6iV.png)

  * 2023.3.25 发布 xscan v1.7.4 
  * 2023.4.3 开始扫一些国内src

![](assert/ZIB0L_image_bqvcpbi6nn.png)
  * 2023.4.9 发布dom-xss扫描工具和源码

![](assert/M94vd_image_pnspcm6rcT.png)
  * 2023.4.21 xscan v1.8.1 发布，增加了无敌多对于src场景的改进
    * 同时微信公众号发表了《自动化漏洞赏金(bugbounty)和xscan扫描器总结》
      * https://mp.weixin.qq.com/s?__biz=MzU2NzcwNTY3Mg==\&mid=2247484800\&idx=1\&sn=7ececf9f462e9e10fd82ed057815b2bf\&chksm=fc986ca7cbefe5b11d7b7570ae09859491ef0429718fe3521b5d976ea1aadd555cfac4cc1d78\&token=399541248\&lang=zh_CN#rd
  * 2023.4.26 xscan v1.8.2 修复了从burp导入的一个bug
  * 2023.6.26 xscan v1.9.3 发布 增加了爬虫表达式引擎，可编写表达式筛选特定url
  * 2023-09-01 xscan 1.9.4 更新
  * 2023-11-05 xscan开源



![](assert/COvhf_image_afqCH9ByDn.png)

  * 2023-11-25 xdomscan发布第一个版本，可以进行domxss扫描



![](assert/mJIQp_image_kKYexGs_7A.png)

  * 2023-12-01 xscan 2.2 发布

![](assert/60fqO_image_bp1NJ_0a7N.png)



## W15SCAN

w15scan是一个针对白帽子刷SRC的攻击面管理系统，从去年一直嚷嚷要做，到今年进度也才百分比的个位数。主要业余时间开发，而且开发涉及的知识很多，前端，后端，扫描端，还得学习ES大数据管理相关的。

和很多人交流，大家对这个系统抱有很大期待，今年给自己的一个期望就是做好他.

放几个路透图把。

首页

![](assert/F8vJK_image_aY7Bo9SIIh.png)

项目页

![](assert/TXE3G_image_fd5KAtck-h.png)

![](assert/V7J8I_image_NIGK7Wk-Ya.png)

编辑资产范围

![](assert/YHyPK_image_PLwyTa_JPz.png)

DNS

![](assert/5Blo3_image__XbaeY92Lj.png)

DNS详情，可关联数据

![](assert/OBw3G_image_ev8rrZ12Zv.png)

web

![](assert/2ytvs_image_FaOjzyX2GW.png)

web聚合搜索

后期会设计通过点击就能搜索的方式

![](assert/C7abY_image_jwFXwEnP9Q.png)

web详情，自动关联

![](assert/9bv4Y_image_NaMVSZuvis.png)

端口扫描

![](assert/TdjBl_image_CFVaXepi8s.png)

端口扫描详情

![](assert/i5xtQ_image_QjYAFd5Lf0.png)

项目资产最短CIDR展示

![](assert/zYCwE_image_wdpUukZqxp.png)

二号模式

![](assert/W4v7S_image_4PzaO_Dk_5.png)

## 星球作业

  * 第五期：web动态爬虫

![](assert/c4ZOP_image_cfonUnmfb5.png)
  * 第六期：训练自己的网络安全大模型

![](assert/qUg5c_image_F1VCzFv2zP.png)



## 星球和微信公众号总结

星球目前总人数

![](assert/xSYHP_image_1Ph4S7XVKz.png)

加入的渠道有三个，通过微信公众号进来的最多。

![](assert/VrLjb_image_8lD8vOQpUc.png)

星球收入勉强能在北京交个房租。

微信公众号 从`2023.1.1` 开始关注只有 `6545`

到今天，`2024.3.19` 已经有接近1w人关注了。

![](assert/TqjhA_image_tUq9knQ-Dd.png)

通过关注趋势图，四月份某一天净增关注人最多

![](assert/zo0Ky_image_mCsFmxWFB8.png)

看了下，应该就是这篇文章

![](assert/0u1t6_image_jDIFkQFMk0.png)

星球原本是发各种原创好玩的技术，但是23年精力相比以前分散了不少，有年龄增长的因素，要开始考虑其他各种事情了。无意间发布的xscan有很多人用，所以也促使我一直不断的改进bug更新。

今年的想法除开工作之外的，就是把w15scan做起来，将这些年积累的扫描器相关的知识，xscan等等先进的技术串联，真正做到攻击面资产管理，持续监控，自动化的bugbounty！
