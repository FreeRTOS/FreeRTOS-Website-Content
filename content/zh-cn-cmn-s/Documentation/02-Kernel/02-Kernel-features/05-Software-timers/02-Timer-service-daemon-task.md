---
title: "FreeRTOS 软件定时器"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: FreeRTOS 软件定时器
relatedLinks:
  - title: API 引用——软件定时器
    link: /Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions/
---

[[关于软件定时器的更多信息……](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)]

另请参阅 [RTOS 守护进程任务启动钩子](/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions/#daemon-task-startup-hook)函数。

### 定时器服务/守护进程任务和定时器命令队列

定时器是一个不属于核心 FreeRTOS 内核的可选功能，由
定时器服务（或守护进程）任务提供。

FreeRTOS 提供了一组与定时器相关的 API 函数。其中许多函数
使用标准 FreeRTOS 队列向定时器服务任务发送命令。用于
此目的的队列称为“定时器命令队列”。“定时器
命令队列”  专用于 FreeRTOS 定时器实现，无法
直接访问。

下图演示了这种情景。左边的代码表示
一个函数，属于用户应用程序的一部分，
并由作为同一用户应用程序的一部分创建的任务调用。右边的代码表示
定时器服务任务实现。
定时器命令队列将用户应用任务和定时器服务任务连接在一起。
在此演示案例中，应用程序代码
调用 xTimerReset() API 函数。其结果是复位命令会发送到定时器命令队列中，
再由定时器服务任务来处理。应用程序代码
只会调用 xTimerReset() API 函数，不会（也无法）直接
访问定时器命令队列。

![RTOS 定时器任务与定时器命令队列](/media/2018/rtos-timer-task-and-timer-command-queue.png)
应用程序代码、FreeRTOS 定时器 API、定时器命令队列和定时器服务任务的上下文。
