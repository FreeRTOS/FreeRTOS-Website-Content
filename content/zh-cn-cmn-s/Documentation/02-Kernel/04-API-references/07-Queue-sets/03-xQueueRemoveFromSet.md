---
title: xQueueRemoveFromSet()
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
BaseType_t xQueueRemoveFromSet
                      (
                          QueueSetMemberHandle_t xQueueOrSemaphore,
                          QueueSetHandle_t xQueueSet
                      );
```

必须在 FreeRTOSConfig.h 中将 configUSE_QUEUE_SETS 设置为 1，xQueueRemoveFromSet() API 函数才可用。

从队列集中删除 RTOS 队列或信号量。

仅当队列或信号量为空时，才能从队列集中删除 RTOS 队列或信号量
。


**参数：** 

- *xQueueOrSemaphore*

  从队列集中移除的队列或信号量的句柄（转换为 QueueSetMemberHandle_t 类型）。
  
- *xQueueSet*

  队列或信号量所在队列集的句柄。


**返回：** 

如果队列或信号量已成功从队列集中删除，
则返回 pdPASS。如果队列不在队列集中，或者
队列（或信号量）不为空，则返回 pdFAIL。


**用法示例：**

此示例假定 xQueueSet 是已创建的队列集，
而 xQueue 是已创建并添加到 xQueueSet 中的队列。

```c
    if( xQueueRemoveFromSet( xQueue, xQueueSet ) != pdPASS )
    {
        /* Either xQueue was not a member of the xQueueSet set, or xQueue is
           not empty and therefore cannot be removed from the set. */
    }
    else
    {
        /* The queue was successfully removed from the set. */
    }
```
