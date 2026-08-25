---
title: FreeRTOS_issocketconnected()
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
BaseType_t FreeRTOS_issocketconnected( Socket_t xSocket );
```

测试套接字是否连接。


**参数：** 

+ *xSocket* 

  被查询的套接字。


**返回：** 

+ 如果 xSocket 参数引用的套接字不是 TCP 套接字，则返回 -pdFREERTOS_ERRNO_EINVAL。

+ 如果套接字处于已创建或 FIN 等待状态，则返回 pdTRUE。否则返回 pdFALSE；

