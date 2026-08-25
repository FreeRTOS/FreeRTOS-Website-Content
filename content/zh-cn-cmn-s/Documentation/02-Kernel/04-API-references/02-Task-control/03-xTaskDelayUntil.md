---
title: xTaskDelayUntil()
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[任务控制 ](/Documentation/02-Kernel/04-API-references/02-Task-control/00-Task-control)]

task. h

```c
BaseType_t xTaskDelayUntil( TickType_t *pxPreviousWakeTime,
                            const TickType_t xTimeIncrement );
```

INCLUDE_xTaskDelayUntil 必须定义为 1 ，此函数才可用。
更多信息，请参阅 [RTOS 配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization)文档。

将任务延迟到指定时间。此函数可以由周期性任务使用，
来确保恒定的执行频率。

此函数与 vTaskDelay() 在一个重要的方面有所不同：vTaskDelay() 会
导致一个任务从调用 vTaskDelay() 起阻塞指定的滴答数，
而 xTaskDelayUntil() 将导致一个任务从
pxPreviousWakeTime 参数中指定的时间起阻塞指定的滴答数。使用
vTaskDelay() 本身很难产生一个固定的执行频率，
因为从一个任务开始执行到该任务调用 vTaskDelay() 之间的时间可能并不固定
[该任务在调用之间可能采取不同的代码路径，
或者每次执行时可能被中断或被抢占的次数不同]。
xTaskDelayUntil() 可以用来生成一个恒定的执行频率。 

vTaskDelay() 指定了相对于函数被调用时的唤醒时间，
而 xTaskDelayUntil() 则指定了它希望解除阻塞的绝对（精确）时间
。

宏 pdMS_TO_TICKS() 可以用来计算以毫秒为单位的时间的 tick 数，
分辨率为一个 tick 周期。


**参数：**


+ *pxPreviousWakeTime* 

  指向一个变量的指针，该变量用于保存任务最后一次解除阻塞的时间。该变量在首次使用前 
  必须用当前时间初始化（见下面的示例）。在这之后，该变量 
  会在 xTaskDelayUntil() 中自动更新。

+ *xTimeIncrement* 

  周期时间段。任务将在 (*pxPreviousWakeTime + xTimeIncrement) 时间取消阻塞。使用 
  相同的 xTimeIncrement 参数值调用 xTaskDelayUntil 将导致任务以固定的间隔周期执行 
  。


**返回：**

可用于检查任务是否实际延迟的值：任务延迟时返回 pdTRUE， 
否则返回 pdFALSE。如果下一个预计唤醒时间已过，则任务将不会延迟。


**用法示例：** 

```c

// Perform an action every 10 ticks.
void vTaskFunction( void * pvParameters )
{
TickType_t xLastWakeTime;
const TickType_t xFrequency = 10;
BaseType_t xWasDelayed;

    // Initialise the xLastWakeTime variable with the current time.
    xLastWakeTime = xTaskGetTickCount ();
    for( ;; )
    {
        // Wait for the next cycle.
        xWasDelayed = xTaskDelayUntil( &xLastWakeTime, xFrequency );

        // Perform action here. xWasDelayed value can be used to determine
        // whether a deadline was missed if the code here took too long.
    }
}

```

