---
title: xTaskResumeFromISR()
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
BaseType_t xTaskResumeFromISR( TaskHandle_t xTaskToResume );
```

`INCLUDE_vTaskSuspend` 和 `INCLUDE_xTaskResumeFromISR` 必须定义为 1，才可使用此函数 
。更多信息，请参阅 [RTOS 配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization)文档。

可从 ISR 内调用的恢复挂起任务的函数。

由多次调用 `vTaskSuspend()` 中的一次调用挂起的任务可通过单次调用 
`xTaskResumeFromISR()` 重新运行。

`xTaskResumeFromISR()` 通常被视为危险函数，因为其
操作未被锁定。因此，如果中断可能在任务被挂起之前到达，
从而中断丢失，
则绝对不应使用该函数
来同步任务与中断。可使用信号量，
或者最好是直达任务通知，来避免这种可能性。
提供了一个使用[直达到任务通知的有效示例](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/03-As-counting-semaphore)
。


**参数：**

- *xTaskToResume*

  要恢复的任务句柄。


**返回：**

- 如果恢复任务导致上下文切换，则返回 *pdTRUE*，
- 否则返回 *pdFALSE*。ISR 使用此信息来确定 ISR 之后是否需要上下文切换。


**用法示例：** 

```c
TaskHandle_t xHandle;

void vAFunction( void )
{
    // Create a task, storing the handle.
    xTaskCreate( vTaskCode, "NAME", STACK_SIZE, NULL, tskIDLE_PRIORITY, &xHandle );

    // ... Rest of code.
}

void vTaskCode( void *pvParameters )
{
    // The task being suspended and resumed.
    for( ;; )
    {
        // ... Perform some function here.

        // The task suspends itself.
        vTaskSuspend( NULL );

        // The task is now suspended, so will not reach here until the ISR resumes it.
    }
}

void vAnExampleISR( void )
{
    BaseType_t xYieldRequired;

    // Resume the suspended task.
    xYieldRequired = xTaskResumeFromISR( xHandle );

    // We should switch context so the ISR returns to a different task.
    // NOTE:  How this is done depends on the port you are using.  Check
    // the documentation and examples for your port.
    portYIELD_FROM_ISR( xYieldRequired );
}
```
