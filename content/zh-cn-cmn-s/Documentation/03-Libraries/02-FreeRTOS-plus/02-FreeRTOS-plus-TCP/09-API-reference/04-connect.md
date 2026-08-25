---
title: FreeRTOS_connect()
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
BaseType_t FreeRTOS_connect( Socket_t xClientSocket,
                             struct freertos_sockaddr *pxAddress,
                             socklen_t xAddressLength );	
```

[将 TCP 套接字](../TCP_Networking_Tutorial_Sending_TCP_Data)连接到远程套接字。

必须首先通过调用 [FreeRTOS_socket()](socket) 成功创建套接字，
然后选择性地通过调用 [FreeRTOS_bind()](bind) 将其与端口绑定。


如果在未绑定到端口号的套接字上调用 FreeRTOS_connect()，
并且 [ipconfigALLOW_SOCKET_SEND_WITHOUT_BIND](../TCP_IP_Configuration#ipconfigallow_socket_send_without_bind) 的值
在 FreeRTOSIPConfig.h 中设置为 1，则 TCP/IP 堆栈会自动将套接字
与私有地址范围中的一个端口号绑定。

FreeRTOS_connect() 具有可选超时。该超时默认为
ipconfigSOCK_DEFAULT_RECEIVE_BLOCK_TIME，并在
调用 FreeRTOS_setsockopt() 时使用 FREERTOS_SO_RCVTIMEO 参数进行修改。如果
连接操作没有立即成功，那么 RTOS 调用任务
将保持在阻塞状态（以便其他任务可以执行），直到
连接请求成功或超时到期。


**参数：** 

+ *xSocket* 

  正在绑定的套接字的句柄。套接字必须已成功创建（请参阅 [FreeRTOS_socket()](socket)）。

+ *pxAddress* 

  指向 freertos_sockaddr 结构体的指针，该结构体包含目标 IP 地址和端口号 
  （本地套接字试图连接的远程套接字）。
  
+ *xAddressLength* 

  目前未使用，但应设置为（结构体 freertos_sockaddr）的大小以确保未来的兼容性。


**返回：** 

+ 如果连接操作成功，则返回 0。

+ 如果 xSocket 不是有效的 TCP 套接字，则返回 -pdFREERTOS_ERRNO_EBADF。

+ 如果 xSocket 在 FreeRTOS_connect() 被调用之前已连接，
  则返回 -pdFREERTOS_ERRNO_EISCONN。

+ 如果 xSocket 的当前状态不允许进行连接操作，则返回
  -pdFREERTOS_ERRNO_EINPROGRESS 或 -pdFREERTOS_ERRNO_EAGAIN。

+ 如果套接字的读取阻塞时间为零，且连接操作
  无法立即成功，则返回 -pdFREERTOS_ERRNO_EWOULDBLOCK。

+ 如果连接尝试超时，则返回 -pdFREERTOS_ERRNO_ETIMEDOUT
  。

请注意，由于 FreeRTOS 没有实现 errno， 
因此出现错误时的行为必然与 connect() 函数不同，后者完全符合预期的伯克利
套接字行为。


**用法示例：** 

请参阅“[发送 TCP 数据](../TCP_Networking_Tutorial_Sending_TCP_Data)”部分，
（FreeRTOS-Plus-TCP 联网教程页面）。

