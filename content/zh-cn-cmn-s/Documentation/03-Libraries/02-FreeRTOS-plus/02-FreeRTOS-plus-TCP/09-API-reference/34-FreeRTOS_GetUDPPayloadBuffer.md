---
title: FreeRTOS_GetUDPPayloadBuffer()
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-TCP API 引用](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS_sockets.h

```c
void *FreeRTOS_GetUDPPayloadBuffer( size_t xRequestedSizeBytes, TickType_t xBlockTimeTicks );
```

从 TCP/IP 堆栈获取缓冲区以用于零拷贝接口。

用于传输数据的零拷贝接口的描述请参阅 [FreeRTOS_sendto() 文档页面](sendto)。


**参数：** 

+ *xRequestedSizeBytes* 
  
  请求的缓冲区的大小。大小以字节为单位。

+ *xBlockTimeTicks* 
  
  如果无法立即获得缓冲区，调用 RTOS 任务将准备等待缓冲区的最长时间 
  。

  如果缓冲区不可用，则调用 RTOS 任务将处于阻塞状态（以便其他任务可以执行）， 
  直到缓冲区可用或阻塞时间到期。

  阻塞时间以滴答为单位。将毫秒时间除以 portTICK_PERIOD_MS， 
  可将以毫秒为单位的时间转换为以滴答为单位的时间。

  为了防止死锁，最大阻塞时间上限为 ipconfigMAX_SEND_BLOCK_TIME_TICKS。 
  ipconfigMAX_SEND_BLOCK_TIME_TICKS 在 FreeRTOSIPConfig.h 中定义。


**返回：** 

+ 如果获取了缓冲区，则返回指向所获缓冲区的指针。

+ 如果无法获取缓冲区，则返回 NULL。


**用法示例：** 

[FreeRTOS_sendto() 文档页面](sendto)包含零拷贝发送操作的示例， 
其中此操作包含对 FreeRTOS_GetUDPPayloadBuffer() 的调用。

