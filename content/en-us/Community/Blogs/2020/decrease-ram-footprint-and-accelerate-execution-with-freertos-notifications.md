---
title: Decrease RAM Footprint and Accelerate Execution with FreeRTOS Notifications
date: 
feature: blog
categories:
  - Long term support
authors: 
  - ribarry
relatedLinks:
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
---

 
by [Richard Barry](../author/ribarry) on 29 Sep 2020

## Introduction


[Queues and semaphores](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/) are textbook features provided by all operating 
systems. Developers new to FreeRTOS use them because they are familiar with them. In most use cases, 
though, FreeRTOS [direct-to-task notifications](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications) provide a smaller and 
up to 45% faster alternative to semaphores, and 
FreeRTOS [message buffers and stream buffers](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers) provide a smaller and 
faster alternative to queues. This blog describes how to use direct-to-task-notifications in place of 
semaphores to create smaller and faster applications. 

Well-architected FreeRTOS applications rarely need to use semaphores.


## Background

FreeRTOS V1.2.0, released in 2002, introduced semaphore functionality by implementing the semaphore API 
as a set of macros that call the queue API. That design choice had the advantage of adding semaphore 
functionality without increasing the code size (important when Flash memory sizes were typically smaller 
than today), but it had the disadvantage of making semaphores atypically heavy objects because they 
inherit all the queue's comprehensive functionality. For example, queues are truly thread and priority 
aware, include an event mechanism and priority ordered lists of tasks waiting to send to and receive 
from the queue. Some semaphore use cases benefit from that comprehensive functionality, but the most 
common semaphore use cases don't require it. So when looking for a lean event mechanism for use by driver 
libraries, we opted not to re-write the semaphore code, but instead to create a new primitive explicitly 
designed for those most common use cases. That primitive is direct-to-task notifications - from here 
on, referred to only as 'notifications'. 


### What are direct-to-task notifications?

Most inter-task communication methods go through intermediary objects, such as a queue, semaphore, or 
event group. The sending task writes to the communication object, and the receiving task reads from 
the communication object. When using a direct-to-task notification, as the name implies, the sending 
task sends a notification directly to the receiving task, without an intermediary object. 

[![](/media/2020/Drawing1.png)](/media/2020/Drawing1.png)   
*Figure 1: Communicating through an intermediary object*

[![](/media/2020/Drawing2.png)](/media/2020/Drawing2.png)   
*Figure 2: Communicating without an intermediary object*

Beginning with FreeRTOS V10.4.0, each task has an array of notifications. Before that, each task had 
a single notification. Each notification comprises a 32-bit value and a Boolean state, which together 
consume just 5 bytes of RAM. 

Just as a task can block on a binary semaphore to wait for that semaphore to become 'available', a task 
can block on a notification to wait for that notification's state to become 'pending'. Likewise, just 
as a task can block on a counting semaphore to wait for that semaphore's count to become non-zero, a 
task can block on a notification to wait for that notification's value to become non-zero. The first 
example below demonstrates that scenario. 

Notifications can do more than communicate events, they can also communicate data in a variety of ways. 
The second example below demonstrates how to use a notification to send a 32-bit value. 


### Example of using a notification to synchronise an interrupt with a task

Listing 1 below shows the structure of the task that is blocking on a notification. If the task blocked 
on a semaphore, then it would call the [xSemaphoreTake()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/12-xSemaphoreTake) API function, but as the task 
is using a notification, it instead calls the [ulTaskNotifyTake()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/03-ulTaskNotifyTake) API function. 
ulTaskNotifyTake() always uses the notification at index 0. Use ulTaskNotifyTakeIndexed() in place of 
ulTaskNotifyTake() to use a notification at any specific array index. 

```c
static void vNotifiedTask( void *pvParameters )  
{  
    for( ;; )  
    {  
        /* Wait to receive a notification sent directly to this task.   
           The first parameter is set to pdFALSE, which makes the call   
           replicate the behavior of a counting semaphore. Set the   
           parameter to pdTRUE to replicate the behavior of a binary   
           semaphore. The second parameter is set to portMAX_DELAY,   
           which makes the task block indefinitely to wait for the  
           notification. That is done to simplify the example – real   
           applications should not block indefinitely as that prevents   
           the task recovering from error conditions. */  

        if( ulTaskNotifyTake( pdFALSE, portMAX_DELAY ) != 0 )  
        {  
            /* The task received a notification – do whatever is   
               necessary to process the received event. */   
            DoSomething();  
        }  
    }  
}  
```
*Listing 1*


Listing 2 shows the structure of an interrupt that is sending a notification. 

```c
static uint32_t vNotifyingISR( void )  
{  
BaseType_t xHigherPriorityTaskWoken;  

    /* The xHigherPriorityTaskWoken parameter must be initialized   
       to pdFALSE as it will get set to pdTRUE inside the interrupt   
       safe API function if calling the API function unblocks a task   
       that has a higher priority than the task in the running state   
       (the task this ISR interrupted). */   
    xHigherPriorityTaskWoken = pdFALSE;  

   /* Send a notification directly to the task that will perform   
      any processing necessitated by this interrupt. */   
    vTaskNotifyGiveFromISR( /* The handle of the task to which   
                               the notification is being sent. */
                            xHandlerTask,  
                            &xHigherPriorityTaskWoken );  

    /* If xHigherPriorityTaskWoken is now pdTRUE then calling   
       portYIELD_FROM_ISR() will result in a context switch, and   
       this interrupt will return directly to the unblocked task.   
       The FAQ "why is there a separate API for use in interrupts"
       describes why it is done this way. */  
    portYIELD_FROM_ISR( xHigherPriorityTaskWoken );  
}  
```
*Listing 2*

  
### Example of using a notification to send a value from an ISR to a task

This next example extends notification usage beyond simply replicating semaphore behavior by demonstrating 
how to send data with a notification. Sending data has minimal additional overhead. 

Listing 3 shows the structure of a function that returns the result of an analog to digital (ADC) conversion. 
The task that calls the function waits for the conversion result in the Blocked state, so it is not consuming 
any CPU cycles. The result is sent to it from the conversion end interrupt service routine (ISR). This scenario 
requires the use of the slightly more complex [xTaskNotify()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/04-xTaskNotify) 
and [xTaskNotifyWait()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/08-xTaskNotifyWait) API functions. As before, xTaskNotify() and xTaskNotifyWait() 
operate on the notification at index 0 of the notification array. Use xTaskNotifyIndexed() and xTaskNotifyWaitIndexed() 
to operate on any specific index in the array. 

```c
#define MAX_ADC_CHANNELS  

/* Holds the handle of a task to notify when an ADC conversion   
   ends on any given ADC channel. */  
static TaskHandle_t xBlockedTasks[ MAX_ADC_CHANNELS ] = { 0 };  

ErrorCode_t xGetADC( uint8_t ucChannel,   
                     uint32_t *pulConversionResult )  
{  
    ErrorCode_t xErrorCode = SUCCESS;  

    /* Check the ADC channel is not already in use. */  
    taskENTER_CRITICAL();  
    {  
        if( xBlockedTasks[ ucChannel ] != NULL )  
        {  
            /* A task is already waiting for a result from   
               this channel. */  
            xErrorCode = CHANNEL_IN_USE;  
        }  
        else  
        {  
            /* Store the handle of the calling task so it can  
               be notified when the conversion is complete. This   
               is cleared back to NULL by the conversion end   
               interrupt. */  
            xBlockedTasks[ ucChannel ] = xTaskGetCurrentTaskHandle();  
        }  
    }  

    taskEXIT_CRITICAL();  

    if( xErrorCode == SUCCESS )  
    {  
        /* Ensure the calling task does not already have a   
           notification pending. xTaskNotifyStateClear() clears   
           the state of the notification at array index 0. Use   
           xTaskNotifyStateClearIndexed() to clear the state of   
           a notification at a specific array index. */  
        xTaskNotifyStateClear( NULL );  

        /* Start the ADC conversion. */  
        StartADCConversion( ucChannel );  

        /* Block to wait for the conversion result. */  
        xResult = xTaskNotifyWait(  
                 /* The new ADC value will overwrite the old   
                    value, so there is no need to clear any bits   
                    before or after waiting for the new   
                    notification value. */  
                 0,  
                 0,  
                 /* The address of the variable in which to   
                    store the result. */  
                 pulConversionResult,  
                 /* Wait indefinitely. Again this is only done  
                    to keep the example simple. Production code   
                    should never block indefinitely as doing so   
                    prevents the task from recovering from   
                    errors. */  
                 portMAX_DELAY );  

        /* If not using an infinite block time then check xResult   
           to see why xTaskNotifyWait() returned. Production code   
           should not use an infinite block time as doing so prevents   
           the task recovering from an error.*/  
   }  

   return xErrorCode;  
}   
```
*Listing 3*
  
  
Finally, Listing 4 shows the structure of the interrupt service routine that uses a notification to send 
the conversion result to the waiting task. 

```c
/* The interrupt service routine (ISR) that executes each time   
   an ADC conversion completes. It is assumed the xBlockedTasks[]   
   array used in Listing 3 is in scope for use by this ISR.*/   
void ADC_ConversionEndISR( void )  
{  
Uint8_t ucChannel;  
uint32_t ulConversionResult;  
BaseType_t xHigherPriorityTaskWoken = pdFALSE, xResult;  

   /* This ISR handles all ADC channels. Determine which   
      channel needs servicing. */  
   ucChannel = ADC_GetChannelNumber();   

   if( ucChannel < MAX_ADC_CHANNELS )  
   {  
       /* Read the conversion result to clear the interrupt. */   
       ulConversionResult = ADC_ReadResult( ucChannel );  

       /* Is a task waiting for a result from channel  
          ucChannel? */   
       if( xBlockedTasks[ ucChannel ] != NULL )  
       {  
           /* Send a notification, and the ADC conversion   
              result, directly to the waiting task. */  
           xTaskNotifyFromISR( /* xTaskToNotify parameter. */  
                               xBlockedTasks[ ucChannel ],  
                               /* ulValue parameter. */  
                               ulConversionResult,          
                               /* eAction parameter. */  
                               eSetValueWithoutOverwrite,   
                               &xHigherPriorityTaskWoken );  
                               
           /* There is no longer a task waiting for a result   
              from channel ucChannel. */  
           xBlockedTasks[ ucChannel ] = NULL;   
       }  
   }  

   /* As normal – see comments in code Listing 2. */   
   portYIELD_FROM_ISR( xHigherPriorityTaskWoken );  
}  
```
*Listing 4*
  

## Conclusion

FreeRTOS is an established product that evolved over nearly two decades, and continues to evolve, to 
include optional features tailored to what we learned are the most common use cases. These features 
include direct-to-task notifications, message buffers, and stream buffers. Developers should use these 
tailored features before older FreeRTOS features because they are smaller and faster, but new FreeRTOS 
developers often overlook them because the concepts don't appear in standard OS texts. Tailoring a feature 
for specific use cases implies a restriction in the number of applicable use cases. The much more flexible 
original FreeRTOS features are still available to cover all use cases – but in most applications the use 
of comprehensive features, such as queues and semaphores, can be the exception rather than the norm.


## About the author

![](https://secure.gravatar.com/avatar/2197982f95321bd156e6f3b3fa184b92?s=200&d=mm&r=g)   
Richard Barry founded the FreeRTOS project in 2003, spent more than a decade developing and promoting 
FreeRTOS through his company Real Time Engineers Ltd, and now continues his work on FreeRTOS within a 
larger team as a principal engineer at Amazon Web Services. Richard graduated with 1st Class Honors in 
Computing for Real Time Systems, and was awarded an Honorary Doctorate for his contributions to the 
development of embedded technology. Richard has also been directly involved in the startup of several 
companies, and authored several books.   
[View articles by this author](../author/ribarry) 


FreeRTOS forums: Get industry-leading support from experts and collaborate with peers around the 
globe. [View Forums](https://forums.freertos.org/)
