---
title: xTimerCreateStatic
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[定时器 API](/Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions/)]

timers.h


```c
 TimerHandle_t xTimerCreateStatic
                 ( const char * const pcTimerName,
                   const TickType_t xTimerPeriod,
                   const UBaseType_t uxAutoReload,
                   void * const pvTimerID,
                   TimerCallbackFunction_t pxCallbackFunction
                   StaticTimer_t *pxTimerBuffer );
```

创建一个新的[软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)实例，
并返回一个可以引用定时器的句柄。

要使此 RTOS API 函数可用：

1. configUSE_TIMERS 和 [configSUPPORT_STATIC_ALLOCATION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configsupport_static_allocation)
   都必须在 FreeRTOSConfig.h中设置为 1。
2. FreeRTOS/Source/timer.c C 源文件必须包含在构建中。

每个软件定时器都需要少量 RAM
来保存定时器的状态。如果定时器是使用 [xTimerCreate()](/Documentation/02-Kernel/04-API-references/11-Software-timers/01-xTimerCreate/) 创建的，
则所需的 RAM 将从 [FreeRTOS 堆](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)自动分配。
如果软件定时器是使用 xTimerCreateStatic() 创建的，
则 RAM 由应用程序编写器提供，这需要用到一个附加参数，
但允许在编译时静态分配 RAM。请参阅
[静态分配与动态分配](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation)页面了解更多信息。

定时器是在休眠状态下创建的。
[xTimerStart()](/Documentation/02-Kernel/04-API-references/11-Software-timers/04-xTimerStart)、
 [xTimerReset()](/Documentation/02-Kernel/04-API-references/11-Software-timers/08-xTimerReset)、
 [xTimerStartFromISR()](/Documentation/02-Kernel/04-API-references/11-Software-timers/09-xTimerStartFromISR)、
 [xTimerResetFromISR()](/Documentation/02-Kernel/04-API-references/11-Software-timers/12-xTimerResetFromISR)、
 [xTimerChangePeriod()](/Documentation/02-Kernel/04-API-references/11-Software-timers/06-xTimerChangePeriod)
 和 [xTimerChangePeriodFromISR()](/Documentation/02-Kernel/04-API-references/11-Software-timers/11-xTimerChangePeriodFromISR) API 函数都可以
 用于将定时器转换为活跃状态。


**参数：**

+ *pcTimerName*

  分配给定时器的可读文本名称。这样做纯粹是为了协助调试。定时器服务/守护进程任务的优先级
  RTOS 内核本身只通过句柄引用定时器，而不是通过其名称。

+ *xTimerPeriod*

  定时器的周期。周期以滴答为单位，宏 pdMS_TO_TICKS() 可用于
  将以毫秒为单位的时间转换为以滴答为单位的时间。例如，如果定时器必须
  在 100 个滴答后过期，则只需将 xNewPeriod 设置为100。或者，如果定时器必须在 500 毫秒之后过期，
  则只需将 xTimerPeriod 设置为 pdMS_TO_TICKS( 500 )。
  只有在 [configTICK_RATE_HZ](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configtick_rate_hz) 小于等于 1000 时，pdMS_TO_TICKS() 才可用。定时器周期
  必须大于 0。

+ *uxAutoReload*

  如果 uxAutoReload 设置为 pdTRUE，
  那么定时器将以 xTimerPeriod 参数设置的频率重复过期。如果 uxAutoReload 设置为 pdFALSE，则此定时器为一次性定时器，
  它会在到期后进入休眠状态。

+ *pvTimerID*

  分配给正在创建的定时器的标识符。通常情况下，
  当同一回调函数分配给多个定时器时，该函数将用于定时器回调函数，
  以识别哪个定时器过期，或者与 [vTimerSetTimerID()](/Documentation/02-Kernel/04-API-references/11-Software-timers/15-vTimerSetTimerID) 和
  [pvTimerGetTimerID()](/Documentation/02-Kernel/04-API-references/11-Software-timers/13-pvTimerGetTimerID) API 函数一起
  用于在定时器回调函数调用之间保存值。

+ *pxCallbackFunction*

  定时器到期时调用的函数。回调函数必须具有
  TimerCallbackFunction_t 定义的原型，即：

  ```c
  void vCallbackFunction( TimerHandle_t xTimer );
  ```

+ *pxTimerBuffer*

  必须指向一个 StaticTimer_t 类型的变量，然后用它来保存定时器的状态。


**返回：**

如果定时器创建成功，则返回新创建定时器的句柄。如果 pxTimerBuffer
为 NULL，则不会创建定时器，并返回 NULL。


**用法示例：**

```c
 pxTimerBuffer #define NUM_TIMERS 5

 /* An array to hold handles to the created timers. */
 TimerHandle_t xTimers[ NUM_TIMERS ];

 /* An array of StaticTimer_t structures, which are used to store
    the state of each created timer. */
 StaticTimer_t xTimerBuffers[ NUM_TIMERS ];

 /* Define a callback function that will be used by multiple timer
    instances. The callback function does nothing but count the number
    of times the associated timer expires, and stop the timer once the
    timer has expired 10 times. The count is saved as the ID of the
    timer. */
 void vTimerCallback( TimerHandle_t xTimer )
 {
 const uint32_t ulMaxExpiryCountBeforeStopping = 10;
 uint32_t ulCount;

    /* Optionally do something if the pxTimer parameter is NULL. */
    configASSERT( pxTimer );

    /* The number of times this timer has expired is saved as the
       timer's ID. Obtain the count. */
    ulCount = ( uint32_t ) pvTimerGetTimerID( xTimer );

    /* Increment the count, then test to see if the timer has expired
       ulMaxExpiryCountBeforeStopping yet. */
    ulCount++;

    /* If the timer has expired 10 times then stop it from running. */
    if( ulCount >= ulMaxExpiryCountBeforeStopping )
    {
        /* Do not use a block time if calling a timer API function
           from a timer callback function, as doing so could cause a
           deadlock! */
        xTimerStop( xTimer, 0 );
    }
    else
    {
       /* Store the incremented count back into the timer's ID field
          so it can be read back again the next time this software timer
          expires. */
       vTimerSetTimerID( xTimer, ( void * ) ulCount );
    }
 }

 void main( void )
 {
 long x;

    /* Create then start some timers. Starting the timers before
       the RTOS scheduler has been started means the timers will start
       running immediately that the RTOS scheduler starts. */
    for( x = 0; x < NUM_TIMERS; x++ )
    {
        xTimers[ x ] = xTimerCreateStatic
                  ( /* Just a text name, not used by the RTOS kernel. */
                    "Timer",
                    /* The timer period in ticks, must be greater than 0. */
                    ( 100 * x ) + 100,
                    /* The timers will auto-reload themselves when they expire. */
                    pdTRUE,
                    /* The ID is used to store a count of the number of times
                       the timer has expired, which is initialised to 0. */
                    ( void * ) 0,
                    /* Each timer calls the same callback when it expires. */
                    vTimerCallback,
                    /* Pass in the address of a StaticTimer_t variable, which
                       will hold the data associated with the timer being
                       created. */
                    &( xTimerBuffers[ x ] );
                  );

        if( xTimers[ x ] == NULL )
        {
            /* The timer was not created. */
        }
        else
        {
            /* Start the timer. No block time is specified, and
               even if one was it would be ignored because the RTOS
               scheduler has not yet been started. */
            if( [xTimerStart](/Documentation/02-Kernel/04-API-references/11-Software-timers/04-xTimerStart)( xTimers[ x ], 0 ) != pdPASS )
            {
                /* The timer could not be set into the Active state. */
            }
        }
    }

    /* ...
 Create tasks here.
 ... */

    /* Starting the RTOS scheduler will start the timers running as they have
       already been set into the active state. */
    vTaskStartScheduler();

    /* Should not reach here. */
    for( ;; );
 }
```
