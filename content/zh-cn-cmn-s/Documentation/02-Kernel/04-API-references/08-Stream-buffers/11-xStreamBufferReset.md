---
title: xStreamBufferReset()
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
BaseType_t xStreamBufferReset( StreamBufferHandle_t xStreamBuffer );
```

将[流缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/02-Stream-buffer-example)重置为其初始空状态。任何在流缓冲区的数据
都将被丢弃。只有当没有任务被阻塞以等待向流缓冲区发送或从流缓冲区接收时，
流缓冲区才能被重置
。

在构建中纳入 FreeRTOS/source/stream_buffer.c 源文件
即可启用流缓冲区功能。


**参数：** 

+ *xStreamBuffer* 

  正在重置的流缓冲区的句柄。


**返回：** 

如果流缓冲区重置，则返回 pdPASS。如果有
一个任务被阻塞，等待向流缓冲区发送或从流缓冲区读取，
那么流缓冲区将不会被重置，并返回 pdFAIL。

