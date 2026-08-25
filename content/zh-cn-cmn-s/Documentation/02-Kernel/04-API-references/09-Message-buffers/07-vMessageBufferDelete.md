---
title: vMessageBufferDelete()
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
void vMessageBufferDelete( MessageBufferHandle_t xMessageBuffer );
```

删除之前创建的[消息缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/03-Message-buffer-example) 
（通过调用 [xMessageBufferCreate()](/Documentation/02-Kernel/04-API-references/09-Message-buffers/01-xMessageBufferCreate) 或 [xMessageBufferCreateStatic()](/Documentation/02-Kernel/04-API-references/09-Message-buffers/02-xMessageBufferCreateStatic) 创建）。
如果使用动态内存（即由 `xMessageBufferCreate()`）创建消息缓冲区，
则会释放分配的内存。

删除消息缓冲区后，不得使用消息缓冲区句柄。

通过将 FreeRTOS/source/stream_buffer.c 源文件包含在构建中
来启用消息缓冲区功能（因为消息缓冲区使用流缓冲区）。


**参数：** 

- *xMessageBuffer*

  要删除的消息缓冲区的句柄。
