---
title: xSemaphoreCreateMutexStatic
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
SemaphoreHandle_t xSemaphoreCreateMutexStatic(
                            StaticSemaphore_t *pxMutexBuffer );
```

创建[互斥锁](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/)，并返回
一个该互斥锁可以引用的句柄。中断服务例程中，
不能使用互斥锁。

[configSUPPORT_STATIC_ALLOCATION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configsupport_static_allocation)
和 [configUSE_MUTEXES](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configuse_mutexes) 必须同时在 FreeRTOSConfig.h 中设置为 1，
xSemaphoreCreateMutexStatic () 才可用。

每个互斥锁需要少量 RAM ，
以此来保持互斥锁的状态。如果互斥锁是使用 [xSemaphoreCreateMutex](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/06-xSemaphoreCreateMutex)() 创建的，
则所需的 RAM 将从 [FreeRTOS 堆](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)自动分配。
如果互斥锁是使用 xSemaphoreCreateMutexStatic () 创建的，
则 RAM 由应用程序编写器提供，这需要用到一个附加参数，
但允许在编译时静态分配 RAM
。有关详细信息，请参阅[静态分配与动态分配](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation)页面。

使用 [xSemaphoreTake](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/12-xSemaphoreTake)() 获取互斥锁，
并使用 [xSemaphoreGive()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/15-xSemaphoreGive) 释放互斥锁。
xSemaphoreTakeRecursive() 和 xSemaphoreGiveRecursive() 仅可用于
使用 [xSemaphoreCreateResursiveMutex](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/08-xSemaphoreCreateRecursiveMutex)() 创建的互斥锁。

互斥锁和[二进制信号量](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/03-vSemaphoreCreateBinary)极为相似，但
有一些细微差异：互斥锁具有优先级继承机制，
但二进制信号量没有。因此，二进制信号量是
实现同步的更好选择（任务之间或任务与中断之间），
也是实施简单互斥方面的更好选择。

如果另一个更高优先级的任务尝试获取相同的互斥锁，
则将暂时提高“获取”互斥锁的任务的优先级。拥有互斥锁的任务
“继承”试图“获取”相同
互斥锁的任务的优先级。这意味着必须始终“归还”互斥锁，否则
优先级较高的任务将始终无法获得互斥锁，而优先级较低
而优先级较低的任务将永远无法“取消继承”优先级。更多有关优先级继承机制的信息，请参阅 
[FreeRTOS 互斥锁文档页面](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes)。

用于实现互斥的互斥锁实例，
详见 [xSemaphoreTake()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/12-xSemaphoreTake) 文档页面。

在获得二进制信号量后无需返回，
因此，任务同步可以通过一个任务/中断持续释放信号量
而另外一个持续获得信号量来实现。相关演示请参阅
[xSemaphoreGiveFromISR()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/17-xSemaphoreGiveFromISR) 文档页面上的示例代码。
请注意，可以使用直接任务通知以更有效的方式
实现相同功能。

对互斥锁和二进制信号量的句柄都分配给
SemaphoreHandle_t 类型的变量，并且可以在任何接受该类型参数的任务级别（与中断
安全相反）API 函数中使用。


**参数：**

+ *pxMutexBuffer*

  必须指向 StaticSemaphore_t 类型的变量，该变量将用于保存互斥锁型信号量的状态。


**返回：**

如果已成功创建互斥锁型信号量，则返回创建的互斥锁的句柄。
因为 pxMutexBuffer 为 NULL 而未创建互斥锁，则返回 NULL。


**用法示例：**

```c
 SemaphoreHandle_t xSemaphore = NULL;
 StaticSemaphore_t xMutexBuffer;

 void vATask( void * pvParameters )
 {
    /* Create a mutex semaphore without using any dynamic memory
       allocation. The mutex's data structures will be saved into
       the xMutexBuffer variable. */
    xSemaphore = xSemaphoreCreateMutexStatic( &xMutexBuffer );

    /* The pxMutexBuffer was not NULL, so it is expected that the
       handle will not be NULL. */
    [configASSERT](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert)( xSemaphore );

    /* Rest of the task code goes here. */
 }
```
