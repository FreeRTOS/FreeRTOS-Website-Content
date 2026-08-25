---
title: "crQUEUE_RECEIVE_FROM_ISR"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[协程专用](/Documentation/02-Kernel/04-API-references/14-Co-routines/00-Co-routine-API)]

croutine.h

```c
BaseType_t crQUEUE_SEND_FROM_ISR
           (
             QueueHandle_t xQueue,
             void *pvBuffer,
             BaseType_t * pxCoRoutineWoken
           )
```

`crQUEUE_SEND_FROM_ISR()` 和 `crQUEUE_RECEIVE_FROM_ISR()` 宏是
协程版的函数，对应于任务中使用的 `xQueueSendFromISR()` 和 `xQueueReceiveFromISR()`
函数。

`crQUEUE_SEND_FROM_ISR()` 和 `crQUEUE_RECEIVE_FROM_ISR()` 只能用于
在协程和 ISR 之间传递数据，而 `xQueueSendFromISR()`
和 `xQueueReceiveFromISR()` 只能用于在任务和 ISR 之间
传递数据。

`crQUEUE_RECEIVE_FROM_ISR` 只能从 ISR 中调用，以从
协程中（发布到队列的协程）正在使用的队列接收数据
。

请参阅在线文档中的协程部分，
了解有关在任务与协程之间以及 ISR 与
协程之间传递数据的信息。


**参数：**

- *xQueue*

  队列的句柄，数据项将发布到此队列。

- *pvBuffer*

  指向缓冲区的指针，接收到的项目将被放入此缓冲区中。队列能够存储的项目的大小
  在创建队列时即已定义，因此队列中的这些字节将复制到 pvBuffer。

- *pxCoRoutineWoken*

  协程在等待队列空间可用时可能会被阻塞。如果 `crQUEUE_RECEIVE_FROM_ISR`
  导致协程解除阻塞，`*pxCoRoutineWoken` 将被设置为 `pdTRUE`，否则 `*pxCoRoutineWoken`
  将保持不变。


**返回值：**

- 如果从队列中成功接收项目，则返回 *pdTRUE*；
- 否则返回 *pdFALSE*。


**用法示例：**

```c
// A co-routine that posts a character to a queue then blocks for a fixed
// period.  The character is incremented each time.
static void vSendingCoRoutine( CoRoutineHandle_t xHandle,
                               UBaseType_t uxIndex )
{
    // cChar holds its value while this co-routine is blocked and must therefore
    // be declared static.
    static char cCharToTx = 'a';
    BaseType_t xResult;

    // All co-routines must start with a call to crSTART().
    crSTART( xHandle );

    for( ;; )
    {
        // Send the next character to the queue.
        crQUEUE_SEND( xHandle,
                      xCoRoutineQueue,
                      &cCharToTx,
                      NO_DELAY,
                      &xResult );

        if( xResult == pdPASS )
        {
            // The character was successfully posted to the queue.
        }
        else
        {
            // Could not post the character to the queue.
        }

        // Enable the UART Tx interrupt to cause an interrupt in this
        // hypothetical UART.  The interrupt will obtain the character
        // from the queue and send it.
        ENABLE_RX_INTERRUPT();

        // Increment to the next character then block for a fixed period.
        // cCharToTx will maintain its value across the delay as it is
        // declared static.
        cCharToTx++;
        if( cCharToTx > 'x' )
        {
            cCharToTx = 'a';
        }
        crDELAY( 100 );
    }

    // All co-routines must end with a call to crEND().
    crEND();
}

// An ISR that uses a queue to receive characters to send on a UART.
void vUART_ISR( void )
{
    char cCharToTx;
    BaseType_t xCRWokenByPost = pdFALSE;

    while( UART_TX_REG_EMPTY() )
    {
        // Are there any characters in the queue waiting to be sent?
        // xCRWokenByPost will automatically be set to pdTRUE if a co-routine
        // is woken by the post - ensuring that only a single co-routine is
        // woken no matter how many times we go around this loop.
        if( crQUEUE_RECEIVE_FROM_ISR( xQueue, &cCharToTx, &xCRWokenByPost ) )
        {
            SEND_CHARACTER( cCharToTx );
        }
    }
}
```

