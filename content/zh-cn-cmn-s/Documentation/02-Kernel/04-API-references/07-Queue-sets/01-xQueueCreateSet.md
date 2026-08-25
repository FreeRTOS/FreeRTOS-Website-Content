---
title: xQueueCreateSet()
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[队列集 API](/Documentation/02-Kernel/04-API-references/07-Queue-sets/00-RTOS-queue-sets)]

queue.h

```c
QueueSetHandle_t xQueueCreateSet
                 (
                     const UBaseType_t uxEventQueueLength
                 );
```

必须在 FreeRTOSConfig.h 中将 configUSE_QUEUE_SETS 设置为 1，才可使用 xQueueCreateSet() API 函数。

队列集提供了一种机制，允许 RTOS 任务同时在多个 RTOS 队列或信号量上 
阻塞（挂起），等待读取操作。请注意，您也可以不使用队列集，而是采用更简单的替代方案。有关详细信息， 
请参阅[阻塞多个对象](/Documentation/02-Kernel/02-Kernel-features/10-Blocking-on-multiple-RTOS-objects)页面。

必须通过调用 xQueueCreateSet() 显式创建队列集，方可使用。创建后， 
可以通过调用 [xQueueAddToSet()](/Documentation/02-Kernel/04-API-references/07-Queue-sets/02-xQueueAddToSet) 在队列集中添加标准 FreeRTOS 队列和信号。
然后，可以使用 [xQueueSelectFromSet()](/Documentation/02-Kernel/04-API-references/07-Queue-sets/04-xQueueSelectFromSet) 来确定 
队列集中的哪些队列或信号量处于可以成功执行读取（针对队列）或获取（针对信号量）操作的状态。

注意：

* 在添加到队列集时，队列和信号量**必须为空**
  。某些方法（例如，通过 vSemaphoreCreateBinary() 宏创建）
  会使二进制信号量在创建时就处于可用状态，
  向队列集中添加这些对象时要特别小心。
  相比之下，通过首选 xSemaphoreCreateBinary() 函数创建的信号量
  不会出现这种情况。

* 阻塞包含互斥锁的队列集不会导致
  互斥锁持有者继承已阻塞任务的优先级。

* 添加到队列集的每个队列中的每个空格都需要额外的 4 个字节 RAM
  。因此，不应将具有较高最大计数值的计数信号量
  添加到队列集中。

* 在对队列集的成员执行接收（对于队列）或获取（对于信号量）操作之前，
  必须先调用
  xQueueSelectFromSet()，该函数会返回一个指向该队列集成员的句柄。


**参数：** 

- *uxEventQueueLength*

  队列集可存储发生在其中的队列和信号量上的事件。uxEventQueueLength
  用于指定队列集中一次最多可以排队的事件数量。

  为确保事件不会丢失，uxEventQueueLength 必须设置为
  添加到队列集中的所有队列长度的总和，其中二进制信号量和互斥锁的长度为 1，
  而计数信号量的长度由其最大计数值确定。例如：

  * 如果队列集包含一个长度为 5 的队列、一个长度为 12 的队列和一个二进制信号量，
    则 uxEventQueueLength 应设置为 (5 + 12 + 1)，即 18。

  * 如果队列集包含三个二进制信号量，则 uxEventQueueLength 应设置为 (1 + 1 + 1)，
    即 3。

  * 如果队列集包含一个最大计数为 5 的计数信号量和一个最大计数为 3 的计数信号量，
    则 uxEventQueueLength 应设置为 (5 + 3)，即 8。


**返回：** 

如果成功创建队列集，则返回所创建队列集的句柄
，否则返回 NULL。


**用法示例：**

```c
/* Define the lengths of the queues that will be added to the queue set. */
#define QUEUE_LENGTH_1		10
#define QUEUE_LENGTH_2		10

/* Binary semaphores have an effective length of 1. */
#define BINARY_SEMAPHORE_LENGTH	1

/* Define the size of the item to be held by queue 1 and queue 2 respectively.
   The values used here are just for demonstration purposes. */
#define ITEM_SIZE_QUEUE_1	sizeof( uint32_t )
#define ITEM_SIZE_QUEUE_2	sizeof( something_else_t )

/* The combined length of the two queues and binary semaphore that will be
   added to the queue set. */
#define COMBINED_LENGTH ( QUEUE_LENGTH_1 +
                          QUEUE_LENGTH_2 +
                          BINARY_SEMAPHORE_LENGTH )

void vAFunction( void )
{
static QueueSetHandle_t xQueueSet;
QueueHandle_t xQueue1, xQueue2, xSemaphore;
QueueSetMemberHandle_t xActivatedMember;
uint32_t xReceivedFromQueue1;
something_else_t xReceivedFromQueue2;

    /* Create the queue set large enough to hold an event for every space in
       every queue and semaphore that is to be added to the set. */
    xQueueSet = xQueueCreateSet( COMBINED_LENGTH );

    /* Create the queues and semaphores that will be contained in the set. */
    xQueue1 = xQueueCreate( QUEUE_LENGTH_1, ITEM_SIZE_QUEUE_1 );
    xQueue2 = xQueueCreate( QUEUE_LENGTH_2, ITEM_SIZE_QUEUE_2 );

    /* Create the semaphore that is being added to the set. */
    xSemaphore = xSemaphoreCreateBinary();

    /* Check everything was created. */
    configASSERT( xQueueSet );
    configASSERT( xQueue1 );
    configASSERT( xQueue2 );
    configASSERT( xSemaphore );

    /* Add the queues and semaphores to the set. Reading from these queues and
       semaphore can only be performed after a call to xQueueSelectFromSet() has
       returned the queue or semaphore handle from this point on. */
    xQueueAddToSet( xQueue1, xQueueSet );
    xQueueAddToSet( xQueue2, xQueueSet );
    xQueueAddToSet( xSemaphore, xQueueSet );

    for( ;; )
    {
        /* Block to wait for something to be available from the queues or
           semaphore that have been added to the set. Don't block longer than
           200ms. */
        xActivatedMember = xQueueSelectFromSet( xQueueSet,
                                                200 / portTICK_PERIOD_MS );

        /* Which set member was selected? Receives/takes can use a block time
           of zero as they are guaranteed to pass because xQueueSelectFromSet()
           would not have returned the handle unless something was available. */
        if( xActivatedMember == xQueue1 )
        {
            xQueueReceive( xActivatedMember, &xReceivedFromQueue1, 0 );
            vProcessValueFromQueue1( xReceivedFromQueue1 );
        }
        else if( xActivatedMember == xQueue2 )
        {
            xQueueReceive( xActivatedMember, &xReceivedFromQueue2, 0 );
            vProcessValueFromQueue2( &xReceivedFromQueue2 );
        }
        else if( xActivatedMember == xSemaphore )
        {
            /* Take the semaphore to make sure it can be "given" again. */
            xSemaphoreTake( xActivatedMember, 0 );
            vProcessEventNotifiedBySemaphore();
            break;
        }
        else
        {
            /* The 200ms block time expired without an RTOS queue or semaphore
               being ready to process. */
        }
    }
}
```
