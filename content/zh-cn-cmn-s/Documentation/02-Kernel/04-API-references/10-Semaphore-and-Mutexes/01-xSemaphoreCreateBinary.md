---
title: xSemaphoreCreateBinary
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[信号量](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/00-Semaphores)]

[**提示：在许多使用场景中，使用直达任务通知要比使用二进制信号量的速度更快，内存效率更高。**](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/02-As-binary-semaphore)


semphr. h


```c
SemaphoreHandle_t xSemaphoreCreateBinary( void );
```

创建一个[二进制信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)，并返回一个可以引用该信号量的句柄。
[configSUPPORT_DYNAMIC_ALLOCATION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configsupport_dynamic_allocation)
必须在 FreeRTOSConfig.h 中设置为 1，或处于未定义状态（默认为 1），
才可使用此 RTOS API 函数。

每个二进制信号量需要少量 RAM，用于保存信号量状态。如果
使用 xSemaphoreCreateBinary() 创建了二进制信号量，那么所需的 RAM
将自动从 [FreeRTOS 堆](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)中分配。如果二进制信号量
是使用 [xSemaphoreCreateBinaryStatic()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/02-xSemaphoreCreateBinaryStatic) 创建的，则 RAM
由应用程序写入器提供，这需要一个附加参数，但允许 RAM 在编译时进行静态分配
。请参阅[静态分配与动态分配](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation)页面
了解更多信息。

信号量是在“空”状态下创建的，这意味着必须先用
[xSemaphoreGive()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/15-xSemaphoreGive) API 函数给出信号量，
然后才能使用 [xSemaphoreTake](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/12-xSemaphoreTake)()  函数来获取（获得）该信号量。

二进制信号量和[互斥锁](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/06-xSemaphoreCreateMutex)非常相似，但
有一些细微差异：互斥锁具有优先级继承机制，
但二进制信号量没有。因此，二进制信号量是
实现同步的更好选择（任务之间或任务与中断之间），
而互斥锁是实现简单互斥的更好选择。

二值信号量并不需要在得到后立即释放，
因此，任务同步可以通过一个任务/中断持续释放信号量
而另外一个持续获得信号量来实现。相关演示请参阅
[xSemaphoreGiveFromISR()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/17-xSemaphoreGiveFromISR) 文档页面上的代码示例。
请注意，
使用[直达任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/02-As-binary-semaphore)往往可以更有效地实现相同的功能。

如果另一个优先级更高的任务试图获得相同的互斥锁，
那么“获取”互斥锁的任务的优先级就有可能被提高。拥有互斥锁的任务“继承”了
试图“获取”相同互斥锁任务的优先级，这意味着必须始终“返回”互斥锁，否则
优先级较高的任务将永远无法获得互斥锁，
而优先级较低的任务将永远无法“取消继承”优先级。用于实现互斥的互斥锁实例，
详见 [xSemaphoreTake()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/12-xSemaphoreTake) 文档页面。

互斥锁和二进制信号量都由 SemaphoreHandle_t 类型的变量引用，同时可以
在任何采用该类型参数的任务级 API 函数中使用。与互斥锁不同，
二进制信号量可用于中断服务程序。


**返回值：**

+ *NULL*

  因为可用 [FreeRTOS 堆](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)不足，所以无法创建信号量。

+ *其他任何值*

  信号量已成功创建。返回值是一个句柄，
  通过该句柄可以引用信号量。


**用法示例：**

```c
SemaphoreHandle_t xSemaphore;

void vATask( void * pvParameters )
{
    /* Attempt to create a semaphore. */
    xSemaphore = xSemaphoreCreateBinary();

    if( xSemaphore == NULL )
    {
        /* There was insufficient FreeRTOS heap available for the semaphore to
           be created successfully. */
    }
    else
    {
        /* The semaphore can now be used. Its handle is stored in the
           xSemahore variable. Calling xSemaphoreTake() on the semaphore here
           will fail until the semaphore has first been given. */
    }
}
```
