---
title: "FreeRTOS_FD_CLR()"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-TCP API Reference](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS\_sockets.h

```c
void FreeRTOS_FD_CLR( Socket_t xSocket, SocketSet_t xSocketSet, BaseType_t xBitsToClear );
```

Sockets in a socket set have a number of associated event bits of interest. An event bit of interest 
becoming set will cause the socket to unblock a call to FreeRTOS\_select(). Event bits of interest are 
set using the [FreeRTOS\_FD\_SET()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/16-FD_SET) API function, and cleared using the FreeRTOS\_FD\_CLR() 
API function. If all the event bits are clear then the socket will be removed from the socket set.
 
ipconfigSUPPORT\_SELECT\_FUNCTION must be set to 1 
in [FreeRTOSIPConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigSUPPORT_SELECT_FUNCTION) for FreeRTOS\_FD\_CLR() 
to be available.
 
Each socket member has its own set of event bits, which can be a bitwise OR combination of the following 
values:
 
+ eSELECT\_READ

  For a socket that is reading data, the eSELECT\_READ event will be pending in a socket as long as 
  the socket contains unread data.  For a socket that is listening for new connections, the eSELECT\_READ 
  event will be pended each time a new connection is received.  

+ eSELECT\_WRITE

  The eSELECT\_WRITE event will remain pending as long as the socket has space for writing.  If a TCP 
  socket is actively connecting to a pear the eSELECT\_WRITE event will be triggered as soon as the 
  connection is established.  One the eSELECT\_WRITE event has been pended it should either be disabled, 
  or the caller should write enough data to the socket so as to completely fill up the transmit buffer - 
  otherwise the pending eSELECT\_WRITE event will not be cleared.  

+ eSELECT\_EXCEPT

  The eSELECT\_EXCEPT event will become pending if the socket gets disconnected.  


**Parameters:** 

+ *xSocket*

  The socket having a bit of interest cleared or being removed from the socket set.  

+ *xSocketSet*

  The socket set the socket is a member of.  

+ *xBitsToClear*

  The bits which should be cleared, use 'eSELECT\_ALL' to clear all bits and remove the socket from 
  the set.  


**Returns:** 

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
       select() with a eSELECT\_WRITE event */  
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
*Example use of the FreeRTOS\_FD\_SET / FD\_CLR / FD\_ISSET() API functions*
