---
title: "xMessageBufferGetStaticBuffers()"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 消息缓冲区 API](/Documentation/02-Kernel/04-API-references/09-Message-buffers/00-RTOS-message-buffer-API)]


message_buffer.h

```c
BaseType_t xMessageBufferGetStaticBuffers( MessageBufferHandle_t xMessageBuffer,
                                           uint8_t ** ppucMessageBufferStorageArea,
                                           StaticMessageBuffer_t ** ppxStaticMessageBuffer );
```

必须将 configSUPPORT_STATIC_ALLOCATION 定义为 1，此函数才可用。请参阅 RTOS 
配置文档了解更多信息。

检索指向静态创建的消息缓冲区的数据结构体缓冲区和存储区缓冲区的指针。 
这些缓冲区与创建时提供的缓冲区相同。


**参数：**

+ *xMessageBuffer*

  数据结构体缓冲区和存储区缓冲区将被检索的消息缓冲区。

+ *ppucMessageBufferStorageArea*

  用于返回指向消息缓冲区存储区缓冲区的指针。

+ *ppxStaticMessageBuffer*

   用于返回指向消息缓冲区的数据结构体缓冲区的指针。


**返回：**

如果检索到缓冲区，则返回 pdTRUE，否则返回 pdFALSE。 


