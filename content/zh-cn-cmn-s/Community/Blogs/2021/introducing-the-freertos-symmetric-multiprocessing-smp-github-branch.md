---
title: 介绍 FreeRTOS 对称多处理 (SMP) 的 Github 分支
created: 2021-06-30 00:00:00.0 UTC
feature: blog
categories:
- 长期支持
authors:
- luciodj
relatedLinks:
- title: 什么是 FreeRTOS
  link: /Why-FreeRTOS/What-is-FreeRTOS/
---

本帖由 [Lucio Di Jasio](../author/luciodj) 于 2021 年 6 月 30 日发布

随着制程缩小，对物理极限的不断接近，在过去十年中，我们都习惯了 
台式机和笔记本中的多核芯片，其复杂程度越来越高，不断增强的性能也在扩展摩尔定律的边界 
。在嵌入式控制中，对成本、大小和稳健性的要求通常优先于性能， 
似乎随着 
IoT、通信、数字信号处理和人工智能出现若干创新的多核微控制器，多核时代终于来临。FreeRTOS  
社区已经认识到这种趋势，因为社区中贡献的许多内容旨在扩展 FreeRTOS 内核 
以支持对称多处理 (SMP) 应用程序。为了创造空间强化这些贡献， 
我们创建了一个新的 [FreeRTOS 内核 SMP 分支](https://github.com/FreeRTOS/FreeRTOS-Kernel/tree/smp)。 

在迄今为止最具影响力的贡献中，我们不得不提到 [Espressif](https://www.espressif.com/en) 
（其中配备 Tensilica Xtensa 和 RISC-V 多核 SoC，用于无线连接和 IoT（之前是 
 FreeRTOS 内核的一个分支）），以及 [XMOS](https://www.xmos.ai/) （配备原始 xcore 平台，通过将不同形式的计算（如DSP、AI 等）融合 
在一个均质的环境中，为 IoT 解决方案的架构提供了极大的灵活性， 
简化了开发、测试和维护方式，提高了成本效益。 
有关 XMOS SMP 移植的更多信息，请参阅 
相关[新闻稿](https://www.xmos.ai/xmos-announces-the-launch-of-smp-freertos-for-multicore-processors-in-collaboration-with-amazon-web-services/)。 
未来几个月将增加适用于更多架构、供应商和 SoC 的移植。虽然仍有很多 
工作要做，但我们邀请所有 FreeRTOS 用户尝试 SMP。 我们非常欢迎您为此提出创意，做出贡献， 
一起书写 FreeRTOS 演变的全新篇章。 

通过克隆 FreeRTOS SMP [Github](https://github.com/FreeRTOS/FreeRTOS-Kernel/tree/smp)  
存储库分支即刻参与，或者选择接收 Github 关于此分支的新消息和活动的通知。


## 作者简介

![](https://secure.gravatar.com/avatar/9938f7b242eb47e5e8c3f41e0e927283?s=200&d=mm&r=g)   
Lucio 是 Amazon Web Services 的产品经理。过去 20 年里，他在半导体行业 
担任过各种技术和营销职务。作为一个富有见解的高产作者，他发表了 
许多关于嵌入式控制应用程序编程的文章和技术书籍。热爱 
飞行的他又获得了 FAA 和 EASA 私人飞行员执照。  
[查看此作者的文章](../author/luciodj) 

FreeRTOS 论坛：获得行业领先的专家支持，并与全球同行 
合作。[查看论坛](https://forums.freertos.org/)

