---
title: "从 FreeRTOS V10.4.4 升级到 V10.4.5"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 路线图和版本说明
description: 关于从 FreeRTOS V10.4.4 升级到 V10.4.5 的信息
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: FreeRTOS 简介
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: FreeRTOS初学者指南
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: 下载 FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: 常见问题
    link: /Why-FreeRTOS/FAQs
---


FreeRTOS V10.4.5 是 FreeRTOS V10.4.4 的升级版，适用于除安全端支持 ARMv8-M 移植以外的所有移植。


### ARMv8-M 安全端移植

从 ARMv8-M MCU（ARM Cortex-M23 和 Cortex-M33）非安全端调用安全函数的任务 
有两种上下文，一种位于非安全端，另一种位于安全端。以前版本的 FreeRTOS 
ARMv8-M 安全端移植会在运行时分配引用安全端上下文的结构体。现在， 
结构体会在编译时进行静态分配。此更改需要引入 
secureconfigMAX_SECURE_CONTEXTS 配置常量，用于设置静态分配的安全上下文的数量。 
如未定义，则 secureconfigMAX_SECURE_context 默认为 8。仅在非安全端使用 FreeRTOS 
代码的应用程序（例如在安全端运行第三方代码的应用程序）， 
不受此更改的影响。
