---
title: "xTaskNotifyStateClear, xTaskNotifyStateClearIndexed"
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
BaseType_t xTaskNotifyStateClear( TaskHandle_t xTask );
  
BaseType_t xTaskNotifyStateClearIndexed( TaskHandle_t xTask, 
                                         UBaseType_t uxIndexToClear );
```

每项 RTOS 任务都有一个[*任务通知数组*](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)。每条任务通知
都有*通知状态*，可以是“挂起”或“非挂起” ，
以及一个 32 位*通知值*。 

如果通知被发送到通知数组中的索引，那么
该索引处的通知被称为“待定” ，直到任务读取
其通知值，或通过调用 xTaskNotifyStateClear () 将通知状态明确清除为“非挂起”为止
。

xTaskNotifyStateClear () 和 xTaskNotifyStateClearIndexed () 是等效宏——唯一的区别
是 xTaskNotifyStateClearIndexed () 可以在数组内任何任务通知上运行，而
xTaskNotifyStateClear () 始终在数组索引 0 处的任务通知上运行。

[configUSE_TASK_NOTIFICATIONS](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configuse_task_notifications) 
必须在 FreeRTOSConfig.h 中设置为 1（或保留为未定义）才能使用这些宏。常量 
[configTASK_NOTIFICATION_ARRAY_ENTRIES](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configtask_notification_array_entries) 
设置每个任务的任务通知数组中的索引数。


**向后兼容性信息：**  

在 FreeRTOS V10.4.0 之前，每个任务有一个单一的“通知值”，且
所有任务通知 API 函数都在该值上运行。用通知值的数组
更换单个通知值需要
新的 API 函数集，该函数集应能在数组内处理具体通知。
xTaskNotifyStateClear() 是原始 API 函数，并且
通过始终在数组内索引 0 处的通知值上运行来保持向后兼容性
。调用 xTaskNotifyStateClear () 等于调用
xTaskNotifyStateClearIndexed ()，其中 uxIndexToNotify 参数设置为 0。


**参数：** 

* *xTask*

  将清除其通知状态的 RTOS 任务的句柄。将 xTask 设置为 NULL 以清除 
  调用任务的通知状态。要获取任务句柄，请使用 [xTaskCreate()](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate) 创建任务 
  并使用 pxCreatedTask 参数，或使用 [xTaskCreateStatic()](/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic) 创建任务并存储返回值， 
  或在调用 [xTaskGetHandle()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#xtaskgethandle) 时使用任务名称。当前执行的 
  RTOS 任务的句柄由 [xTaskGetCurrentTaskHandle()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#xtaskgetcurrenttaskhandle) API 函数返回。

* *uxIndexToClear*

  目标任务数组中要执行的通知值的索引。例如，将 uxIndexToClear 设置为 1
  将清除数组内索引为 1 时的通知状态。uxIndexToClear 必须小于
  configTASK_NOTIFICATION_ARRAY_ENTRIES。ulTaskNotifyStateClear() 没有此参数，并且始终作用于
  索引 0 的通知上。


**返回：** 

如果 xTask 引用的任务有挂起的通知，则通知
已清除，然后返回 pdTRUE。如果 xTask 引用的任务
有待处理的通知，那么返回 pdFALSE。


**用法示例：**

[更多示例请参阅主[RTOS 任务通知页面](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)]

```c
/* An example UART send function. The function starts a UART transmission then  
   waits to be notified that the transmission is complete. The transmission  
   complete notification is sent from the UART interrupt. The calling task's  
   notification state is cleared before the transmission is started to ensure it is  
   not co-incidentally already pending before the task attempts to block on its  
   notification state. */  

void vSerialPutString( const char * const pcStringToSend,  
                       unsigned short usStringLength )  
{  
const TickType_t xMaxBlockTime = pdMS_TO_TICKS( 5000 );  
  
    /* xSendingTask holds the handle of the task waiting for the transmission to  
       complete. If xSendingTask is NULL then a transmission is not in progress.  
       Don't start to send a new string unless transmission of the previous string  
       is complete. */  
    if( ( xSendingTask == NULL ) && ( usStringLength > 0 ) )  
    {  
        /* Ensure the calling task's 0th notification state is not already  
           pending. */  
        xTaskNotifyStateClearIndexed( NULL, 0 );  

        /* Store the handle of the transmitting task. This is used to unblock  
           the task when the transmission has completed. */  
        xSendingTask = xTaskGetCurrentTaskHandle();  

        /* Start sending the string - the transmission is then controlled by an  
           interrupt. */  
        UARTSendString( pcStringToSend, usStringLength );  

        /* Wait in the Blocked state (so not using any CPU time) until the UART  
           ISR sends the 0th notification to xSendingTask to notify (and unblock) the  
           task when the transmission is complete. */  
        ulTaskNotifyTake( 0, pdTRUE, xMaxBlockTime );  
    }  
}  
```
