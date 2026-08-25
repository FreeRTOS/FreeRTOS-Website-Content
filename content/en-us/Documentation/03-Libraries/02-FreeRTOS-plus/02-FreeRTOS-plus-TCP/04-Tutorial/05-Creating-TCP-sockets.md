---
title: Create, Configure and Bind a TCP Socket
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

Part of the [FreeRTOS-Plus-TCP Networking Tutorial](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

TCP [Sockets](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket) are:

- Created using the [FreeRTOS\_socket()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket)
  API function with the xType (second) parameter set to FREERTOS\_SOCK\_STREAM and the xProtocol (third)
  parameter set to FREERTOS\_IPPROTO\_TCP.

- Configured using the [FreeRTOS\_setsockopt()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/11-setsockopt) function.

- and [bound to a port](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/03-bind) using the [FreeRTOS\_bind()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/03-bind) function.

If the socket is used to implement a [server](/Documentation/03-Libraries/02-FreeRTOS-plus/FreeRTOS-Plus/FreeRTOS_Plus_TCP/UDP_client_server) then
call [FreeRTOS\_listen()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/05-listen) to place the socket into
the Listening state, and call [FreeRTOS\_accept()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/06-accept)
to accept incoming connections. Source code examples are provided on this page.

To change the size of the receive and send buffers used by the TCP socket from
their defaults call [FreeRTOS\_setsockopt()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/11-setsockopt)
using the FREERTOS\_SO\_RCVBUF and
FREERTOS\_SO\_SNDBUF parameters respectively. This must be done immediately
after the socket is created, before it is connected.

If [ipconfigUSE\_TCP\_WIN](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/06-Configuration#ipconfigUSE_TCP_WIN)
is set to 1 in FreeRTOSIPConfig.h then the
socket will use a [sliding window](http://en.wikipedia.org/wiki/Sliding_window)
to minimise overhead and maximise throughput. The size of the sliding
window can be changed from its default using the FREERTOS\_SO\_WIN\_PROPERTIES
parameter to FreeRTOS\_setsockopt(). The sliding window size is
specified in units of MSS (so if the MSS is set to 200 bytes then a
sliding window size of 2 is equal to 400 bytes) and must always be
smaller than or equal to the size of the internal buffers in both directions.

By default a child socket is automatically created to handle any connections accepted
on a listening TCP/IP socket (the default behaviour can be changed using
the FREERTOS\_SO\_REUSE\_LISTEN\_SOCKET parameter in a call to FreeRTOS_setsockopt()).
Child sockets inherit the buffer sizes and
sliding window sizes of their parent sockets.

The first example below demonstrates how to create, configure and bind
a client socket. The second example below demonstrates how to create,
configure, and bind a server socket, then how to accept new connections on
the server socket.

```c
void vCreateTCPClientSocket( void )
{
Socket_t xClientSocket;
socklen_t xSize = sizeof( freertos_sockaddr );
static const TickType_t xTimeOut = pdMS_TO_TICKS( 2000 );

    /* Attempt to open the socket. */
    xClientSocket = FreeRTOS_socket( PF_INET,
                                     SOCK_STREAM,  /* SOCK_STREAM for TCP. */
                                     IPPROTO_TCP );

    /* Check the socket was created. */
    configASSERT( xClientSocket != FREERTOS_INVALID_SOCKET );

    /* If FREERTOS_SO_RCVBUF or FREERTOS_SO_SNDBUF are to be used with
       FreeRTOS_setsockopt() to change the buffer sizes from their default then do
       it here!. (see the FreeRTOS_setsockopt() documentation. */

    /* If ipconfigUSE_TCP_WIN is set to 1 and FREERTOS_SO_WIN_PROPERTIES is to
       be used with FreeRTOS_setsockopt() to change the sliding window size from
       its default then do it here! (see the FreeRTOS_setsockopt()
       documentation. */

    /* Set send and receive time outs. */
    FreeRTOS_setsockopt( xClientSocket,
                         0,
                         FREERTOS_SO_RCVTIMEO,
                         &xTimeOut,
                         sizeof( xTimeOut ) );

    FreeRTOS_setsockopt( xClientSocket,
                         0,
                         FREERTOS_SO_SNDTIMEO,
                         &xTimeOut,
                         sizeof( xTimeOut ) );

    /* Bind the socket, but pass in NULL to let FreeRTOS-Plus-TCP choose the port number.
       See the next source code snipped for an example of how to bind to a specific
       port number. */
    FreeRTOS_bind( xClientSocket, NULL, xSize );
}
```   
*Creating, configuring and binding a TCP client socket*


```c
void vCreateTCPServerSocket( void )
{
struct freertos_sockaddr xClient, xBindAddress;
Socket_t xListeningSocket, xConnectedSocket;
socklen_t xSize = sizeof( xClient );
static const TickType_t xReceiveTimeOut = portMAX_DELAY;
const BaseType_t xBacklog = 20;

    /* Attempt to open the socket. */
    xListeningSocket = FreeRTOS_socket( FREERTOS_AF_INET4, /* Or FREERTOS_AF_INET6 for IPv6. */
                                        SOCK_STREAM,  /* SOCK_STREAM for TCP. */
                                        IPPROTO_TCP );

    /* Check the socket was created. */
    configASSERT( xListeningSocket != FREERTOS_INVALID_SOCKET );

    /* If FREERTOS_SO_RCVBUF or FREERTOS_SO_SNDBUF are to be used with
       FreeRTOS_setsockopt() to change the buffer sizes from their default then do
       it here!. (see the FreeRTOS_setsockopt() documentation. */

    /* If ipconfigUSE_TCP_WIN is set to 1 and FREERTOS_SO_WIN_PROPERTIES is to
       be used with FreeRTOS_setsockopt() to change the sliding window size from
       its default then do it here! (see the FreeRTOS_setsockopt()
       documentation. */

    /* Set a time out so accept() will just wait for a connection. */
    FreeRTOS_setsockopt( xListeningSocket,
                         0,
                         FREERTOS_SO_RCVTIMEO,
                         &xReceiveTimeOut,
                         sizeof( xReceiveTimeOut ) );

    /* Set the listening port to 10000. */
    memset( &xBindAddress, 0, sizeof(xBindAddress) );
    xBindAddress.sin_port = ( uint16_t ) 10000;
    xBindAddress.sin_port = FreeRTOS_htons( xBindAddress.sin_port );
    xBindAddress.sin_family = FREERTOS_AF_INET4; /* FREERTOS_AF_INET6 to be used for IPv6 */

    /* Bind the socket to the port that the client RTOS task will send to. */
    FreeRTOS_bind( xListeningSocket, &xBindAddress, sizeof( xBindAddress ) );

    /* Set the socket into a listening state so it can accept connections.
       The maximum number of simultaneous connections is limited to 20. */
    FreeRTOS_listen( xListeningSocket, xBacklog );

    for( ;; )
    {
        /* Wait for incoming connections. */
        xConnectedSocket = FreeRTOS_accept( xListeningSocket, &xClient, &xSize );
        configASSERT( xConnectedSocket != FREERTOS_INVALID_SOCKET );

        /* Spawn a RTOS task to handle the connection. */
        xTaskCreate( prvServerConnectionInstance,
                     "EchoServer",
                     usUsedStackSize,
                     ( void * ) xConnectedSocket,
                     tskIDLE_PRIORITY,
                     NULL );
    }
}
```   
*Creating, configuring and binding a TCP server socket*

[Back to the RTOS TCP networking tutorial index](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)
