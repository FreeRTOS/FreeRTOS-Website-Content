---
title: vTaskStepTick
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[RTOS 内核控制](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/00-Kernel-control)]

task.h

```c
 void vTaskStepTick( TickType_t xTicksToJump );
```

如果 RTOS 配置为使用[无滴答空闲功能](/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support)，
则只要空闲任务是唯一能够执行的任务，
滴答中断就会停止，并且微控制器会进入低功耗状态。在退出低功率状态时，
必须校正滴答计数值，
以包含停止时所经过的时间。

如果 FreeRTOS 移植包含默认 [portSUPPRESS_TICKS_AND_SLEEP()](/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support) 实现，
则会在内部使用 `vTaskStepTick()` 来确保
滴答计数值正确。`vTaskStepTick()` 是一个公共 API 函数，
可用于覆盖默认的 `portSUPPRESS_TICKS_AND_SLEEP()` 实现，
如果正在使用的移植不提供默认值，则提供 `portSUPPRESS_TICKS_AND_SLEEP()`
。

必须将 `configUSE_TICKLESS_IDLE` 配置常量设置为 1，
`vTaskStepTick()` 才可用。


**参数：** 

- *xTicksToJump*

  自滴答中断停止以来经过的 RTOS 滴答数。为使该功能正确运行， 
  参数必须小于或等于 `portSUPPRESS_TICKS_AND_SLEEP()` 参数。


**返回：** 

*无。*


**用法示例：**

该示例演示了对多个函数的调用。只有 `vTaskStepTick()`
是 FreeRTOS API 的一部分。其他函数特定于
所用硬件上可用的时钟和节能模式，因此必须
由应用程序写入器提供。

```c
/* First define the portSUPPRESS_TICKS_AND_SLEEP(). The parameter is the time,
   in ticks, until the kernel next needs to execute. */
#define portSUPPRESS_TICKS_AND_SLEEP( xIdleTime ) vApplicationSleep( xIdleTime )

/* Define the function that is called by portSUPPRESS_TICKS_AND_SLEEP(). */
void vApplicationSleep( TickType_t xExpectedIdleTime )
{
    unsigned long ulLowPowerTimeBeforeSleep, ulLowPowerTimeAfterSleep;

    /* Read the current time from a time source that will remain operational
       while the microcontroller is in a low power state. */
    ulLowPowerTimeBeforeSleep = ulGetExternalTime();

    /* Stop the timer that is generating the tick interrupt. */
    prvStopTickInterruptTimer();

    /* Configure an interrupt to bring the microcontroller out of its low power
       state at the time the kernel next needs to execute. The interrupt must be
       generated from a source that is remains operational when the microcontroller
       is in a low power state. */
    vSetWakeTimeInterrupt( xExpectedIdleTime );

    /* Enter the low power state. */
    prvSleep();

    /* Determine how long the microcontroller was actually in a low power state
       for, which will be less than xExpectedIdleTime if the microcontroller was
       brought out of low power mode by an interrupt other than that configured by
       the vSetWakeTimeInterrupt() call. Note that the scheduler is suspended
       before portSUPPRESS_TICKS_AND_SLEEP() is called, and resumed when
       portSUPPRESS_TICKS_AND_SLEEP() returns. Therefore no other tasks will
       execute until this function completes. */
    ulLowPowerTimeAfterSleep = ulGetExternalTime();

    /* Correct the kernels tick count to account for the time the microcontroller
       spent in its low power state. */
    vTaskStepTick( ulLowPowerTimeAfterSleep - ulLowPowerTimeBeforeSleep );

    /* Restart the timer that is generating the tick interrupt. */
    prvStartTickInterruptTimer();
}
```
