---
title: FreeRTOS_FD_CLR()
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
void FreeRTOS_FD_CLR( Socket_t xSocket, SocketSet_t xSocketSet, BaseType_t xBitsToClear );
```

套接字集中的套接字具有多个相关联的相关事件位。设置相关事件位后， 
套接字会解除对 FreeRTOS_select() 调用的阻塞。相关事件位使用 
[FreeRTOS_FD_SET()](FD_SET) API 函数设置，使用 FreeRTOS_FD_CLR() 
API 函数清零。所有事件位均已清零，则该套接字会从套接字集中移除。

ipconfigSUPPORT_SELECT_FUNCTION 必须在 
[FreeRTOSIPConfig.h](../TCP_IP_Configuration#ipconfigSUPPORT_SELECT_FUNCTION) 中设为 1，FreeRTOS_FD_CLR()  
才可用。

每个套接字成员都有自己的事件位集，可以是以下值的 
按位或组合值：

+ eSELECT_READ

  对于正在读取数据的套接字，只要套接字中包含未读数据，eSELECT_READ 事件都将在套接字中处于挂起的状态 
  。  对于正在监听新连接的套接字， 
  每次接收到新连接时，eSELECT_READ 事件将被挂起。  

+ eSELECT_WRITE

  只要套接字有写入空间，eSELECT_WRITE 事件都将留在挂起状态中。  如果 TCP  
  套接字正主动连接到 pear，则在建立连接后， 
  会立即触发 eSELECT_WRITE 事件。  当 eSELECT_WRITE 事件被挂起后，就应将其禁用， 
  或者调用者应在套接字中写入足够的数据以填满传输缓冲区， 
  否则，挂起的 eSELECT_WRITE 事件将不会被清除。  

+ eSELECT_EXCEPT

  如果套接字断开连接，则 eSELECT_EXCEPT 事件会进入挂起状态。  


**参数：** 

+ *xSocket*

  具有一个已清零相关位或正从套接字集中移除相关位的套接字。  

+ *xSocketSet*

  套接字成员所属的套接字集。  

+ *xBitsToClear*

  应清零的位，使用 'eSELECT_ALL' 将所有位清零 
  并将套接字从套接字集中移除。  


**返回：** 

void


```c
/* FreeRTOS includes. */  
#include "FreeRTOS.h"  
#include "task.h"  
#include "queue.h"  
  
/* FreeRTOS-Plus-TCP includes. */  
#include "FreeRTOS_IP.h"  
#include "FreeRTOS_Sockets.h"  
  
void vConnectExample( )  
{  
Socket_t xSocket;  
struct freertos_sockaddr xEchoServerAddress;  
const TickType_t xZeroTimeOut = 0;  
SocketSet_t xSocketSet;  
  
    /* Create a TCP socket. */  
    xSocket = FreeRTOS_socket( FREERTOS_AF_INET, FREERTOS_SOCK_STREAM, FREERTOS_IPPROTO_TCP );  
  
    /* Create a socket set. */  
    xSocketSet = FreeRTOS_CreateSocketSet()( );  
  
    /* Make the socket a member of the set.  
       Only the WRITE event can unblock a call to select() */  
    FreeRTOS_FD_SET( xSocket, xSocketSet, eSELECT_WRITE );  
  
    /* When working with select(), time-outs on API's aren't necessary */  
    FreeRTOS_setsockopt( xSocket, 0, FREERTOS_SO_RCVTIMEO, &xZeroTimeOut, sizeof( xZeroTimeOut ) );  
    FreeRTOS_setsockopt( xSocket, 0, FREERTOS_SO_SNDTIMEO, &xZeroTimeOut, sizeof( xZeroTimeOut ) );  
  
    /* Fill in the peer's address */  
    xEchoServerAddress.sin_port = FreeRTOS_htons( echoECHO_PORT );  
    xEchoServerAddress.sin_addr = FreeRTOS_inet_addr_quick( configECHO_SERVER_ADDR0,  
                                                            configECHO_SERVER_ADDR1,  
                                                            configECHO_SERVER_ADDR2,  
                                                            configECHO_SERVER_ADDR3 );  
  
    /* Now initiate an active connect procedure to a peer. This call is non-blocking */  
    FreeRTOS_connect( xSocket, &xEchoServerAddress, sizeof( xEchoServerAddress ) );  
  
    /* Now block for at most 30 seconds. A successful connection will unblock  
       select() with a eSELECT_WRITE event */  
    if( FreeRTOS_select( xSocketSet, 30000 ) != 0 )  
    {  
        BaseType_t xMask = FreeRTOS_FD_ISSET ( xSocket, xSocketSet );  
        if( xMask != 0 )  
        {  
            /* Clear the WRITE event bit, it is not interesting any more */  
            FreeRTOS_FD_CLR( xSocket, xSocketSet, eSELECT_WRITE );  
  
            /* Set the READ event bit */  
            FreeRTOS_FD_SET( xSocket, xSocketSet, eSELECT_READ );  
        }  
    }  
}  
```
*FreeRTOS_FD_SET / FD_CLR / FD_ISSET() API 函数使用示例*

