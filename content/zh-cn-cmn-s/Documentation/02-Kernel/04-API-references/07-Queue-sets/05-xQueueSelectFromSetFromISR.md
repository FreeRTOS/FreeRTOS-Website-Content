---
title: xQueueSelectFromSetFromISR()
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[队列集 API](/Documentation/02-Kernel/04-API-references/07-Queue-sets/00-RTOS-queue-sets)]

queue.h

```c
 QueueSetMemberHandle_t xQueueSelectFromSetFromISR
                       (
                             QueueSetHandle_t xQueueSet
                        );
```

必须在 FreeRTOSConfig.h 中将 configUSE_QUEUE_SETS 设置为 1，xQueueSelectFromSetFromISR() API 函数才可用。

[xQueueSelectFromSet()](/Documentation/02-Kernel/04-API-references/07-Queue-sets/04-xQueueSelectFromSet) 的一个版本，
可以从中断服务程序 (ISR) 中使用。


**参数：** 

+ *xQueueSet* 

  正在查询的队列集。读取时不可能阻塞， 
  因为该函数旨在通过中断使用。


**返回：** 

xQueueSelectFromSetFromISR() 将返回一个队列的句柄（被转换为 QueueSetMemberHandle_t 类型），
该队列包含在包含数据的队列集中，
或队列集中可用信号量的句柄（转换为 QueueSetMemberHandle_t 类型），
该信号量包含在可用的队列集中；如果不存在这样的队列或信号量，则返回 NULL
。

