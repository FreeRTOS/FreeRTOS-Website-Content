---
title: "ulTaskNotifyTake, ulTaskNotifyTakeIndexed"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 任务通知 API](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/00-RTOS-task-notifications)]

task.h

```c
uint32_t ulTaskNotifyTake( BaseType_t xClearCountOnExit,
                           TickType_t xTicksToWait );
   
uint32_t ulTaskNotifyTakeIndexed( UBaseType_t uxIndexToWaitOn, 
                                  BaseType_t xClearCountOnExit, 
                                  TickType_t xTicksToWait );
```

每个任务都有一组“任务通知” （或仅“通知” ） ，每个
通知都包含状态和一个 32 位值。[直达任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications) 
直接发送给任务的事件，可以取消接收任务的阻塞状态，还
可以选择通过多种方式更新接收任务的某个通知值。 
例如，通知可覆盖接收任务的通知值中的一个，或仅设置 
接收任务的通知值中的一个或多个比特位。

`ulTaskNotifyTake()` 是一个宏， 
[用于将任务通知作为一种速度更快、重量更轻的二进制或计数信号量](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/00-RTOS-task-notifications#uses) 
替代品。FreeRTOS 信号量是使用 `xSemaphoreTake()` API 函数`ulTaskNotifyTake()`提取的，
是使用通知值代替信号量的等效宏。

`ulTaskNotifyTake()` 和 `ulTaskNotifyTakeIndexed()` 是等效的宏 - 唯一的区别
是 `ulTaskNotifyTakeIndexed()` 可以在数组内的任何任务通知上运行，
而 `ulTaskNotifyTake()` 始终在数组索引 0 处的任务通知上运行。

当任务使用通知值作为二进制或计数信号量时，其他任务和中断应使用 
[xTaskNotifyGive()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/01-xTaskNotifyGive) 宏或 
[xTaskNotify()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/04-xTaskNotify) 函数将数据发给任务，其中函数的 eAction 参数设置为 eIncrement 
（这两者是等效的）。

`ulTaskNotifyTake()` 可以在退出时清除任务的通知值为 0，在这种情况下， 
通知值起到二进制信号量的作用；或在退出时递减任务的通知值，在这种情况下， 
通知值更像是计数信号量。

RTOS 任务可以使用 `ulTaskNotifyTake()` [可选]进入阻塞状态以等待任务通知指。 
任务处于“阻塞”状态时不会占用任何 CPU 时间。

**注意：**数组中的每条通知均独立运行 
——任务一次只能阻塞数组中的一个通知， 
并且不会被发送到任何其他数组索引的通知解除阻塞。

然而当通知被挂起时，[xTaskNotifyWait()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/08-xTaskNotifyWait) 将返回，`ulTaskNotifyTake()` 
将在任务的通知值不为零时返回，并在返回之前递减任务通知值 
。

必须在 FreeRTOSConfig.h 中将 [configUSE_TASK_NOTIFICATIONS](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configuse_task_notifications) 设置为 1（或 
保留为未定义) ，这些宏才能可用。常量 
[configTASK_NOTIFICATION_ARRAY_ENTRIES](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configtask_notification_array_entries) 
设置每个任务的任务通知数组中的索引数。


**向后兼容性信息：**  

在 FreeRTOS V10.4.0 之前，每个任务有一个单一的“通知值”，且
所有任务通知 API 函数都在该值上运行。用通知值的数组
更换单个通知值需要
新的 API 函数集，该函数集应能在数组内处理具体通知。
`ulTaskNotifyTake()` 是原始 API 函数，并且
通过始终在数组内索引 0 处的通知值上运行保持
向后兼容性。调用 `ulTaskNotifyTake()` 等同于调用
`ulTaskNotifyTakeIndexed()`，其 `uxIndexToWaitOn` 参数设置为 0。


**参数：** 

- *uxIndexToWaitOn*

  调用任务的通知值数组中的索引， 
  调用任务将在该索引上等待非零通知。`uxIndexToWaitOn` 必须小于 `configTASK_NOTIFICATION_ARRAY_ENTRIES`。 
  
  `xTaskNotifyTake()` 没有此参数，总是在索引 0 处等待通知。

- *xClearCountOnExit*

  如果收到 RTOS 任务通知，且 `xClearCountOnExit` 设置为 `pdFALSE`，那么 RTOS 任务的 
  通知值将在 `ulTaskNotifyTake()` 退出前递减。这相当于 
  成功调用 `xSemaphoreTake()` 后，计数信号量的值被递减。如果收到 RTOS 任务通知 
  且 `xClearCountOnExit` 设置为 `pdTRUE`，则 RTOS 任务的通知值 
  将在 `ulTaskNotifyTake()` 退出前重置为 0。这等同于
  在成功调用 `xSemaphoreTake()` 后，将二进制信号量的值保留为 0（或空，或“不可用”）。

- *xTicksToWait*

  表示如果调用 
  `ulTaskNotifyTake()` 时尚未收到通知，在阻塞状态下等待收到通知的最长时间。处于阻塞状态的 RTOS 任务不会消耗 
  任何 CPU 时间。时间以 RTOS 滴答周期为单位。`pdMS_TO_TICKS()` 宏可用于 
  将以毫秒为单位的时间转换为以滴答为单位的时间。


**返回：** 

 - 被递减或清楚之前的任务通知值的值
   （请参阅 `xClearCountOnExit` 的说明）。


**用法示例：**

[更多示例请参阅主[RTOS 任务通知页面](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)]

```c
 /* An interrupt handler. The interrupt handler does not perform any processing,  
    instead it unblocks a high priority task in which the event that generated the  
    interrupt is processed. If the priority of the task is high enough then the  
    interrupt will return directly to the task (so it will interrupt one task but  
    return to a different task), so the processing will occur contiguously in time -  
    just as if all the processing had been done in the interrupt handler itself. */  
void vANInterruptHandler( void )  
{  
    BaseType_t xHigherPriorityTaskWoken;  

    /* Clear the interrupt. */  
    prvClearInterruptSource();  

    /* xHigherPriorityTaskWoken must be initialised to pdFALSE. If calling  
       vTaskNotifyGiveFromISR() unblocks the handling task, and the priority of  
       the handling task is higher than the priority of the currently running task,  
       then xHigherPriorityTaskWoken will automatically get set to pdTRUE. */  
    xHigherPriorityTaskWoken = pdFALSE;  

    /* Unblock the handling task so the task can perform any processing necessitated  
       by the interrupt. xHandlingTask is the task's handle, which was obtained  
       when the task was created. */  
    vTaskNotifyGiveIndexedFromISR( xHandlingTask, 0, &xHigherPriorityTaskWoken );  

    /* Force a context switch if xHigherPriorityTaskWoken is now set to pdTRUE.  
       The macro used to do this is dependent on the port and may be called  
       portEND_SWITCHING_ISR. */  
    portYIELD_FROM_ISR( xHigherPriorityTaskWoken );  
}  

/*-----------------------------------------------------------*/  

/* A task that blocks waiting to be notified that the peripheral needs servicing,  
   processing all the events pending in the peripheral each time it is notified to   
   do so. */  
void vHandlingTask( void *pvParameters )  
{  
    BaseType_t xEvent;  

    for( ;; )  
    {  
        /* Block indefinitely (without a timeout, so no need to check the function's  
           return value) to wait for a notification. Here the RTOS task notification  
           is being used as a binary semaphore, so the notification value is cleared  
           to zero on exit. NOTE! Real applications should not block indefinitely,  
           but instead time out occasionally in order to handle error conditions  
           that may prevent the interrupt from sending any more notifications. */  
        ulTaskNotifyTakeIndexed( 0,               /* Use the 0th notification */  
                                 pdTRUE,          /* Clear the notification value   
                                                     before exiting. */  
                                 portMAX_DELAY ); /* Block indefinitely. */  

        /* The RTOS task notification is used as a binary (as opposed to a  
           counting) semaphore, so only go back to wait for further notifications  
           when all events pending in the peripheral have been processed. */  
        do  
        {  
            xEvent = xQueryPeripheral();  

            if( xEvent != NO_MORE_EVENTS )  
            {  
                vProcessPeripheralEvent( xEvent );  
            }  
        } while( xEvent != NO_MORE_EVENTS );  
    }  
}  
```
