---
title: vTaskDelay()
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
void vTaskDelay( const TickType_t xTicksToDelay );
```

`INCLUDE_vTaskDelay` 必须定义为 1，才可使用此函数。
更多信息，请参阅 [RTOS 配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization)文档。

按给定的滴答数延迟任务。任务保持阻塞的实际时间取决于滴答频率 
。常量 `portTICK_PERIOD_MS` 可用于根据滴答频率计算实际时间， 
其中使用一个滴答周期的分辨率。

`vTaskDelay()` 指定任务想要取消阻塞的时间，该时间**相对于**调用 `vTaskDelay()` 的时间 
。例如，指定 100 个滴答的阻塞周期将导致任务 
在 `vTaskDelay()` 被调用之后取消阻塞 100 个滴答。因此，`vTaskDelay()` 不能很好地控制 
周期性任务的频率，因为途经代码的路径以及其他任务和中断 
将影响 `vTaskDelay()` 被调用的频率，从而影响任务下一次执行的时间 
。请参阅 `vTaskDelayUntil()`，了解设计用于方便 
固定频率执行的替代 API 函数。此函数指定调用任务应取消阻塞的绝对时间（而非相对时间）来实现这一点 
。


**参数：**

- *xTicksToDelay*

  调用任务应阻塞的 tick 周期数。


**用法示例：** 

```c
void vTaskFunction( void * pvParameters )
{
    /* Block for 500ms. */
    const TickType_t xDelay = 500 / portTICK_PERIOD_MS;

    for( ;; )
    {
        /* Simply toggle the LED every 500ms, blocking between each toggle. */
        vToggleLED();
        vTaskDelay( xDelay );
    }
}
```

