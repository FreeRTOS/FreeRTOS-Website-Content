---
title: FreeRTOS_inet_addr_quick()
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
uint32_t FreeRTOS_inet_addr_quick( uint8_t ucOctet1, uint8_t ucOctet2,
```

FreeRTOS_inet_addr_quick() 是一个宏，能将
以四个分开的数字八位组表达的 IP 地址（例如 192, 168, 0, 100）转换为
按网络字节顺序表示的 32 位数字的 IP 地址。

[FreeRTOS_inet_addr()](inet_addr) 函数可将以点分十进制表示的 IP 地址
（例如 "192.168.0.100"）转换为以网络字节顺序表示的 32 位 IP 地址。

FreeRTOS_inet_addr_quick() 因体积更小且执行速度更快而成为首选方法。 
之所以提供 FreeRTOS_inet_addr()，是因为该方法符合预期的 Berkeley 套接字函数原型。


**参数：** 

+ *ucOctet1*

  四个八位组 IP 地址中的第一个八位组。  

+ *ucOctet2*

  四个八位组 IP 地址中的第二个八位组。  

+ *ucOctet3*

  四个八位组 IP 地址中的第三个八位组。  

+ *ucOctet4*

  四个八位组 IP 地址中的第四个八位组。  


**返回：** 

由四个参数以网络字节顺序表示为单个 32 位数字的 IP 地址。


**用法示例：** 

该示例向 IP 地址为 192.168.0.100 的端口 5000 发送了一个字符串，其中使用 FreeRTOS_inet_addr_quick() 
将 IP 地址从单个八位组转换为所需的 32 位格式的字符串。套接字 
作为函数参数传入，并假定已 
通过调用 [FreeRTOS_socket()](socket) 来创建。如果 ipconfigALLOW_SOCKET_SEND_WITHOUT_BIND 在
FreeRTOSIPConfig.h 中未设置为 1，则套接字也假定为 
已通过 [FreeRTOS_bind()](bind) 与端口号绑定。


```c
/* FreeRTOS-Plus-TCP sockets include. */  
#include "FreeRTOS_sockets.h"  
  
void aFunction( Socket_t xSocket )  
{  
struct freertos_sockaddr xDestinationAddress;  
const int8_t *pcMessageToSend = "String being sent";  
  
    /* Generate the destination address. */  
    xDestinationAddress.sin_addr = FreeRTOS_inet_addr_quick( 192, 168, 0, 100 );  
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

