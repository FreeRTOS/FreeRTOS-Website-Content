---
title: FreeRTOS_maywrite()
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
BaseType_t FreeRTOS_maywrite( Socket_t xSocket );
```

在 Tx 流充满之前，返回可添加到 TCP 套接字的 Tx 流中的字节数。


**参数：** 

+ *xSocket*

  被查询的套接字。


**返回：** 

+ 如果 xSocket 参数引用的套接字不是 TCP 套接字，则返回 -pdFREERTOS_ERRNO_EINVAL。

+ 如果套接字未处于允许发送数据的状态（例如处于监听状态或 
  正在关闭），则返回 -1。

+ 如果套接字处于“已建立”状态，则返回值为可添加到套接字 
  Tx 流的字节数。

