---
title: FreeRTOS-Plus-TCP 库现在更加稳健和安全
date: 2022 年 8 月 9 日
feature: blog
categories:
- 长期支持
authors:
- wallit
---
在开展 [FreeRTOS Labs IPv6](../../FreeRTOS-Plus/FreeRTOS_Plus_TCP/IPv6/index) 项目的同时， 
我们正继续提升 
 [FreeRTOS-Plus-TCP](https://github.com/freertos/freertos-plus-tcp) 库的稳健性、安全性和模块性。今天我们 
很高兴推出专为实现此目的而开发的 FreeRTOS-Plus-TCP V3.0.0 库。

FreeRTOS-Plus-TCP V3.0.0 为代码的所有行和分支增加了全面的单元测试覆盖范围，并 
经过了 AWS Security 的渗透测试和协议测试，以降低暴露于安全 
漏洞的风险。对于上下文，协议测试涉及针对 IPv4、TCP、 
UDP、DHCP、ARP 和 ICMP 的合规性和减值检查，这有助于确保 FreeRTOS-Plus-TCP TCP/IP 堆栈更稳健。
还对源代码进行了重组，提升其模块化和扩展性水平，使其更容易添加单元测试。

新的源代码组织要求更新现有项目。但是，如果您想继续使用 
现有源代码组织，您可以使用脚本生成较旧的文件和目录结构 
。如需进一步了解并下载最新库，请访问 
 [FreeRTOS-Plus-TCP GitHub 存储库](https://github.com/freertos/freertos-plus-tcp)。

  
## 作者简介

![](https://secure.gravatar.com/avatar/fb75dac2926bf515a691ef90995a1554?s=200&d=mm&r=g)   
Toshiyanger Walling 是 Amazon Web Services FreeRTOS 团队的软件开发经理， 
负责管理 FreeRTOS 软件构建和维护团队。  
[查看此作者的文章](../author/wallit) 

FreeRTOS 论坛：获得行业领先的专家支持，并与全球同行 
合作。[查看论坛](https://forums.freertos.org/)

