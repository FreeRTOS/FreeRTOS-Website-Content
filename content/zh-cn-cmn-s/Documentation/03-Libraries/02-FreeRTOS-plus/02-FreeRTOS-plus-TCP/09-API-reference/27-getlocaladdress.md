---
title: FreeRTOS_GetLocalAddress()
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
size_t FreeRTOS_GetLocalAddress( ConstSocket_t xSocket, 
                                 struct freertos_sockaddr * pxAddress );
```

返回绑定套接字的本地 IP 地址和端口。


**参数：** 


+ *xSocket*

  被查询的套接字。  

+ *pxAddress*

  本地地址详细信息将返回到其中的 freertos_sockaddr 结构体。  


**返回：** 

始终返回 sizeof( freertos_sockaddr )。

