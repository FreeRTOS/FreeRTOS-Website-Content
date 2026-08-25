---
title: xMessageBufferIsFull()
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
BaseType_t xMessageBufferIsFull( MessageBufferHandle_t xMessageBuffer );
```

查询[消息缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/03-Message-buffer-example)以查看其是否已满。
如果消息缓冲区无法再接受任何大小的消息，则消息缓冲区已满，
直到通过从消息缓冲区中删除消息来提供空间为止。

通过在构建中包含 FreeRTOS/source/stream_buffer.c 源文件
来启用消息缓冲区功能（因为消息缓冲区使用流缓冲区）。


**参数：** 

- *xMessageBuffer*

  正在查询的消息缓冲区的句柄。


**返回：** 

如果消息缓冲区已满，则返回 pdTRUE。否则，返回 pdFALSE。

