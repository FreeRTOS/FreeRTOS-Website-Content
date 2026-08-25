---
title: "xTimerGetReloadMode , uxTimerGetReloadMode"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[定时器 API](/Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions/)]

task.h

```c
BaseType_t  xTimerGetReloadMode( TimerHandle_t xTimer );
UBaseType_t uxTimerGetReloadMode( TimerHandle_t xTimer );
```

查询 xTimer 句柄引用的[软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)的“模式”。 

该模式可以是自动重载定时器（每次到期都会自动重置），或者 
一次性计时器（除非手动重新启动，否则仅到期一次）。

xTimerGetReloadMode 和 uxTimerGetReloadMode 仅在其返回类型上有所不同。xTimerGetReloadMode 
返回 BaseType_t，以匹配实际返回值 pdTRUE/pdFALSE 的类型。提供 uxTimerGetReloadMode 是为了保证向后兼容， 
新的应用程序应该使用 xTimerGetReloadMode 来代替。

这些 API 函数仅在已构建项目中包含 FreeRTOS 'timers.c' 源文件， 
并且在 FreeRTOSConfig.h中将 configUSE_TIMERS 设置为 1 时才可用。


**参数：**

+ *xTimer* 

  要查询的定时器的句柄。该句柄将从用于创建定时器的 
  [xTimerCreate()](/Documentation/02-Kernel/04-API-references/11-Software-timers/01-xTimerCreate/) 或 [xTimerCreateStatic()](/Documentation/02-Kernel/04-API-references/11-Software-timers/22-xTimerCreateStatic) 调用中 
  返回。


**返回：**

如果句柄为 xTimer 的定时器为自动重载定时器，则返回 pdTRUE，否则返回 pdFALSE。
