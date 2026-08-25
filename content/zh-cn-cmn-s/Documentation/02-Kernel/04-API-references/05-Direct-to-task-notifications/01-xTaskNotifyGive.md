---
title: "xTaskNotifyGive 和 xTaskNotifyGiveIndexed"
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
 BaseType_t xTaskNotifyGive( TaskHandle_t xTaskToNotify );

 BaseType_t xTaskNotifyGiveIndexed( TaskHandle_t xTaskToNotify, 
                                    UBaseType_t uxIndexToNotify );
```

每项任务都有一个“任务通知”数组（或简称“通知”），
每条通知都包含一个状态和一个 32 位的值。[直达任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)是
直接发送给任务的事件，可以解除接收任务的阻塞状态，
还可以通过多种不同的方式更新接收任务的某个通知值。 
例如，通知可覆盖接收任务的某个通知值，或仅设置 
接收任务某个通知值中的一个或多个位。

xTaskNotifyGive() 宏可在 
将任务通知[用作速度更快的轻量级二进制或计数信号量](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/00-RTOS-task-notifications#uses)的替代方案时使用。 
FreeRTOS 信号量通过 xSemaphoreGive() API 函数释放，而 xTaskNotifyGive()
与其等效，使用接收 RTOS 任务的某个通知值代替信号量。

xTaskNotifyGive() 与 xTaskNotifyGiveIndexed() 是等效宏，唯一区别在于 
xTaskNotifyGiveIndexed() 可以操作数组中的任何任务通知，而 xTaskNotifyGive() 
总是操作数组中索引为 0 的任务通知。

当任务通知值用作二进制或计数信号量的等效物时， 
接收通知的任务应该使用 [ulTaskNotifyTake()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/03-ulTaskNotifyTake) API 函数来等待通知，
而不是使用 [xTaskNotifyWait()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/08-xTaskNotifyWait) API 函数。

**注意：**数组中的所有通知均独立操作， 
即一项任务在同一时间只能在数组中的一条通知上处于阻塞状态，并且不会被发送到其他数组索引的通知解除阻塞状态。

xTaskNotifyGive() 不能在中断服务程序中调用。 
请使用 [vTaskNotifyGiveFromISR()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/02-vTaskNotifyGiveFromISR) 代替。

必须在 FreeRTOSConfig.h 中将 [configUSE_TASK_NOTIFICATIONS](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configuse_task_notifications) 设置为 1 
（或保留为未定义状态），才可使用这些宏。常量 
[configTASK_NOTIFICATION_ARRAY_ENTRIES](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configtask_notification_array_entries) 决定了 
每项任务的任务通知数组中的索引数。


**向后兼容性信息：**  

在 FreeRTOS V10.4.0 之前，每项任务只有一个“通知值”，
所有任务通知 API 函数都只能操作这一个值。用通知值数组
替代单个通知值需要
一组新的 API 函数，以处理数组中的特定通知。
xTaskNotifyGive() 是原始 API 函数，
为保持向后兼容，
始终操作数组中索引为 0 的通知值。调用 xTaskNotifyGive() 等同于调用
xTaskNotifyGiveIndexed()，其中 uxIndexToNotify 参数设置为 0。


**参数：** 

* *xTaskToNotify*

  接收通知的 RTOS 任务的句柄，通知值会递增。可通过以下方法获取任务句柄：
  使用 [xTaskCreate()](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate) 创建任务，并通过 pxCreatedTask 参数获取句柄；
  使用 [xTaskCreateStatic()](/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic) 创建任务，并存储返回值作为句柄；
  调用 [xTaskGetHandle()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#xtaskgethandle)，通过任务名称获取句柄。当前正在执行的 RTOS 任务的句柄
  由 [xTaskGetCurrentTaskHandle()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#xtaskgetcurrenttaskhandle) API 函数返回。

* *uxIndexToNotify*

  目标任务的通知值数组中要向其发送通知的索引。
  uxIndexToNotify 必须小于 configTASK_NOTIFICATION_ARRAY_ENTRIES。
  xTaskNotifyGive() 没有此参数，并且总是将通知发送到索引 0。


**返回：** 

xTaskNotifyGiveIndexed() 是一个宏，调用 [xTaskNotifyIndexed()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/04-xTaskNotify)，
并将 eAction 参数设置为 eIncrement，因此所有调用都返回 pdPASS。


**用法示例：**

[更多示例请参阅 [RTOS 任务通知主页面](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)]

```c
/* Prototypes of the two tasks created by main(). */  
static void prvTask1( void *pvParameters );  
static void prvTask2( void *pvParameters );  


/* Handles for the tasks create by main(). */  
static TaskHandle_t xTask1 = NULL, xTask2 = NULL;  

/* Create two tasks that send notifications back and forth to each other,   
   then start the RTOS scheduler. */  
void main( void )  
{  
    xTaskCreate( prvTask1, "Task1", 200, NULL, tskIDLE_PRIORITY, &xTask1 );  
    xTaskCreate( prvTask2, "Task2", 200, NULL, tskIDLE_PRIORITY, &xTask2 );  
    vTaskStartScheduler();  
}  

/*-----------------------------------------------------------*/  

/* prvTask1() uses the 'indexed' version of the API. */  
static void prvTask1( void *pvParameters )  
{  
    for( ;; )  
    {  
        /* Send notification to prvTask2(), bringing it out of the   
           Blocked state. */  
        xTaskNotifyGiveIndexed( xTask2, 0 );  

        /* Block to wait for prvTask2() to notify this task. */  
        ulTaskNotifyTakeIndexed( 0, pdTRUE, portMAX_DELAY );  
    }  
}  

/*-----------------------------------------------------------*/  

/* prvTask2() uses the original version of the API (without the   
   'Indexed'). */  
static void prvTask2( void *pvParameters )  
{  
    for( ;; )  
    {  
        /* Block to wait for prvTask1() to notify this task. */  
        ulTaskNotifyTake( pdTRUE, portMAX_DELAY );  

        /* Send a notification to prvTask1(), bringing it out of the   
           Blocked state. */  
        xTaskNotifyGive( xTask1 );  
    }  
}  
```
