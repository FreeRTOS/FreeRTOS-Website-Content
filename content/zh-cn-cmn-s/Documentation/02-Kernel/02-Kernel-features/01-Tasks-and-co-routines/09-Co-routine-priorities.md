---
title: "FreeRTOS 协程"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: 适用于单核、非对称多核 (AMP) 和对称多核 (SMP) RTOS 配置的 FreeRTOS 调度算法
relatedLinks:
  - title: API 引用——协程
    link: /Documentation/02-Kernel/04-API-references/14-Co-routines/00-Co-routine API/
  - title: 协程示例
    link: /Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/11-Co-routine-example/
---

[[更多关于协程的信息……](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/06-Co-routine-overview)]


### 协程优先级

每个协程均会被分配优先级，值从 0 到 ( configMAX_CO_ROUTINE_PRIORITIES - 1 ) 不等。 
configMAX_CO_ROUTINE_PRIORITIES 在 FreeRTOSConfig.h 中定义， 
可以根据应用程序进行设置。

优先级数字较低，表示协程优先级也较低。

协程优先级只与其他协程相关。如果在同一应用程序内混用任务和协程， 
则任务的优先级将始终高于协程。
