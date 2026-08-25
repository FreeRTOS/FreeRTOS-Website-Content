---
title: Sending Data Using a TCP Socket
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

Part of the [FreeRTOS-Plus-TCP Networking Tutorial](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

[**Note:** This page does not describe the callback or zero copy interfaces,
which are available for expert users.]

After a TCP [socket](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket) has been [created, configured, and bound](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/05-Creating-TCP-sockets)
it can be connected to a remote socket using the [FreeRTOS_connect()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/04-connect) API
function, or it can [accept](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/06-accept)
connections from a remote socket. Once
connected, data is sent to the remote socket using the [FreeRTOS_send()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/07-send) API
function.

The source code below shows a function that creates a socket, sends data
to the socket, then gracefully shuts down and closes the socket. Both IPv4
and IPv6 use cases are shown. Note that this socket is not explicitly bound 
to a port number - causing it to be bound automatically inside the 
FreeRTOS\_connect() API function.

**IPv4**

```c
void vTCPSend( char *pcBufferToTransmit, const size_t xTotalLengthToSend )
{
Socket_t xSocket;
struct freertos_sockaddr xRemoteAddress;
BaseType_t xAlreadyTransmitted = 0, xBytesSent = 0;
TaskHandle_t xRxTask = NULL;
size_t xLenToSend;

    /* Set the IP address (192.168.0.200) and port (1500) of the remote socket
       to which this client socket will transmit. */
    memset( &xRemoteAddress, 0, sizeof(xRemoteAddress) );
    xRemoteAddress.sin_port = FreeRTOS_htons( 1500 );
    xRemoteAddress.sin_address.ulIP_IPv4 = FreeRTOS_inet_addr_quick( 192, 168, 0, 200 );
    xRemoteAddress.sin_family = FREERTOS_AF_INET4;

    /* Create a socket. */
    xSocket = FreeRTOS_socket( FREERTOS_AF_INET,
                               FREERTOS_SOCK_STREAM,/* FREERTOS_SOCK_STREAM for TCP. */
                               FREERTOS_IPPROTO_TCP );
    configASSERT( xSocket != FREERTOS_INVALID_SOCKET );

    /* Connect to the remote socket. The socket has not previously been bound to
       a local port number so will get automatically bound to a local port inside
       the FreeRTOS_connect() function. */
    if( FreeRTOS_connect( xSocket, &xRemoteAddress, sizeof( xRemoteAddress ) ) == 0 )
    {
        /* Keep sending until the entire buffer has been sent. */
        while( xAlreadyTransmitted < xTotalLengthToSend )
        {
            /* How many bytes are left to send? */
            xLenToSend = xTotalLengthToSend - xAlreadyTransmitted;
            xBytesSent = FreeRTOS_send( /* The socket being sent to. */
                                        xSocket,
                                        /* The data being sent. */
                                        &( pcBufferToTransmit[ xAlreadyTransmitted ] ),
                                        /* The remaining length of data to send. */
                                        xLenToSend,
                                        /* ulFlags. */
                                        0 );

            if( xBytesSent >= 0 )
            {
                /* Data was sent successfully. */
                xAlreadyTransmitted += xBytesSent;
            }
            else
            {
                /* Error - break out of the loop for graceful socket close. */
                break;
            }
        }
    }

    /* Initiate graceful shutdown. */
    FreeRTOS_shutdown( xSocket, FREERTOS_SHUT_RDWR );

    /* Wait for the socket to disconnect gracefully (indicated by FreeRTOS\_recv()
       returning a -pdFREERTOS_ERRNO_EINVAL error) before closing the socket. */
    while( FreeRTOS_recv( xSocket, pcBufferToTransmit, xTotalLengthToSend, 0 ) >= 0 )
    {
        /* Wait for shutdown to complete. If a receive block time is used then
           this delay will not be necessary as FreeRTOS_recv() will place the RTOS task
           into the Blocked state anyway. */
        vTaskDelay( pdTICKS_TO_MS( 250 ) );

        /* Note - real applications should implement a timeout here, not just
           loop forever. */
    }

    /* The socket has shut down and is safe to close. */
    FreeRTOS_closesocket( xSocket );
}
```
*Example using FreeRTOS_send()*


**IPv6**

```c
void vTCPSend( char *pcBufferToTransmit, const size_t xTotalLengthToSend )
{
Socket_t xSocket;
struct freertos_sockaddr xRemoteAddress;
BaseType_t xAlreadyTransmitted = 0, xBytesSent = 0;
TaskHandle_t xRxTask = NULL;
size_t xLenToSend;

    /* Set the IP address (2001:470:ed44::9c08:38cc:599f:f62a) and port (1500) of 
       the remote socket to which this client socket will transmit. */
    memset( &xRemoteAddress, 0, sizeof(xRemoteAddress) );
    xRemoteAddress.sin_port = FreeRTOS_htons( 1500 );
    FreeRTOS_inet_pton6( "2001:470:ed44::9c08:38cc:599f:f62a", 
                         (void *) xRemoteAddress.sin_address.xIP_IPv6.ucBytes );
    xRemoteAddress.sin_family = FREERTOS_AF_INET6;
    /* Create a socket. */
    xSocket = FreeRTOS_socket( FREERTOS_AF_INET6,
                               FREERTOS_SOCK_STREAM, /* FREERTOS_SOCK_STREAM for TCP. */
                               FREERTOS_IPPROTO_TCP );
    configASSERT( xSocket != FREERTOS_INVALID_SOCKET );

    /* Connect to the remote socket.  The socket has not previously been bound to
       a local port number so will get automatically bound to a local port inside
       the FreeRTOS_connect() function. */
    if( FreeRTOS_connect( xSocket, &xRemoteAddress, sizeof( xRemoteAddress ) ) == 0 )
    {
        /* Keep sending until the entire buffer has been sent. */
        while( xAlreadyTransmitted < xTotalLengthToSend )
        {
            /* How many bytes are left to send? */
            xLenToSend = xTotalLengthToSend - xAlreadyTransmitted;
            xBytesSent = FreeRTOS_send( /* The socket being sent to. */
                                        xSocket,
                                        /* The data being sent. */
                                        &( pcBufferToTransmit[ xAlreadyTransmitted ] ),
                                        /* The remaining length of data to send. */
                                        xLenToSend,
                                        /* ulFlags. */
                                        0 );

            if( xBytesSent >= 0 )
            {
                /* Data was sent successfully. */
                xAlreadyTransmitted += xBytesSent;
            }
            else
            {
                /* Error - break out of the loop for graceful socket close. */
                break;
            }
        }
    }

    /* Initiate graceful shutdown. */
    FreeRTOS_shutdown( xSocket, FREERTOS_SHUT_RDWR );

    /* Wait for the socket to disconnect gracefully (indicated by FreeRTOS_recv()
       returning a -pdFREERTOS_ERRNO_EINVAL error) before closing the socket. */
    while( FreeRTOS_recv( xSocket, pcBufferToTransmit, xTotalLengthToSend, 0 ) >= 0 )
    {
        /* Wait for shutdown to complete.  If a receive block time is used then
           this delay will not be necessary as FreeRTOS_recv() will place the RTOS task
           into the Blocked state anyway. */
        vTaskDelay( pdTICKS_TO_MS( 250 ) );

        /* Note - real applications should implement a timeout here, not just
           loop forever. */
    }

    /* The socket has shut down and is safe to close. */
    FreeRTOS_closesocket( xSocket );
}
```
*Example using FreeRTOS_send()*

[Back to the RTOS TCP networking tutorial index](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)
