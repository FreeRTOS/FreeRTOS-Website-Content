---
title: xStreamBufferBytesAvailable()
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
size_t xStreamBufferBytesAvailable( StreamBufferHandle_t xStreamBuffer );
```

查询[流缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/02-Stream-buffer-example)以查看它包含多少数据，
该值等于在流缓冲区为空之前
可以从流缓冲区读取的字节数。

在构建中纳入 FreeRTOS/source/stream_buffer.c 源文件
即可启用流缓冲区功能。


**参数：** 

+ *xStreamBuffer* 

  正在查询的流缓冲区的句柄。


**返回：** 

在流缓冲区为空之前可从流缓冲区读取的
字节数。

