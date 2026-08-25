---
title: "ulTaskNotifyValueClear, ulTaskNotifyValueClearIndexed"
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
uint32_t ulTaskNotifyValueClear( TaskHandle_t xTask, 
                                 uint32_t ulBitsToClear );
  
uint32_t ulTaskNotifyValueClearIndexed( TaskHandle_t xTask, 
                                        UBaseType_t uxIndexToClear,
                                        uint32_t ulBitsToClear );
```

每项 RTOS 任务都有一个[*任务通知数组*](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)。每条任务通知
都有*通知状态*，可以是“挂起”或“非挂起” ，
以及一个 32 位*通知值*。 

`ulTaskNotifyValueClearIndexed()` 清除 `ulBitsToClear` 位掩码指定的位
（该掩码位于 `xTask` 所引用任务的数组索引 `uxIndexToClear` 的通知值中）。

`ulTaskNotifyValueClear()` 和 `ulTaskNotifyValueClearIndexed()` 是等效的宏 - 唯一的区别
是 `ulTaskNotifyValueClearIndexed()` 可以在数组内的任何任务通知上运行，
而 `ulTaskNotifyValueClear()` 始终在数组索引 0 处的任务通知上运行。

[configUSE_TASK_NOTIFICATIONS](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configuse_task_notifications) 
必须在 FreeRTOSConfig.h 中设置为 1（或保留为未定义）才能使用这些宏。
常量 [configTASK_NOTIFICATION_ARRAY_ENTRIES](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configtask_notification_array_entries) 设置 
每个任务的任务通知数组中的索引数。


**参数：**

- *xTask*

  将清除其通知值中的位的 RTOS 任务的句柄。将 `xTask` 设置为 NULL， 
  以清除调用任务通知值中的位。要获取任务句柄，请使用 
  [xTaskCreate()](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate) 创建任务并使用 `pxCreatedTask` 参数， 
  或使用 [xTaskCreateStatic()](/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic) 创建任务并存储返回值， 
  或在调用 [xTaskGetHandle()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#xtaskgethandle) 时使用任务名称。
  
  当前执行的 RTOS 任务的句柄通过以下方式 
  执行 [xTaskGetCurrentTaskHandle()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#xtaskgetcurrenttaskhandle) API 函数的任务或文件本地定义。

- *uxIndexToClear*

  目标任务通知值数组中的索引，用于清除其中的位。 `uxIndexToClear` 
  必须小于 `configTASK_NOTIFICATION_ARRAY_ENTRIES`。 `ulTaskNotifyValueClear()` 没有此 
  参数，并始终在索引 0 处清除通知值中的位。

- *ulBitsToClear*

  要在 `xTask` 的通知值中清除的位的位掩码。将某个位设置为 1， 
  可清除任务通知值中的相应位。将 `ulBitsToClear` 设置为 0xffffffff（32位架构上的`UINT_MAX`） 
  可将通知值清除为 0。将 `ulBitsToClear` 设置为 0， 
  可在不清除任何位的情况下查询任务的通知值。


**返回：**

- `ulBitsToClear` 指定位清零前目标任务的通知值。


**用法示例：**

```c
    #define MESSAGE_RECEIVED_BIT 8  
    #define TICKS_UNTIL_TIMEOUT  100  

    unsigned long ulNotification, ulMessageReceivedMask;  

    /* Clear any message received events. */  
    ulMessageReceivedMask = 1u << MESSAGE_RECEIVED_BIT;  
    ulTaskNotifyValueClear( ulMessageReceivedMask );  

    /* Send a message that expects a response. */  
    send_message();  

    /* Block this task until it has another pending notification. In this example,  
       the task only ever uses the MESSAGE_RECEIVED_BIT of its notification value,   
       so the next event can only ever be on message received. */  

    xTaskNotifyWait( 0u, /* Don't clear any notification bits on entry. */  
                     0u, /* Don't clear any notification bits on exit. */  
                     &ulNotification,  
                     TICKS_UNTIL_TIMEOUT );  

    /* If there wasn't a timeout, then the only possible event was received.  
       In this example, that is the MESSAGE_RECEIVED_EVENT. */  
    if( ulNotification == 0u )   
    {  
        /* Handle the response timeout. */  
        process_response_timeout();  
    }   
    else if( ulNotification == ulMessageReceivedMask )  
    {  
        /* Process the response event. */  
        process_response();  

        ulTaskNotifyValueClear( ulMessageReceivedMask );  
    }   
    else   
    {  
        /* The example task should only ever receive MESSAGE_RECEIVED_EVENTS. */  
        process_error();  
    }  
```
