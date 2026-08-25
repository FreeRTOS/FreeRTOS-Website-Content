---
title: 具有统一 IPv4 和 IPv6 功能且支持多接口的 FreeRTOS-Plus-TCP 现已全面推出
date: 2023 年 8 月 16 日
feature: blog
authors:
  - stanmoy
---

我们很高兴地宣布具有统一 IPv4 和 IPv6 功能且支持多接口的 FreeRTOS-Plus-TCP v4.0.0 
现已全面推出。开发者现可使用 FreeRTOS-Plus-TCP 库进行基于 IPv6 的嵌入式 
应用程序开发，设计使用多个网络接口的应用程序，并在同一库中同时选择 IPv6、IPv4、 
TCP 和 UDP，以优化内存占用。

FreeRTOS-Plus-TCP 已使用 C 边界模型检查器 
([CBMC](/Community/Blogs/2020/ensuring-the-memory-safety-of-freertos-part-1)) 
自动推理工具进行内存安全性检查，该工具旨在帮助缓解缓冲区溢出等代码安全问题。 
此外，FreeRTOS-Plus-TCP 已通过渗透测试，并已完成特定代码质量检查， 
包括 [MISRA-C](https://www.misra.org.uk/) 合规性和 [Coverity](https://scan.coverity.com/) 静态分析， 
旨在帮助提高嵌入式系统中代码的安全性、可移植性和可靠性 
（请参阅 [LTS 代码质量检查清单](/Documentation/03-Libraries/01-Library-overview/03-LTS-libraries/01-LTS-libraries#lts-code-quality-checklist)）。 
如需了解更多信息并开始使用，请参阅 FreeRTOS-Plus-TCP 库简介页面 
（位于 [freertos.org](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP)）、 
[演示](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/FreeRTOS_Plus_TCP_IPv6_Demo/IPv6_Multi_WinSim_demo) 
或 [GitHub](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP) 上的代码。

