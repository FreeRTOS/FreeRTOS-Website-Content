---
title: vTimerSetReloadMode
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[定时器 API](/Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions/)]

timers.h


```c
 void vTimerSetReloadMode( TimerHandle_t xTimer,
                           const UBaseType_t uxAutoReload );
```

将[软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)的“模式”更新为自动重新加载定时器或一次性
定时器。

自动重新加载定时器每次过期都会自行重置，从而导致定时器
定期到期（并因此执行其回调）。

一次性定时器不会自动重置，因此除非手动重新启动，
否则只会过期一次（并因此执行其回调）。

此 API 函数仅在已构建项目中包含 FreeRTOS/Source/timers.c 源文件时
可用。


**参数：** 

- *xTimer* 

  要更新的定时器的句柄。该句柄将从用于创建定时器的 
  [xTimerCreate()](/Documentation/02-Kernel/04-API-references/11-Software-timers/01-xTimerCreate/)
  或 [xTimerCreateStatic()](/Documentation/02-Kernel/04-API-references/11-Software-timers/22-xTimerCreateStatic) 的调用中返回。

- *uxAutoReload*

  将 `uxAutoReload` 设置为 `pdTRUE` 可将定时器设置为自动重新加载模式，设置为 `pdFALSE` 则可将定时器设置为一次性模式。
