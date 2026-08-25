---
title: xTaskGetApplicationTaskTag, xTaskGetApplicationTaskTagFromISR
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
TaskHookFunction_t xTaskGetApplicationTaskTag( TaskHandle_t xTask );
TaskHookFunction_t xTaskGetApplicationTaskTagFromISR( TaskHandle_t xTask );
```

configUSE_APPLICATION_TASK_TAG 必须定义为 1，这些函数才可用。
更多信息，请参阅 [RTOS 配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization)文档。

xTaskGetApplicationTaskTagFromISR() 是 xTaskGetApplicationTaskTag() 的一个版本，
可以从中断服务程序 (ISR) 中调用。

返回与任务关联的“标签”值。标签值的含义和用途
由应用程序编写者定义。RTOS 内核本身通常不会
访问标签值。

此功能仅适用于高级用户。

**参数：**

+ *xTask* 

  正在查询的任务的句柄。任务可以使用 NULL 作为参数值来查询自己的标签值。


**返回：** 

 正在查询的任务的“标签”值。


**用法示例：** 

```c
/* In this example, an integer is set as the task tag value. */
void vATask( void *pvParameters )
{
    /* Assign a tag value of 1 to the currently executing task.
       The (void *) cast is used to prevent compiler warnings. */
    vTaskSetApplicationTaskTag( NULL, ( void * ) 1 );

    for( ;; )
    {
        /* Rest of task code goes here. */
    }
}

void vAFunction( void )
{
TaskHandle_t xHandle;
int iReturnedTaskHandle;

    /* Create a task from the vATask() function, storing the handle to the
       created task in the xTask variable. */

    /* Create the task. */
    if( xTaskCreate(
                     vATask,        /* Pointer to the function that implements
                                       the task. */
                     "Demo task",   /* Text name given to the task. */
                     STACK_SIZE,    /* The size of the stack that should be created
                                       for the task. This is defined in words, not
                                        bytes. */
                     NULL,          /* The task does not use the parameter. */
                     TASK_PRIORITY, /* The priority to assign to the newly created
                                       task. */
                     &xHandle       /* The handle to the task being created will be
                                       placed in xHandle. */
                   ) == pdPASS )
    {
       /* The task was created successfully. Delay for a short period to allow
          the task to run. */
       vTaskDelay( 100 );

       /* What tag value is assigned to the task? The returned tag value is
          stored in an integer, so cast to an integer to prevent compiler
          warnings. */
       iReturnedTaskHandle = ( int ) xTaskGetApplicationTaskTag( xHandle );
    }
}
```
