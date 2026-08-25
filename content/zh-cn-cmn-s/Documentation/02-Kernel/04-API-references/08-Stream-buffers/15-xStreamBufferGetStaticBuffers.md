---
title: xStreamBufferGetStaticBuffers()
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 流缓冲区 API](/Documentation/02-Kernel/04-API-references/08-Stream-buffers/00-RTOS-stream-buffer-API)]


stream_buffer.h

```c
 BaseType_t xStreamBufferGetStaticBuffers( StreamBufferHandle_t xStreamBuffer,
                                           uint8_t ** ppucStreamBufferStorageArea,
                                           StaticStreamBuffer_t ** ppxStaticStreamBuffer );
```

`configSUPPORT_STATIC_ALLOCATION` 必须定义为 1，才可使用此函数。请参阅 
[RTOS 配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization) 文档 
了解更多信息。

检索指向静态创建的流缓冲区数据结构体缓冲区和存储区域缓冲区的指针。 
这些缓冲区与创建时提供的缓冲区相同。


**参数：**

+ `xStreamBuffer`

  数据结构体缓冲区和存储区缓冲区将被检索的流缓冲区。

+ `ppucStreamBufferStorageArea`

  用于返回指向流缓冲区存储区缓冲区的指针。

+ `ppxStaticStreamBuffer`

  用于返回指向流缓冲区的数据结构体缓冲区的指针。


**返回：**

+ 如果检索到缓冲区，则返回 `pdTRUE`， 
+ 否则返回 `pdFALSE`。 


