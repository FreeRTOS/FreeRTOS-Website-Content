---
title: "xQueueGetStaticBuffers()"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[队列管理](/Documentation/02-Kernel/04-API-references/06-Queues/00-QueueManagement)]

queue.h

```c
 BaseType_t xQueueGetStaticBuffers( QueueHandle_t xQueue,
                                    uint8_t ** ppucQueueStorage,
                                    StaticQueue_t ** ppxStaticQueue );
```

`configSUPPORT_STATIC_ALLOCATION` 必须定义为 1，才可使用此函数。有关详细信息，请参阅 
[RTOS 配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization)文档。

检索指向静态创建队列的数据结构体缓冲区和存储区缓冲区的指针。这些 
缓冲区在创建时提供。

**参数：**

+ `xQueue`

  要检索其数据结构体缓冲区和存储区缓冲区的队列。

+ `ppucQueueStorage`

  用于返回指向队列存储区缓冲区的指针。

+ `ppxStaticQueue`

  用于返回指向队列数据结构体缓冲区的指针。

**返回：**

+ 如果检索到缓冲区，则返回 `pdTRUE`， 
+ 否则返回 `pdFALSE`。 


