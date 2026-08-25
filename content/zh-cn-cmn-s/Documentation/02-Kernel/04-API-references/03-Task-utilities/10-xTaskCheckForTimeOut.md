---
title: xTaskCheckForTimeOut()
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[任务实用程序](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities)]

task.h

```c
BaseType_t xTaskCheckForTimeOut( TimeOut_t * const pxTimeOut,
                                 TickType_t * const pxTicksToWait );
```

此功能仅适用于高级用户。

任务可以进入阻止状态以等待事件。通常情况下，任务
不会无限期地在阻止状态下等待，而是会指定一个超时时间段
。如果在任务等待的事件发生之前，超时期限已到，
任务将从阻止状态中删除。

如果任务在等待事件发生的过程中多次进入和退出阻塞状态，
对于事件发生，那么每次任务进入阻止状态时使用的超时时间
必须调整，才能确保花费在
阻止状态的所有时间不会超过最初指定的时时间。
xTaskCheckForTimeOut () 执行调整，同时考虑到
诸如滴答数溢出等情况，这种情况会形成容易出错的手动
调整。

xTaskCheckForTimeOut () 与 vTaskSetTimeOutState () 一起使用。
调用 vTaskSetTimeOutState () 以设置初始条件，然后
可以调用 xTaskCheckForTimeOut () 检查超时条件，并且
如果没有发生超时，则调整所述剩余块时间。


**参数：** 

+ *pxTimeOut* 

   指向结构体的指针，该结构体用于保存确定超时是否发生所需的信息。 
   pxTimeOut 使用 vTaskSetTimeOutState() 初始化。

+ *pxTicksToWait* 

  用于传出调整后的阻塞时间， 
  即考虑到已在阻塞状态下花费的时间后剩余的阻塞时间。


**返回：** 

如果返回 pdTRUE ，则没有块时间剩余，并且发生超时。

如果返回 pdFALSE ，则保留一些块时间，因此未发生超时。


**用法示例：**

```c
/* Driver library function used to receive uxWantedBytes from an Rx buffer that
   is filled by a UART interrupt. If there are not enough bytes in the Rx buffer
   then the task enters the Blocked state until it is notified that more data has
   been placed into the buffer. If there is still not enough data then the task
   re-enters the Blocked state, and xTaskCheckForTimeOut() is used to re-calculate
   the Block time to ensure the total amount of time spent in the Blocked state does
   not exceed MAX_TIME_TO_WAIT. This continues until either the buffer contains at
   least uxWantedBytes bytes, or the total amount of time spent in the Blocked state
   reaches MAX_TIME_TO_WAIT – at which point the task reads however many bytes are
   available up to a maximum of uxWantedBytes. */
size_t xUART_Receive( uint8_t *pucBuffer, size_t uxWantedBytes )
{
size_t uxReceived = 0;
TickType_t xTicksToWait = MAX_TIME_TO_WAIT;
TimeOut_t xTimeOut;

   /* Initialize xTimeOut. This records the time at which this function was
      entered. */
   vTaskSetTimeOutState( &xTimeOut );

   /* Loop until the buffer contains the wanted number of bytes, or a timeout
      occurs. */
   while( UART_bytes_in_rx_buffer( pxUARTInstance ) < uxWantedBytes )
   {
      /* The buffer didn't contain enough data so this task is going to
         enter the Blocked state. Adjusting xTicksToWait to account for any time
         that has been spent in the Blocked state within this function so far to
         ensure the total amount of time spent in the Blocked state does not exceed
         MAX_TIME_TO_WAIT. */
      if( xTaskCheckForTimeOut( &xTimeOut, &xTicksToWait ) != pdFALSE )
      {
         /* Timed out before the wanted number of bytes were available, exit the
            loop. */
         break;
      }

      /* Wait for a maximum of xTicksToWait ticks to be notified that the receive
         interrupt has placed more data into the buffer. */
      ulTaskNotifyTake( pdTRUE, xTicksToWait );
   }

   /* Attempt to read uxWantedBytes from the receive buffer into pucBuffer. The
      actual number of bytes read (which might be less than uxWantedBytes) is
      returned. */
   uxReceived = UART_read_from_receive_buffer( pxUARTInstance,
                                               pucBuffer,
                                               uxWantedBytes );

   return uxReceived;
}
```
