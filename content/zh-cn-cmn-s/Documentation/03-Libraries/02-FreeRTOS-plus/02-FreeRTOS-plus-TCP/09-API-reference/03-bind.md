---
title: FreeRTOS_bind()
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
BaseType_t FreeRTOS_bind( Socket_t xSocket,
                          struct freertos_sockaddr *pxAddress,
                          socklen_t xAddressLength );
```

将套接字与本地端口号绑定。绑定套接字会将套接字 
与本地 IP 地址上的端口号关联起来，从而使套接字接收发送到该 IP 地址和 
端口号组合的所有数据。

[嵌入式网络基础知识和术语表](../networking_basics)页面的网络寻址和绑定部分
介绍了套接字绑定的主题。

49408 (0xC100) 至 65280 (0xff00) 以上的端口号被视为可用于 IP 堆栈动态分配的私有编号， 
因此应避免使用。指定端口号为 0 或将
pxAddress 作为 NULL 传递，也会导致该套接字被绑定到私有范围的端口号上。

为方便起见，如果在 FreeRTOSIPConfig.h 中将 ipconfigALLOW_SOCKET_SEND_WITHOUT_BIND 设为 1， 
那么在未首先绑定端口号的套接字上调用 [FreeRTOS_send()](send) 时，
也会导致该套接字被绑定到私有范围的端口号上。

FreeRTOS -Plus- TCP [当前]未使用所有函数参数。不使用的参数保留在函数原型中， 
以确保与预期的标准伯克利套接字 API 保持一致， 
并确保与 FreeRTOS-Plus-TCP 的未来版本兼容。


**参数：** 

+ *xSocket*

  正在绑定到地址的套接字的句柄。该套接字必须是之前 
  通过成功调用 [FreeRTOS_socket()](socket) 创建的。 

+ *pxAddress*

   指向 freertos_sockaddr 结构体的指针，该结构体包含绑定端口号的详细信息 
   。请参阅提供的示例。 

+ *xAddressLength*

   目前未使用，但应设置为 sizeof( struct freertos_sockaddr ) 
   以确保未来的兼容性。 


**返回：** 

返回 0，表示绑定成功（0 是标准伯克利套接字 
绑定成功时的返回值，与 FreeRTOS 标准相反，其中 0 表示失败！）。

 + 返回 -pdFREERTOS_ERRNO_EINVAL，表示套接字未被绑定，可能是 
   因为指定的端口号已被使用。

 + 返回 -pdFREERTOS_ERRNO_ECANCELED，表示调用 RTOS 任务未收到来自 
   IP RTOS 任务对绑定请求的响应。


**用法示例：** 

请参阅[ FreeRTOS-Plus-TCP 联网教程](../TCP_Networking_Tutorial_TCP_Client_and_Server)示例
页面，以及 [FreeRTOS_socket()](socket) API 文档页面的示例。

