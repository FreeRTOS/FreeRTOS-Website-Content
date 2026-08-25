---
title: FreeRTOS 常见问题 - 调度
created: 2018-09-20 00:00:00.0 UTC
description: 有关 FreeRTOS 调度的信息
---


## FreeRTOS 调度策略是什么？

请参阅[本页](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/04-Task-scheduling)，此页面专门介绍单核处理器 
和多核处理器的调度策略。


## 如何调度具有同等优先级的任务？

轮循调度：优先级相同且处于就绪状态的任务轮流运行。


## 如何调度具有同等空闲优先级的任务？

按照具有同等其他优先级时的方式调度。但是，如果存在其他可以运行的具有空闲优先级的应用程序任务，则可以配置 [configIDLE_SHOULD_YIELD](/Documentation/02-Kernel/03-Supported-devices/02-Customization) 常量， 
强制空闲任务在完成一次循环迭代后让出处理器 
。
