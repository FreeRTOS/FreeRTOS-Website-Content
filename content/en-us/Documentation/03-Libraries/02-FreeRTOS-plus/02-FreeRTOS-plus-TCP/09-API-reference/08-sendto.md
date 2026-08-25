---
title: "FreeRTOS_sendto()"
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
int32_t FreeRTOS_sendto( Socket_t xSocket,
                         const void *pvBuffer,
                         size_t xTotalDataLength,
                         uint32_t ulFlags,
                         const struct freertos_sockaddr *pxDestinationAddress,
                         socklen_t xDestinationAddressLength );
```

Send data to a UDP socket (see [FreeRTOS\_send()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/07-send) for the TCP equivalent). The socket must have 
already been created by a successful call to [FreeRTOS\_socket()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket).
 
This function can be used with standard calling semantics, or zero copy calling semantics:
 
* Standard sendto() semantics
 
  Data is copied from the address pointed to by the pvBuffer parameter into a network buffer allocated 
  internally by the TCP/IP stack.
 
  The standard sendto() semantics are used when the ulFlags parameter does not have the FREERTOS\_ZERO\_COPY 
  bit set. See the example at the bottom of this page, and other application examples provided on this website.

* Zero copy sendto() semantics
 
  The application writer:

  1. Obtains a buffer from the TCP/IP stack.
  2. Writes the data to be sent into the buffer obtained from the TCP/IP stack.
  3. Uses a pointer to the (already complete) buffer as the pvBuffer parameter.

  The TCP/IP stack then passes a reference to the same buffer through the TCP/IP stack to the Ethernet 
  driver, where it is transmitted (normally by DMA where the hardware permits).
 
  The zero copy sendto() semantics are used when the ulFlags parameter has the FREERTOS\_ZERO\_COPY bit 
  set. See the examples at the bottom of this page, and other application examples provided on this 
  website.

FreeRTOS\_sendto() has an optional timeout. The timeout defaults 
to [ipconfigSOCK\_DEFAULT\_SEND\_BLOCK\_TIME](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigSOCK_DEFAULT_SEND_BLOCK_TIME),
and is modified using [FreeRTOS\_setsockopt()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/11-setsockopt).  If the send operation cannot queue the 
bytes for transmission immediately then the calling RTOS task will be held in the Blocked state (so that 
other tasks can execute) until either the bytes can be queued for sending, or the timeout expires. A timeout 
will occur if:
 

* The standard sendto() semantics are used, and the TCP/IP stack was not able to obtain a network buffer 
  in time. Or,

* No space became available on the queue used to send messages to the IP RTOS task (see the 
  ipconfigEVENT\_QUEUE\_LENGTH setting in the FreeRTOSIPConfig.h header file).


If FreeRTOS\_sendto() is called on a socket that is not [bound to a port](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/03-bind) number, and the value 
of ipconfigALLOW\_SOCKET\_SEND\_WITHOUT\_BIND is set to 1 in FreeRTOSIPConfig.h, then the TCP/IP stack 
will automatically bind the socket to a port number from the private address range.
 

FreeRTOS-Plus-TCP does not [currently] use all the function parameters. The parameters that are not used 
are retained in the function's prototype to ensure consistency with the expected standard Berkeley sockets 
API, and to ensure compatibility with future versions of FreeRTOS-Plus-TCP.
 

**Parameters:** 

+ *xSocket* 

  The handle of the socket to which data is being sent. The socket must have already been created 
  (see [FreeRTOS\_socket()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket)).  

+ *pvBuffer*

  If the standard calling semantics are being used (the ulFlags parameter does not have the FREERTOS\_ZERO\_COPY 
  bit set) then pvBuffer points to the source of the data being transmitted. FreeRTOS\_sendto() will copy 
  data from pvBuffer into a network buffer inside the TCP/IP stack. If the zero copy calling semantics 
  are being sued (the ulFlags parameter does have the FREERTOS\_ZERO\_COPY bit set) then pvBuffer points 
  to a buffer that was previously obtained from the TCP/IP stack and already contains the data being 
  sent. the TCP/IP stack will take control of the buffer rather than copy data out of the buffer. See 
  the example usage section below, and the application examples provided on this website.  

+ *xTotalDataLength*

  The number of bytes to send.  

+ *ulFlags* 

  A bitwise set of options that affect the send operation.  If ulFlags has the FREERTOS\_ZERO\_COPY 
  bit set, then the function will use the zero copy semantics, otherwise the function will use the standard 
  copy mode semantics. See the description of the pvBuffer parameter above.  Future FreeRTOS-Plus-TCP 
  versions may implement other bits.  

+ *pxDestinationAddress*

  A pointer to a freertos\_sockaddr structure that contains the destination IP address and port number 
  (the socket the data is being sent to). See the example below.  

+ *xDestinationAddressLength*

  Not currently used, but should be set to sizeof( struct freertos\_sockaddr ) to ensure future compatibility.  


**Returns:** 

The number of bytes that were actually queue for sending, which will be 0 if an error or timeout occurred.
 
Note that, because FreeRTOS does not implement errno, the behaviour in the presence of an error is 
necessarily different to that of sendto() functions that are fully compliant with the expected Berkeley
sockets behaviour.
 

**Example usage:** 

The first example sends to a socket using the standard calling semantics (see below for another example 
that uses the zero copy calling semantics). The socket is passed in as the function parameter, and is 
assumed to have already been created using a call to [FreeRTOS\_socket()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket). If 
ipconfigALLOW\_SOCKET\_SEND\_WITHOUT\_BIND is not set to 1 in FreeRTOSIPConfig.h, then the socket is 
also assumed to have been bound to a port number using [FreeRTOS\_bind()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/03-bind).

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
    memset( &xDestinationAddress, 0, sizeof(xDestinationAddress) );
    xDestinationAddress.sin_address.ulIP_IPv4 = FreeRTOS_inet_addr_quick( 192, 168, 0, 100 );
    xDestinationAddress.sin_port = FreeRTOS_htons( 1024 );  
    xDestinationAddress.sin_family = FREERTOS_AF_INET4;
 
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
*Example using FreeRTOS_sendto() with the standard (as opposed to zero copy) calling semantics*

This second example sends to a socket using the zero copy calling semantics (see
above for an example that uses the standard calling semantics). The
socket is passed in as the function parameter, and is assumed to have already
been created using a call to [FreeRTOS\_socket()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket). If ipconfigALLOW\_SOCKET\_SEND\_WITHOUT\_BIND
is not set to 1 in FreeRTOSIPConfig.h, then the socket is also assumed to have been
bound to a port number using [FreeRTOS\_bind()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/03-bind).

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
    memset( &xDestinationAddress, 0, sizeof(xDestinationAddress) );
    xDestinationAddress.sin_address.ulIP_IPv4 = FreeRTOS_inet_addr_quick( 192, 168, 0, 100 );
    xDestinationAddress.sin_port = FreeRTOS_htons( 1024 );  
    xDestinationAddress.sin_family = FREERTOS_AF_INET4;

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
*Example using FreeRTOS_sendto() with the zero copy calling semantics*
