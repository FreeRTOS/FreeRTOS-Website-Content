---
title: "crQUEUE_SEND_FROM_ISR"
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
              void *pvItemToQueue,
              BaseType_t xCoRoutinePreviouslyWoken
            )
```

`crQUEUE_SEND_FROM_ISR()` 是一个宏。上述原型中的数据类型仅供参考。

`crQUEUE_SEND_FROM_ISR()` 和 `crQUEUE_RECEIVE_FROM_ISR()` 宏是
协程版的函数，对应于任务中使用的 `xQueueSendFromISR()` 和 `xQueueReceiveFromISR()`
函数。

`crQUEUE_SEND_FROM_ISR()` 和 `crQUEUE_RECEIVE_FROM_ISR()` 只能用于
在协程和 ISR 之间传递数据，而 `xQueueSendFromISR()`
和 `xQueueReceiveFromISR()` 只能用于在任务和 ISR 之间
传递数据。

`crQUEUE_SEND_FROM_ISR` 只能从 ISR 调用，以将数据发送到
协程内正在使用的队列。

请参阅在线文档中的协程部分，
了解有关在任务与协程之间以及 ISR 与
协程之间传递数据的信息。


**参数：**

- *xQueue*

  队列的句柄，数据项将发布到此队列。

- *pvItemToQueue*

  指向待入队列的数据项的指针。队列能够存储的项目的大小
  在创建队列时即已定义，因此 `pvItemToQueue` 中的这些字节将复制到
  队列存储区。

- *xCoRoutinePreviouslyWoken*

  包含此参数，ISR 就可以从单个中断多次发送到同一个队列。可编辑
  第一个调用应始终传入 `pdFALSE`。后续调用应传入从上一个调用返回的值
  。


**返回值：**

- 如果发布到队列将协程唤醒，则返回 *pdTRUE*。ISR 使用此信息来确定
  ISR 之后是否需要上下文切换。


**用法示例：**

```c
// A co-routine that blocks on a queue waiting for characters to be received.
static void vReceivingCoRoutine( CoRoutineHandle_t xHandle,
                                 UBaseType_t uxIndex )
{
    char cRxedChar;
    BaseType_t xResult;

    // All co-routines must start with a call to crSTART().
    crSTART( xHandle );

    for( ;; )
    {
        // Wait for data to become available on the queue.  This assumes the
        // queue xCommsRxQueue has already been created!
        crQUEUE_RECEIVE( xHandle,
                         xCommsRxQueue,
                         &uxLEDToFlash,
                         portMAX_DELAY,
                         &xResult );

        // Was a character received?
        if( xResult == pdPASS )
        {
            // Process the character here.
        }
    }

    // All co-routines must end with a call to crEND().
    crEND();
}

// An ISR that uses a queue to send characters received on a serial port to
// a co-routine.
void vUART_ISR( void )
{
    char cRxedChar;
    BaseType_t xCRWokenByPost = pdFALSE;

    // We loop around reading characters until there are none left in the UART.
    while( UART_RX_REG_NOT_EMPTY() )
    {
        // Obtain the character from the UART.
        cRxedChar = UART_RX_REG;

        // Post the character onto a queue.  xCRWokenByPost will be pdFALSE
        // the first time around the loop.  If the post causes a co-routine
        // to be woken (unblocked) then xCRWokenByPost will be set to pdTRUE.
        // In this manner we can ensure that if more than one co-routine is
        // blocked on the queue only one is woken by this ISR no matter how
        // many characters are posted to the queue.
        xCRWokenByPost = crQUEUE_SEND_FROM_ISR( xCommsRxQueue,
                                                 &cRxedChar,
                                                 xCRWokenByPost );
    }
}
```

