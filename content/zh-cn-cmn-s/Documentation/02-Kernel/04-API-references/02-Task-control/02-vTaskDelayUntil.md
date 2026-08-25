---
title: vTaskDelayUntil()
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
void vTaskDelayUntil( TickType_t *pxPreviousWakeTime,
                      const TickType_t xTimeIncrement );
```

`INCLUDE_vTaskDelayUntil` 必须定义为 1，才可使用此函数。
更多信息，请参阅 [RTOS 配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization)文档。

将任务延迟到指定时间。此函数可以由周期性任务使用，
来确保恒定的执行频率。

此函数与 `vTaskDelay()` 在一个重要方面有所不同：`vTaskDelay()`
会指定任务想要取消阻塞的时间，该时间是*相对于* `vTaskDelay()` 被调用的时间， 
而 `vTaskDelayUntil()` 会指定任务希望取消阻塞的*绝对*时间。

`vTaskDelay()` 将导致一个任务从调用 `vTaskDelay()` 时起阻塞指定的滴答数
。因此，很难单独使用 `vTaskDelay()` 来生成固定的
执行频率，因为任务在调用 `vTaskDelay()` 后取消阻塞与该任务
再次调用 `vTaskDelay()` 之间的时间可能不是固定的（该任务可能在两次调用之间
采用不同的代码路径，或者可能在每次执行时被打断或被抢占
的次数不同）。

`vTaskDelay()` 指定了相对于函数被调用时的唤醒时间，
而 `vTaskDelayUntil()` 则指定了它希望解除阻塞的绝对（精确）时间
。

应注意，如果 `vTaskDelayUntil()` 被用于指定已过去的唤醒时间，
该函数将立即返回（不阻塞）。因此，使用
`vTaskDelayUntil()` 定期执行的任务，在周期性执行因任何原因停止
（例如，任务被挂起），而导致任务错过一个或多个周期性执行时，
必须重新计算其所需的唤醒
时间。这可以通过检查由引用传递的变量来发现， 
该变量是针对当前滴答计数的 `pxPreviousWakeTime` 参数。但是，这在大多数使用场景下
并非必要。

常量 `portTICK_PERIOD_MS` 配合滴答周期分辨率
可用于从滴答频率计算实际时间。

当调用了 `vTaskSuspendAll()` 挂起 RTOS 调度器时，不得调用此函数。


**参数：**

- *pxPreviousWakeTime*

  指向一个变量的指针，该变量用于保存任务最后一次解除阻塞的时间。该变量在首次使用前 
  必须用当前时间初始化（见下面的示例）。在这之后，该变量 
  会在 `vTaskDelayUntil()` 内自动更新。
  
- *xTimeIncrement*

  周期时间段。该任务将在 `(*pxPreviousWakeTime + xTimeIncrement)` 时间解除阻塞。 
  使用相同的 `xTimeIncrement` 参数值调用 `vTaskDelayUntil` 将导致任务 
  以固定的间隔期执行。


**用法示例：** 

```c
// Perform an action every 10 ticks.
void vTaskFunction( void * pvParameters )
{
    TickType_t xLastWakeTime;
    const TickType_t xFrequency = 10;

    // Initialise the xLastWakeTime variable with the current time.
    xLastWakeTime = xTaskGetTickCount();

    for( ;; )
    {
        // Wait for the next cycle.
        vTaskDelayUntil( &xLastWakeTime, xFrequency );

        // Perform action here.
    }
}
```
