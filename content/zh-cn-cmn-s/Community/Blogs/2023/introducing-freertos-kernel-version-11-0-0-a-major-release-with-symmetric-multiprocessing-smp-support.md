---
title: '11.0.0 版 FreeRTOS 内核简介: 支持对称多处理 (SMP) 的主要版本'
date: 2023 年 12 月 15 日
feature: blog
authors:
- aggarg
---
11.0.0 版 FreeRTOS 内核现已可供[下载](https://github.com/FreeRTOS/FreeRTOS-Kernel/releases/tag/V11.0.0)。此版本具有以下功能：

* 虽然 FreeRTOS 于 2017 年推出了对非对称多处理 (AMP) 的支持，但 11.0.0 版 FreeRTOS 
 首次将对称多处理 (SMP) 支持纳入主线版本。借助 SMP， 
 FreeRTOS 内核的实例可以在多个相同的处理器核心中调度任务。 
 要想快速入门，最简单的方法是使用以下任一预配置示例项目：


	+ [XCORE AI](https://github.com/FreeRTOS/FreeRTOS-Community-Supported-Demos/tree/main/XCORE.AI_xClang)
	+ [Raspberry Pico](https://github.com/FreeRTOS/FreeRTOS-Community-Supported-Demos/tree/main/CORTEX_M0%2B_RP2040)
	+ [TI Sitara AM64x](https://github.com/FreeRTOS/FreeRTOS-Partner-Supported-Demos/tree/main/CORTEX_A53_64-BIT_TI_AM64_SMP)详情请参阅 [FreeRTOS SMP 网页](../../symmetric-multiprocessing-introduction.md)。
* 将 MISRA 合规性检查从 PC Lint 切换到 Coverity，并从 MISRA C:2004 更新到 MISRA C:2012。
* FreeRTOS 移植新增多项安全增强功能，具有内存保护支持 (MPU)，可提高安全性。
* 优化跟踪支持，可更好地与跟踪工具集成。
* 其他一些增强和优化，例如可防止缓冲区溢出的 `vTaskList` 
 和 `vTaskGetRunTimeStats` 更新、堆强化、CMake 
 改进等。


FreeRTOS V11.0.0 直接取代了 FreeRTOS V10.6.x。


有关完整变更列表，请参阅[版本说明](https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/History.txt)。期待您的 
后续反馈。如有任何意见或请求，请访问 [FreeRTOS 论坛](https://forums.freertos.org/)！

