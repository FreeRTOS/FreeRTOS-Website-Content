---
title: vQueueUnregisterQueue
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
 void vQueueUnregisterQueue( QueueHandle_t xQueue );
```

从队列注册表中移除队列。


**参数：**

- *xQueue*

  要从注册表中移除的队列的句柄。


队列注册表有两个用途，都与 RTOS 内核感知调试相关：

1. 可将文本名称和队列关联，以在调试 GUI 中轻松识别队列。
2. 提供调试器定位每个已注册队列和信号量所需的信息。

队列注册表仅在使用 RTOS 内核感知调试器时才有作用。

`configQUEUE_REGISTRY_SIZE` 定义可以注册的队列和信号量的最大数量。 
仅需注册那些要使用 RTOS 内核感知调试器查看的队列和信号量。 


### 示例 

```c
void vAFunction( void )
{
    QueueHandle_t xQueue;

    /* Create a queue big enough to hold 10 chars. */
    xQueue = xQueueCreate( 10, sizeof( char ) );

    /* We want this queue to be viewable in a RTOS kernel aware debugger, 
       so register it. */
    vQueueAddToRegistry( xQueue, "AMeaningfulName" );

    /* The queue gets used here. */

    /* At some later time, the queue is going to be deleted, first 
       remove it from the registry. */
    vQueueUnregisterQueue( xQueue );
    vQueueDelete( xQueue );
}
```
