---
title: FreeRTOS 常见问题 - ISR
created: 2018-09-20 00:00:00.0 UTC
description: ISR 故障排除
---


## 是否可以在 ISR 中进行上下文切换？

是的。每个 RTOS 移植都提供宏，以在 ISR 中请求上下文切换。宏 
名称取决于移植（因历史原因）。它将是 
portYIELD_FROM_ISR() 或 portEND_SWITCHING_ISR。请参阅 
[文档页面](/Documentation/02-Kernel/03-Supported-devices/00-Supported-devices)，
了解正在使用的移植的相关信息。

每个官方移植都随附一个演示应用程序，用于演示从 ISR 进行上下文切换。


## 如何撰写 RTOS 安全 ISR？

这取决于所使用的 FreeRTOS 的微控制器和工具链移植。请参阅 
[文档页面](/Documentation/02-Kernel/03-Supported-devices/00-Supported-devices)和演示应用程序， 
了解所使用的 RTOS 移植的相关信息。


## 可以嵌套中断吗？

这取决于移植。更多信息，请参阅 
[configKERNEL_INTERRUPT_PRIORITY 和 configMAX_SYSCALL_INTERRUPT_PRIORITY](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#kernel_priority) 
配置参数以获取更多信息。
