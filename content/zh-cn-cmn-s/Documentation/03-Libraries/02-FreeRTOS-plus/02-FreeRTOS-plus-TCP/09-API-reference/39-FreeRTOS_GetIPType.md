---
title: "FreeRTOS_GetIPType()"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-TCP API 引用](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS_Sockets.h

```c
BaseType_t FreeRTOS_GetIPType( ConstSocket_t xSocket );
```

获取 IP 版本（"ipTYPE_IPv4" 或 "ipTYPE_IPv6"）。


**参数：**

+ *xSocket*

  待检查的套接字。


**返回：**

ipTYPE_IPv4 或 ipTYPE_IPv6。

