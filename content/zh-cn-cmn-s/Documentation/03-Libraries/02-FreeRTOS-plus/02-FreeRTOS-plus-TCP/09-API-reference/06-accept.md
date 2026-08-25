---
title: FreeRTOS_accept()
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
Socket_t FreeRTOS_accept( Socket_t xServerSocket,
                           struct freertos_sockaddr *pxAddress,
                           socklen_t *pxAddressLength );
```

接受 TCP 套接字的连接。

必须首先通过调用 [FreeRTOS_socket()](socket) 成功创建套接字，
再调用 [FreeRTOS_bind()](bind) 将其与移植绑定，然后利用 
[FreeRTOS_listen()](listen) 调用将其置于侦听状态。

默认情况下，将创建一个新的套接字（子套接字）来处理任何接受的连接。新的 
套接字将由 [FreeRTOS_accept()](accept) 返回，并可立即使用。子套接字 
继承父套接字的所有属性。

FREERTOS_SO_REUSE_LISTEN_SOCKET 参数 
可与 [FreeRTOS_setsockopt()](setsockopt) 调用一起使用（可选），以配置父套接字自行处理任何已接受的连接， 
而无需为此创建子套接字。当套接字一次只处理一个连接时， 
这是一个节省资源的有用方法。例如，如果套接字用于实现 
远程登录服务器，而该服务器只允许同时进行一个连接。

FreeRTOS_accept() 具有可选超时。超时默认为 ipconfigSOCK_DEFAULT_RECEIVE_BLOCK_TIME， 
并使用 FREERTOS_SO_RCVTIMEO 参数通过调用 FreeRTOS_setsockopt 修改。如果 
接受操作没有立即成功，则调用 RTOS 任务将处于阻塞状态 
（以便其他 RTOS 任务可以执行），直到连接被接受或超时结束。


 **参数：** 

+ *xServerSocket*

  接收新连接的侦听套接字的句柄。  

+ *pxAddress*

  指向 freertos_sockaddr 结构体的指针，该结构体将（由 FreeRTOS_accept() 填充） 
  填入接受连接的套接字的 IP 地址和端口号。  

+ *pxAddressLength*

  目前未使用，但应设置为（结构体 freertos_sockaddr）的大小以确保未来的兼容性。  


**返回：** 

+ 如果接受了来自远程套接字的连接，并创建了一个新的本地套接字来处理接受的连接， 
  则会返回新套接字的句柄。

+ 如果 xServerSocket 不是有效的 TCP 套接字，则返回 FREERTOS_INVALID_SOCKET。

+ 如果 xServerSocket 不处于侦听状态（请参阅 [FreeRTOS_listen()](listen)），则返回 
  FREERTOS_INVALID_SOCKET 。

+ 如果在来自远程套接字的连接被接受之前发生超时，则返回 NULL。

请注意，由于 FreeRTOS 没有实现 errno， 
因此出现错误时的行为必然与 connect() 函数不同，后者完全符合预期的伯克利
套接字行为。


**用法示例：** 

请参阅“创建、配置和绑定 TCP 服务器套接字”源代码示例 
（位于 [“创建、配置和绑定 TCP 客户端和服务器套接字”](../TCP_Networking_Tutorial_TCP_Client_and_Server) 一节）
，节选自《FreeRTOS-Plus-TCP 联网教程》。

