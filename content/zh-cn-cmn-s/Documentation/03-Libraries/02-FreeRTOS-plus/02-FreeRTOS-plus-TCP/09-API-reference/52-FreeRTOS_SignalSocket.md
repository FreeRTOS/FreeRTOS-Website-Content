---
title: FreeRTOS_SignalSocket()
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
BaseType_t FreeRTOS_SignalSocket( Socket_t xSocket );

BaseType_t FreeRTOS_SignalSocketFromISR( Socket_t xSocket,
                                         BaseType_t *pxHigherPriorityTaskWoken );
```

用于向套接字发送信号，其结果是：任何在读取套接字时被阻塞的任务 
都将离开阻塞状态（中止阻塞操作），任务的读取 
操作（[FreeRTOS_recv()](recv) 或 [FreeRTOS_recvfrom()](recvfrom)）返回 -pdFREERTOS_ERRNO_EINTR。

如果此套接字是某套接字集 (SocketSet_t) 的一部分，则使用该套接字集的 [FreeRTOS_select()](select) 
调用也会被中断，并返回 eSELECT_INTR。

FreeRTOS_SignalSocketFromISR() 是 FreeRTOS_SignalSocket() 的一个版本，可从中断服务程序 (ISR) 中使用 
。


[ipconfigSUPPORT_SIGNALS](../TCP_IP_Configuration#ipconfigSUPPORT_SIGNALS) 必须在  
FreeRTOSIPConfig.h 中设为 1，FreeRTOS_SignalSocket() 才可用。


**参数：** 


+ *xSocket* 
  
  信号要发往的套接字。

 

+ *pxHigherPriorityTaskWoken* 
  
  \[仅用于 FreeRTOS_SignalSocketFromISR()。\]

  `pxHigherPriorityTaskWoken` 必须初始化为 0。

  如果发送信号至套接字导致任务取消阻塞，而且取消阻塞的任务的优先级高于当前运行的任务，则 FreeRTOS_SignalSocketFromISR()  
  将设 *pxHigherPriorityTaskWoken 为 pdTRUE
  。

  如果 FreeRTOS_SignalSocket() 将此值设置为 pdTRUE，则应在退出中断之前请求上下文切换 
  。用于请求 ISR 执行上下文切换的宏名称取决于 
  具体移植，可能称为 portYIELD_FROM_ISR() 或 portEND_SWITCHING_ISR()。请参阅 
  为相关移植所提供的文件和示例。


**返回：** 

如果 xSocket 不是有效的套接字，则返回 -pdFREERTOS_ERRNO_EINVAL。否则将返回 0 。

