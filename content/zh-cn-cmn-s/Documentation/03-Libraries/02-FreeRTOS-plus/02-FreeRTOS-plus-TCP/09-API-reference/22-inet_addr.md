---
title: FreeRTOS_inet_addr()
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
uint32_t FreeRTOS_inet_addr( const uint8_t * pucIPAddress );
```

FreeRTOS_inet_addr() 函数可将以点分十进制表示的 IP 地址
（例如 "192.168.0.100"）转换为
以网络字节顺序表示的 32 位 IP 地址。

[FreeRTOS_inet_addr_quick()](inet_addr_quick)是一个宏， 
能将以四个独立数字八位字节（如 192、168、0、100）表示的 IP 地址转换为 
以网络字节顺序表示的 32 位数字的 IP 地址。

FreeRTOS_inet_addr_quick() 是首选方法，因为它体积更小，执行速度更快。 
提供 FreeRTOS_inet_addr() 是因为它符合预期的伯克利套接字函数原型。

ipconfigINCLUDE_FULL_INET_ADDR 必须在 FreeRTOSIPConfig.h for FreeRTOS_inet_addr() 中 
设置为 1 才可用。FreeRTOS_inet_addr_quick() 始终可用。


**参数：** 

+ *pucIPAddress*

  指向一个字符串的指针，该字符串包含转换为十进制点格式的 IP 地址。  


**返回：** 

如果 pucIPAddress 参数指向的字符串格式有效， 
那么将返回按网络字节顺序表示为 32 位数字的相同 IP 地址。在所有其他情况下，返回 0。


**用法示例：** 

该示例向 IP 地址为 192.168.0.100 的端口 5000 发送了一个字符串，其中使用 FreeRTOS_inet_addr 
将 IP 地址从字符串转换为必要的 32 位格式。套接字作为函数参数传入， 
并假定已通过调用 
[FreeRTOS_socket()](socket) 创建。如果 ipconfigALLOW_SOCKET_SEND_WITHOUT_BIND 在
FreeRTOSIPConfig.h 中未设置为 1，则套接字也假定为已 
使用 [FreeRTOS_bind()](bind) 与端口号绑定。


```c
/* FreeRTOS-Plus-TCP sockets include. */  
#include "FreeRTOS_sockets.h"  
  
void aFunction( Socket_t xSocket )  
{  
struct freertos_sockaddr xDestinationAddress;  
const int8_t *pcMessageToSend = "String being sent";  
  
    /* Generate the destination address. */  
    xDestinationAddress.sin_addr = FreeRTOS_inet_addr( "192.168.0.100" );  
    xDestinationAddress.sin_port = FreeRTOS_htons( 5000 );  
  
    /* Send the message. */  
    iReturned = FreeRTOS_sendto(  
                                    /* The socket being send to. */  
                                    xSocket,  
                                    /* The data being sent. */  
                                    pcMessageToSend,  
                                    /* The length of the data being sent. */  
                                    strlen( pcMessageToSend ),  
                                    /* ulFlags with the FREERTOS_ZERO_COPY bit clear. */  
                                    0,  
                                    /* Where the data is being sent. */  
                                    &xDestinationAddress,  
                                    /* Not used but should be set as shown. */  
                                    sizeof( xDestinationAddress )  
                               );  
}  
```
*FreeRTOS_inet_addr_quick() API 函数用法示例*

