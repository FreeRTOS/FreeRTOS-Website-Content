---
title: pvTimerGetTimerID
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
 void *pvTimerGetTimerID( TimerHandle_t xTimer );
```

返回分配给[软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)的 ID。

使用创建定时器时调用 [xTimerCreate()](/Documentation/02-Kernel/04-API-references/11-Software-timers/01-xTimerCreate/) 的 `pvTimerID` 参数
为定时器分配 ID。

创建定时器时，会为定时器分配一个标识符 (ID)，
您随时可以使用 [vTimerSetTimerID()](/Documentation/02-Kernel/04-API-references/11-Software-timers/15-vTimerSetTimerID) API 函数更改此 ID。

如果将同一个回调函数分配给多个定时器，
则可以在回调函数内检查定时器标识符，
以确定哪个定时器实际已到期。

在定时器回调函数的调用之间，定时器标识符也可用于将数据存储在定时器中
。


**参数：**

- *xTimer*

  被查询的定时器。


**返回：**

- 分配给被查询的定时器的 ID。


**用法示例：**

请参阅 [xTimerCreate() 文档页面](/Documentation/02-Kernel/04-API-references/11-Software-timers/01-xTimerCreate/)
和 [vTimerSetTimerID() 文档页面](/Documentation/02-Kernel/04-API-references/11-Software-timers/15-vTimerSetTimerID)上的示例。
