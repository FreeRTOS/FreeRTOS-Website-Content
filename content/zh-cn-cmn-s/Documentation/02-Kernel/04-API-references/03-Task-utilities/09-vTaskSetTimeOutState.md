---
title: vTaskSetTimeOutState()
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[任务实用程序](/Documentation/02-Kernel/04-API-references/03-Task-utilities/00-Task-utilities)]

task.h

```c
void vTaskSetTimeOutState( TimeOut_t * const pxTimeOut );
```

此功能仅适用于高级用户。

任务可以进入阻止状态以等待事件。通常情况下，任务不会无限期地在阻塞状态下等待， 
而是会指定一个超时时间。如果在任务等待的事件发生之前，超时期限已到， 
则会解除任务的阻塞状态。

如果任务在等待事件发生的过程中多次进入和退出阻塞状态， 
则必须调整任务每次进入“阻塞”状态时使用的超时时间， 
以确保在“阻塞”状态下花费的所有时间总和不超过最初指定的超时时间。 
`xTaskCheckForTimeOut()` 在执行调整时，会考虑到偶尔出现的情况， 
如滴答计数溢出，否则手动调整很容易出错。

`vTaskSetTimeOutState()` 与 `xTaskCheckForTimeOut()` 一起使用。调用 `vTaskSetTimeOutState()` 设置初始条件， 
然后调用 `xTaskCheckForTimeOut()` 检查超时情况， 
如果没有发生超时，则调整剩余块时间。


**参数：** 

- *pxTimeOut*

  指向结构体的指针，该结构体将被初始化，用于保存判断超时是否发生所需的信息。


**用法示例：**

有关示例，请参阅 [xTaskCheckForTimeOut()](/Documentation/02-Kernel/04-API-references/03-Task-utilities/10-xTaskCheckForTimeOut)
文档页面。
  
