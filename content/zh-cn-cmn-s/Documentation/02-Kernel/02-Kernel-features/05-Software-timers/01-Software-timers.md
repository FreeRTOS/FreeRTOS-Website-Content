---
title: "FreeRTOS 软件定时器"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: FreeRTOS 软件定时器
relatedLinks:
  - title: API 引用 — 软件定时器
    link: /Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions/
---

本页内容：

- [软件定时器简介](#软件定时器简介)
- [软件定时器实现的效率考虑因素](#软件定时器实现的效率考虑因素)
- [关于写入定时器回调函数的重要信息](#关于写入定时器回调函数的重要信息)
- [定时器服务/守护进程任务和定时器命令队列](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/02-Timer-service-daemon-task)
- [配置应用程序以使用软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/03-Timer-daemon-configuration)
- [单次定时器与自动重载定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/04-One-shot-vs-auto-load)
- [重置软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/05-Resetting-a-timer)
- [API](/Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions/)

### 软件定时器简介

软件定时器（简称“定时器” ）能够让函数在
未来的设定时间执行。由定时器执行的函数称为定时器的
回调函数。从定时器启动到其回调函数执行之间的时间
被称为定时器的周期。简而言之，
当定时器的周期到期时，定时器的回调函数会被执行。

请注意，在使用软件定时器之前，必须明确地创建它。

### 软件定时器实现的效率考虑因素

软件定时器功能很容易实现，
但很难高效地实现。FreeRTOS 的实现不从中断上下文中执行定时器回调函数，
不消耗**任何**处理时间，
除非定时器实际上已经过期，不给 tick 中断增加任何处理开销，
并且在中断被禁用时
不走行任何链接列表结构体。

定时器服务任务（主要）利用现有 FreeRTOS 功能，
允许在对应用程序的可执行二进制文件的大小造成影响最小的情况下，
将定时器功能添加到应用程序中。

### 关于写入定时器回调函数的重要信息

定时器回调函数在定时器服务任务的上下文中执行。因此，
定时器回调函数永远不试图阻塞是**至关重要的**
。例如，定时器回调函数在访问队列或信号量时，不得调用 vTaskDelay()、
vTaskDelayUntil()，也不得
指定非零阻塞时间。
