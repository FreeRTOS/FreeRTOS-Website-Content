---
title: vStreamBufferSetStreamBufferNotificationIndex()
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
void vStreamBufferSetStreamBufferNotificationIndex( StreamBufferHandle_t xStreamBuffer,
                                                    UBaseType_t uxNotificationIndex );
```

设置 
所提供的[流缓冲区](/Documentation/02-Kernel/04-API-references/08-Stream-buffers/00-RTOS-stream-buffer-API)使用的任务通知索引。 
对该流缓冲区的 API（如 [xStreamBufferSend](03-xStreamBufferSend) 
或 [xStreamBufferReceive](05-xStreamBufferReceive)）的连续调用将使用这个新索引 
来进行任务通知。

将 FreeRTOS/source/stream_buffer.c 源文件包含在构建中， 
并在 FreeRTOSConfig.h 中将 `configUSE_STREAM_BUFFERS` 配置常量设置为 1 即可启用流缓冲区功能。


**参数：**

+ `xStreamBuffer`

  用于设置任务通知索引的流缓冲区句柄。

+ `uxNotificationIndex`

  要设置的任务通知索引。

