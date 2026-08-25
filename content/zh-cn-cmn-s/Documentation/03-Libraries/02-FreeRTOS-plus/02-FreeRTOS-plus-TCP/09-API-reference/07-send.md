---
title: FreeRTOS_send()
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
BaseType_t FreeRTOS_send( Socket_t xSocket,
                          const void *pvBuffer,
                          size_t xDataLength,
                          BaseType_t xFlags );
```

发送数据至 TCP 套接字（请参阅 [FreeRTOS_sendto()](sendto) 了解 UDP 相应内容）。

套接字须已通过 [FreeRTOS_socket()](socket) 调用创建，
并已绑定到端口号，且已连接到远程套接字。

可通过调用 [FreeRTOS_bind()](bind) 将套接字与端口号明确绑定。

套接字可使用 [FreeRTOS_connect()](connect) 主动连接远程套接字。
如果 FreeRTOS_connect() 在未绑定端口号的套接字上被调用，并且 
[ipconfigALLOW_SOCKET_SEND_WITHOUT_BIND](../TCP_IP_Configuration#ipconfigallow_socket_send_without_bind) 的值
在 FreeRTOSIPConfig.h 中设置为 1，则 TCP/IP 协议栈会自动将套接字绑定到 
私有地址范围内的端口号上。

或者，套接字可以使用 [FreeRTOS_accept()](accept) 等待传入连接。

FreeRTOS_send() 具有可选超时。该超时默认为 
[ipconfigSOCK_DEFAULT_SEND_BLOCK_TIME](../TCP_IP_Configuration#ipconfigSOCK_DEFAULT_SEND_BLOCK_TIME)，
并使用 FREERTOS_SO_SNDTIMEO 参数通过调用 [FreeRTOS_setsockopt()](setsockopt) 修改。
如果发送操作不能立即将字节加入队列等待传输，那么调用 RTOS 任务 
将保持在阻塞状态（以便其他任务可以执行），直到 
字节可以排队发送或超时结束。

FreeRTOS -Plus- TCP [当前]未使用所有函数参数。不使用的参数保留在函数原型中， 
以确保与预期的标准伯克利套接字 API 保持一致， 
并确保与 FreeRTOS-Plus-TCP 的未来版本兼容。


**参数：** 

+ *xSocket*

  接收发送数据的套接字的句柄。套接字必须已成功创建， 
  并与一个端口号绑定（请参阅 [FreeRTOS_socket()](socket) 和 [FreeRTOS_bind()](bind)）。  


+ *pvBuffer* 

  指向传输数据的来源。  


+ *xDataLength*

  待发送的字节数。  


+ *xFlags*

  目前未使用。未来的 FreeRTOS-Plus-TCP 版本可能会使用 ulFlags 参数实现发送选项 
  。  


**返回：** 

+ 如果发送成功，则返回排队等待发送的字节数 
  （注意可能比 xTotalDataLength 参数请求的字节数少）。

+ 如果由于套接字已关闭或被关闭而无法发送数据，则返回 -pdFREERTOS_ERRNO_ENOTCONN 
  。

+ 如果由于内存不足而无法发送数据，则返回 -pdFREERTOS_ERRNO_ENOMEM。

+ 如果由于 xSocket 不是有效的 TCP 套接字而无法发送数据，则返回 -pdFREERTOS_ERRNO_EINVAL 
  。

+ 如果在可以发送任何数据之前发生超时，则返回 -pdFREERTOS_ERRNO_ENOSPC。

请注意，由于 FreeRTOS 没有实现 errno， 
因此出现错误时的行为必然与 connect() 函数不同，后者完全符合预期的伯克利
套接字行为。


**用法示例：** 

请参阅[“创建、配置和绑定 TCP 客户端和服务器套接字”](../TCP_Networking_Tutorial_TCP_Client_and_Server)一节
（位于 FreeRTOS-Plus-TCP 联网教程页面），了解如何准备 TCP 套接字以发送数据的示例 
。

请参阅 FreeRTOS-Plus-TCP 联网教程页面的 [“发送 TCP 数据”](../TCP_Networking_Tutorial_Sending_TCP_Data)一节 
了解向 TCP 套接字发送数据的示例。

