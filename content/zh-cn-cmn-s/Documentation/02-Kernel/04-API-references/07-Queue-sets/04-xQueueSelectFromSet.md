---
title: xQueueSelectFromSet()
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
 QueueSetMemberHandle_t xQueueSelectFromSet
                       (
                             QueueSetHandle_t xQueueSet,
                             const TickType_t xTicksToWait
                        );
```

必须在 FreeRTOSConfig.h 中将 configUSE_QUEUE_SETS 设置为 1，才可使用 xQueueSelectFromSet() API 函数。

xQueueSelectFromSet() 会从队列集的成员中选择包含数据的队列
或可用（可以获取）的信号量。
xQueueSelectFromSet() 实际上
允许任务同时在队列集中的所有队列和信号量上
阻塞（挂起），等待读取操作。

注意：

* 您也可以不使用队列集，而是采用更简单的替代方案。请参阅
  [阻塞多个对象](/Documentation/02-Kernel/02-Kernel-features/10-Blocking-on-multiple-RTOS-objects)页面，
  了解更多信息。

* 阻塞包含互斥锁的队列不会导致
  互斥锁持有者继承被阻塞任务的优先级。

* 在对队列集的成员执行接收（对于队列）或获取（对于信号量）操作之前，
  必须先调用
  xQueueSelectFromSet()，该函数会返回一个指向该队列集成员的句柄。


**参数：** 

+ *xQueueSet* 

  任务（可能）在其上处于阻塞状态的队列集。

+ *xTicksToWait* 

  调用任务处于阻塞状态（其他任务继续执行） 
  且愿意等待队列集的成员准备好进行成功的队列读取或信号量获取操作的最长时间 
  （以滴答为单位）。


**返回：** 

xQueueSelectFromSet() 将返回队列集中包含数据的队列的句柄
（转换为 QueueSetMemberHandle_t 类型），
或返回队列集中可用信号量的句柄（转换为 QueueSetMemberHandle_t 类型）；
如果在指定的阻塞时间到期之前不存在这样的队列或信号量，
则返回 NULL。


**用法示例：**

请参阅 [xQueueCreateSet()](/Documentation/02-Kernel/04-API-references/07-Queue-sets/01-xQueueCreateSet) 文档页面上的示例。  
