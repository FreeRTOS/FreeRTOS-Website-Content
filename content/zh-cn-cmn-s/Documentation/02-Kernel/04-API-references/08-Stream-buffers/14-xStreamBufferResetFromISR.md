---
title: xStreamBufferResetFromISR()
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
BaseType_t xStreamBufferResetFromISR( StreamBufferHandle_t xStreamBuffer );
```

xStreamBufferReset() API 函数的中断安全版本。

重置[流缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/02-Stream-buffer-example)， 
使其恢复到初始空状态。流缓冲区中的任何数据都将被丢弃。只有在没有阻塞任务等待向流缓冲区发送或从流缓冲区接收数据时， 
才能重置流缓冲区。

使用 `xStreamBufferReset()` 从任务重置流缓冲区。使用 `xStreamBufferResetFromISR()` 
从中断服务程序 (ISR) 重置流缓冲区。

将 FreeRTOS/source/stream_buffer.c 源文件包含在构建中即可启用流缓冲区功能 
。


**参数：**

+ `xStreamBuffer`

  要重置的流缓冲区的句柄。


**返回：**

+ 如果流缓冲区重置，则返回 pdPASS。 
+ 如果有阻塞任务等待向流缓冲区发送数据或从流缓冲区读取数据， 
  则流缓冲区将不会被重置，并返回 pdFAIL。


