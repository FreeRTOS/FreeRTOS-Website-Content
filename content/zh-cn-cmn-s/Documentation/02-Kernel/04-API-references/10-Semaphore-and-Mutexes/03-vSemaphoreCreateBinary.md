---
title: vSemaphoreCreateBinary
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[信号量](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/00-Semaphores)]

semphr.h 

```c
vSemaphoreCreateBinary( SemaphoreHandle_t xSemaphore )
```

**注意：**`vSemaphoreCreateBinary()` 宏仍保留在源代码中，以确保向后兼容性， 
但不应在新设计中使用。使用 [xSemaphoreCreateBinary()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/01-xSemaphoreCreateBinary) 
函数代替。

 此外，在许多情况下，使用 
[直达任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)来代替二进制信号量更快、更节省内存。

使用现有队列机制创建信号量的*宏*。队列长度为 1 ， 
因为这是二进制信号量。数据大小为 0 ，因为实际上我们并不会存储任何数据， 
只想知道队列为空还是满。

二进制信号量和[互斥锁](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/06-xSemaphoreCreateMutex)非常相似，但有一些小差异： 
互斥锁包含优先级继承机制，而二进制信号量不包含。这使得二进制信号量 
成为实现同步（任务之间或任务与中断之间）的更好选择， 
而互斥锁则成为实现简单互斥的更好选择。

在获得二进制信号量后无需返回， 
因此任务同步可以通过一个任务/中断持续“给予”信号量，而另一个任务/中断持续“获取”信号量来实现。 
[xSemaphoreGiveFromISR()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/17-xSemaphoreGiveFromISR) 文档页面上的示例代码对此进行了演示。

如果另一个优先级更高的任务尝试获取相同的互斥锁，
那么“获取”互斥锁的任务的优先级就有可能被提高。拥有互斥锁的任务“继承”了
试图“获取”相同互斥锁任务的优先级，这意味着必须始终“返回”互斥锁，否则
优先级较高的任务将永远无法获得互斥锁，
而优先级较低的任务将永远无法“取消继承”优先级。用于实现互斥的互斥锁实例，
详见 [xSemaphoreTake()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/12-xSemaphoreTake) 文档页面。

互斥锁和二进制信号量都分配给了 `SemaphoreHandle_t` 类型的变量，
可在任何采用此类型参数的 API 函数中使用。


**参数：**

- *xSemaphore*

  已创建信号量的句柄，应为 `SemaphoreHandle\_t` 类型。 


**用法示例：** 

```c
 SemaphoreHandle_t xSemaphore;

 void vATask( void * pvParameters )
 {
    // Semaphore cannot be used before a call to vSemaphoreCreateBinary ().
    // This is a macro so pass the variable in directly.
    vSemaphoreCreateBinary( xSemaphore );

    if( xSemaphore != NULL )
    {
        // The semaphore was created successfully.
        // The semaphore can now be used.
    }
 }
 ```
