---
title: xQueueReceive
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[队列管理 ](/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]

queue.h 

```c
BaseType_t xQueueReceive(
                          QueueHandle_t xQueue,
                          void *pvBuffer,
                          TickType_t xTicksToWait
);
```

这是用于调用 `xQueueGenericReceive()` 函数的宏。

从队列中接收项目。该项目通过复制接收，因此必须提供足够大小的缓冲区。 
创建队列时定义了复制到缓冲区中的字节数。

中断服务程序中不得使用此函数。请参阅 xQueueReceiveFromISR 
了解可以选择的替代方案。

**参数：**

- *xQueue*

  要从中接收项目的队列的句柄。
  
- *pvBuffer*

  指向要将所接收项目复制到缓冲区的指针。
  
- *xTicksToWait*

  如果在调用时队列为空， 
  则任务应阻塞等待项目接收的最长时间。如果队列为空，将 `xTicksToWait` 设置为 0 将导致函数立即返回 
  。时间是以滴答周期为单位定义的，因此如果需要，应使用常量 `portTICK_PERIOD_MS` 
  转换为实时。如果 [INCLUDE_vTaskSuspend](/Documentation/02-Kernel/03-Supported-devices/02-Customization) 设置为 “1”， 
  则将阻塞时间指定为 `portMAX_DELAY` 会导致任务无限期地阻塞 
  （没有超时）。


**返回：**

- 如果从队列中成功接收项目，则返回 *pdTRUE*； 
- 否则返回 *pdFALSE*。


**用法示例：**

```c
/* Define a variable of type struct AMMessage. The examples below demonstrate
   how to pass the whole variable through the queue, and as the structure is
   moderately large, also how to pass a reference to the variable through a queue. */
struct AMessage
{
    char ucMessageID;
    char ucData[ 20 ];
} xMessage;

/* Queue used to send and receive complete struct AMessage structures. */
QueueHandle_t xStructQueue = NULL;

/* Queue used to send and receive pointers to struct AMessage structures. */
QueueHandle_t xPointerQueue = NULL;

void vCreateQueues( void )
{
    xMessage.ucMessageID = 0xab;
    memset( &( xMessage.ucData ), 0x12, 20 );
    
    /* Create the queue used to send complete struct AMessage structures. This can
       also be created after the schedule starts, but care must be task to ensure
       nothing uses the queue until after it has been created. */
    xStructQueue = xQueueCreate(
        /* The number of items the queue can hold. */
        10,
        /* Size of each item is big enough to hold the<br /> whole structure. */
        sizeof( xMessage ) );
        
    /* Create the queue used to send pointers to struct AMessage structures. */
    xPointerQueue = xQueueCreate(
        /* The number of items the queue can hold. */
        10,
        /* Size of each item is big enough to hold only a pointer. */
        sizeof( &xMessage ) );
                          
    if( ( xStructQueue == NULL ) || ( xPointerQueue == NULL ) )
    {
        /* One or more queues were not created successfully as there was not enough
           heap memory available. Handle the error here. Queues can also be created
           statically. */
    }
}

/* Task that writes to the queues. */
void vATask( void *pvParameters )
{
    struct AMessage *pxPointerToxMessage;
    
    /* Send the entire structure to the queue created to hold 10 structures. */
    xQueueSend( /* The handle of the queue. */
                xStructQueue,
                /* The address of the xMessage variable. sizeof( struct AMessage )
                    bytes are copied from here into the queue. */
                ( void * ) &xMessage,
                /* Block time of 0 says don't block if the queue is already full.
                   Check the value returned by xQueueSend() to know if the message
                   was sent to the queue successfully. */
                ( TickType_t ) 0 );
                             
    /* Store the address of the xMessage variable in a pointer variable. */
    pxPointerToxMessage = &xMessage;
    
    /* Send the address of xMessage to the queue created to hold 10 pointers. */
    xQueueSend( /* The handle of the queue. */
                xPointerQueue,
                /* The address of the variable that holds the address of xMessage.
                   sizeof( &xMessage ) bytes are copied from here into the queue. As the
                   variable holds the address of xMessage it is the address of xMessage
                   that is copied into the queue. */
                ( void * ) &pxPointerToxMessage,
                ( TickType_t ) 0 );
                
    /* ... Rest of task code goes here. */
}

/* Task that reads from the queues. */
void vADifferentTask( void *pvParameters )
{
    struct AMessage xRxedStructure, *pxRxedPointer;
    
    if( xStructQueue != NULL )
    {
        /* Receive a message from the created queue to hold complex struct AMessage
           structure. Block for 10 ticks if a message is not immediately available.
           The value is read into a struct AMessage variable, so after calling
           xQueueReceive() xRxedStructure will hold a copy of xMessage. */
        if( xQueueReceive( xStructQueue,
                           &( xRxedStructure ),
                           ( TickType_t ) 10 ) == pdPASS )
        {
            /* xRxedStructure now contains a copy of xMessage. */
        }
    }
   
    if( xPointerQueue != NULL )
    {
        /* Receive a message from the created queue to hold pointers. Block for 10
           ticks if a message is not immediately available. The value is read into a
           pointer variable, and as the value received is the address of the xMessage
           variable, after this call pxRxedPointer will point to xMessage. */
        if( xQueueReceive( xPointerQueue,
                          &( pxRxedPointer ),
                          ( TickType_t ) 10 ) == pdPASS )
        {
            /* *pxRxedPointer now points to xMessage. */
        }
    }
   
    /* ... Rest of task code goes here. */
}   
```
*演示如何发送和接收结构体以及指向结构体的指针*
