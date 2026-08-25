---
title: vTaskSetApplicationTaskTag
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
void vTaskSetApplicationTaskTag(
                                 TaskHandle_t xTask,
                                 TaskHookFunction_t pxTagValue );
```

`configUSE_APPLICATION_TASK_TAG` 必须定义为 1，才可使用此函数。
更多信息，请参阅 [RTOS 配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization)文档。

可为每个任务分配“标签”值。该值仅供应用程序使用—— 
RTOS 内核本身不以任何方式使用它。[RTOS 追踪宏](/Documentation/02-Kernel/02-Kernel-features/09-RTOS-trace-feature) 
文档页面提供了一个很好的示例，介绍了应用程序如何使用该功能。


**参数：**

- *xTask*

  正在向其分配标签值的任务的句柄。将 `xTask` 传递为 NULL 会导致将标签 
  分配给调用任务。
  
- *pxTagValue*

  正在分配给任务标签的值。该值为 `TaskHookFunction_t` 类型， 
  可将函数指针赋值为标签，尽管实际上可以分配任何值。请参阅以下示例。


**用法示例：** 

```c
/* In this example an integer is set as the task tag value. 
   See the RTOS trace hook macros documentation page for an 
   example how such an assignment can be used. */
void vATask( void *pvParameters )
{
    /* Assign a tag value of 1 to myself. */
    vTaskSetApplicationTaskTag( NULL, ( void * ) 1 );

    for( ;; )
    {
        /* Rest of task code goes here. */
    }
}
/***********************************************/

/* In this example a callback function is being assigned as the task tag.
   First define the callback function - this must have type TaskHookFunction_t
   as per this example. */
static BaseType_t prvExampleTaskHook( void * pvParameter )
{
    /* Perform some action - this could be anything from logging a value,
       updating the task state, outputting a value, etc. */
    return 0;
}

/* Now define the task that sets prvExampleTaskHook as its hook/tag value.
   This is in fact registering the task callback, as described on the
   xTaskCallApplicationTaskHook() documentation page. */
void vAnotherTask( void *pvParameters )
{
    /* Register our callback function. */
    vTaskSetApplicationTaskTag( NULL, prvExampleTaskHook );

    for( ;; )
    {
        /* Rest of task code goes here. */
    }
}

/* As an example use of the hook (callback) we can get the RTOS kernel to call the
   hook function of each task that is being switched out during a reschedule. */
#define traceTASK_SWITCHED_OUT() xTaskCallApplicationTaskHook( pxCurrentTCB, 0 )
```
