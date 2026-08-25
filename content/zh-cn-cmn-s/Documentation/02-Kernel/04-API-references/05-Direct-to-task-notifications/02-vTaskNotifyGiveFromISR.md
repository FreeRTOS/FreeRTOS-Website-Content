---
title: "vTaskNotifyGiveFromISR 和 vTaskNotifyGiveIndexedFromISR"
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
void vTaskNotifyGiveFromISR( TaskHandle_t xTaskToNotify,
                             BaseType_t *pxHigherPriorityTaskWoken );

void vTaskNotifyGiveIndexedFromISR( TaskHandle_t xTaskHandle, 
                                    UBaseType_t uxIndexToNotify, 
                                    BaseType_t *pxHigherPriorityTaskWoken );
```

可在中断服务程序 (ISR) 中使用的 `xTaskNotifyGive()` 和 `xTaskNotifyGiveIndexed()` 版本
。请参阅 [xTaskNotifyGive()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/01-xTaskNotifyGive) API 函数文档页面， 
了解其操作和必要的配置参数
以及向后兼容性信息。


**参数：** 

- *xTaskToNotify*

  接收通知的 RTOS 任务的句柄，通知值会递增。可通过以下方法获取任务句柄： 
  使用 [xTaskCreate()](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate) 创建任务，并通过 `pxCreatedTask` 参数获取句柄； 
  使用 [xTaskCreateStatic()](/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic) 创建任务，并存储返回值作为句柄； 
  调用 [xTaskGetHandle()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#xtaskgethandle)，通过任务名称获取句柄。当前 
  正在执行的 RTOS 任务的句柄 
  由 [xTaskGetCurrentTaskHandle()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities/#xtaskgetcurrenttaskhandle) API 函数返回。
  
- *uxIndexToNotify*

  目标任务的通知值数组中要向其发送通知的索引。 
  `uxIndexToNotify` 必须小于 `configTASK_NOTIFICATION_ARRAY_ENTRIES`。 `xTaskNotifyGiveFromISR()` 
  没有此参数，并且总是将通知发送到索引 0。
  
- *pxHigherPriorityTaskWoken*

  `*pxHigherPriorityTaskWoken` 必须初始化为 0。如果发送通知导致任务解除阻塞，并且解除阻塞的任务的优先级高于当前正在运行的任务，则 `vTaskNotifyGiveFromISR()` 
  会将 `*pxHigherPriorityTaskWoken` 设置为 `pdTRUE`
  。如果 `vTaskNotifyGiveFromISR()` 
  将此值设置为 `pdTRUE`，则应在中断退出前请求上下文切换。 
  请参阅下方示例。`pxHigherPriorityTaskWoken` 是可选参数，可设置为 NULL。


**用法示例：**

[更多示例请参阅 [RTOS 任务通知主页面](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)]

```c
/* This is an example of a transmit function in a generic peripheral driver. An  
   RTOS task calls the transmit function, then waits in the Blocked state (so not  
   using an CPU time) until it is notified that the transmission is complete. The  
   transmission is performed by a DMA, and the DMA end interrupt is used to notify  
   the task. */  
static TaskHandle_t xTaskToNotify = NULL;  

/* The peripheral driver's transmit function. */  
void StartTransmission( uint8_t *pcData, size_t xDataLength )  
{  
    /* At this point xTaskToNotify should be NULL as no transmission is in  
       progress. A mutex can be used to guard access to the peripheral if  
       necessary. */  
    configASSERT( xTaskToNotify == NULL );  

    /* Store the handle of the calling task. */  
    xTaskToNotify = xTaskGetCurrentTaskHandle();  

    /* Start the transmission - an interrupt is generated when the transmission  
       is complete. */  
    vStartTransmit( pcData, xDatalength );  
}  

/*-----------------------------------------------------------*/  

/* The transmit end interrupt. */  
void vTransmitEndISR( void )  
{  
    BaseType_t xHigherPriorityTaskWoken = pdFALSE;  

    /* At this point xTaskToNotify should not be NULL as a transmission was  
       in progress. */  
    configASSERT( xTaskToNotify != NULL );  

    /* Notify the task that the transmission is complete. */  
    vTaskNotifyGiveIndexedFromISR( xTaskToNotify, 0, &xHigherPriorityTaskWoken );  

    /* There are no transmissions in progress, so no tasks to notify. */  
    xTaskToNotify = NULL;  

    /* If xHigherPriorityTaskWoken is now set to pdTRUE then a context switch  
       should be performed to ensure the interrupt returns directly to the highest  
       priority task. The macro used for this purpose is dependent on the port in  
       use and may be called portEND_SWITCHING_ISR(). */  
    portYIELD_FROM_ISR( xHigherPriorityTaskWoken );  
}  

/*-----------------------------------------------------------*/  

/* The task that initiates the transmission, then enters the Blocked state (so  
   not consuming any CPU time) to wait for it to complete. */  
void vAFunctionCalledFromATask( uint8_t ucDataToTransmit, size_t xDataLength )  
{  
    uint32_t ulNotificationValue;  
    const TickType_t xMaxBlockTime = pdMS_TO_TICKS( 200 );  

    /* Start the transmission by calling the function shown above. */  
    StartTransmission( ucDataToTransmit, xDataLength );  

    /* Wait for the transmission to complete. */  
    ulNotificationValue = ulTaskNotifyTakeIndexed( 0, pdFALSE, xMaxBlockTime );  

    if( ulNotificationValue == 1 )  
    {  
        /* The transmission ended as expected. */  
    }  
    else  
    {  
        /* The call to ulTaskNotifyTake() timed out. */  
    }  
}  
```
