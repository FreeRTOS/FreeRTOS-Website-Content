---
title: xSemaphoreCreateRecursiveMutex
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
SemaphoreHandle_t xSemaphoreCreateRecursiveMutex( void )
```

创建一个[递归互斥锁](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/05-Recursive-mutexes)，并返回一个可以引用该互斥锁的句柄
。不能在中断服务程序中使用递归互斥锁。
[configSUPPORT_DYNAMIC_ALLOCATION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configsupport_dynamic_allocation) 和
configUSE_RECURSIVE_MUTEXES 必须在 FreeRTOSConfig.h 中设置为 1，xSemaphoreCreateRecursiveMutex()
才可用（configSUPPORT_DYNAMIC_ALLOCATION 也可以不定义，这种情况下
默认为 1）。

每个递归互斥锁都需要少量 RAM，用于保存递归互斥锁的状态。
如果互斥锁是使用 [xSemaphoreCreateRecursiveMutex()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/08-xSemaphoreCreateRecursiveMutex) 创建的，
则所需的 RAM 将从 [FreeRTOS 堆](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)自动分配。
如果一个递归互斥锁是使用 xSemaphoreCreateRecursiveMutexStatic() 创建的，
那么RAM 由应用程序写入器提供，这需要用到一个附加参数，
但允许在编译时静态分配 RAM
。有关详细信息，请参阅[静态分配与动态分配](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation)页面。

递归互斥锁分别使用 [xSemaphoreTakeRecursive()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/14-xSemaphoreTakeRecursive) 和
[xSemaphoreGiveRecursive()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/16-xSemaphoreGiveRecursive) API 函数“获取”和“释放”。
不得使用 xSemaphoreTake() 和 xSemaphoreGive()。

xSemaphoreCreateMutex()和
xSemaphoreCreateMutexStatic()用于创建非递归互斥锁。非递归互斥锁只能被一个任务
获取一次，如果同一个任务想再次获取则会失败，
因为当任务第一次释放互斥锁时，互斥锁就一直
处于释放状态。

与非递归互斥锁相反，递归互斥锁可以被同一个任务获取很多次，
获取多少次就需要释放多少次，
此时才会返回递归互斥锁。

与非递归互斥锁一样，递归互斥锁采用优先级继承
算法。如果另一个优先级更高的任务试图获得相同的互斥锁，
则将暂时提高“获取”互斥锁的任务的优先级。拥有互斥锁的任务
“继承”试图“获取”相同
互斥锁的任务的优先级。这意味着必须始终“归还”互斥锁，否则
优先级较高的任务将始终无法获得互斥锁，而优先级较低
的任务将永远无法“取消继承”优先级。更多有关优先级继承机制的信息，请参阅 
[FreeRTOS 互斥锁文档页面](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes)。


**返回：**

如果已成功创建递归互斥锁，则返回创建的互斥锁的句柄。如果
导致递归互斥项没有创建的原因是
[无法分配](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)保存互斥锁所需的内存，则返回 NULL。


**用法示例：**

```c
 SemaphoreHandle_t xMutex;

 void vATask( void * pvParameters )
 {
    Create a recursive mutex.
    xMutex = xSemaphoreCreateRecursiveMutex();

    if( xMutex != NULL )
    {
        /* The recursive mutex was created successfully and
           can now be used. */
    }
 }
```
