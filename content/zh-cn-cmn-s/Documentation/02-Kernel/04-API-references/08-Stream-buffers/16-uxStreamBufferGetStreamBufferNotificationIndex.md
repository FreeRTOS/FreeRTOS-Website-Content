---
title: uxStreamBufferGetStreamBufferNotificationIndex()
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
UBaseType_t uxStreamBufferGetStreamBufferNotificationIndex( StreamBufferHandle_t xStreamBuffer );
```

检索 
提供的[流缓冲区](/Documentation/02-Kernel/04-API-references/08-Stream-buffers/00-RTOS-stream-buffer-API)使用的任务通知索引， 
该索引可使用 [vStreamBufferSetStreamBufferNotificationIndex](17-vStreamBufferSetStreamBufferNotificationIndex) 设置。 
如果未使用 `vStreamBufferSetStreamBufferNotificationIndex` 更改流缓冲区的任务通知索引， 
此函数返回默认值 `tskDEFAULT_INDEX_TO_NOTIFY`。

将 FreeRTOS/source/stream_buffer.c 源文件包含在构建中， 
并在 FreeRTOSConfig.h 中将 `configUSE_STREAM_BUFFERS` 配置常量设置为 1 即可启用流缓冲区功能。


**参数：**

+ `xStreamBuffer`

  用于检索任务通知索引的流缓冲区句柄。


**返回：**

+ 用于流缓冲区的任务通知索引。

