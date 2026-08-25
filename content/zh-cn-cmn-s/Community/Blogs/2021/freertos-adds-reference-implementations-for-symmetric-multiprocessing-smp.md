---
title: FreeRTOS 添加对称多处理 (SMP) 的参考实现
created: 2021-10-14 00:00:00.0 UTC
feature: blog
categories:
- 长期支持
authors:
- stanmoy
relatedLinks:
- title: 什么是 FreeRTOS
  link: /Why-FreeRTOS/What-is-FreeRTOS/
---

本帖由 [Tanmoy Sen](../author/stanmoy) 于 2021 年 10 月 14 日发布

今年早些时候，我们[推出了](/Community/Blogs/2021/introducing-the-freertos-symmetric-multiprocessing-smp-github-branch) 
用于多核微控制器的 FreeRTOS 对称多处理 GitHub 分支。我们 
很高兴告诉大家，我们现已在 [XMOS](https://www.xmos.ai/) 
的 xcore 和 [Raspberry 的 Pi Pico ](https://www.raspberrypi.com/products/raspberry-pi-pico/) 这两个平台上推出参考实现。通过 FreeRTOS SMP， 
开发人员可以使用多核微控制器的 SMP 功能来设计应用程序。

多核微控制器，其中两个或多个相同的处理器内核共享同一内存，使得操作 
系统能够在内核之间分配任务，以根据应用程序的需要平衡处理器负载。 
这使得应用程序可以优化多核微控制器的资源利用率。FreeRTOS 
SMP 内核为具有多个计算核的系统提供了一套一致的配置选项、API 和行为 
。有了 SMP 内核，您将能够轻轻松松地在多核和单核系统之间进行转换 
。 

有关 FreeRTOS SMP 内核的详细信息，请参阅 
[带有 FreeRTOS](/Documentation/02-Kernel/02-Kernel-features/13-Symmetric-multiprocessing-introduction/) 的对称多处理 (SMP)  
（在 FreeRTOS.org 上） 
以及[移植到 FreeRTOS SMP 内核](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-SMP/blob/main/Porting-to-FreeRTOS-SMP-Kernel)。 
您可以从 [GitHub](https://github.com/FreeRTOS/FreeRTOS-Kernel/tree/smp) 下载 FreeRTOS SMP 内核源代码开始。


## 作者简介

![](https://secure.gravatar.com/avatar/4b004f93afe063d6b8444f0fafc89d00?s=200&d=mm&r=g)   
Tanmoy Sen 是 Amazon Web Services 的高级产品经理，他专注于帮助客户和 
嵌入式开发人员将基于微控制器的设备连接到云端。  
[查看此作者的文章](../author/stanmoy) 

FreeRTOS 论坛：获得行业领先的专家支持，并与全球同行 
合作。[查看论坛](https://forums.freertos.org/)

