---
title: xQueuePeekFromISR
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[队列管理](/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]


queue.h 

```c
BaseType_t xQueuePeekFromISR(
                              QueueHandle_t xQueue,
                              void *pvBuffer,
                             );
```

可以用于中断服务程序 (ISR) 的 [xQueuePeek()](/Documentation/02-Kernel/04-API-references/06-Queues/13-xQueuePeek) 版本
。

从队列中接收项目，而无须从队列中删除该项目。
项目通过复制的方式接收，因此必须提供
足够大的缓冲区。复制到缓冲区中的字节数
在创建队列时即已定义。

成功接收的项目将保留在队列中，因此会在下一次调用时返回，
或者在调用任何队列接收函数时返回。


**参数：** 


+ *xQueue*  

  要从中接收项目的队列的句柄。

+ *pvBuffer*  

  指向缓冲区的指针，接收的项目将复制到此缓冲区。缓冲区的大小必须至少足够 
  存储在创建队列时定义的队列项目的大小。


**返回：** 

+ 如果成功从队列中接收（窥视）项目，则返回 pdTRUE，
+ 否则返回 pdFALSE。

