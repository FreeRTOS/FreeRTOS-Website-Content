---
title: xSemaphoreCreateMutex
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
SemaphoreHandle_t xSemaphoreCreateMutex( void )
```

创建[互斥锁](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/)，并返回
一个该互斥锁可以引用的句柄。中断服务例程中，
不能使用互斥锁。

[configSUPPORT_DYNAMIC_ALLOCATION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configsupport_dynamic_allocation)
和 [configUSE_MUTEXES](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configuse_mutexes) 必须同时在 FreeRTOSConfig.h 中设置为 1，
`xSemaphoreCreateMutex()` 才可用。（`configSUPPORT_DYNAMIC_ALLOCATION` 也可以不定义，
在这种情况下，它将默认为 1。）

每个互斥锁需要少量 RAM ，
以此来保持互斥锁的状态。如果互斥锁是使用 `xSemaphoreCreateMutex()` 创建的，
则所需的 RAM 将从 [FreeRTOS 堆](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)自动分配。
如果互斥锁是使用 [xSemaphoreCreateMutexStatic()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/07-xSemaphoreCreateMutexStatic) 创建的，
那么应由应用程序写入器提供 RAM，
但允许在编译时静态分配 RAM
。有关详细信息，请参阅[静态分配与动态分配](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation)页面。


使用 [xSemaphoreTake](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/12-xSemaphoreTake)() 获取互斥锁，
并使用 [xSemaphoreGive()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/15-xSemaphoreGive) 给出互斥锁。`xSemaphoreTakeRecursive()` 和 `xSemaphoreGiveRecursive()`
只能在使用 [xSemaphoreCreateRecursiveMutex](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/08-xSemaphoreCreateRecursiveMutex)() 创建的互斥锁上使用。

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

一旦获得二进制信号量，则无需要返回
因此，任务同步可以通过一个任务/中断持续释放信号量
而另外一个持续获得信号量来实现。相关演示请参阅
[xSemaphoreGiveFromISR()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/17-xSemaphoreGiveFromISR) 文档页面上的示例代码。
请注意，可以使用直接任务通知以更有效的方式
实现相同功能。

互斥锁和二进制信号量的句柄都分配给
`SemaphoreHandle_t` 类型的变量，并且可以在任何接受该类型参数的任务级别（与中断
安全相反）API 函数中使用。


**返回：**

- 如果已成功创建互斥锁型信号量，则返回创建的互斥锁的句柄。

- 如果由于[无法分配](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)保存互斥锁所需的内存而未创建互斥锁，则返回 NULL。


**用法示例：**

```c
SemaphoreHandle_t xSemaphore;

void vATask( void * pvParameters )
{
   /* Create a mutex type semaphore. */
   xSemaphore = xSemaphoreCreateMutex();

   if( xSemaphore != NULL )
   {
       /* The semaphore was created successfully and
          can be used. */
   }
}
```
