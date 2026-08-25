---
title: FreeRTOS_recv()
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
BaseType_t FreeRTOS_recv( Socket_t xSocket,
                          void *pvBuffer,
                          size_t xBufferLength,
                          BaseType_t xFlags );
```
从 TCP 套接字接收数据（请参阅 [FreeRTOS_recvfrom()](recvfrom) 了解 UDP 相应内容）。

套接字须已通过 [FreeRTOS_socket()](socket) 调用创建， 
并已绑定到端口号，且已连接到远程套接字。

可通过调用 [FreeRTOS_bind()](bind) 将套接字与端口号明确绑定。

套接字可使用 [FreeRTOS_connect()](connect) 主动连接远程套接字。
如果 FreeRTOS_connect() 在未绑定端口号的套接字上被调用，并且 
[ipconfigALLOW_SOCKET_SEND_WITHOUT_BIND](../TCP_IP_Configuration#ipconfigallow_socket_send_without_bind) 的值
在 FreeRTOSIPConfig.h 中设置为 1，则 TCP/IP 堆栈会自动将套接字
与私有地址范围中的一个端口号绑定。

或者，套接字可以使用 [FreeRTOS_accept()](accept) 等待传入连接。

FreeRTOS_recv() 具有可选超时。该超时默认为 
[ipconfigSOCK_DEFAULT_RECEIVE_BLOCK_TIME](../TCP_IP_Configuration#ipconfigsock_default_receive_block_time)，
并使用 FREERTOS_SO_RCVTIMEO 参数通过调用 
[FreeRTOS_setsockopt()](setsockopt) 修改。如果接收操作无法立即返回接收的字节， 
则调用 RTOS 任务将被保持在阻塞状态（以便其他任务
可以执行），直到接收到任何一个字节，或者超时结束。

FreeRTOS-Plus-TCP [当前]未使用所有函数参数。未使用的参数 
保留在函数原型中，以确保与预期的标准伯克利套接字 API 保持一致， 
并确保与 FreeRTOS-Plus-TCP 的未来版本兼容。


**参数：** 

+ *xSocket*

  从中读取数据的套接字的句柄。  

+ *pvBuffer*

  将放置接收数据的缓冲区。  

+ *xBufferLength*

  pvBuffer 参数指向的缓冲区大小（字节数）， 
  因此也是将读取的最大字节数。  

+ *ulFlags*

  目前未使用。未来的 FreeRTOS-Plus-TCP 版本可能会使用 ulFlags 参数实现接收选项 
  。  


**返回：** 

+ 如果接收成功，则返回接收的字节数 
  （放在 pvBuffer 指向的缓冲区中）。

+ 如果在接收数据之前发生超时，则返回 0。

+ 如果没有足够的内存供套接字创建 Rx 或 Tx 流， 
  则返回 -pdFREERTOS_ERRNO_ENOMEM。

+ 如果套接字已关闭或被关闭，则返回 -pdFREERTOS_ERRNO_ENOTCONN。

+ 如果[套接字接收到信号](FreeRTOS_SignalSocket)，导致读取操作中止， 
  则返回 -pdFREERTOS_ERRNO_EINTR。

+ 如果套接字无效，不是 TCP 套接字，或者未绑定，则返回 -pdFREERTOS_ERRNO_EINVAL。

请注意，由于 FreeRTOS 没有实现 errno， 
因此出现错误时的行为必然与 recv() 函数不同，后者完全符合预期的伯克利
套接字行为。


**用法示例：** 

请参阅[“创建、配置和绑定 TCP 客户端和服务器套接字”](../TCP_Networking_Tutorial_TCP_Client_and_Server)一节
（位于 FreeRTOS-Plus-TCP 联网教程页面），了解如何准备 TCP 套接字以接收数据的示例 
。

请参阅 FreeRTOS-Plus-TCP 联网教程页面的 [“接收 TCP 数据”](../TCP_Networking_Tutorial_Receiving_TCP_Data)一节 
了解从 TCP 套接字接收数据的示例。

