---
title: vTaskSuspend()
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
void vTaskSuspend( TaskHandle_t xTaskToSuspend );
```

`INCLUDE_vTaskSuspend` 必须定义为 1，才可使用此函数。有关详细信息，请参阅 
[RTOS 配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization)文档。

挂起任意任务。无论任务优先级如何，任务被挂起后将永远无法获取任何微控制器处理时间。

对 `vTaskSuspend` 的调用不会累积次数，例如：若在同一任务上调用 `vTaskSuspend()` 两次， 
将仍然仅需调用一次 `vTaskResume()`，即可准备完毕挂起的任务。


**参数：**

- *xTaskToSuspend*

  被挂起的任务句柄。传递空句柄将导致调用任务被挂起。


**用法示例：** 

```c
void vAFunction( void )
{
    TaskHandle_t xHandle;

    // Create a task, storing the handle.
    xTaskCreate( vTaskCode, "NAME", STACK_SIZE, NULL, tskIDLE_PRIORITY, &xHandle );

    // ...

    // Use the handle to suspend the created task.
    vTaskSuspend( xHandle );

    // ...
   
    // The created task will not run during this period, unless
    // another task calls vTaskResume( xHandle ).

    //...

    // Suspend ourselves.
    vTaskSuspend( NULL );

    // We cannot get here unless another task calls vTaskResume
    // with our handle as the parameter.
}
```
