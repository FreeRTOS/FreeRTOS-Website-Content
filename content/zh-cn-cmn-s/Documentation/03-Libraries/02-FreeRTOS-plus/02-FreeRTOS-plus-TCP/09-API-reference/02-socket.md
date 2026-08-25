---
title: FreeRTOS_socket()
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
Socket_t FreeRTOS_socket( BaseType_t xDomain, BaseType_t xType, BaseType_t xProtocol );
```

创建 TCP 或 UDP [套接字](../socket)。

请参阅 [FreeRTOS-Plus-TCP 网络教程](../TCP_Networking_Tutorial)，了解有关 
使用 TCP 和 UDP 套接字的更多信息。


**参数：** 


+ *xDomain*

   必须设置为 FREERTOS_AF_INET。    

+ *xType*

  设置为 FREERTOS_SOCK_STREAM，以创建 [TCP](../TCP) 套接字。设置为 FREERTOS_SOCK_DGRAM， 
  以创建 [UDP](../UDP) 套接字。其他值均无效。

+ *xProtocol*

   设置为 FREERTOS_IPPROTO_TCP，以创建 TCP 套接字。设置为 FREERTOS_IPPROTO_UDP，以创建 UDP 
   套接字。其他值均无效。    


**返回：** 

如果成功创建套接字，则返回套接字句柄。如果 
没有足够的 [FreeRTOS 堆内存](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)来创建套接字， 
则返回 FREERTOS_INVALID_SOCKET。


**用法示例：** 

以下代码片段分别展示了如何创建 UDP 和 TCP 套接字。


```c
/* FreeRTOS-Plus-TCP sockets include. */  
#include "FreeRTOS_sockets.h"  
  
void aFunction( void )  
{  
/* Variable to hold the created socket. */  
Socket_t xSocket;  
struct freertos_sockaddr xBindAddress;  
  
    /* Create a **UDP** socket. */  
    xSocket = FreeRTOS_socket( FREERTOS_AF_INET,  
                               FREERTOS_SOCK_DGRAM,  
                               FREERTOS_IPPROTO_UDP );  
  
    /* Check the socket was created successfully. */  
    if( xSocket != FREERTOS_INVALID_SOCKET )  
    {  
        /* The socket was created successfully and can now be used to send data  
           using the FreeRTOS_sendto() API function. Sending to a socket that has  
           not first been bound will result in the socket being automatically bound  
           to a port number. Use FreeRTOS_bind() to bind the socket to a  
           specific port number. This example binds the socket to port 9999. The  
           port number is specified in network byte order, so FreeRTOS_htons() is  
           used. */  
        xBindAddress.sin_port = FreeRTOS_htons( 9999 );  
        if( FreeRTOS_bind( xSocket, &xBindAddress, sizeof( &xBindAddress ) ) == 0 )  
        {  
            /* The bind was successful. */  
        }  
    }  
    else  
    {  
        /* There was insufficient FreeRTOS heap memory available for the socket  
           to be created. */  
    }  
}  
```
*使用 FreeRTOS_socket() API 函数创建 UDP 套接字的示例*


```c
/* FreeRTOS-Plus-TCP sockets include. */  
#include "FreeRTOS_sockets.h"  
  
void aFunction( void )  
{  
/* Variable to hold the created socket. */  
Socket_t xSocket;  
struct freertos_sockaddr xBindAddress;  
  
    /* Create a **TCP** socket. */  
    xSocket = FreeRTOS_socket( FREERTOS_AF_INET,  
                               FREERTOS_SOCK_STREAM,  
                               FREERTOS_IPPROTO_TCP );  
  
    /* Check the socket was created successfully. */  
    if( xSocket != FREERTOS_INVALID_SOCKET )  
    {  
        /* The socket was created successfully and can now be used to connect to  
           a remote socket using FreeRTOS_connect(), before sending data using  
           FreeRTOS_send()). Alternatively the socket can be bound to a port using  
           FreeRTOS_bind(), before listening for incoming connections using  
           FreeRTOS_listen(). */  
    }  
    else  
    {  
        /* There was insufficient FreeRTOS heap memory available for the socket  
           to be created. */  
    }  
}  
```
*使用 FreeRTOS_socket() API 函数创建 TCP 套接字的示例*

