---
title: FreeRTOS_sendto()
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
int32_t FreeRTOS_sendto( Socket_t xSocket,
                         const void *pvBuffer,
                         size_t xTotalDataLength,
                         uint32_t ulFlags,
                         const struct freertos_sockaddr *pxDestinationAddress,
                         socklen_t xDestinationAddressLength );
```

发送数据至 UDP 套接字（请参阅 [FreeRTOS_send()](send) 了解 TCP 相应内容）。该套接字必须是 
通过成功调用 [FreeRTOS_socket()](socket) 创建的。

此函数可以与标准调用语义或零拷贝调用语义一起使用：

* 标准 sendto() 语义

  数据从 pvBuffer 参数指向的地址 
  复制到 TCP/IP 堆栈内部分配的网络缓冲区。

  当 ulFlags 参数未设置 FREERTOS_ZERO_COPY 位时， 
  将使用标准 sendto() 语义。请参阅此页面底部的示例和本网站上提供的其他应用程序示例。

* 零拷贝 sendto() 语义

  应用程序写入器：

  1. 从 TCP/IP 堆栈获取缓冲区。
  2. 将要发送的数据写入从 TCP/IP 堆栈获取的缓冲区。
  3. 将指向（已完成的）缓冲区的指针用作 pvBuffer 参数。

  然后，TCP/IP 堆栈通过 TCP/IP 堆栈将同一缓冲区的引用传递给以太网驱动程序， 
  并在那里进行传输（通常在硬件允许的情况下通过 DMA 传输）。

  当 ulFlags 参数设置了 FREERTOS_ZERO_COPY 位时，将使用零拷贝 sendto() 语义 
  。请参阅此页面底部的示例和本网站上提供的其他应用程序示例 
  。

FreeRTOS_sendto() 具有可选超时。该超时默认为 
[ipconfigSOCK_DEFAULT_SEND_BLOCK_TIME](../TCP_IP_Configuration#ipconfigSOCK_DEFAULT_SEND_BLOCK_TIME)，
可使用 [FreeRTOS_setsockopt()](setsockopt) 进行修改。  如果发送操作无法立即排队发送字节， 
则调用 RTOS 任务将处于阻塞状态（以便其他任务可以执行）， 
直到字节排队发送或超时结束。如果出现以下情况， 
将发生超时：


* 由于使用了标准 sendto() 语义，TCP/IP 堆栈无法及时获取网络缓冲区 
  。或者

* 用于向 IP RTOS 任务发送消息的队列没有可用空间 
  （请参阅 FreeRTOSIPConfig.h 头文件中的 ipconfigEVENT_QUEUE_LENGTH 设置）。


如果 FreeRTOS_sendto() 在未[绑定端口号](bind)的套接字上被调用，并且 
在 FreeRTOSIPConfig. h 中将 ipconfigALLOW_SOCKET_SEND_WITHOUT_BIND 设置为 1，则 TCP/IP 堆栈 
会自动将套接字与私有地址范围内的端口号绑定。


FreeRTOS -Plus- TCP [当前]未使用所有函数参数。不使用的参数保留在函数原型中， 
以确保与预期的标准伯克利套接字 API 保持一致， 
并确保与 FreeRTOS-Plus-TCP 的未来版本兼容。


**参数：** 

+ *xSocket* 

  接收发送数据的套接字的句柄。套接字必须已成功创建， 
  （请参阅 [FreeRTOS_socket()](socket)）。  

+ *pvBuffer*

  如果使用的是标准调用语义（ulFlags 参数未设置 FREERTOS_ZERO_COPY 位）， 
  那么 pvBuffer 会指向传输数据的来源。FreeRTOS_sendto() 会将 
  pvBuffer 中的数据复制到 TCP/IP 堆栈中的网络缓冲区。如果使用的是零拷贝调用语义 
  （ulFlags 参数设置了 FREERTOS_ZERO_COPY 位），那么 pvBuffer 会指向 
  先前已从 TCP/IP 堆栈中获取的缓冲区，并已包含发送的数据。 
  TCP/IP 堆栈会控制该缓冲区，而不是从该缓冲区复制数据。请参阅 
  下面的使用示例部分以及本网站提供的应用示例。  

+ *xTotalDataLength*

  待发送的字节数。  

+ *ulFlags* 

  一组影响发送操作的逐位选项。  如果 ulFlags 设置了 FREERTOS_ZERO_COPY 位， 
  则函数将使用零拷贝语义，否则函数将使用标准 
  拷贝模式语义。请参阅上面 pvBuffer 参数的说明。  未来的 FreeRTOS-Plus-TCP 
  版本可能实现其他位。  

+ *pxDestinationAddress*

  指向 freertos_sockaddr 结构体的指针，该结构体包含目标 IP 地址和端口号 
  （数据发送到的套接字）。请参阅以下示例。  

+ *xDestinationAddressLength*

  目前未使用，但应设置为（结构体 freertos_sockaddr）的大小以确保未来的兼容性。  


**返回：** 

实际排队发送的字节数，如果发生错误或超时，则为 0。

请注意，由于 FreeRTOS 没有实现 errno， 
因此出现错误时的行为必然与 sendto() 函数不同，后者完全符合预期的伯克利
套接字行为。


**用法示例：** 

第一个示例使用标准调用语义向套接字发送数据（请参阅 
以下另一使用零拷贝调用语义的示例）。套接字作为函数参数传入， 
并假定已通过调用 [FreeRTOS_socket()](socket) 创建。如果 
在 FreeRTOSIPConfig. h 中将 ipconfigALLOW_SOCKET_SEND_WITHOUT_BIND 设置为 1， 
则也假定套接字已通过 [FreeRTOS_bind()](bind) 绑定到端口号上。

```c
/* FreeRTOS-Plus-TCP sockets include. */  
#include "FreeRTOS_sockets.h"  
  
void vStandardSendExample( Socket_t xSocket )  
{  
/* Note - the RTOS task stack must be big enough to hold this array!. */  
uint8_t ucBuffer[ 128 ];  
struct freertos_sockaddr xDestinationAddress;  
int32_t iReturned;  
  
    /* Fill in the destination address and port number, which in this case is  
       port 1024 on IP address 192.168.0.100. */  
    xDestinationAddress.sin_addr = FreeRTOS_inet_addr_quick( 192, 168, 0, 100 );  
    xDestinationAddress.sin_port = FreeRTOS_htons( 1024 );  
  
    /* The local buffer is filled with the data to be sent, in this case it is  
       just filled with 0xff. */  
    memset( ucBuffer, 0xff, 128 );  
  
    /* Send the buffer with ulFlags set to 0, so the FREERTOS_ZERO_COPY bit  
       is clear. */  
    iReturned = FreeRTOS_sendto(  
                                 /* The socket being send to. */  
                                 xSocket,  
                                 /* The data being sent. */  
                                 ucBuffer,  
                                 /* The length of the data being sent. */  
                                 128,  
                                 /* ulFlags with the FREERTOS_ZERO_COPY bit clear. */  
                                 0,  
                                 /* Where the data is being sent. */  
                                 &xDestinationAddress,  
                                 /* Not used but should be set as shown. */  
                                 sizeof( xDestinationAddress )  
                               );  
  
    if( iReturned == 128 )  
    {  
        /* The data was successfully queued for sending. 128 bytes will have  
           been copied out of ucBuffer and into a buffer inside the TCP/IP stack.  
           ucBuffer can be re-used now. */  
    }  
}  
```
*使用 FreeRTOS_sendto() 与标准（和零拷贝相反）调用语义的示例*

第二个示例使用零拷贝调用语义向套接字发送数据（请参阅
以上另一使用标准调用语义的示例）。套接字
被作为函数参数传入，并假定已经
通过调用 [FreeRTOS_socket()](socket) 创建。如果 ipconfigALLOW_SOCKET_SEND_WITHOUT_BIND 在
FreeRTOSIPConfig.h 中未设置为 1，那么套接字也被认为已经
使用 [FreeRTOS_bind()](bind) 绑定到端口号上。

```c
/* FreeRTOS-Plus-TCP sockets include. */  
#include "FreeRTOS_sockets.h"  
  
void vZeroCopySendExample( Socket_t xSocket )  
{  
struct freertos_sockaddr xDestinationAddress;  
uint8_t *pucUDPPayloadBuffer;  
int32_t iReturned;  
  
    /* Fill in the destination address and port number, which in this case is  
       port 1024 on IP address 192.168.0.100. */  
    xDestinationAddress.sin_addr = FreeRTOS_inet_addr_quick( 192, 168, 0, 100 );  
    xDestinationAddress.sin_port = FreeRTOS_htons( 1024 );  
  
    /* Obtain a buffer from the TCP/IP stack that is large enough to hold the data  
       being sent. Although the maximum amount of time to wait for a buffer is passed  
       into FreeRTOS_GetUDPPayloadBuffer() as portMAX_DELAY, the actual maximum time  
       will be capped to ipconfigMAX_SEND_BLOCK_TIME_TICKS (defined in  
       FreeRTOSIPConfig.h) */  
    pucUDPPayloadBuffer = ( uint8_t * ) FreeRTOS_GetUDPPayloadBuffer( 128,  
                                                                      portMAX_DELAY );  
    if( pucUDPPayloadBuffer != NULL )  
    {  
        /* Write the data being sent directly into the buffer obtained from the  
           IP stack. In this case the data is just set to 0xff. */  
        memset( pucUDPPayloadBuffer, 0xff, 128 );  
  
        /* Pass the buffer (by reference) into the TCP/IP stack using the zero 
           copy  semantics. Ensure to read the remaining source code comments 
           for information on managing the pucUDPPayloadBuffer pointer after 
           this call to  FreeRTOS_sendto(). */  
        iReturned = FreeRTOS_sendto(  
                                     /* The socket being sent to. */  
                                     xSocket,  
                                     /* The buffer that already contains the  
                                        data being sent. */ 
                                     &xBufferDescriptor,  
                                     /* The length of the data being send. */  
                                     128,  
                                     /* ulFlags with the FREERTOS_ZERO_COPY bit  
                                        set. */  
                                     FREERTOS_ZERO_COPY,  
                                     /* Where the data is being sent. */  
                                     &xDestinationAddress,  
                                     /* Not used but should be set as shown. */  
                                     sizeof( xDestinationAddress )  
                                    );  
  
        if( iReturned != 0 )  
        {  
            /* The buffer pointed to by pucUDPPayloadBuffer was successfully  
               passed (by reference) into the TCP/IP stack and is now queued 
               for sending. The TCP/IP stack is responsible for returning the 
               buffer after it has been sent, and pucUDPPayloadBuffer can be 
               used safely in another call to FreeRTOS_GetUDPPayloadBuffer(). */
        }  
        else  
        {  
            /* The buffer pointed to by pucUDPPayloadBuffer was not successfully  
               passed (by reference) to the TCP/IP stack. To prevent memory and 
               network  buffer leaks the buffer must be either reused or, as in 
               this case,  released back to the TCP/IP stack. */  
            FreeRTOS_ReleaseUDPPayloadBuffer( ( void * ) pucUDPPayloadBuffer );  
        }  
    }  
}  
```
*使用 FreeRTOS_sendto() 和零拷贝调用语义的示例*

