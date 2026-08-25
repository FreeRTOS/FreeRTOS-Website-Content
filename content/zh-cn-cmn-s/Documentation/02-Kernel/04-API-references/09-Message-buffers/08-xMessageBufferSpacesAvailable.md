---
title: xMessageBufferSpacesAvailable()
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
size_t xMessageBufferSpacesAvailable( MessageBufferHandle_t xMessageBuffer );
```

查询一个[消息缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/03-Message-buffer-example)，以查看它包含多少空闲空间，
这等于在消息缓冲区满之前可以
向它发送的数据量。返回的值比可发送到消息缓冲区的
最大消息大小多了 4 个字节。

通过在构建中包含 FreeRTOS/source/stream_buffer.c 源文件
来启用消息缓冲区功能（因为消息缓冲区使用流缓冲区）。


**参数：** 

- *xMessageBuffer*

  正在查询的消息缓冲区的句柄。


**返回：** 

 在消息缓冲区满之前，可以写入消息缓冲区的
 字节数。当消息被
 写入消息缓冲区时，还会额外写入 sizeof( size_t ) 字节
 以存储消息的长度。sizeof( size_t ) 在 32 位架构上通常为 4 字节，
 因此如果 xMessageBufferSpacesAvailable()  返回 10，
 则可以写入消息缓冲区的最大消息的大小
 为 6 字节。

