---
title: vStreamBufferDelete()
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
void vStreamBufferDelete( StreamBufferHandle_t xStreamBuffer );
```

删除之前创建的[流缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/02-Stream-buffer-example) 
（通过调用 [xStreamBufferCreate()](/Documentation/02-Kernel/04-API-references/08-Stream-buffers/01-xStreamBufferCreate) 或 [xStreamBufferCreateStatic()](/Documentation/02-Kernel/04-API-references/08-Stream-buffers/02-xStreamBufferCreateStatic) 创建）。
如果使用动态内存（即由 xStreamBufferCreate()）创建流缓冲区，
则会释放分配的内存。

在删除流缓冲区后，不得使用流缓冲区句柄。

在构建中纳入 FreeRTOS/source/stream_buffer.c 源文件
即可启用流缓冲区功能。


**参数：** 

- *xStreamBuffer*

  要删除的流缓冲区的句柄。
