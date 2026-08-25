---
title: "crQUEUE_SEND"
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
crQUEUE_SEND(
              CoRoutineHandle_t xHandle,
              QueueHandle_t xQueue,
              void *pvItemToQueue,
              TickType_t xTicksToWait,
              BaseType_t *pxResult
            )
```

`crQUEUE_SEND` 是一个宏。上述原型中的数据类型仅供参考。

`crQUEUE_SEND()` 和 `crQUEUE_RECEIVE()` 宏是协程版的函数，
对应于任务中使用的 `xQueueSend()` 和 `xQueueReceive()` 函数。

`crQUEUE_SEND` 和 `crQUEUE_RECEIVE` 只能在协程中使用，而 `xQueueSend()`
和 `xQueueReceive()` 只能在任务中使用。**请注意**，协程
只能向其他协程发送数据。协程不能通过队列向任务发送数据，
任务也不能通过队列向协程发送数据。

`crQUEUE_SEND` 只能通过协程函数本身调用，
不能通过协程函数调用的其他函数调用。这是因为
协程无法维持自己的堆栈。

请参阅在线文档中的协程部分，
了解有关在任务与协程之间以及 ISR 与
协程之间传递数据的信息。


**参数：**

- *xHandle*

  调用协程的句柄。这是协程函数的 `xHandle` 参数。

- *xQueue*

  队列的句柄，数据将发布到此队列。使用
  `xQueueCreate()` API 函数创建队列时，该句柄作为返回值获得。

- *pvItemToQueue*

  指向发布到队列中的数据的指针。每个队列项的字节数
  会在创建队列时指定。此字节数从 `pvItemToQueue` 复制到队列本身。

- *xTickToDelay*

  如果队列中无立即可用空间，协程会阻塞以等待
  队列可用空间的滴答数。此滴答数可以转换为实际时间，实际时间
  由 `configTICK_RATE_HZ`（在 FreeRTOSConfig.h 中设置）定义。常量 `portTICK_PERIOD_MS` 可用于
  将滴答数转换为毫秒（请参阅下方示例）。

- *pxResult*

  如果从队列中成功检索到数据，则 `pxResult` 指向的变量将设置为 `pdPASS`，
  否则设置为 ProjDefs.h 中定义的错误。


**用法示例：**

```c
// Co-routine function that blocks for a fixed period then posts a number onto
// a queue.
static void prvCoRoutineFlashTask( CoRoutineHandle_t xHandle,
                                   UBaseType_t uxIndex )
{
    // Variables in co-routines must be declared static if they must maintain
    // value across a blocking call.
    static BaseType_t xNumberToPost = 0;
    static BaseType_t xResult;

    // Co-routines must begin with a call to crSTART().
    crSTART( xHandle );

    for( ;; )
    {
        // This assumes the queue has already been created.
        crQUEUE_SEND( xHandle,
                      xCoRoutineQueue,
                      &xNumberToPost,
                      NO_DELAY,
                      &xResult );

        if( xResult != pdPASS )
        {
            // The message was not posted!
        }

        // Increment the number to be posted onto the queue.
        xNumberToPost++;

        // Delay for 100 ticks.
        crDELAY( xHandle, 100 );
    }

    // Co-routines must end with a call to crEND().
    crEND();
 }
```

