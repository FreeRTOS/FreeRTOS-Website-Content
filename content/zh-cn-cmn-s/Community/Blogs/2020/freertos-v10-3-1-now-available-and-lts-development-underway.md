---
title: FreeRTOS V10.3.1 现已发布，LTS 版本正在开发中
created: 2020-02-18 00:00:00.0 UTC
feature: blog
categories:
  - 长期支持
authors:
  - ribarry
relatedLinks:
  - title: FreeRTOS 简介
    link: /Why-FreeRTOS/What-is-FreeRTOS/
---

本帖由 [Richard Barry](../author/ribarry) 发表于 2020 年 2 月 18 日

很高兴分享以下更新：

FreeRTOS V10.3.1 现已可供下载。此版本增强了 
ARM v7-M 和 ARM v8-M 内核的内存保护单元 (MPU) 移植，并扩展了 RISC-V 支持， 
新增 [IAR 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/SiFive/RTOS-RISC-V-FreedomStudio-IAR-HiFive-RevB)。随着这一版本的发布， 
我们将正式从长期使用的 SourceForge SVN 存储库切换为 
托管于 https://github.com/FreeRTOS 的 Git 存储库。 

SVN 存储库已在 Git 存储库中镜像了一段时间， 
在 Git 中完成的开发现将反向镜像回 SVN。我们希望 Git 工作流程能够简化 
您与 FreeRTOS 的交互。

我们最近还对 FreeRTOS.org 网站进行了改进，比如更新网站界面以提升 
导航体验。我们新增了包含 FreeRTOS 内核和其他库的下载、[博客](../../blog)， 
并直接在 [.org 网站上托管FreeRTOS ]社区论坛(https://forums.freertos.org/) FreeRTOS 
。论坛旨在帮助您快速寻求支持并参与社区讨论。 
未来几个月会陆续推出更多网站更改。

此外，我们还发布了新库，旨在帮助您解决 IoT 用例， 
比如将设备安全连接到云端以及通过 over-the-air 更新功能 
远程更新现场部署的设备。[库类别页面](/Documentation/03-Libraries/01-Library-overview/Library-categories) 介绍了 
如何对库进行分组，选择一个组后即可查看各个库的信息。为帮助您 
快速入门，我们添加了 IoT 参考集成链接，这些集成是 
预集成 FreeRTOS 项目，移植到基于微控制器的评估板上，可显示 
端到端云连接。有关项目及其文档，请查看 [IoT 参考集成页面](../../iot-reference-integrations) 
。

最后，我们已开始着手开发长期支持 (LTS) 版本。LTS 版本 
与不断发展的开放基线分开维护，并在发布后维护多年。您可以 
在 [LTS 页面](../../ltsroadmap) 上关注我们的进度。

感谢所有用户的支持，我们会继续优化 FreeRTOS。


## 作者简介

![](https://secure.gravatar.com/avatar/2197982f95321bd156e6f3b3fa184b92?s=200&d=mm&r=g)   
Richard Barry 于 2003 年创立了 FreeRTOS 项目，十余年来，一直致力于通过其公司 Real Time Engineers Ltd 开发并推广 FreeRTOS。 
现在他仍在从事 FreeRTOS 工作，加入了更大的团队， 
在 Amazon Web Services 担任首席工程师。Richard 毕业时荣获实时系统计算专业一等荣誉学位， 
并因对嵌入式技术发展的贡献而被授予荣誉博士学位。 
Richard 还直接参与多家公司的创办，并撰写了几本书籍。  
[查看此作者的文章](../author/ribarry) 


FreeRTOS 论坛：获得行业领先的专家支持，并与全球同行 
合作。[查看论坛](https://forums.freertos.org/)

