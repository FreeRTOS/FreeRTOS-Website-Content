---
title: vTaskResume()
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[任务控制](/Documentation/02-Kernel/04-API-references/02-Task-control/00-Task-control)]

task. h 

```c
void vTaskResume( TaskHandle_t xTaskToResume );
```

`INCLUDE_vTaskSuspend` 必须定义为 1，才可使用此函数。有关详细信息，请参阅 
[RTOS 配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization)文档。

恢复已挂起的任务。

因一次或多次调用 `vTaskSuspend(`) 而挂起的任务可通过 
单次调用 `vTaskResume()` 恢复运行。


**参数：**


- *xTaskToResume*

  待恢复任务的句柄。


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

    // Resume the suspended task ourselves.
    vTaskResume( xHandle );

    // The created task will once again get microcontroller processing
    // time in accordance with its priority within the system.
}
```

