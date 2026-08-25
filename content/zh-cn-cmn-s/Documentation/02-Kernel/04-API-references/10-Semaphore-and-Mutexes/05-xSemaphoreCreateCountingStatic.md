---
title: xSemaphoreCreateCountingStatic
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[信号量](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/00-Semaphores)]

[**提示：在许多情况下， “任务通知”可以提供计数信号量的轻量级替代方案**](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/03-As-counting-semaphore)


semphr. h

```c
SemaphoreHandle_t xSemaphoreCreateCountingStatic(
                                 UBaseType_t uxMaxCount,
                                 UBaseType_t uxInitialCount
                                 StaticSemaphore_t *pxSemaphoreBuffer );
```

创建一个[计数信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/03-Counting-semaphores/)，
并返回一个可以引用该新建信号量的句柄。
[configSUPPORT_STATIC_ALLOCATION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configsupport_static_allocation)
必须在 FreeRTOSConfig.h 中设置为 1，才可使用此 RTOS API 函数。

每个计数信号量需要少量 RAM ，用于保存
信号量的状态。如果使用 [xSemaphoreCreateCounting()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/04-xSemaphoreCreateCounting) 创建计数信号量，
则所需的 RAM 将从 [FreeRTOS 堆](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)自动分配。
如果使用 xSemaphoreCreateCountingStatic () 创建计数信号量，
则 RAM 由应用程序编写器提供，这需要用到一个附加参数，
但允许在编译时静态分配 RAM
。有关详细信息，请参阅[静态分配与动态分配](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation)页面。


计数信号量通常用于两种情况：

1. 盘点事件。

   在此使用场景中，
   每次发生事件（增加信号量计数值）时 ，事件处理程序都会“给出”信号量，处理程序任务
   每次处理事件时，都会“获取”信号量
   （递减信号量计数值）。因此，计数值是
   已发生的事件数量和
   已处理的数量之间的差。在这种情况下，
   初始计数值最好为零。

   请注意，
   使用[直达任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)往往可以更有效地实现相同的功能。

2. 资源管理。

   在此使用方案中，计数值表示可用的资源数量
   。若要获取对资源的控制权，任务就必须首先获取
   信号量-递减信号量计数值。当计数值
   达到零，则表示没有可用资源。当任务结束使用
   资源时，它会“返回”信号量-增加信号量计数
   值。在这种情况下，初始计数值最好
   等于所述最大计数值，表明所有资源都是可用的。


**参数：**

+ *uxMaxCount*

  可以达到的最大计数值。当信号量达到此值时，它不能再
  被“给出”。

+ *uxInitialCount*

  创建信号量时分配给信号量的计数值。

+ *pxSemaphoreBuffer*

  必须指向一个 StaticSemaphore_t 类型的变量，然后用它来保存信号量的数据结构体。


**返回：**

如果已成功创建信号量，则将返回该信号量的句柄。如果 pxSemaphoreBuffer 为 NULL，
则返回 NULL。


**用法示例：**

```c
static StaticSemaphore_t xSemaphoreBuffer;

void vATask( void * pvParameters )
{
SemaphoreHandle_t xSemaphore;

    /* Create a counting semaphore that has a maximum count of 10 and an
       initial count of 0. The semaphore's data structures are stored in the
       xSemaphoreBuffer variable - no dynamic memory allocation is performed. */
    xSemaphore = xSemaphoreCreateCountingStatic( 10, 0, &xSemaphoreBuffer );

    /* pxSemaphoreBuffer was not NULL so it is expected that the semaphore
       will be created. */
    [configASSERT](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert)( xSemaphore );
}
```
