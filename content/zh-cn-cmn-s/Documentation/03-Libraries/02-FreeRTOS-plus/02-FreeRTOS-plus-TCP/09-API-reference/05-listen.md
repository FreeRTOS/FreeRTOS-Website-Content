---
title: FreeRTOS_listen()
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
BaseType_t FreeRTOS_listen( Socket_t xSocket, BaseType_t xBacklog );
```

使 TCP 套接字进入监听状态，可接受来自远程套接字的传入连接请求 
。

必须首先通过调用 [FreeRTOS_socket()](socket) 成功创建套接字，
然后调用 [FreeRTOS_bind()](bind) 将其与移植绑定。

默认情况下，将创建一个新的套接字（子套接字）来处理任何接受的连接。新的 
套接字将由 [FreeRTOS_accept()](accept) 返回，并可立即使用。子套接字 
继承父套接字的所有属性。

FREERTOS_SO_REUSE_LISTEN_SOCKET 参数 
可与 [FreeRTOS_setsockopt()](setsockopt) 调用一起使用（可选），以配置父套接字自行处理任何已接受的连接， 
而无需为此创建子套接字。当套接字一次只处理一个连接时， 
这是一个节省资源的有用方法。例如，如果套接字用于实现 
远程登录服务器，而该服务器只允许同时进行一个连接。


**参数：** 

+ *xSocket*

  进入监听状态的套接字的句柄。必须已通过 
  调用 [FreeRTOS_socket()](socket)) 创建了套接字， 
  并通过调用 [FreeRTOS_bind()](bind))  
   绑定了端口号。
+ *xBacklog* 

  在默认情况下，每个新连接都会创建一个新的套接字， 
  积压值会对同时连接的客户端数量做出限制。  


**返回：** 

+ 如果套接字成功置于监听状态，则返回 0。

+ 如果 xSocket 不是有效的 TCP 套接字，则返回 -pdFREERTOS_ERRNO_EOPNOTSUPP。

+ 如果 xSocket 未处于绑定状态但处于关闭状态，则返回 -pdFREERTOS_ERRNO_EOPNOTSUPP。

请注意，由于 FreeRTOS 没有实现 errno， 
因此出现错误时的行为必然与 connect() 函数不同，后者完全符合预期的伯克利
套接字行为。


**用法示例：** 

请参阅“创建、配置和绑定 TCP 服务器套接字”源代码示例 
[《创建、配置和绑定 TCP 客户端和服务器套接字》一章](../TCP_Networking_Tutorial_TCP_Client_and_Server)
（FreeRTOS-Plus-TCP 联网教程页面）。

