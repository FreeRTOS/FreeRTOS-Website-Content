---
title: xSemaphoreGetMutexHolder
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
TaskHandle_t xSemaphoreGetMutexHolder( SemaphoreHandle_t xMutex );
```

必须在 FreeRTOSConfig.h 中将 INCLUDE_xSemaphoreGetMutexHolder 设置为 1，
此函数才可用。

返回保存函数参数指定的互斥锁的任务的句柄（若有）。

xSemaphoreGetMutexHolder () 可以可靠地用于确定调用任务是否
是互斥锁持有者，但如果由调用任务之外的任务持有互斥锁，则无法可靠地使用
xSemaphoreGetMutexHolder () 。这是因为 MUTEX 支架可能会
在调用该函数的调用任务与测试该函数返回值之间
更改。

configUSE_MUTEXES 必须在 FreeRTOSConfig.h 中设置为 1，xSemaphoreGetMutexHolder() 才可用。


**参数：**

+ *xMutex* 

  正在查询的互斥体的句柄。


**返回：**

保存 xMutex 参数指定的互斥锁的任务的句柄。如果 
在 xMutex 参数中传递的信号量不是互斥锁型信号量，或者如果互斥锁可用，但未被任何任务保存， 
则返回 NULL。
  
