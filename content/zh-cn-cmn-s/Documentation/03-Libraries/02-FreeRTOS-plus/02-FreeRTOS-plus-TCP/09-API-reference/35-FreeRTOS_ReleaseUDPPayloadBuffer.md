---
title: FreeRTOS_ReleaseUDPPayloadBuffer()
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
void FreeRTOS_ReleaseUDPPayloadBuffer( void *pvBuffer );
```

FreeRTOS_ReleaseUDPPayloadBuffer() 用于将通过零拷贝接口使用的缓冲区返回到 TCP/IP 堆栈 
。

有关传输数据的零拷贝接口信息，请参阅 [FreeRTOS_sendto() 文档页面](sendto)。

有关接收数据的零拷贝接口信息，请参阅 [FreeRTOS_recvfrom() 文档页面](recvfrom)。

如果出现以下情况，则需要将缓冲区返回到堆栈：

1. 缓冲区通过调用 FreeRTOS_recvfrom() 获取，并且其中包含的数据不再需要；或者

2. 缓冲区通过调用 [FreeRTOS_GetUDPPayloadBuffer()](FreeRTOS_GetUDPPayloadBuffer) 获取， 
   但无法传递到 TCP/IP 堆栈（对使用缓冲区的 FreeRTOS_sendto() 的调用操作 
   失败）。

缓冲区也可重复使用，而不是返回到 TCP/IP 堆栈。


**参数：** 

+ *pvBuffer*

  返回到 TCP/IP 堆栈的缓冲区。


**用法示例：** 

[FreeRTOS_sendto() 文档页面](sendto)包含零拷贝发送操作示例， 
演示了在发送操作失败时如何使用 FreeRTOS_ReleaseUDPPayloadBuffer()。

[FreeRTOS_recvfrom() 文档页面](recvfrom)包含的示例演示了 
如何使用 FreeRTOS_ReleaseUDPPayloadBuffer() 释放通过调用 FreeRTOS_recvfrom() 获取的缓冲区。

