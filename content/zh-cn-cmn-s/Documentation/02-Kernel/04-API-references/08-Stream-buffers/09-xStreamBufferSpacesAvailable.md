---
title:
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

xStreamBufferSpacesAvailable()

[[RTOS 流缓冲区 API](/Documentation/02-Kernel/04-API-references/08-Stream-buffers/00-RTOS-stream-buffer-API)]

stream_buffer.h

```c
size_t xStreamBufferSpacesAvailable( StreamBufferHandle_t xStreamBuffer );
```

查询[流缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/02-Stream-buffer-example)以查看有多少可用空间——
等于在流缓冲区满之前可以向它发送的数据量
。

在构建中纳入 FreeRTOS/source/stream_buffer.c 源文件
即可启用流缓冲区功能。


**参数：** 

+ *xStreamBuffer* 

  正在查询的流缓冲区的句柄。


**返回：** 
在流缓冲区满之前，
可以写入流缓冲区的字节数。

