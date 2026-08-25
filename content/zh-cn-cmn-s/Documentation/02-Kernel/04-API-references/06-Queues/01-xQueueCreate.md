---
title: xQueueCreate
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[队列管理](/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]

queue. h

```c
 QueueHandle_t xQueueCreate( UBaseType_t uxQueueLength,
                             UBaseType_t uxItemSize );
```

创建新[队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)并返回一个可以引用该队列的
句柄。  [configSUPPORT_DYNAMIC_ALLOCATION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configsupport_dynamic_allocation)
必须在 FreeRTOSConfig.h 中设置为 1，或保留为未定义状态（默认为 1），
才可使用此 RTOS API 函数。

每个队列都需要 RAM 来保存队列状态
以及队列中包含的项目（队列存储区）。
如果使用 `xQueueCreate()` 创建队列，则所需的 RAM 会自动
从 [FreeRTOS 堆](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)中分配。  如果
使用 [xQueueCreateStatic()](/Documentation/02-Kernel/04-API-references/06-Queues/02-xQueueCreateStatic) 创建队列，
则 RAM 由应用程序编写者提供，这会产生更多的参数，
但这样能够在编译时静态分配 RAM
。有关详细信息，请参阅[静态分配与动态分配](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation)页面。


**参数：**

- *uxQueueLength*

  队列一次可存储的最大项目数。

- *uxItemSize*

  存储队列中每个项目所需的大小（以字节为单位）。

  项目通过复制而非引用的方式入队，因此该参数值是每个入队项目将复制的
  字节数。队列中的每个项目必须具有相同的大小。


**返回：**

- 如果队列创建成功，则返回所创建队列的句柄。如果创建队列所需的内存
  [无法分配](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)，则返回 NULL。


**用法示例：**

```c
struct AMessage
{
    char ucMessageID;
    char ucData[ 20 ];
};

void vATask( void *pvParameters )
{
QueueHandle_t xQueue1, xQueue2;

    /* Create a queue capable of containing 10 unsigned long values. */
    xQueue1 = xQueueCreate( 10, sizeof( unsigned long ) );

    if( xQueue1 == NULL )
    {
        /* Queue was not created and must not be used. */
    }

    /* Create a queue capable of containing 10 pointers to AMessage
       structures. These are to be queued by pointers as they are
       relatively large structures. */
    xQueue2 = xQueueCreate( 10, sizeof( struct AMessage * ) );

    if( xQueue2 == NULL )
    {
        /* Queue was not created and must not be used. */
    }

    /* ... Rest of task code. */
 }
```
