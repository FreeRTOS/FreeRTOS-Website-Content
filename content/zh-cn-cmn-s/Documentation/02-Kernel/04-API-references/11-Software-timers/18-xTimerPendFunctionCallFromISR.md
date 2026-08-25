---
title: xTimerPendFunctionCallFromISR()
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[定时器 API](/Documentation/02-Kernel/04-API-references/11-Software-timers/00-FreeRTOS-Software-Timer-API-Functions/)]

timers.h

```c
 BaseType_t xTimerPendFunctionCallFromISR(
                       PendedFunction_t xFunctionToPend,
                       void *pvParameter1,
                       uint32_t ulParameter2,
                       BaseType_t *pxHigherPriorityTaskWoken );
```

在应用程序中断服务程序中使用此函数，
用于将函数的执行推迟到 RTOS 守护进程任务（即定时器服务任务，因此该函数
在 timers.c 中实现，并以“Timer”为前缀）。

理想情况下，中断服务程序 (ISR) 需尽可能短，
但有时 ISR 要么需要处理很多任务，
要么需要执行非确定性任务。在这些情况下，可使用 xTimerPendFunctionCallFromISR() 将
函数的处理推迟到 RTOS 守护进程任务。

这里提供了一种允许中断直接返回到
随后将执行挂起函数任务的机制。使用该机制，
回调函数可在中断时间内连续执行，
就像回调在中断本身中执行一样。

可延迟到 RTOS 守护进程任务的函数必须具有以下
原型：

```c
 void vPendableFunction( void * pvParameter1, uint32_t ulParameter2 );
```

pvParameter1 和 ulParameter2 供应用程序代码使用。

INCLUDE_xTimerPendFunctionCall() 和 configUSE_TIMERS 必须同时设置为
设置为 1，xTimerPendFunctionCallFromISR() 才可用。


**参数：** 

+ *xFunctionToPend* 

  从定时器服务/守护进程任务中执行的函数。函数必须符合上面所示的 PendedFunction_t 
  原型。

+ *pvParameter1* 

  回调函数的第一个参数的值。该参数为 void \* 类型， 
  可用于传递任何类型。例如，整数类型可转换为 void \*， 
  或者可使用 void \* 指向结构体。

+ *ulParameter2* 

  回调函数的第二个参数的值。

+ *pxHigherPriorityTaskWoken* 

  如上所述，调用 xTimerPendFunctionCallFromSR() 
  将导致消息被发送至 RTOS 定时器守护进程任务。如果守护进程任务的优先级 
  （通过 FreeRTOSConfig.h 中的 [configTIMER_TASK_PRIORITY](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configtimer_task_priority) 设置） 
  高于当前正在运行的任务（中断中断的任务）的优先级， 
  那么 \*pxHigherPriorityTaskWoken 将在 xTimerPendFunctionCallFromISR() 中被设置为 pdTRUE， 
  表示应在中断退出前请求上下文切换。因此，\*pxHigherPriorityTaskWoken 
  必须初始化为 pdFALSE。请参阅下面的示例代码。


**返回：** 

如果消息成功发送到 RTOS 定时器守护进程任务，则返回 pdPASS，否则返回 pdFALSE。


**用法示例：**

```c
/* The callback function that will execute in the context of the daemon task.
   Note callback functions must all use this same prototype. */
void vProcessInterface( void *pvParameter1, uint32_t ulParameter2 )
{
BaseType_t xInterfaceToService;

    /* The interface that requires servicing is passed in the second
       parameter. The first parameter is not used in this case. */
    xInterfaceToService = ( BaseType_t ) ulParameter2;

    /* ...Perform the processing here... */
}

/* An ISR that receives data packets from multiple interfaces */
void vAnISR( void )
{
BaseType_t xInterfaceToService, xHigherPriorityTaskWoken;

    /* Query the hardware to determine which interface needs processing. */
    xInterfaceToService = prvCheckInterfaces();

    /* The actual processing is to be deferred to a task. Request the
       vProcessInterface() callback function is executed, passing in the
       number of the interface that needs processing. The interface to
       service is passed in the second parameter. The first parameter is
       not used in this case. */
    xHigherPriorityTaskWoken = pdFALSE;
    xTimerPendFunctionCallFromISR( vProcessInterface,
                                   NULL,
                                   ( uint32_t ) xInterfaceToService,
                                   &xHigherPriorityTaskWoken );

    /* If xHigherPriorityTaskWoken is now set to pdTRUE then a context
       switch should be requested. The macro used is port specific and will
       be either portYIELD_FROM_ISR() or portEND_SWITCHING_ISR() - refer to
       the documentation page for the port being used. */
    portYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}
```
