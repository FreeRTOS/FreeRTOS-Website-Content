---
title: xQueueOverwrite
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
 BaseType_t xQueueOverwrite(
 QueueHandle_t xQueue,
 const void * pvItemToQueue
 );
```

这是用于调用 xQueueGenericSend() 函数的宏。

即使队列已满的情况下也将写入队列的 [xQueueSendToBack()](/Documentation/02-Kernel/04-API-references/06-Queues/05-xQueueSendToBack) 版本， 
同时覆盖队列中已经 
存在的数据。

xQueueOverwrite() 旨在用于长度为 1 的队列， 
这意味着队列要么为空，要么为满。

不得从中断服务程序 (ISR) 调用此函数。
请参阅 xQueueOverwriteFromISR()，了解可在 ISR 中使用的替代函数。

如果应用程序使用 `xQueueOverwrite` 向一个已经满的队列写入数据，并且该队列恰好是队列集合的成员,
那么由于队列中的项目数量没有变化，`xQueueSetSelect` 将不会返回该队列句柄。
**参数：**

+ *xQueue*  

  接收发送数据的队列的句柄。

+ *pvItemToQueue*  

  指向待入队数据项的指针。创建队列时定义了队列将保留的项的大小， 
  [因此固定数量的字节](/Documentation/02-Kernel/04-API-references/06-Queues/01-xQueueCreate)将从 pvItemToQueue 复制到 
  队列存储区。


**返回：** 

xQueueOverwrite() 是用于调用 xQueueGenericSend() 的宏，
因此与 
xQueueSendToFront() 具有相同的返回值。不过，由于
xQueueOverwrite() 将写入队列（即使队列已满），
pdPASS 是唯一可以返回的值。


**用法示例：**

```c
void vFunction( void *pvParameters )
{
QueueHandle_t xQueue;
unsigned long ulVarToSend, ulValReceived;

   /* Create a queue to hold one unsigned long value. It is strongly
      recommended *not* to use xQueueOverwrite() on queues that can
      contain more than one value, and doing so will trigger an assertion
if configASSERT() is defined. */
    xQueue = xQueueCreate( 1, sizeof( unsigned long ) );

    /* Write the value 10 to the queue using xQueueOverwrite(). */
    ulVarToSend = 10;
    xQueueOverwrite( xQueue, &ulVarToSend );

    /* Peeking the queue should now return 10, but leave the value 10 in
       the queue. A block time of zero is used as it is known that the
       queue holds a value. */
    ulValReceived = 0;
    xQueuePeek( xQueue, &ulValReceived, 0 );

    if( ulValReceived != 10 )
    {
        /* Error, unless another task removed the value. */
    }

    /* The queue is still full. Use xQueueOverwrite() to overwrite the
       value held in the queue with 100. */
    ulVarToSend = 100;
    xQueueOverwrite( xQueue, &ulVarToSend );

    /* This time read from the queue, leaving the queue empty once more.
       A block time of 0 is used again. */
    xQueueReceive( xQueue, &ulValReceived, 0 );

    /* The value read should be the last value written, even though the
       queue was already full when the value was written. */
    if( ulValReceived != 100 )
    {
        /* Error unless another task is using the same queue. */
    }

    /* ... */
}
```
