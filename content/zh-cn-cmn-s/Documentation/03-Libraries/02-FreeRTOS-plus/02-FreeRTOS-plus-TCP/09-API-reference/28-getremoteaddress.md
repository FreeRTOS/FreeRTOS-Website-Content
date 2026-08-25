---
title: FreeRTOS_GetRemoteAddress()
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
BaseType_t FreeRTOS_GetRemoteAddress( Socket_t xSocket, struct freertos_sockaddr *pxAddress );
```

返回已连接的 TCP 套接字的远程 IP 地址和端口。


**参数：** 

+ *xSocket*

  被查询的套接字。  

+ *pxAddress*

  远程地址详细信息将返回到其中的 freertos_sockaddr 结构体。  


**返回：** 

+ 如果 xSocket 参数引用的套接字不是 TCP 套接字，则返回 -pdFREERTOS_ERRNO_EINVAL。

+ 在所有其他情况下，返回 sizeof( freertos_sockaddr )，并且 pxAddress->sin_addr 将被设置为 
  远程连接套接字的 IP 地址，pxAddress->sin_port 将被设置为远程连接套接字的 TCP 端口
  号。

