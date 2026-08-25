---
title: "FreeRTOS_select()"
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
BaseType_t FreeRTOS_select( SocketSet_t xSocketSet, TickType_t xBlockTimeTicks );
```

Block on a "socket set" until an event of interest occurs on a socket within the set. 
ipconfigSUPPORT\_SELECT\_FUNCTION must be set to 1 
in [FreeRTOSIPConfig.h](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigSUPPORT_SELECT_FUNCTION)
for FreeRTOS\_select() (and its associated functions) to be available.
 
*Socket Sets* allow an application RTOS task to block on multiple sockets simultaneously.
 
To use a socket set:
 
1. Create a socket set by calling [FreeRTOS\_CreateSocketSet()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/15-createsocketset). A socket set is 
   equivalent to the Berkeley sockets fd\_set type.

2. Add one or more sockets to the set using calls to FreeRTOS\_FD\_SET(). FreeRTOS\_FD\_SET() is 
   equivalent to the Berkeley sockets FD\_SET() macro.

3. Call FreeRTOS\_Select() to test the sockets in the set to see if any of the sockets have an event pending.

4. If FreeRTOS\_select() returns a non-zero value then check all sockets in the set using a call 
   to [FreeRTOS\_FD\_ISSET()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/18-FD_ISSET) to determine which events are pending.

A socket can only be a member of one set at any time.
 
The [FreeRTOS\_FD\_CLR()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/17-FD_CLR) API function removes a socket from a set.
 

**Parameters:** 


+ *xSocketSet*

  The socket set being tested.  


+ *xBlockTimeTicks*

  The maximum time, in ticks, that the calling RTOS task will remain in the Blocked state (with other 
  tasks executing) to wait for a member of the socket set to get an event.  


**Returns:** 

If xBlockTimeTicks expired before a socket in the socket set had an event, then zero is returned. Otherwise 
a non-zero value is returned. All sockets which belong to the socket set must be checked by 
calling [FreeRTOS\_FD\_ISSET()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/18-FD_ISSET)

If a socket in the set [receives a signal](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket), causing the task that was blocked 
on the socket to abort its read operation, then the call to FreeRTOS\_select() will return eSELECT\_INTR.
 

**Example usage:** 

```c
/* FreeRTOS includes. */  
#include "FreeRTOS.h"  
#include "task.h"  
#include "queue.h"  
  
/* FreeRTOS-Plus-TCP includes. */  
#include "FreeRTOS_IP.h"  
#include "FreeRTOS_Sockets.h"  
  
static void prvMultipleSocketRxTask( void *pvParameters )  
{  
SocketSet_t xFD_Set;  
BaseType_t xResult;  
Socket_t xSockets[2];  
struct freertos_sockaddr xAddress;  
uint32_t xClientLength = sizeof( struct freertos_sockaddr ), x;  
uint32_t ulReceivedValue = 0;  
int32_t lBytes;  
const TickType_t xRxBlockTime = 0;  
  
    /* Create the set of sockets that will be passed into FreeRTOS_select(). */  
    xFD_Set = FreeRTOS_CreateSocketSet();  
  
    /* Create two sockets to add to the set. */  
    for( x = 0; x < 2; x++ )  
    {  
        /* Create the socket. */  
        xSockets[x] = FreeRTOS_socket( FREERTOS_AF_INET,  
                                       FREERTOS_SOCK_DGRAM,  
                                       FREERTOS_IPPROTO_UDP );  
  
        /* Bind the socket to a port number 1000, 1001... */  
        xAddress.sin_port = FreeRTOS_htons( 1000 + x );  
        FreeRTOS_bind( xSockets[x], &xAddress, sizeof( struct freertos_sockaddr ) );  
  
        /* Once it has been tested that a socket has a eSELECT_READ  
           event, blocking on a read call is not necessary any more. Set the  
           Rx block time to 0. */  
        FreeRTOS_setsockopt( xSockets[x], 0, FREERTOS_SO_RCVTIMEO,  
                             &xRxBlockTime, sizeof( xRxBlockTime ) );  
  
        /* Add the created socket to the set for the READ event only. */  
        FreeRTOS_FD_SET( xSockets[x], xFD_Set, eSELECT_READ );  
    }  
  
    for( ;; )  
    {  
        /* Wait for any event within the socket set. */  
        xResult = FreeRTOS_select( xFD_Set, portMAX_DELAY );  
        if( xResult != 0 )  
        {  
            /* The return value should never be zero because FreeRTOS_select() was called  
               with an indefinite delay (assuming INCLUDE_vTaskSuspend is set to 1).  
               Now check each socket which belongs to the set if it had an event */  
  
            for( x = 0; x < 2; x++ )  
            {  
                if( FreeRTOS_FD_ISSET ( xSockets[x], xFD_Set ) )  
                {  
                    /* Read from the socket. */  
                    lBytes = FreeRTOS_recvfrom( xSockets[x], &( ulReceivedValue ), 
                                                sizeof( uint32_t ), 0, &xAddress,  
                                                &xClientLength );  
                    /* Process the received data here. */  
                }  
            }  
        }  
    }  
}  
```
*Example use of the FreeRTOS\_select() API function*
