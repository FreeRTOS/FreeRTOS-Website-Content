---
title: xMessageBufferReset()
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
BaseType_t xMessageBufferReset( MessageBufferHandle_t xMessageBuffer );
```

重置[消息缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/03-Message-buffer-example)， 
使其恢复到初始空状态。消息缓冲区中的任何数据都将被丢弃。只有在 
没有任务阻塞等待向消息缓冲区发送或从消息缓冲区接收消息时，
才能重置消息缓冲区。

使用 `xMessageBufferReset()` 从任务重置消息缓冲区。使用 `xMessageBufferResetFromISR()` 
从中断服务程序 (ISR) 重置消息缓冲区。 

通过将 FreeRTOS/source/stream_buffer.c 源文件包含在构建中
来启用消息缓冲区功能（因为消息缓冲区使用流缓冲区）。


**参数：** 

- *xMessageBuffer*

  正在重置的消息缓冲区的句柄。


**返回：** 

+ 如果消息缓冲区被重置，则返回 pdPASS。 

+ 如果有阻塞任务等待向消息缓冲区发送数据或从消息缓冲区读取数据， 
  则消息缓冲区将不会被重置，并返回 pdFAIL。
  
