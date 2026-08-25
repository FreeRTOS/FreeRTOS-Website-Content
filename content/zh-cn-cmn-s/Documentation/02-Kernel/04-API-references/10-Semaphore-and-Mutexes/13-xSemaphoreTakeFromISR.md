---
title: xSemaphoreTakeFromISR
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[信号量](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/00-Semaphores)]

semphr. h 

```c
xSemaphoreTakeFromISR
 (
 SemaphoreHandle_t xSemaphore,
 signed BaseType_t *pxHigherPriorityTaskWoken
 )
```

可从 ISR 调用的 [xSemaphoreTake()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/12-xSemaphoreTake)
版本。与 xSemaphoreTake() 不同，xSemaphoreTakeFromISR() 不允许
指定阻塞时间。


**参数：**

+ *xSemaphore* 

  信号量被“获取”。信号量由 SemaphoreHandle_t 类型的变量引用， 
  必须在使用之前显式创建。

+ *pxHigherPriorityTaskWoken* 

  信号量可能（尽管不太可能，并且取决于信号量类型） 
  阻塞一个或多个任务，等待给出信号量。调用 xSemaphoreTakeFromISR () 将 
  使被阻塞的任务等待信号量离开阻塞状态。如果调用 
  API 函数导致任务离开阻塞状态， 
  且未阻塞任务的优先级等于或高于当前正在执行的任务（被中断的任务），那么 
  API 函数将从内部把 *pxHigherPriorityTaskWoken 设置为 pdTRUE。 
  如果 xSemaphoreTakeFromISR() 将 *pxHigherPriorityTaskWoken 设置为 pdTRUE， 
  则应在退出中断之前执行上下文切换。这将确保中断直接返回到最高优先级的就绪状态任务 
  。该机制与 xQueueReceiveFromISR() 函数中使用的机制相同， 
  读者可以参考 [xQueueReceiveFromISR()](/Documentation/02-Kernel/04-API-references/06-Queues/10-xQueueReceiveFromISR) 文档以获得进一步解释。从 FreeRTOS 
  V7.3.0 开始，pxHigherPriorityTaskWoken 是一个可选参数，可设置为 NULL。


**返回：**

如果成功获取信号量，则返回 pdTRUE。如果因为信号量不可用而未成功获取信号量， 
则返回 pdFALSE。
  
