---
title: FreeRTOS_shutdown()
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
BaseType_t FreeRTOS_shutdown( Socket_t xSocket, BaseType_t xHow );
```

在已连接的 TCP 套接字上禁用读取和写入。连接的 TCP 套接字须正常停用，
才能关闭成功。


**参数：** 


+ *xSocket*

  正在停用的套接字。  


+ *xHow*

  必须设置为 FREERTOS_SHUT_RDWR。  

  FreeRTOS-Plus-TCP 目前不使用 xHow 参数，因为它总是同时停用读取和写入。 
  加入 xHow 是为了确保函数原型符合预期的伯克利套接字标准， 
  并与未来可能接受其他参数值的 FreeRTOS-Plus-TCP 版本兼容 
  。  


**返回：** 

+ 如果停用请求成功，则返回 0。在套接字上 
  调用 [FreeRTOS_recv()](recv) 后会返回 -pdFREERTOS_ERRNO_EINVAL，表明停用已完成。

+ 如果 xSocket 不是有效的 TCP 套接字，则返回 -pdFREERTOS_ERRNO_EOPNOTSUPP。

+ 如果 xSocket 是有效的 TCP 套接字，但该套接字未连接到远程套接字， 
  则返回 -pdFREERTOS_ERRNO_EOPNOTSUPP。

请注意，由于 FreeRTOS 没有实现 errno， 
因此出现错误时的行为必然与 connect() 函数不同，后者完全符合预期的伯克利
套接字行为。


**用法示例：** 

在[发送 TCP 数据](../TCP_Networking_Tutorial_Sending_TCP_Data)
和[接收 TCP 数据](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/07-Receiving-TCP-data)页面上的源代码示例演示了如何停止并关闭
已连接的套接字。

