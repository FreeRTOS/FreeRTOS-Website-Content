---
title: xQueueAddToSet()
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
 BaseType_t xQueueAddToSet
                      (
                          QueueSetMemberHandle_t xQueueOrSemaphore,
                          QueueSetHandle_t xQueueSet
                      );
```

必须在 FreeRTOSConfig.h 中将 configUSE_QUEUE_SETS 设置为 1，才可使用 xQueueAddToSet() API 函数。

将 RTOS 队列或信号量添加至先前
通过调用 [xQueueCreateSet()](/Documentation/02-Kernel/04-API-references/07-Queue-sets/01-xQueueCreateSet) 创建的队列集中。

在对队列集的成员执行接收（对于队列）或获取（对于信号量）操作之前，
必须先调用
xQueueSelectFromSet()，该函数会返回一个指向该队列集成员的句柄。


**参数：** 

- *xQueueOrSemaphore*

  要添加到队列集中的队列或信号量的句柄（转换为 QueueSetMemberHandle_t 类型）。

- *xQueueSet*

  要向其中添加队列或信号量的队列集的句柄。


**返回：** 

如果队列或信号量成功添加到队列集，
则返回 pdPASS。如果队列因是另一个队列集的成员而无法成功添加到队列集，
则返回 pdFAIL
。


**用法示例：**

请参阅 [xQueueCreateSet()](/Documentation/02-Kernel/04-API-references/07-Queue-sets/01-xQueueCreateSet) 文档页面上的示例。
  
