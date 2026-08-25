---
title: xStreamBufferSetTriggerLevel()
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
BaseType_t xStreamBufferSetTriggerLevel( StreamBufferHandle_t xStreamBuffer,
                                         size_t xTriggerLevel );
```

[流缓冲区](/Documentation/02-Kernel/04-API-references/08-Stream-buffers/00-RTOS-stream-buffer-API)的触发等级是指 
在流缓冲区中被阻塞以等待数据的任务离开阻塞状态之前，流缓冲区中必须有的字节数 
。例如，如果一个任务在读取触发等级为 1 的空流缓冲区时被阻塞， 
那么当单个字节写入缓冲区或该任务的阻塞时间到期时， 
该任务才会被解除阻塞。另一个示例是，如果一个任务在读取触发等级为 10 的空流缓冲区时被阻塞， 
那么直到流缓冲区至少包含 10 个字节或该任务的阻塞时间结束， 
该任务才会被解除阻塞。如果读任务的阻塞时间在达到触发等级之前过期， 
那么该任务仍将接收实际可用的字节数。将触发等级 
设置为 0 将导致使用触发等级 1。指定 
大于缓冲区大小的触发等级是无效的。

触发等级在创建流缓冲区时设置，可使用 xStreamBufferSetTriggerLevel() 进行修改。

将 FreeRTOS/source/stream_buffer.c 源文件包含在构建中即可启用流缓冲区功能。


**参数：** 

+ *xStreamBuffer* 

  正在更新的流缓冲区的句柄。

+ *xTriggerLevel* 

  流缓冲区的新触发等级。


**返回：** 

如果 xTriggerLevel 小于或等于流缓冲区的长度， 
将更新触发等级并返回 pdTRUE。否则，返回 pdFALSE。
