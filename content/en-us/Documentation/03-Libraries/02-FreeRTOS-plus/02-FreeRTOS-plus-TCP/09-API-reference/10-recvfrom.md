---
title: "FreeRTOS_recvfrom()"
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
int32_t FreeRTOS_recvfrom( Socket_t xSocket,
                           void *pvBuffer,
                           size_t xBufferLength,
                           uint32_t ulFlags,
                           struct freertos_sockaddr *pxSourceAddress,
                           socklen_t *pxSourceAddressLength );
```

Receive data from a UDP socket (see [FreeRTOS\_recv()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/09-recv) for the TCP equivalent). The socket must 
have already been created by a successful call to [FreeRTOS\_socket()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket).
 
This function can be used with standard calling semantics, or zero copy calling semantics:
 
* Standard recvfrom() semantics
 
  Data is copied from a network buffer inside the TCP/IP stack into the buffer pointed to by the pvBuffer 
  parameter.
 
  The standard recvfrom() semantics are used when the ulFlags parameter does not have the FREERTOS\_ZERO\_COPY 
  bit set. See the example at the bottom of this page, and other application examples provided on this website.

* Zero copy recvfrom() semantics
 
  The application writer receives from the TCP/IP stack a reference to the buffer that already contains 
  the received data. No data is copied.
 
  The zero copy recvfrom() semantics are used when the ulFlags parameter has the FREERTOS\_ZERO\_COPY 
  bit set. See the examples at the bottom of this page, and other application examples provided on this 
  website.

FreeRTOS\_recvfrom() has an optional timeout. The timeout defaults to portMAX\_DELAY and is modified 
using [FreeRTOS\_setsockopt()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/11-setsockopt). If the receive operation cannot complete immediately 
because there is no data queued on the socket to receive then the calling RTOS task will be held in 
the Blocked state (so that other tasks can execute) until either data has been received, or the
timeout expires.
 

FreeRTOS-Plus-TCP does not [currently] use all the function parameters. The parameters that are not used 
are retained in the function's prototype to ensure consistency with the expected standard Berkeley sockets 
API, and to ensure compatibility with future versions of FreeRTOS-Plus-TCP.
 

**Parameters:** 

+ *xSocket*

  The handle of the socket from which data is being read. The socket must have already been 
  created (see [FreeRTOS\_socket()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket)).  


+ *pvBuffer*

  If the standard calling semantics are used (the ulFlags parameter does not have the FREERTOS\_ZERO\_COPY 
  bit set) then pvBuffer points to the buffer into which received data will be copied.  If the zero copy 
  calling semantics are used (the ulFlags parameter does have the FREERTOS\_ZERO\_COPY bit set) 
  then *pvBuffer will be set (by FreeRTOS\_recvfrom()) to point to the buffer that already holds the 
  received data. pvBuffer is used to pass a reference to the received data out of FreeRTOS\_recvfrom() 
  without any data being copied.  The example at the bottom of this page, and other application examples 
  provided on this website, demonstrate FreeRTOS\_recvfrom() being used with both the standard and zero 
  copy calling semantics.  

+ *xBufferLength*

  If the standard calling semantics are used (the ulFlags parameter does not have the FREERTOS\_ZERO\_COPY 
  bit set) then xBufferLength must be set to the size in bytes of the buffer pointed to by the pvBuffer 
  parameter.  If the zero copy calling semantics are used (the ulFlasg parameter does not have the 
  FREERTOS\_ZERO\_COPY bit set) then pvBuffer does not point to a buffer and xBufferLength is not used.  

+ *ulFlags*

  A bitwise set of options that affect the receive operation.  If ulFlags has the FREERTOS\_ZERO\_COPY 
  bit set, then the function will use the zero copy semantics, otherwise the function will use the traditional 
  copy mode semantics. See the description of the pvBuffer parameter above.  Future FreeRTOS-Plus-TCP 
  versions may implement other bits.  

+ *pxSourceAddress*

  A pointer to a freertos\_sockaddr structure that will be set (by FreeRTOS\_recvrom()) to contain 
  the IP address and port number of the socket that sent the data just received. See the example below.  

+ *pxSourceAddressLength* 

  Not currently used, but should be set to sizeof( struct freertos\_sockaddr ) to ensure future compatibility.  


**Returns:** 

+ If no bytes are received before the configured block time expires then -pdFREERTOS\_ERRNO\_EWOULDBLOCK 
  is returned.
 
+ If the socket is not bound to a port number then -pdFREERTOS\_ERRNO\_EINVAL is returned.
 
+ If the [socket received a signal](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket), causing the read operation to be aborted, 
  then -pdFREERTOS\_ERRNO\_EINTR is returned.
 
+ If data is successfully received then the number of bytes received is returned.
 

**Example usage:** 

The first example receives from a socket using the standard calling semantics (see below for another 
example that uses the zero copy calling semantics). The socket is passed in as the function parameter, 
and is assumed to have already been created using a call to [FreeRTOS\_socket()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket), and bound 
to an address using a call to [FreeRTOS\_bind()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/03-bind)

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
  
    /* Receive into the buffer with ulFlags set to 0, so the FREERTOS\_ZERO\_COPY bit  
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
                                    /* ulFlags with the FREERTOS\_ZERO\_COPY bit clear. */ 
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
*Example using FreeRTOS_recvfrom() with the standard (as opposed to zero copy) calling semantics*


This second example received from a socket using the zero copy calling semantics (see above for an example 
that uses the standard calling semantics). The socket is passed in as the function parameter, and is 
assumed to have already been created using a call to [FreeRTOS\_socket()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket), and bound to a 
port number using [FreeRTOS\_bind()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/03-bind).

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
                                   /* ulFlags with the FREERTOS\_ZERO\_COPY bit set. */
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
*Example using FreeRTOS_recvfrom() with the zero copy calling semantics*
