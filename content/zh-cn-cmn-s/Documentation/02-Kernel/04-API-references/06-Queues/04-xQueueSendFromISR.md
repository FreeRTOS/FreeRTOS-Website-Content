---
title: xQueueSendFromISR
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
 BaseType_t xQueueSendFromISR
           (
               QueueHandle_t xQueue,
               const void *pvItemToQueue,
               BaseType_t *pxHigherPriorityTaskWoken
           );
 ```

此宏用于调用 `xQueueGenericSendFromISR()` 函数。之所以包含此宏，
是为了向后兼容某些版本的 FreeRTOS，
这些版本未提供 `xQueueSendToBackFromISR()` 和 `xQueueSendToFrontFromISR()`
宏。

将项目发布到队列尾部。可以在中断服务程序中安全使用此函数。

项目通过复制而非引用的方式入队，因此最好只将较小的项目放入队列，
特别是从 ISR 调用时。在大多数情况下，最好存储一个指向正在排队的项目的指针。


**参数：**

- *xQueue*

  要向其中发布项目的队列的句柄。

- *pvItemToQueue*

  指向要放入队列中的项目的指针。队列能够存储的项目的大小 
  在创建队列时即已定义，因此 `pvItemToQueue` 中的这些字节将复制到 
  队列存储区中。

- *pxHigherPriorityTaskWoken*

  如果发送到队列会导致任务解除阻塞，并且解除阻塞的任务的优先级高于当前正在运行的任务，则 `xQueueSendFromISR()` 会将 `*pxHigherPriorityTaskWoken` 设置为 `pdTRUE` 
  。 
  如果 `xQueueSendFromISR()` 将此值设置为 `pdTRUE`，则应在中断退出前请求上下文切换 
  。从 FreeRTOS V7.3.0 开始，`pxHigherPriorityTaskWoken` 为可选参数， 
  可设置为 NULL。


**返回：**

- 如果数据成功发送至队列，则返回 *pdTRUE*， 
- 否则返回 *errQUEUE_FULL*。

缓冲 IO 的用法示例（每次调用时 ISR 可获得多个值）： 

```c
void vBufferISR( void )
{
    char cIn;
    BaseType_t xHigherPriorityTaskWoken;

    /* We have not woken a task at the start of the ISR. */
    xHigherPriorityTaskWoken = pdFALSE;

    /* Loop until the buffer is empty. */
    do
    {
        /* Obtain a byte from the buffer. */
        cIn = portINPUT_BYTE( RX_REGISTER_ADDRESS );

       /* Post the byte. */
       xQueueSendFromISR( xRxQueue, &cIn, &xHigherPriorityTaskWoken );

    } while( portINPUT_BYTE( BUFFER_COUNT ) );

    /* Now the buffer is empty we can switch context if necessary. */
    if( xHigherPriorityTaskWoken )
    {
        /* Actual macro used here is port specific. */
        taskYIELD_FROM_ISR ();
    }
}
```
