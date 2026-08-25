---
title: "FreeRTOS_closesocket()"
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
BaseType_t FreeRTOS_closesocket( Socket_t xSocket );
```

Close a socket.
 
The function is named FreeRTOS\_closesocket() rather than simply FreeRTOS\_close() to avoid potential 
name space collisions with functions in FreeRTOS-Plus-IO.
 
A socket should be [shutdown](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/12-shutdown) gracefully before it is closed, and cannot be used after it 
has been closed.
 

**Parameters:** 

+ *xSocket*

  The handle of the socket being closed. The socket must have already been created 
  (see [FreeRTOS\_socket()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket)), and cannot be used after it has been closed.  


**Returns:** 

0 is always returned.
 
Although FreeRTOS-Plus-TCP does not [currently] use the return value in a meaningful way, the return 
value is included in the function prototype to ensure consistency with the expected standard Berkeley 
sockets API, and to ensure compatibility with future versions of FreeRTOS-Plus-TCP.
 

**Example usage:** 

```c
/* FreeRTOS-Plus-TCP sockets include. */  
#include "FreeRTOS_sockets.h"  
  
void aFunction( void )  
{  
Socket_t xSocket;  
  
    /* Create a socket. */  
    xSocket = FreeRTOS_socket( FREERTOS_AF_INET, FREERTOS_SOCK_STREAM, FREERTOS_IPPROTO_TCP );  
  
    if( xSocket != FREERTOS_INVALID_SOCKET )  
    {  
        /*  
         * The socket can now be used...  
         */  
  
         /* . . . */  
  
         /* Initialise a shutdown before closing the socket. */  
         FreeRTOS_shutdown( xSocket );  
  
        /* Wait for the socket to disconnect gracefully (indicated by FreeRTOS\_recv()  
           returning a FREERTOS\_EINVAL error) before closing the socket. */  
        while( FreeRTOS_recv( xSocket, pcBufferToTransmit, xTotalLengthToSend, 0 ) >= 0 )  
        {  
            /* Wait for shutdown to complete. If a receive block time is used then  
               this delay will not be necessary as FreeRTOS\_recv() will place the RTOS task  
               into the Blocked state anyway. */  
            [vTaskDelay](/Documentation/02-Kernel/04-API-references/02-Task-control/01-vTaskDelay)( pdTICKS_TO_MS( 250 ) );  
  
            /* Note - real applications should implement a timeout here, not just  
               loop forever. */  
        }  
  
         /* Close the socket again. */  
         FreeRTOS_closesocket( xSocket );  
    }  
}  
```
*Example use of the FreeRTOS_closesocket() API function*
