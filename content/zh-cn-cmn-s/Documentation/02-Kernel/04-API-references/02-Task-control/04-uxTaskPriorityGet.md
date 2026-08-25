---
title: uxTaskPriorityGet()
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
UBaseType_t uxTaskPriorityGet( const TaskHandle_t xTask );
```

`INCLUDE_uxTaskPriorityGet` 必须定义为 1，才可使用此函数。有关详细信息，请参阅 
[RTOS 配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization)文档。

获取任意任务的优先级。


**参数：**

- *xTask*

  待查询任务的句柄。传递 NULL 句柄会返回调用任务的优先级。


**返回：**

- `xTask` 的优先级。


**用法示例：** 

```c
void vATaskFunction( void * pvParams )
{
    TaskHandle_t xHandle;

    ( void ) pvParams;

    // Create a task, storing the handle.
    xTaskCreate( vTaskCode, "NAME", STACK_SIZE, NULL, tskIDLE_PRIORITY, &xHandle );

    // ...

    // Use the handle to obtain the priority of the created task.
    // It was created with tskIDLE_PRIORITY, but may have changed
    // it itself.
    if( uxTaskPriorityGet( xHandle ) != tskIDLE_PRIORITY )
    {
        // The task has changed its priority.
    }

    // ...

    // Is our priority higher than the created task?
    if( uxTaskPriorityGet( xHandle ) < uxTaskPriorityGet( NULL ) )
    {
        // Our priority (obtained using NULL handle) is higher.
    }
}
```

