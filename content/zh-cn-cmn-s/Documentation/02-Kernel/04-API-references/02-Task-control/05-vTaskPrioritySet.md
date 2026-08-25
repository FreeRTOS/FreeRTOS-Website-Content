---
title: vTaskPrioritySet()
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
void vTaskPrioritySet( TaskHandle_t xTask,
                       UBaseType_t uxNewPriority );
```

`INCLUDE_vTaskPrioritySet` 必须定义为 1，才可使用此函数。有关详细信息，请参阅 
[RTOS 配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization)文档。

设置任何任务的优先级。

如果正在设置的优先级高于当前执行任务的优先级，则函数返回之前将发生上下文切换。


**参数：**

- *xTask*

  正在设置优先级的任务的句柄。空句柄会设置调用任务的优先级。

- *uxNewPriority*

  将要设置任务的优先级。应断言优先级低于 `configMAX_PRIORITIES`。 
  如果 `configASSERT` 未定义，则优先级默认上限为 (`configMAX_PRIORITIES` - 1)。


**用法示例：**

```c
void vAFunction( void )  
{  
    TaskHandle_t xHandle;  

    // Create a task, storing the handle.  
    xTaskCreate( vTaskCode, "NAME", STACK_SIZE, NULL, tskIDLE_PRIORITY, &xHandle );  

    // ...  

    // Use the handle to raise the priority of the created task.  
    vTaskPrioritySet( xHandle, tskIDLE_PRIORITY + 1 )  

    // ...  

    // Use a NULL handle to raise our priority to the same value.  
    vTaskPrioritySet( NULL, tskIDLE_PRIORITY + 1 );  
 }  
```
