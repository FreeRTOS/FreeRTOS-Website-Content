---
title: uxSemaphoreGetCount
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[信号量](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/00-Semaphores)]

semphr. h

```c
UBaseType_t uxSemaphoreGetCount( SemaphoreHandle_t xSemaphore );
```

返回信号量计数。


**参数：** 

- *xSemaphore*

  正在查询的信号量的句柄。


**返回：** 

如果信号量是计数信号量，则返回信号量的当前计数值
。如果信号量是二进制信号量，
则当信号量可用时，返回 1，当信号量不可用时，
返回 0。

