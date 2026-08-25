---
title: vTaskDelete
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

task. h 

```c
void vTaskDelete( TaskHandle_t xTask );
```

`INCLUDE_vTaskDelete` 必须定义为 1，才可使用此函数。有关更多信息，请参阅 [RTOS 配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization)文档 
。

从 RTOS 内核管理中移除任务。要删除的任务将从所有就绪、 
阻塞、挂起和事件列表中移除。

注意：空闲任务负责释放由 RTOS 内核分配给已删除任务的 
内存。因此，如果应用程序调用了 
`vTaskDelete()`，请务必确保空闲任务获得足够的微控制器处理时间。任务代码分配的内存不会自动释放， 
应在任务删除之前手动释放。

请参阅演示应用程序文件 death.c，获取使用 `vTaskDelete()` 的代码示例。


**参数：**

- *xTask*

  要删除的任务的句柄。如果传递 NULL，会删除调用任务。


**用法示例：** 

```c
void vOtherFunction( void )
{
    TaskHandle_t xHandle = NULL;

    // Create the task, storing the handle.
    xTaskCreate( vTaskCode, "NAME", STACK_SIZE, NULL, tskIDLE_PRIORITY, &xHandle );

    // Use the handle to delete the task.
    if( xHandle != NULL )
    {
        vTaskDelete( xHandle );
    }
}
```
