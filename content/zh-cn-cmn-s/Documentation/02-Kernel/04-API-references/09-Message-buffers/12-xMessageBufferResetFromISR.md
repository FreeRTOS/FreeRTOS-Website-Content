---
title: "xMessageBufferResetFromISR()"
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
BaseType_t xMessageBufferResetFromISR( MessageBufferHandle_t xMessageBuffer );
```

xMessageBufferReset() API 函数的中断安全版本。

将消息缓冲区重置为其初始空状态。消息缓冲区中的任何数据都将被丢弃。 
只有在没有任务阻塞等待向消息缓冲区发送或从消息缓冲区接收消息时， 
才能重置消息缓冲区。

使用 xMessageBufferReset() 从任务重置消息缓冲区。使用 xMessageBufferResetFromISR() 
从中断服务程序 (ISR) 重置消息缓冲区。

通过在构建中包含 FreeRTOS/source/stream_buffer.c 源文件 
来启用消息缓冲区功能（因为消息缓冲区使用流缓冲区）。


**参数：**

+ *xMessageBuffer*

  要重置的消息缓冲区的句柄。


**返回：**

如果消息缓冲区被重置，则返回 pdPASS。如果有阻塞任务等待向流缓冲区发送数据或从流缓冲区读取数据， 
则消息缓冲区将不会被重置，并返回 pdFAIL。

