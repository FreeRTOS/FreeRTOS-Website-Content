---
title: FreeRTOS_recvfrom()
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
int32_t FreeRTOS_recvfrom( Socket_t xSocket,
                           void *pvBuffer,
                           size_t xBufferLength,
                           uint32_t ulFlags,
                           struct freertos_sockaddr *pxSourceAddress,
                           socklen_t *pxSourceAddressLength );
```

从 UDP 套接字接收数据（请参阅 [FreeRTOS_recv()](recv) 了解 TCP 相应内容）。套接字必须是 
通过成功调用 [FreeRTOS_socket()](socket) 创建的。

此函数可以与标准调用语义或零拷贝调用语义一起使用：

* 标准 recvfrom() 语义

  数据从 TCP/IP 堆栈内的网络缓冲区复制到 pvBuffer 
  参数指向的缓冲区。

  当 ulFlags 参数未设置 FREERTOS_ZERO_COPY 位时， 
  将使用标准 recvfrom() 语义。请参阅此页面底部的示例和本网站上提供的其他应用程序示例。

* 零拷贝 recvfrom() 语义

  应用程序写入器会从 TCP/IP 堆栈中接收到 
  对已包含接收数据的缓冲区的引用。不复制任何数据。

  当 ulFlags 参数的 FREERTOS_ZERO_COPY 位被设置时， 
  将使用零拷贝 recvfrom() 语义。请参阅此页面底部的示例和本网站上提供的其他应用程序示例 
  。

FreeRTOS_recvfrom() 具有可选超时。超时默认为 portMAX_DELAY， 
可通过 [FreeRTOS_setsockopt()](setsockopt) 进行修改。如果接收操作无法立即完成， 
因为套接字上没有排队等待接收的数据，那么调用 RTOS 任务将 
处于阻塞状态（以便其他任务可以执行），直到接收到数据或
超时到期。


FreeRTOS -Plus- TCP [当前]未使用所有函数参数。不使用的参数保留在函数原型中， 
以确保与预期的标准伯克利套接字 API 保持一致， 
并确保与 FreeRTOS-Plus-TCP 的未来版本兼容。


**参数：** 

+ *xSocket*

  从中读取数据的套接字的句柄。套接字必须已经 
  创建（请参阅 [FreeRTOS_socket()](socket)）。  


+ *pvBuffer*

  如果使用标准调用语义（ulFlags 参数未设置 FREERTOS_ZERO_COPY 位）， 
  则 pvBuffer 指向将接收数据复制到其中的缓冲区。  如果使用零拷贝调用语义 
  （ulFlags 参数未设置 FREERTOS_ZERO_COPY 位）， 
  则 *pvBuffer 将（通过 FreeRTOS_recvfrom()）被设置为指向已接收数据的缓冲区。 
  pvBuffer 用于将接收到的数据引用传出 FreeRTOS_recvfrom()， 
  而无需复制任何数据。  此页面底部的示例和本网站上提供的其他应用程序示例 
  演示了 FreeRTOS_recvfrom() 和标准调用语义以及 
  零拷贝调用语义一起使用。  

+ *xBufferLength*

  如果使用标准调用语义（ulFlags 参数未设置 FREERTOS_ZERO_COPY 位）， 
  则 xBufferLength 必须设置为 pvBuffer 参数指向的缓冲区的大小 
  （单位：字节）。  如果使用零拷贝调用语义（ulFlasg 参数未设置 
  FREERTOS_ZERO_COPY 位）则 pvBuffer 不指向缓冲区，xBufferLength 也不会被使用。  

+ *ulFlags*

  影响接收操作的一组按位选项。  如果 ulFlags 设置了 FREERTOS_ZERO_COPY 位， 
  则函数将使用零拷贝语义，否则函数将使用传统的 
  拷贝模式语义。请参阅上面 pvBuffer 参数的说明。  未来的 FreeRTOS-Plus-TCP 
  版本可能实现其他位。  

+ *pxSourceAddress*

  指向 freertos_sockaddr 结构体的指针，该结构体将（由 FreeRTOS_recvrom() 设置） 
  包含发送刚刚接收到的数据的套接字的 IP 地址和端口号。请参阅以下示例。  

+ *pxSourceAddressLength* 

  目前未使用，但应设置为（结构体 freertos_sockaddr）的大小以确保未来的兼容性。  


**返回：** 

+ 如果在配置的块时间到期之前未接收到任何字节，则返回 -pdFREERTOS_ERRNO_EWOULDBLOCK 
  。

+ 如果套接字未绑定到端口号，则返回 -pdFREERTOS_ERRNO_EINVAL。

+ 如果[套接字接收到信号](FreeRTOS_SignalSocket)，导致读取操作中止， 
  则返回 -pdFREERTOS_ERRNO_EINTR。

+ 如果成功接收数据，则返回接收到的字节数。


**用法示例：** 

第一个示例使用标准调用语义从套接字接收数据 
（另一个使用零拷贝调用语义的示例见下文）。套接字作为函数参数传入， 
假定已通过调用 [FreeRTOS_socket()](socket) 创建， 
并使用 [FreeRTOS_bind()](bind) 调用绑定到一个地址。

```c
/* FreeRTOS-Plus-TCP sockets include. */  
#include "FreeRTOS_sockets.h"  
  
void vStandardReceiveExample( Socket_t xSocket )  
{  
/* Note - the RTOS task stack must be big enough to hold this array!. */  
uint8_t ucBuffer[ 128 ];  
int8_t cIPAddressString[ 16 ];  
struct freertos_sockaddr xSourceAddress;  
socklen_t xAddressLength = sizeof(xSourceAddress);  
int32_t iReturned;   
  
    /* Receive into the buffer with ulFlags set to 0, so the FREERTOS_ZERO_COPY bit  
       is clear. */  
    iReturned = FreeRTOS_recvfrom(  
                                    /* The socket data is being received on. */  
                                    xSocket,  
                                    /* The buffer into which received data will 
                                       be  copied. */  
                                    ucBuffer,  
                                    /* The length of the buffer into which data 
                                       will be  copied. */  
                                    128,  
                                    /* ulFlags with the FREERTOS_ZERO_COPY bit clear. */ 
                                    0,  
                                    /* Will get set to the source of the received data. */  
                                    &xSourceAddress,  
                                    /* Not used but should be set as shown. */  
                                    &xAddressLength  
                               );  
  
    if( iReturned > 0 )  
    {  
        /* Data was received from the socket. Prepare the IP address for  
           printing to the console by converting it to a string. */  
        FreeRTOS_inet_ntoa( xSourceAddress.sin_addr, ( char * ) cIPAddressString );  
  
        /* Print out details of the data source. */  
        printf( "Received %d bytes from IP address %s port number %drn",  
                    iReturned, /* The number of bytes received. */  
                    cIPAddressString, /* The IP address that sent the data. */  
                    FreeRTOS_ntohs( xSourceAddress.sin_port ) ); /* The source port. */  
    }  
}  
```
*使用 FreeRTOS_recvfrom() 与标准（和零拷贝相反）调用语义的示例*


第二个示例从使用零拷贝调用语义的套接字接收数据 
（使用标准调用语义的示例见上文）。套接字作为函数参数传入， 
假定已通过调用 [FreeRTOS_socket()](socket) 创建， 
并使用 [FreeRTOS_bind()](bind) 绑定到一个端口号。

```c
/* FreeRTOS-Plus-TCP sockets include. */  
#include "FreeRTOS_sockets.h"  
  
void vZeroCopyReceiveExample( Socket_t xSocket )  
{  
struct freertos_sockaddr xSourceAddress;  
socklen_t xAddressLength = sizeof(xSourceAddress);  
uint8_t *pucReceivedUDPPayload;  
int32_t iReturned;  
  
    /* Receive using the zero copy semantics. The address of the  
       pucReceivedUDPPayload pointer is passed in the pvBuffer parameter. */  
    iReturned = FreeRTOS_recvfrom(  
                                   /* The socket being received from. */  
                                      xSocket,  
                                   /* pucReceivedUDPPayload will get  
                                      set to points to the received data. */ 
                                   &pucReceivedUDPPayload,  
                                   /* Ignored because the pvBuffer parameter  
                                      does not point to a buffer. */  
                                   0,  
                                   /* ulFlags with the FREERTOS_ZERO_COPY bit set. */
                                   FREERTOS_ZERO_COPY,  
                                   /* Will get set to the source of the received  
                                      data. */  
                                   &xSourceAddress,  
                                   /* Not used but should be set as shown. */  
                                   &xAddressLength  
                                 );  
  
    if( iReturned > 0 )  
    {  
        /* Data was received from the socket. Convert the IP address to a  
           string. */  
        FreeRTOS_inet_ntoa( xSourceAddress.sin_addr, ( char * ) cIPAddressString );  
  
        /* Print out details of the data source. */  
        printf( "Received %d bytes from IP address %s port number %drn",  
                    iReturned, /* The number of bytes received. */  
                    cIPAddressString, /* The IP address that sent the data. */  
                    FreeRTOS_ntohs( xSourceAddress.sin_port ) ); /* The source port. */  
  
        /* pucReceivedUDPPayload now points to the received data. For  
           example, *pucReceivedUDPPayload (or pucReceivedUDPPayload[ 0 ]) is the first  
           received byte. *(pucReceivedUDPPayload + 1 ) (or pucReceivedUDPPayload[ 1 ])  
           is the second received byte, etc.  
  
           The application writer is now responsible for the buffer. To prevent  
           memory and network buffer leaks the buffer *must* be returned to the IP  
           stack when it is no longer required. The following call is used to  
           return the buffer. */  
        FreeRTOS_ReleaseUDPPayloadBuffer( ( void * ) pucReceivedUDPPayload );  
    }  
}  
```
*使用 FreeRTOS_recvfrom() 和零拷贝调用语义的示例*

