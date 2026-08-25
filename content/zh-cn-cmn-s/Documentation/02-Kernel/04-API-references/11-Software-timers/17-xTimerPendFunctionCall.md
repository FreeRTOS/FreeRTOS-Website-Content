---
title: xTimerPendFunctionCall()
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
 BaseType_t xTimerPendFunctionCall(
                            PendedFunction_t xFunctionToPend,
                            void *pvParameter1,
                            uint32_t ulParameter2,
                            TickType_t xTicksToWait );
```

用于将函数的执行挂起到 RTOS 守护进程任务（定时器
服务任务，因此此函数前缀为“Timer”）。

可延迟到 RTOS 守护进程任务的函数必须具有以下
原型：

```c
 void vPendableFunction( void * pvParameter1, uint32_t ulParameter2 );
```

pvParameter1 和 ulParameter2 供应用程序代码使用。

INCLUDE_xTimerPendFunctionCall() 和 configUSE_TIMERS 必须同时设置为 1，xTimerPendFunctionCall() 才可用 
。


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

+ *xTicksToWait* 

  调用该函数后，将向队列中的定时器守护进程任务发送一条消息。xTicksToWait 
  是指如果发现定时器队列已满，调用任务应在阻塞状态（不使用任何处理时间） 
  下等待定时器队列空间变为可用的时间。队列的长度由 
  FreeRTOSConfig.h 中的 configTIMER_QUEUE_LENGTH 值设置。


**返回：** 

如果消息成功发送到 RTOS 定时器守护进程任务，则返回 pdPASS， 
否则返回 pdFALSE。

