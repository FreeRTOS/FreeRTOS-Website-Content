---
title: xStreamBufferIsEmpty()
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
BaseType_t xStreamBufferIsEmpty( StreamBufferHandle_t xStreamBuffer );
```

查询[流缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/02-Stream-buffer-example)以查看其是否为空。
如果流缓冲区不包含任何数据，则为空。

在构建中纳入 FreeRTOS/source/stream_buffer.c 源文件
即可启用流缓冲区功能。


**参数：** 

+ *xStreamBuffer* 

  正在查询的流缓冲区的句柄。


**返回：** 

如果流缓冲区为空，则返回 pdTRUE。否则
返回 pdFALSE。

