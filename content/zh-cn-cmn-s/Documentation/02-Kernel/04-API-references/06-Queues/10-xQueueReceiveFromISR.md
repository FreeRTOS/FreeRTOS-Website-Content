---
title: xQueueReceiveFromISR
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[队列管理 ](/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]

queue. h 

```c
 BaseType_t xQueueReceiveFromISR
           (
               QueueHandle_t xQueue,
               void *pvBuffer,
               BaseType_t *pxHigherPriorityTaskWoken
           );
 ```

从队列中接收项目。从中断服务程序内使用此函数是安全的。


**参数：**

- *xQueue*

  要从中接收项目的队列的句柄。

- *pvBuffer* 

  指向缓冲区的指针，接收到的项目将被复制到这个缓冲区。 

- *pxHigherPriorityTaskWoken*

  任务可被阻塞，以等待队列可用空间。如果 `xQueueReceiveFromISR` 导致 
  该任务解除阻塞，`*pxHigherPriorityTaskWoken` 将被设置为 `pdTRUE`，否则 `*pxHigherPriorityTaskWoken` 
  将保持不变。从 FreeRTOS V7.3.0 开始，`pxHigherPriorityTaskWoken` 为可选参数， 
  可设置为 NULL。


**返回：**

- 如果从队列中成功接收项目，则返回 *pdTRUE*；
- 否则返回 *pdFALSE*。


**用法示例：** 

```c
QueueHandle_t xQueue;

/* Function to create a queue and post some values. */
void vAFunction( void *pvParameters )
{
    char cValueToPost;
    const TickType_t xTicksToWait = ( TickType_t )0xff;

    /* Create a queue capable of containing 10 characters. */
    xQueue = xQueueCreate( 10, sizeof( char ) );
    if( xQueue == 0 )
    {
        /* Failed to create the queue. */
    }

    /* ... */

    /* Post some characters that will be used within an ISR. If the queue
       is full then this task will block for xTicksToWait ticks. */
    cValueToPost = 'a';
    xQueueSend( xQueue, ( void * ) &cValueToPost, xTicksToWait );
    cValueToPost = 'b';
    xQueueSend( xQueue, ( void * ) &cValueToPost, xTicksToWait );

    /* ... keep posting characters ... this task may block when the queue
       becomes full. */

    cValueToPost = 'c';
    xQueueSend( xQueue, ( void * ) &cValueToPost, xTicksToWait );
}

/* ISR that outputs all the characters received on the queue. */
void vISR_Routine( void )
{
BaseType_t xTaskWokenByReceive = pdFALSE;
char cRxedChar;

    while( xQueueReceiveFromISR( xQueue,
                                ( void * ) &cRxedChar,
                                &xTaskWokenByReceive) )
    {
        /* A character was received. Output the character now. */
        vOutputCharacter( cRxedChar );

        /* If removing the character from the queue woke the task that was
           posting onto the queue xTaskWokenByReceive will have been set to
           pdTRUE. No matter how many times this loop iterates only one
           task will be woken. */
    }

    if( xTaskWokenByReceive != pdFALSE )
    {
        /* We should switch context so the ISR returns to a different task.
           NOTE: How this is done depends on the port you are using. Check
           the documentation and examples for your port. */
        taskYIELD ();
    }
}
```
  
