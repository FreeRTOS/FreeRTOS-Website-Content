---
title: xTaskCallApplicationTaskHook
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
BaseType_t xTaskCallApplicationTaskHook(
                                         TaskHandle_t xTask,
                                         void *pvParameter );
```

configUSE_APPLICATION_TASK_TAG 必须定义为 1，此函数才可用。
更多信息，请参阅 [RTOS 配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization)文档。

可为每个任务分配“标签”值。通常情况下，该值仅供应用程序使用， 
RTOS 内核不会访问它。不过，也可以使用该标签为任务分配钩子（或回调）函数， 
通过调用 xTaskCallApplicationTaskHook() 来执行钩子函数。每个 
任务都可定义自己的回调，或者干脆不定义回调。

尽管可以使用第一个函数参数来调用任何任务的钩子函数， 
任务钩子函数最常用的是跟踪钩子宏，如下例所示。

任务钩子函数必须具有 TaskHookFunction_t 类型，即接受一个 void * 参数， 
并返回一个 BaseType_t 类型的值。void * 参数可用于向钩子函数传递任何信息。


**参数：**

+ *xTask* 

  其钩子函数被调用的任务的句柄。传递 NULL 作为 xTask 将调用 
  与当前执行的任务相关的钩子函数。

+ *pvParameter* 

  要传递给钩子函数的值。这可以是指向一个结构体的指针，也可以是一个数值。


**用法示例：** 

```c
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

/* As an example use of the hook (callback) we can get the RTOS kernel to
   call the hook function of each task that is being switched out during a
   reschedule. */
#define traceTASK_SWITCHED_OUT() xTaskCallApplicationTaskHook( pxCurrentTCB, 0 )
```
