---
title: 通过 FreeRTOS 通知减少 RAM 占用空间并加速执行
date: null
feature: blog
categories:
- 长期支持
authors:
- stanmoy
relatedLinks:
- title: 什么是 FreeRTOS
  link: /Why-FreeRTOS/What-is-FreeRTOS/
---



本帖由 [Richard Barry](../author/ribarry) 于 2020 年 9 月 29 日发布

## 简介

[队列和信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)是所有操作系统都提供的 
典型功能。刚入门 FreeRTOS 的开发人员之所以使用这些功能，是因为他们熟悉这些功能。但在大多数用例中， 
FreeRTOS [直接任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)提供的信号量替代方案 
更小且速度快了高达 45%，而且 
FreeRTOS [消息缓冲区和流缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers)提供的队列替代方案 
更小且速度更快。这篇博客介绍了如何使用直接任务通知代替 
信号量来创建更小更快的应用程序。 

架构良好的 FreeRTOS 应用程序很少需要使用信号量。


## 背景

2002 年发布的 FreeRTOS V1.2.0 将信号量 API 实现为一组 
调用队列 API 的宏，从而引入了信号量功能。这种设计选择的优点是添加信号量 
功能而不增加代码大小（当 Flash 内存通常比现在小时，这一点 
很重要），但它的缺点是使信号量成为异常重的对象，因为它们 
继承了队列的所有综合功能。例如，队列能真正做到线程和优先级 
感知，包括事件机制和按优先级排序的任务列表，列表中的任务等待发送到队列 
并从队列接收。一些信号量用例受益于这种综合功能，但最 
常见的信号量用例则不需要。因此，在寻找驱动程序库使用的精益事件 
机制时，我们选择不重写信号量代码，而是创建一个为那些最常见的 
用例明确设计的新原语。该原语是直接任务通知，从这里 
开始简称为“通知“。 


### 什么是直接任务通知？

大多数任务间通信方法借助中间对象，如队列、信号量或 
事件组。发送任务写入通信对象，而接收任务从 
通信对象中读取。使用直接任务通知时，顾名思义，发送 
任务直接向接收任务发送通知，无需借助中间对象。 

[\![](/media/2020/Drawing1.png)](/media/2020/Drawing1.png)   
*图 1：通过中间对象进行通信*

[\![](/media/2020/Drawing2.png)](/media/2020/Drawing2.png)   
*图 2：无需中间对象进行通信*

从 FreeRTOS V10.4.0 开始，每个任务都有一组通知。在此之前，每个任务只有 
一个通知。每个通知包括一个 32 位值和一个布尔状态，它们总共 
只消耗 5 个字节的 RAM。 

正如任务可以在二进制信号量上进入阻塞状态以等待此信号量变得“可用”，任务 
也可以在通知上进入阻塞状态，以等待通知状态变为“挂起”。同样，正如 
任务可以在计数信号量上进入阻塞状态以等待信号量的计数变为非零，任务 
也可以在通知上进入阻塞状态，以等待通知的值变为非零。下面的 
第一个示例演示了这种场景。 

通知不仅可以传达事件，还可以通过多种方式传达数据。 
下面的第二个示例演示如何使用通知发送 32 位值。 


### 使用通知将中断与任务同步的示例

下面的列表 1 显示了在通知上进入阻塞状态的任务结构。如果任务在信号量上 
进入阻塞状态，则此任务将调用 [xSemaphoreTake()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/12-xSemaphoreTake) API 函数。但由于任务 
正在使用通知，因此它会调用 [ulTaskNotifyTake()](../../ulTaskNotifyTake) API 函数。 
ulTaskNotifyTake() 始终使用索引 0 处的通知。使用 ulTaskNotifyTakeIndexed() 代替 
ulTaskNotifyTake() 后可在任何特定数组索引处使用通知。 

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
*列表 1*


 列表 2 显示了发送通知的中断的结构。 

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
*列表 2*

  
### 使用通知将值从 ISR 发送到任务的示例

下一个示例通过演示如何使用通知发送数据来扩展通知的使用，让通知不仅仅 
局限于复制信号量行为。发送数据的额外开销极少。 

列表 3 显示返回模拟到数字 (ADC) 转换结果的函数结构。 
调用该函数的任务在阻塞状态等待转换结果，因此它不消耗 
任何 CPU 周期。结果从转换结束中断服务程序 (ISR) 发送至此任务。此场景 
需要使用略微复杂一些的 [xTaskNotify()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/04-xTaskNotify)  
和 [xTaskNotifyWait()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/08-xTaskNotifyWait) API 函数。如前所述，xTaskNotify() 和 xTaskNotifyWait()  
在通知数组索引 0 处的通知上运行。使用 xTaskNotifyIndexed() 和 xTaskNotifyWaitIndexed() 
在数组的任何特定索引上运行。 

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
*列表 3*
  
  
最后，列表 4 显示了使用通知将转换结果发送到等待任务的 
中断服务程序结构。 

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
*列表 4*
  

## 结论

FreeRTOS 是一款成熟的产品，经过近 20 年的发展，继续演进， 
从而包括针对我们所了解的最常见用例的定制可选功能。这些功能 
包括直接任务通知、消息缓冲区和流缓冲区。开发人员应优先使用 
这些量身定制的功能而非旧的 FreeRTOS 功能，因为新功能更小、更快，但新的 FreeRTOS  
开发人员经常忽略它们，因为这些概念没有出现在标准操作系统文本中。为特定用例 
定制功能意味着限制适用用例的数量。灵活得多的 
原始 FreeRTOS 功能仍可用于涵盖所有用例——但在大多数应用程序中，使用 
队列和信号量等综合功能可能是例外而不是常态。


## 作者简介

![](https://secure.gravatar.com/avatar/2197982f95321bd156e6f3b3fa184b92?s=200&d=mm&r=g)   
Richard Barry 于 2003 年创立了 FreeRTOS 项目，花了十多年时间通过其公司 
Real Time Engineers Ltd 开发并推广 FreeRTOS 。现在他仍在继续改进 FreeRTOS， 
但已加入 Amazon Web Services 的更大团队担任首席工程师。Richard 毕业时荣获实时系统计算的 
一等学位，还因对嵌入式技术开发的贡献而被授予 
荣誉博士学位。Richard 还直接参与创办了几家 
公司，并撰写了几本书籍。  
[查看此作者的文章](../author/ribarry) 


FreeRTOS 论坛：获得行业领先的专家支持，并与全球同行 
合作。[查看论坛](https://forums.freertos.org/)

