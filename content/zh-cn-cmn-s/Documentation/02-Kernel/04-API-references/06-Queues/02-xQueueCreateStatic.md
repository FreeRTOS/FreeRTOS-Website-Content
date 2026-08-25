---
title: xQueueCreateStatic
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
 QueueHandle_t xQueueCreateStatic(
                             UBaseType_t uxQueueLength,
                             UBaseType_t uxItemSize,
                             uint8_t *pucQueueStorageBuffer,
                             StaticQueue_t *pxQueueBuffer );
```

创建新[队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)并返回一个可以引用该队列的
句柄。  [configSUPPORT_STATIC_ALLOCATION](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configsupport_static_allocation)
必须在 FreeRTOSConfig.h 中设置为 1，才可使用此 RTOS API 函数。

每个队列都需要 RAM 来保存队列状态
以及队列中包含的项目（队列存储区）。
如果使用 [xQueueCreate()](/Documentation/02-Kernel/04-API-references/06-Queues/01-xQueueCreate) 创建队列，
则这部分 RAM 会自动从 [FreeRTOS 堆](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)中分配。
如果使用 xQueueCreateStatic() 创建队列，
则 RAM 由应用程序编写者提供，这会产生更多的参数，
但这样能够在编译时静态分配 RAM
。有关详细信息，请参阅[静态分配与动态分配](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation)页面。


**参数：**

+ *uxQueueLength*

  队列一次可存储的最大项目数。

+ *uxItemSize*

  存储队列中每个项目所需的大小（以字节为单位）。

  项目通过复制而非引用的方式入队，因此该参数值是每个入队项目将复制的
  字节数。队列中的每个项目必须具有相同的大小。

+ *pucQueueStorageBuffer*

  如果 uxItemSize 不为零，则 pucQueueStorageBuffer 必须指向一个 uint8_t 数组，该数组的大小
  至少要能容纳队列中最多可能存在的项目的总字节数，
  即 ( uxQueueLength * uxItemSize ) 字节。如果 uxItemSize 为零，则 pucQueueStorageBuffer 可以为 NULL。

+ *pxQueueBuffer*

   必须指向 StaticQueue_t 类型的变量，该变量将用于保存队列的数据结构体。


**返回：**

如果队列创建成功，
则返回所创建队列的句柄。如果 pxQueueBuffer 为 NULL，则返回 NULL。


**用法示例：**

```c

/* The queue is to be created to hold a maximum of 10 uint64_t
   variables. */
#define QUEUE_LENGTH    10
#define ITEM_SIZE       sizeof( uint64_t )

/* The variable used to hold the queue's data structure. */
static StaticQueue_t xStaticQueue;

/* The array to use as the queue's storage area. This must be at least
   uxQueueLength * uxItemSize bytes. */
uint8_t ucQueueStorageArea[ QUEUE_LENGTH * ITEM_SIZE ];

void vATask( void *pvParameters )
{
QueueHandle_t xQueue;

    /* Create a queue capable of containing 10 uint64_t values. */
    xQueue = xQueueCreateStatic( QUEUE_LENGTH,
                                 ITEM_SIZE,
                                 ucQueueStorageArea,
                                 &xStaticQueue );

    /* pxQueueBuffer was not NULL so xQueue should not be NULL. */
    configASSERT( xQueue );
 }
```

