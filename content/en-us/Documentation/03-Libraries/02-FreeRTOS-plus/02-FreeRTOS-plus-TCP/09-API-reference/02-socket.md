---
title: "FreeRTOS_socket()"
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
Socket_t FreeRTOS_socket( BaseType_t xDomain, BaseType_t xType, BaseType_t xProtocol );
```

Create a TCP or UDP [socket](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket).
 
See the [FreeRTOS-Plus-TCP networking tutorial](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial) for more information on 
using both TCP and UDP sockets.
 

**Parameters:** 


+ *xDomain*

   Must be set to FREERTOS\_AF\_INET.    

+ *xType*

  Set to FREERTOS\_SOCK\_STREAM to create a [TCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/10-TCP) socket. Set to FREERTOS\_SOCK\_DGRAM 
  to create a [UDP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/09-UDP) socket. No other values are valid.

+ *xProtocol*

   Set to FREERTOS\_IPPROTO\_TCP to create a TCP socket. Set to FREERTOS\_IPPROTO\_UDP to create a UDP 
   socket. No other values are valid.    


**Returns:** 

If a socket is created successfully, then the socket handle is returned. If there is 
insufficient [FreeRTOS heap memory](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) available for the socket to be created then 
FREERTOS\_INVALID\_SOCKET is returned.
 

**Example usage:** 

The following code snippets show how to create a UDP and TCP socket respectively.
 

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
*Example use of the FreeRTOS\_socket() API function to create a UDP socket*


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
*Example use of the FreeRTOS\_socket() API function to create a TCP socket*
