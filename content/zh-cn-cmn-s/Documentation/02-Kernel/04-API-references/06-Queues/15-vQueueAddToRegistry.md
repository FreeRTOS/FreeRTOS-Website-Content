---
title: vQueueAddToRegistry
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[队列管理 ](/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]

queue.h 

```c
void vQueueAddToRegistry(
                          QueueHandle_t xQueue,
                          char *pcQueueName,
                        );
```

为队列指定名称，并将队列添加到注册表。


**参数：**

- *xQueue*

  添加到注册表的队列的句柄。
  
- *pcQueueName*

  为队列指定的名称。此为文本字符串，仅为便于调试之用。队列注册表 
  仅存储指向该字符串的指针，因此该字符串必须具有持久性（全局变量， 
  或最好是在 ROM/Flash 中），而不是在堆栈上定义。


队列注册表有两项用途，都与 RTOS 内核感知调试相关：

1. 可将文本名称和队列关联，以在调试 GUI 中轻松识别队列。
2. 包含调试器定位每个已注册队列和信号量所需的信息。

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
}
```
