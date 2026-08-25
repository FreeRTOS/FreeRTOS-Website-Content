---
title: "钩子函数"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: 钩子函数相关信息
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: FreeRTOS简介
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: FreeRTOS 初学者指南
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: 下载 FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: 常见问题
    link: /Why-FreeRTOS/FAQs
---

### 空闲钩子函数

空闲任务可以选择性地调用应用程序定义的钩子（或回调）函数 — 空闲钩子。
空闲任务以最低优先级运行，只有在没有可以运行的更高优先级任务时
这种空闲钩子函数才会运行。这使得空闲钩子函数成为使处理器进入低功率状态的理想场所 --
每当没有要执行的处理时自动进入
节能模式。

只有 configUSE_IDLE_HOOK 在 FreeRTOSConfig.h 中设置为 1 时，才会调用空闲钩子。当
该操作完成后，应用程序必须提供具有以下原型的钩子函数：

```c
void vApplicationIdleHook( void );
```

只要空闲任务正在运行，就会重复调用空闲钩子。最重要的是，空闲钩子函数
不调用任何可能导致其阻塞的 API 函数。此外，如果应用程序
使用 vTaskDelete() API 函数，则必须允许空闲任务钩子定期返回
（这是因为空闲任务负责清理 RTOS
内核分配给已删除任务的资源）。

---

### Tick 钩子函数

tick 中断可以选择性地调用应用程序定义的钩子（或回调）函数 — tick 钩子。
tick 钩子提供了一个方便的地方来实现定时器功能。

只有 configUSE_TICK_HOOK 在 FreeRTOSConfig.h 中设置为 1 时，才会调用 tick 钩子。该操作完成后，
应用程序必须提供具有以下原型的钩子函数：

```c
void vApplicationTickHook( void );
```

vApplicationTickHook() 从 ISR 内执行，因此必须非常短，不使用很多堆栈，并且不
调用任何不以 "FromISR" 或 "FROM_ISR" 结尾的 API 函数。

请参阅[演示应用程序文件 crhook.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS/Demo/Common/Minimal/crhook.c)，了解 tick 钩子使用方法的示例。

---

### Malloc 失败钩子函数

[heap_1.c、heap_2.c、heap_3.c、heap_4.c 和 heap_5.c](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) 实现的内存分配方案
可以选择性包含 malloc() 失败钩子（或回调）函数，该函数可以配置为在
pvPortMalloc() 返回 NULL 时调用。

定义 malloc() 失败钩子将有助于识别由堆内存不足引起的问题，特别是
在 API 函数中调用 pvPortMalloc() 失败时。

只有 configUSE_MALLOC_FAILED_HOOK 在 FreeRTOSConfig.h 中设置为 1 时，才会调用 malloc 失败钩子。
该操作完成后，应用程序必须提供具有以下原型的钩子函数：

```c
void vApplicationMallocFailedHook( void );
```

---

### 堆栈溢出钩子函数

请参阅[堆栈溢出保护](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/02-Stack-usage-and-stack-overflow-checking)页面，获取详细信息。

---

### 守护进程任务启动钩子

RTOS 守护进程任务与[定时器服务任务](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/02-Timer-service-daemon-task)相同。
有时它被称为守护进程任务，是因为该任务现在不仅仅用于服务定时器。

如果 configUSE_DAEMON_TASK_STARTUP_HOOK 在 FreeRTOSConfig.h 中设置为 1 ，
则守护进程任务首次开始执行时，会调用守护进程任务启动钩子
。如果应用程序包含会从调度器启动后执行中受益的初始化代码，
这将非常有用，允许
初始化代码利用 RTOS 功能。

如果 configUSE_DAEMON_TASK_STARTUP_HOOK 设置为 1 ，则应用程序编写者必须
提供守护进程任务启动钩子函数的实现，且具有以下名称和原型
。

```c
void vApplicationDaemonTaskStartupHook( void );
```
