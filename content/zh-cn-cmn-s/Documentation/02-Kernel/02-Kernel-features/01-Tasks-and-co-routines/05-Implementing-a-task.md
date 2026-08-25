---
title: "FreeRTOS 调度（单核、AMP 和 SMP）"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: 适用于单核、非对称多核 (AMP) 和对称多核 (SMP) RTOS 配置的 FreeRTOS 调度算法
relatedLinks:
  - title: API 引用——任务创建
    link: /Documentation/02-Kernel/04-API-references/01-Task-creation/00-TaskHandle/
  - title: API 引用——任务控制
    link: /Documentation/02-Kernel/04-API-references/02-Task-control/00-Task-control/
  - title: API 引用——任务实用程序
    link: /Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/
---

[[有关任务的更多信息……](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/00-Tasks-and-co-routines/)]

### 实现任务

任务应具有以下结构体：

```c
void vATaskFunction( void *pvParameters )
{
    for( ;; )
    {
        -- Task application code here. --
    }

    /* Tasks must not attempt to return from their implementing
       function or otherwise exit. In newer FreeRTOS port
       attempting to do so will result in an configASSERT() being
       called if it is defined. If it is necessary for a task to
       exit then have the task call vTaskDelete( NULL ) to ensure
       its exit is clean. */
    vTaskDelete( NULL );
}
```

TaskFunction_t 类型是指返回 void 并将 void 指针作为其唯一参数的函数
。所有实现任务的函数都应为此类型。该参数可用于
将任何类型的信息传递到任务中，
如一些[标准演示应用程序任务](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)所示。

任务函数不应返回，因此通常实现为连续循环。但是，
[正如 RTOS 调度算法介绍页面所述](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/04-Task-scheduling/#using-a-prioritised-preemptive-scheduler---avoiding-task-starvation)，
通常最好创建事件驱动型任务，避免优先级较低的任务因缺少处理时间而饥饿，
从而形成以下结构体：

```c
void vATaskFunction( void *pvParameters )
{
    for( ;; )
    {
        /* Psudeo code showing a task waiting for an event
           with a block time. If the event occurs, process it.
           If the timeout expires before the event occurs, then
           the system may be in an error state, so handle the
           error. Here the pseudo code "WaitForEvent()" could
           replaced with xQueueReceive(), ulTaskNotifyTake(),
           xEventGroupWaitBits(), or any of the other FreeRTOS
           communication and synchronisation primitives. */
        if( WaitForEvent( EventObject, TimeOut ) == pdPASS )
        {
            -- Handle event here. --
        }
        else
        {
            -- Clear errors, or take actions here. --
        }
    }

    /* As per the first code listing above. */
    vTaskDelete( NULL );
}
```

再次提醒，如需查看更多示例，请参阅 RTOS 演示应用程序。

如需创建任务，请调用 [xTaskCreate()](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate/) 
或 [xTaskCreateStatic()](/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic)；如需删除任务， 
调用 [vTaskDelete()](/Documentation/02-Kernel/04-API-references/01-Task-creation/03-vTaskDelete/)。


---

### 任务创建宏

可以_选择_使用 portTASK_FUNCTION 或 portTASK_FUNCTION_PROTO 宏定义任务函数
。提供这些宏是为了允许将编译器特定的语法分别添加到函数定义
和原型中。所用端口（目前仅限 PIC18 fedC 端口）相关文档中未作具体说明，
则无需使用这些宏。

上述函数的原型可以写为：

```c
void vATaskFunction( void *pvParameters );
```

或者

```c
portTASK_FUNCTION_PROTO( vATaskFunction, pvParameters );
```

同样，上述函数同样可以写为：

```c
portTASK_FUNCTION( vATaskFunction, pvParameters )
{
    for( ;; )
    {
        -- Task application code here. --
    }
}
```
