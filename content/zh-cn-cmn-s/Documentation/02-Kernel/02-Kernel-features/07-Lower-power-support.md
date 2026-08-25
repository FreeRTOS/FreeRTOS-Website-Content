---
title: "低功耗支持"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: 节能状态简介
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: FreeRTOS 简介
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: FreeRTOS 初学者指南
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: 下载 FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: 常见问题
    link: /Why-FreeRTOS/FAQs
---


*无滴答空闲模式*

[**另请参阅[适用于 ARM Cortex-M MCU 的低功耗功能](/low-power-ARM-cortex-rtos)**]

[**另请参阅[SAM4L](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/Atmel_SAM4L-EK_Low_Power_Tick-less_RTOS_Demo)、[RX100](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Renesas/RX100_RSK_Low_Power_Tick-less_RTOS_Demo)、
[STM32L](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ST-Microelectronics/STM32L-discovery-low-power-tickless-RTOS-demo)、
[CEC1302](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Microchip/Microchip_CEC1302_ARM_Cortex-M4F_Low_Power_Demo)
和 [EFM32](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Silicon-labs/EFM32-Giant-Gecko-Pearl-Gecko-tickless-RTOS-demo) MCU**]无滴答演示


## 节能简介

通常，
要降低运行 FreeRTOS 的微控制器的功耗，可使用[空闲任务钩子](/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions)将微控制器置于低功耗状态
。由于必须定期退出然后重新进入低功耗状态以处理滴答中断，
这种简单方法所能实现的节能效果是有限的
。此外，如果滴答
中断的频率太高，每个滴答进入和然后退出低功耗状态所消耗的能量和时间
将超过除了最有效的节能模式之外的
任何其他节能量。

FreeRTOS 无滴答闲置模式在闲置期间（没有可执行的应用程序任务的期间）
停止周期性滴答中断，
然后，在滴答中断重启时，对 RTOS 滴答计数值
进行校正调整。

通过停止滴答中断，微控制器可以维持在深度节能状态，
直到中断发生，或者到了 RTOS 内核
将任务转换为“就绪”状态的时间。

 
## portSUPPRESS_TICKS_AND_SLEEP() 宏

```c
    portSUPPRESS_TICKS_AND_SLEEP( xExpectedIdleTime )
```

通过
在 FreeRTOSConfig.h 中将 configUSE_TICKLESS_IDLE 定义为 1，
可以启用内置的无滴答空闲功能（适用于支持此功能的移植）。可以为
任何 FreeRTOS 移植（包含内置此功能的移植）提供用户定义的无滴答空闲功能，
方法为：在 FreeRTOSConfig.h 中将 configUSE_TICKLESS_IDLE 定义为 2。

启用无滴答空闲功能后，如果以下两个条件同时为真，
内核将调用 portSUPPRESS_TICKS_AND_SLEEP() 宏
：

1. 空闲任务是唯一能够运行的任务，
   因为所有应用程序任务要么处于阻塞状态，要么处于挂起状态。

2. 在内核将应用程序任务转出阻塞状态之前，至少还要经过 *n* 个完整的滴答周期，
   其中
   *n* 由 configEXPECTED_IDLE_TIME_BEFORE_SLEEP 定义
   （位于 FreeRTOSConfig.h 中）设置。

PortSUPPRESS_ticks_and_SLEEP() 的单个参数值等于
任务进入就绪状态之前的
滴答周期总数。因此，该参数值是
微控制器在滴答中断停止（抑制）的情况下
可以安全地保持在深度睡眠状态的时间。

**注意**：如果从 portSUPPRESS_TICKS_AND_SLEEP() 中调用 [eTaskConfirmSleepModeStatus()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/11-eTaskConfirmSleepModeStatus) 时返回  eNoTasksWaitingTimeout，
则微控制器
可以无限期地保持在深度睡眠状态。如果满足以下条件，则 eTaskConfirmSleepModeStatus() 将只返回
eNoTasksWaitingTimeout：

1. 未使用软件定时器，
   因此调度器在将来的任何时间都不会执行定时器回调函数。

2. 所有应用程序任务或者处于挂起状态，
   或者处于具有无限超时（portMAX_DELAY 的超时值）的阻塞状态，
   因此，调度器在将来的任何固定时间
   都不会将任务从阻塞状态转换出来。

为避免出现争用情况， RTOS 调度器在
调用 portSUPPRESS_TICKS_AND_SLEEP() 之前挂起， 并在 portSUPPRESS_TICKS_AND_SLEEP() 完成时
恢复。这确保了在微控制器退出低功耗状态、
portSUPPRESS_TICKS_AND_SLEEP() 完成执行之间，应用程序任务无法执行。
此外，portSUPPRESS_TICKS_AND_SLEEP() 函数必须在停止滴答源和
微控制器进入休眠状态之间创建一个小的临界区。
应从该临界区调用 eTaskConfirmSleepModeStatus()
。

现在，所有 GCC、IAR 和 Keil ARM Cortex-M 移植都提供了一个
默认的 portSUPPRESS_TICKS_AND_SLEEP() 实现。有关
使用 ARM Cortex-M 实现的重要信息，
请参阅[适用于 ARM Cortex-M MCU 的低功耗功能](/low-power-ARM-cortex-rtos)页面。

默认实现会陆续添加到其他 FreeRTOS 移植
。下面描述的钩子可用于
向任何移植添加无滴答功能。

 
## 实现 portSUPPRESS_TICKS_AND_SLEEP()

如果正在使用的 FreeRTOS 移植没有提供
portSUPPRESS_TICKS_AND_SLEEP() 的默认实现，则应用程序编写者可以
通过在 FreeRTOSConfig.h 中定义 portSUPPRESS_TICKS_AND_SLEEP() 来提供自己的实现。

如果正在使用的 FreeRTOS 移植提供了
portSUPPRESS_TICKS_AND_SLEEP() 的默认实现，则应用程序编写者
可以通过
（位于 FreeRTOSConfig.h 中）设置。

以下源代码是应用程序编写者
如何实现 portSUPPRESS_TICKS_AND_SLEEP() 的示例。
该示例是基本的，内核时间
和日历时间可能会有一些落后。FreeRTOS 官方版本
试图通过提供更复杂的实现
来消除任何落后（尽可能）。

在示例中显示的函数调用中，仅 [vTaskStepTick()](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/07-vTaskStepTick)
和 [eTaskConfirmSleepModeStatus()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/11-eTaskConfirmSleepModeStatus)
是 FreeRTOS API 的一部分。其他功能特定于
所用硬件上可用的时钟和节能模式，因此必须
由应用程序编写者提供。

---

```c
/* First define the portSUPPRESS_TICKS_AND_SLEEP() macro. The parameter is the
   time, in ticks, until the kernel next needs to execute. */
#define portSUPPRESS_TICKS_AND_SLEEP( xIdleTime ) vApplicationSleep( xIdleTime )

/* Define the function that is called by portSUPPRESS_TICKS_AND_SLEEP(). */
void vApplicationSleep( TickType_t xExpectedIdleTime )
{
unsigned long ulLowPowerTimeBeforeSleep, ulLowPowerTimeAfterSleep;
eSleepModeStatus eSleepStatus;

    /* Read the current time from a time source that will remain operational
       while the microcontroller is in a low power state. */
    ulLowPowerTimeBeforeSleep = ulGetExternalTime();

    /* Stop the timer that is generating the tick interrupt. */
    prvStopTickInterruptTimer();

    /* Enter a critical section that will not effect interrupts bringing the MCU
       out of sleep mode. */
    disable_interrupts();

    /* Ensure it is still ok to enter the sleep mode. */
    eSleepStatus = eTaskConfirmSleepModeStatus();

    if( eSleepStatus == eAbortSleep )
    {
        /* A task has been moved out of the Blocked state since this macro was
           executed, or a context siwth is being held pending. Do not enter a
           sleep state. Restart the tick and exit the critical section. */
        prvStartTickInterruptTimer();
        enable_interrupts();
    }
    else
    {
        if( eSleepStatus == eNoTasksWaitingTimeout )
        {
            /* It is not necessary to configure an interrupt to bring the
               microcontroller out of its low power state at a fixed time in the
               future. */
            prvSleep();
        }
        else
        {
            /* Configure an interrupt to bring the microcontroller out of its low
               power state at the time the kernel next needs to execute. The
               interrupt must be generated from a source that remains operational
               when the microcontroller is in a low power state. */
            vSetWakeTimeInterrupt( xExpectedIdleTime );

            /* Enter the low power state. */
            prvSleep();

            /* Determine how long the microcontroller was actually in a low power
               state for, which will be less than xExpectedIdleTime if the
               microcontroller was brought out of low power mode by an interrupt
               other than that configured by the vSetWakeTimeInterrupt() call.
               Note that the scheduler is suspended before
               portSUPPRESS_TICKS_AND_SLEEP() is called, and resumed when
               portSUPPRESS_TICKS_AND_SLEEP() returns. Therefore no other tasks will
               execute until this function completes. */
            ulLowPowerTimeAfterSleep = ulGetExternalTime();

            /* Correct the kernels tick count to account for the time the
               microcontroller spent in its low power state. */
            vTaskStepTick( ulLowPowerTimeAfterSleep - ulLowPowerTimeBeforeSleep );
        }

        /* Exit the critical section - it might be possible to do this immediately
           after the prvSleep() calls. */
        enable_interrupts();

        /* Restart the timer that is generating the tick interrupt. */
        prvStartTickInterruptTimer();
    }
}
```
*用户定义的 portSUPPRESS_TICKS_AND_SLEEP() 实现示例*

---

