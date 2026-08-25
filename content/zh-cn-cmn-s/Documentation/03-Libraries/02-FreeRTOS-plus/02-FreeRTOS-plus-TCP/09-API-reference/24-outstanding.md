---
title: FreeRTOS_outstanding()
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
BaseType_t FreeRTOS_outstanding( Socket_t xSocket );
```

返回 TCP 套接字 Tx 流中尚未传输的字节数。


**参数：** 

+ *xSocket* 

  被查询的套接字。


**返回：** 

如果 xSocket 参数引用的套接字不是 TCP 套接字，则返回 -pdFREERTOS_ERRNO_EINVAL 
。

如果 xSocket 参数引用的套接字还没有 Tx 流，则返回 0 
（Tx 流在需要时才会创建）。

在所有其他情况下，返回值是套接字 Tx 流中剩余的字节数。

