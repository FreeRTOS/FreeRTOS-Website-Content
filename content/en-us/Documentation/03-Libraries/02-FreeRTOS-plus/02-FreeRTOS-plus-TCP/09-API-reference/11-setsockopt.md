---
title: "FreeRTOS_setsockopt()"
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
BaseType_t FreeRTOS_setsockopt( Socket_t xSocket, int32_t lLevel,
                                int32_t lOptionName, const void *pvOptionValue,
                                size_t xOptionLength );
```

Sets a socket option.
 

**Parameters:** 

+ *xSocket*

  The target socket (the socket being modified). The socket must have already been created by a successful 
  call to [FreeRTOS\_socket()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket).  

+ *lLevel*

  FreeRTOS-Plus-TCP does not [currently] use the lLevel parameter. The parameter is included to ensure 
  consistency with the expected standard Berkeley sockets API, and to ensure compatibility with future 
  versions of FreeRTOS-Plus-TCP.  

+ *lOptionName*

  The option being set or modified. See [below](#valid-loptionname-values) for valid values.  

+ *pvOptionValue*

  The meaning of pvOptionValue is dependent on the value of lOptionName. See the description of the 
  lOptionName parameter.  

+ *xOptionLength*

  FreeRTOS-Plus-TCP does not [currently] use the xOptionLength parameter. The parameter is included 
  to ensure consistency with the expected standard Berkeley sockets API, and to ensure compatibility 
  with future versions of FreeRTOS-Plus-TCP.  


**Returns:** 

+ -pdFREERTOS\_ERRNO\_EINVAL is returned if an invalid lOptionName value is used, otherwise 0 is returned.
  (0 is the standard Berkeley sockets success return value, contrary to the FreeRTOS standard where 0 
  means fail!)
 

**Example usage:** 

This example creates a UDP socket, configures the socket's behaviour in accordance with the function's 
parameters, then returns the created and configured socket.

```c
/* FreeRTOS-Plus-TCP sockets include. */  
#include "FreeRTOS_sockets.h"  
  
Socket_t xCreateASocket( TickType_t xReceiveTimeout_ms,  
                         TickType_t xSendTimeout_ms,  
                         int32_t iUseChecksum )  
{  
/* Variable to hold the created socket. */  
Socket_t xSocket;  
  
    /* Create the socket. */  
    xSocket = FreeRTOS_socket( FREERTOS_AF_INET,  
                               FREERTOS_SOCK_DGRAM,  
                               FREERTOS_IPPROTO_UDP );  
  
    /* Check the socket was created successfully. */  
    if( xSocket != FREERTOS_INVALID_SOCKET )  
    {  
        /* Convert the receive timeout into ticks. */  
        xReceiveTimeout_ms /= portTICK_PERIOD_MS;  
  
        /* Set the receive timeout. */  
        FreeRTOS_setsockopt( xSocket,            /* The socket being modified. */  
                             0,                   /* Not used. */  
                             FREERTOS_SO_RCVTIMEO,/* Setting receive timeout. */  
                             &xReceiveTimeout_ms, /* The timeout value. */  
                             0 );                 /* Not used. */  
  
        /* Convert the send timeout into ticks. */  
        xSendTimeout_ms /= portTICK_PERIOD_MS;  
  
        /* Set the send timeout. */  
        FreeRTOS_setsockopt( xSocket,            /* The socket being modified. */  
                             0,                   /* Not used. */  
                             FREERTOS_SO_SNDTIMEO,/* Setting send timeout. */  
                             &xSendTimeout_ms,    /* The timeout value. */  
                             0 );                 /* Not used. */  
  
        if( iUseChecksum == pdFALSE )  
        {  
            /* Turn the UDP checksum creation off for outgoing UDP packets. */  
            FreeRTOS_setsockopt( xSocket,        /* The socket being modified. */  
                                 0,               /* Not used. */  
                                 FREERTOS_SO_UDPCKSUM_OUT, /* Setting checksum on/off. */  
                                 NULL,            /* NULL means off. */  
                                 0 );             /* Not used. */  
        }  
        else  
        {  
            /* The checksum is used by default, so there is nothing to do here.  
               If the checksum was off it could be turned on again using an option  
               value other than NULL, for example ( ( void * ) 1 ). */  
        }  
    }  
  
    return xSocket;  
}  
```
*Example use of the FreeRTOS\_setsockopt() API function*


### Valid lOptionName Values

+ FREERTOS\_SO\_RCVTIMEO
  
  Sets the [receive timeout](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigsock_default_receive_block_time) 
  when [FreeRTOS\_recvfrom()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/10-recvfrom) is called with a UDP socket, or [FreeRTOS\_recv()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/09-recv)
  is called with a TCP socket.
 
  If lOptionName is FREERTOS\_SO\_RECTIMEO then pvOptionValue must point to a variable of type TickType\_t.
 
  Timeout values are specified in ticks. To convert a time in milliseconds to a time in ticks divide the
  time in milliseconds by portTICK\_PERIOD\_MS or use the pdMS\_TO\_TICKS() macro.
 

+ FREERTOS\_SO\_SNDTIMEO
 
  Sets the [transmit timeout](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigSOCK_DEFAULT_SEND_BLOCK_TIME) 
  when [FreeRTOS\_send()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/07-send) is used with a TCP socket, or [FreeRTOS\_sendto()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/08-sendto)
  is used with a UDP socket.
 
  If lOptionName is FREERTOS\_SO\_SNDTIMEO then pvOptionValue must point to a variable of type TickType\_t.
 
  Timeout values are specified in ticks. To convert a time in milliseconds to a time in ticks divide the 
  time in milliseconds by portTICK\_PERIOD\_MS or use the pdMS\_TO\_TICKS() macro.
 

+ FREERTOS\_SO\_UDPCKSUM\_OUT
 
  Only valid for UDP sockets.
 
  Turn on or off the generation of checksum values for outgoing UDP packets.
 
  If lOptionName is FREERTOS\_SO\_UDPCKSUM\_OUT and lOptionValue is NULL (0) then outgoing UDP packets 
  will always have their checksum set to 0.
 
  If lOptionName is FREERTOS\_SO\_UDPCKSUM\_OUT and lOptionValue is any value other than NULL (0) then 
  outgoing UDP packets will include a valid checksum value.
 

+ FREERTOS\_SO\_SET\_SEMAPHORE
 
  Only available if [ipconfigSOCKET\_HAS\_USER\_SEMAPHORE](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigSOCKET_HAS_USER_SEMAPHORE)
  is set to 1 in FreeRTOSIPConfig.h.
 
  This option allows a reference to a semaphore to be passed to a socket. The TCP/IP RTOS task will then 
  give to the semaphore on any of these events:
 
  * Arrival of new data
  * After delivering data, when new transmission buffer space becomes available
  * An outgoing TCP connection has succeeded
  * A new client has connected to a TCP socket
  * A TCP connection was closed or reset

  Example use:

  ```c
  /* Declare the semaphore. */
  SemaphoreHandle_t xSemaphore;

  /* Create the semaphore. */
  xSemaphore = xSemaphoreCreateBinary();
  if( xSemaphore != NULL )
  {
      /* Pass the semaphore to the socket. */
      FreeRTOS_setsockopt( xSocket,
                           0,
                           FREERTOS_SO_SET_SEMAPHORE,
                           ( void * )&xSemaphore,
                           sizeof( xSemaphore ) );
  
      /* The semaphore has been passed to the socket
         and will be used.
  
         **Note:** If a socket has a reference to a semaphore
         then the semaphore must not be deleted! To
         remove the semaphore call FreeRTOS_setsockopt()
         again, but this time with a NULL semaphore. */
      SemaphoreHandle_t xNoSem = NULL;
      FreeRTOS_setsockopt( xSocket,
                           0,
                           FREERTOS_SO_SET_SEMAPHORE,
                           ( void * ) &xNoSem,
                           sizeof( xNoSem ) );
  
      /* Now the semaphore can be deleted. */
      vSemaphoreDelete( xSemaphore );
  }
  ```
  *Example of passing a semaphore to a socket*


+ FREERTOS\_SO\_WAKEUP\_CALLBACK

  Only available if [ipconfigSOCKET\_HAS\_USER\_WAKE\_CALLBACK](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigsocket_has_user_wake_callback)
  is set to 1 in FreeRTOSIPConfig.h.
  
  Each socket can have a callback function that is executed when there is an event the socket's owner 
  might want to process. This is to register and set the wakeup callback function for the socket.

  The callback function should be of the following type:

  ```
  void (* SocketWakeupCallback_t)( struct xSOCKET * pxSocket );
  ```
 
+ FREERTOS\_SO\_SET\_LOW\_HIGH\_WATER

  Only valid for TCP sockets.
  
  This is used to set the low- and the high-water values for TCP reception. It is useful when streaming 
  music. The option value should be of the type `LowHighWater_t`  with the following structure definition:

  ``` 
  typedef struct xLOW_HIGH_WATER
      {
          size_t uxLittleSpace; /**< Send a STOP when buffer space drops below X bytes */
          size_t uxEnoughSpace; /**< Send a GO when buffer space grows above X bytes */
      } LowHighWater_t;[/code-table]
  ```
 

+ FREERTOS\_SO\_RCVBUF
 
  Only valid for TCP sockets.
 
  Sets the size of the [receive buffer](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigTCP_RX_BUFFER_LENGTH).
  Ideally this should be set to twice the size of the [sliding window](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigUSE_TCP_WIN).
 
  This parameter can only be set between the socket being created and data being received on the socket 
  because the size of the receive buffer is fixed after the buffer has been created.
 
  If lOptionName is FREERTOS\_SO\_RCVBUF then pvOptionValue must point to a variable of type int32\_t.
 
  The receive buffer size is specified in bytes. Internally the specified size will get rounded up to 
  the nearest multiple of the [ipconfigTCP\_MSS](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigTCP_MSS) size. For 
  example, if ipconfigTCP\_MSS is 500 then setting a buffer size of 400 will result in a buffer size 
  of 500 (1 * ipconfigTCP\_MSS), setting a buffer size of 500 will result in a buffer size 
  of 500 (1 * ipconfigTCP\_MSS), and setting a buffer size of 510 will result in a buffer size 
  of 1000 (2 * ipconfigTCP\_MSS).
 

+ FREERTOS\_SO\_SNDBUF
  
  Only valid for TCP sockets.
 
  Sets the size of the [transmit buffer](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigTCP_RX_BUFFER_LENGTH).
  This is not related to the size of the packets or the sliding window, it only sets the size of the buffer.
 
  This parameter can only be set between the socket being created and data being sent on the socket because 
  the size of the send buffer is fixed after the buffer has been created.
 
  If lOptionName is FREERTOS\_SO\_SNDBUF then pvOptionValue must point to a variable of type int32\_t.
 
  The receive buffer size is specified in bytes. Internally the specified size will get rounded up to 
  the nearest multiple of the [ipconfigTCP\_MSS](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigTCP_MSS) size. For 
  example, if ipconfigTCP\_MSS is 500 then setting a buffer size of 400 will result in a buffer size 
  of 500 (1 * ipconfigTCP\_MSS), setting a buffer size of 500 will result in a buffer size 
  of 500 (1 * ipconfigTCP\_MSS), and setting a buffer size of 510 will result in a buffer size 
  of 1000 (2 * ipconfigTCP\_MSS).
 

+ FREERTOS\_SO\_WIN\_PROPERTIES
 
  Advanced users only.
 
  Only valid for TCP sockets.
 
  Sets the size of the [receive buffer](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigTCP_RX_BUFFER_LENGTH),
  receive [sliding window](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigUSE_TCP_WIN),
  [transmit buffer](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigTCP_RX_BUFFER_LENGTH) and transmit sliding window 
  in one call.
 
  The buffer and sliding window sizes can only be set between the socket being created and any data being 
  sent to the socket or received from the socket.

  Example use:

  ```c
  /* Declare an xWinProperties structure. */
  WinProperties_t  xWinProps;

  /* Fill in the required buffer and window sizes. */
  /* Unit: bytes */
  xWinProps.lTxBufSize = 4 * ipconfigTCP_MSS;
  /* Unit: MSS */
  xWinProps.lTxWinSize = 2;
  /* Unit: bytes */
  xWinProps.lRxBufSize = 4 * ipconfigTCP_MSS;
  /* Unit: MSS */
  xWinProps.lRxWinSize = 2;

  /* Use the structure with the
     FREERTOS_SO_WIN_PROPERTIES parameter in a call to
     FreeRTOS_setsockopt(). */
  FreeRTOS_setsockopt( xSocket,
                       0,
                       FREERTOS_SO_WIN_PROPERTIES,
                       ( void * ) &xWinProps,
                       sizeof( xWinProps ) );
  ```
  *Example of setting the buffer and sliding window sizes*


+ FREERTOS\_SO\_REUSE\_LISTEN\_SOCKET
 
  Only valid for TCP sockets.
 
  By default a [listening](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/05-listen) socket will create a new socket to handle any accepted connections.
  FREERTOS\_SO\_REUSE\_LISTEN\_SOCKET can be used to change this behaviour so accepted connections are 
  handled by the listening socket itself.
 
  If lOptionName is FREERTOS\_SO\_REUSE\_LISTEN\_SOCKET then pvOptionValue must point to a variable of 
  type BaseType\_t that is set to 1 to indicate that the listening socket should be re-used for incoming 
  connections, or 0 to indicate that the listening socket should create a new socket to handle each 
  incoming connection.
 
  For a re-usable socket it is optional to call FreeRTOS\_accept(). You can also call FreeRTOS\_connected() 
  to determine if the socket is already connected. It is preferred to call FreeRTOS\_accept() because it 
  marks the change from unconnected to connected.
 
  When successful, FreeRTOS\_accept() will return a reference to the parent socket that has connected. 
  It is now marked as accepted and it stops listening for new connections.
 
  At the end of the connection, the socket must be closed by calling FreeRTOS\_closesocket(). After that 
  a new socket can be created and bound to the same port.
 
  Example use:

  ```c
  BaseType_t xReuseSocket = pdTRUE;
  FreeRTOS_setsockopt( xSocket,
                       0,
                       FREERTOS_SO_REUSE_LISTEN_SOCKET,
                       ( void * ) &xReuseSocket,
                       sizeof( xReuseSocket ) );
  ```
  *Example of setting the re-use option to true*


+ FREERTOS\_SO\_CLOSE\_AFTER\_SEND
 
  Advanced users only.
 
  Only valid for TCP sockets.
 
  FREERTOS\_SO\_CLOSE\_AFTER\_SEND TCP allows a socket to be closed immediately after the last data has 
  been delivered. This option is useful for example in FTP where a file is being sent. Before calling 
  FreeRTOS\_send() for the last time, set this option, so the stack knows that the last packet must include
  the FIN flag. The stack will make sure that the connection is only closed after the last byte has been 
  delivered, and acknowledged by the peer.
 
  If lOptionName is FREERTOS\_SO\_CLOSE\_AFTER\_SEND then pvOptionValue must point to a variable of type
  BaseType\_t that is set to 1 to indicate that the socket should be closed after the last data has been 
  sent, or 0 to indicate that the socket should use its default behaviour of keeping the socket open until 
  explicitly by either peer.
 
  Example use:

  ```c
  BaseType_t xCloseAfterNextSend = pdTRUE;
  FreeRTOS_setsockopt( xSocket,
                       0,
                       FREERTOS_SO_CLOSE_AFTER_SEND,
                       ( void * ) &xCloseAfterNextSend,
                       sizeof( xCloseAfterNextSend ) );
  ```
  *Example of using the FREERTOS\_SO\_CLOSE\_AFTER\_SEND parameter*


+ FREERTOS\_SO\_SET\_FULL\_SIZE
 
  Advanced users only.
 
  Only valid for TCP sockets.
 
  The FREERTOS\_SO\_SET\_FULL\_SIZE option tells the TCP/IP stack not to send any data from the socket 
  until there is at least one complete [MSS](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigTCP_MSS) size of data 
  ready to be sent. This option can be used to improve performance, but must be used with care. This 
  option does not expire, so make sure the option is switched off on the last send, so that the last 
  bytes (less than MSS) will also be delivered.
 
  If lOptionName is FREERTOS\_SO\_SET\_FULL\_SIZE then pvOptionValue must point to a variable of type
  BaseType\_t that is set to 1 to indicate that the socket should only send when there is at least MSS 
  bytes waiting to be delivered, or 0 to indicate that the socket should use its default behaviour.
 

+ FREERTOS\_SO\_STOP\_RX
  
  Advanced users only.
 
  Only valid for TCP sockets.
 
  A TCP socket will constantly advertise a window size to its peer, so the peer knows how many bytes it 
  may send until it has to wait for an acknowledge. This all happens automatically with a low and a high 
  water mark.
 
  FREERTOS\_SO\_STOP\_RX forces the socket to advertise a window of zero, enabling the socket to temporarily 
  stop receiving data.
 
  If lOptionName is FREERTOS\_SO\_STOP\_RX then pvOptionValue must point to a variable of type BaseType\_t 
  that is set to 1 to indicate that the socket should advertise a window size of 0, or 0 to indicate that 
  the socket should use its default behaviour.

  ```c
  BaseType_t xValue = pdTRUE;

  /* Temporarily advertise a window size of 0 to stop
  reception of data */
  FreeRTOS_setsockopt( xSocket,
                       0,
                       FREERTOS_SO_STOP_RX,
                       ( void * ) &xValue,
                       sizeof( xValue ) );
  {
      /* Do what ever you need to do. */
  }
  
  xValue = pdFALSE;
  
  /* Allow further reception */
  FreeRTOS_setsockopt( xSocket,
                       0,
                       FREERTOS_SO_STOP_RX,
                       ( void * ) &xValue,
                       sizeof( xValue ) );
  ```
  *Example of using the FREERTOS_SO_STOP_RX parameter*


+ FREERTOS\_SO\_UDP\_MAX\_RX\_PACKETS
  
  Only valid for UDP sockets and if [ipconfigUDP\_MAX\_RX\_PACKETS](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigUDP_MAX_RX_PACKETS)
  is set to 1 in FreeRTOSIPConfig.h.
 
  The parameter ipconfigUDP\_MAX\_RX\_PACKETS makes it possible to limit the maximum number of packets 
  stored in one UDP socket. This option can change this limitation for an individual socket.
 
  If lOptionName is FREERTOS\_SO\_UDP\_MAX\_RX\_PACKETS then pvOptionValue must point to a variable of type
  BaseType\_t that holds the maximum number of RX packets that can be queued on the UDP socket.

  ```c
  /* Allow a maximum of ten packets. */
  BaseType_t xValue = 10;
  
  FreeRTOS_setsockopt( xSocket,
                       0,
                      FREERTOS_SO_UDP_MAX_RX_PACKETS,
                      ( void * ) &xValue,
                      sizeof( xValue ) );
  ```
  *Example of using the FREERTOS_SO_UDP_MAX_RX_PACKETS parameter*


+ FREERTOS\_SO\_TCP\_CONN\_HANDLER
 
  Advanced users only.
 
  Only valid for TCP sockets.
 
  Stores the address of a function to call on connect and disconnect events on the TCP socket.
 

+ FREERTOS\_SO\_TCP\_RECV\_HANDLER
 
  Advanced users only.
 
  Only valid for TCP sockets.
 
  Stores the address of a function to call when data is received on the TCP socket.
 

+ FREERTOS\_SO\_TCP\_SENT\_HANDLER
 
  Advanced users only.
 
  Only valid for TCP sockets.
 
  Stores the address of a function to call when data sent to the TCP socket has been delivered and confirmed 
  by the peer.
 

+ FREERTOS\_SO\_UDP\_RECV\_HANDLER
 
  Advanced users only.
 
  Only valid for UDP sockets.
 
  Stores the address of a function to call immediately upon reception of data on the UDP socket.
 

+ FREERTOS\_SO\_UDP\_SENT\_HANDLER
  
  Advanced users only.
 
  Only valid for UDP sockets.
 
  Stores the address of a function to call immediately that data has been sent to the UDP socket.
 
