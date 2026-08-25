---
title: "Sending Data Using a TCP Socket (zero copy interface)"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

Part of the [FreeRTOS-Plus-TCP Networking Tutorial](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

Refer to [Sending UDP Data (zero copy interface)](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/11-Sending-UDP-data-zero-copy) 
for receiving data using UDP zero copy interface.

The [FreeRTOS\_send()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/07-send) TCP/IP stack API function 
is used to send data to a [TCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/10-TCP) socket. Data can only 
be sent after the socket has 
been [created, configured, bound](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/05-Creating-TCP-sockets), 
and connected to a remote socket using 
the [FreeRTOS\_connect()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/04-connect) 
API function, or it can accept connections from a remote socket.

The source code snippets below show a function that creates a socket, sends data to the socket using 
the zero copy interface, then gracefully shuts down and closes the socket. Both IPv4 and IPv6 use cases 
are shown. Note that this socket is not explicitly bound to a port number - causing it to be bound 
automatically inside the FreeRTOS_connect() API function.


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
    memset( &xBindAddress, 0, sizeof(xBindAddress) );
    xRemoteAddress.sin_port = FreeRTOS_htons( 1500 );
    xRemoteAddress.sin_address.ulIP_IPv4 = FreeRTOS_inet_addr_quick( 192, 168, 0, 200 );
    xRemoteAddress.sin_family = FREERTOS_AF_INET4;


    /* Create a socket. */
    xSocket = FreeRTOS_socket( FREERTOS_AF_INET,
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
            BaseType_t xAvlSpace = 0;
            BaseType_t xBytesToSend = 0;
            uint8_t *pucTCPZeroCopyStrmBuffer;
            
            /* This RTOS task is going to send using the zero copy interface.  The
               data being sent is therefore written directly into the TCP TX stream
               buffer that is passed into, rather than copied into, the FreeRTOS_send()
               function. */

            /* Obtain the pointer to the current head of sockets TX stream buffer 
               using FreeRTOS_get_tx_head */
            pucTCPZeroCopyStrmBuffer = FreeRTOS_get_tx_head( xSocket, &xAvlSpace );

            if(pucTCPZeroCopyStrmBuffer)
            {
                /* Check if there is enough space in the stream buffer to place 
                   the entire data. */
                if((xTotalLengthToSend - xAlreadyTransmitted) > xAvlSpace)
                {
                    xBytesToSend = xAvlSpace;
                }
                else
                {
                    xBytesToSend = (xTotalLengthToSend - xAlreadyTransmitted);
                }
                memcpy( pucTCPZeroCopyStrmBuffer, 
                        ( void * ) (( (uint8_t *) pcBufferToTransmit ) + xAlreadyTransmitted),  
                        xBytesToSend);
            }
            else
            {
                /* Error - break out of the loop for graceful socket close. */
                break;
            }

            /* Call the FreeRTOS_send with buffer as NULL indicating to the stack
               that it's a zero copy */
            xBytesSent = FreeRTOS_send( /* The socket being sent to. */
                                        xSocket,
                                        /* The data being sent. */
                                        NULL,
                                        /* The remaining length of data to send. */
                                        xBytesToSend,
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
*IPv4 Example using FreeRTOS_send() with the zero copy calling semantics*


**IPv6**

```c
void vTCPSend( char *pcBufferToTransmit, const size_t xTotalLengthToSend )
{
    Socket_t xSocket;
    struct freertos_sockaddr xRemoteAddress;
    BaseType_t xAlreadyTransmitted = 0, xBytesSent = 0;
    TaskHandle_t xRxTask = NULL;
    size_t xLenToSend;

    /* Set the IP address (2001:470:ed44::9c08:38cc:599f:f62a) and port (1500) of the remote socket
       to which this client socket will transmit. */
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
            BaseType_t xAvlSpace = 0;
            BaseType_t xBytesToSend = 0;
            uint8_t *pucTCPZeroCopyStrmBuffer;
            
            /* This RTOS task is going to send using the zero copy interface.  The
               data being sent is therefore written directly into the TCP TX stream
               buffer that is passed into, rather than copied into, the FreeRTOS_send()
               function. */

            /* Obtain the pointer to the current head of sockets TX stream buffer 
            using FreeRTOS_get_tx_head */
            pucTCPZeroCopyStrmBuffer = FreeRTOS_get_tx_head( xSocket, &xAvlSpace );

            if(pucTCPZeroCopyStrmBuffer)
            {
                /* Check of there is enough space in the stream buffer to place 
                   the entire data. */
                if((xTotalLengthToSend - xAlreadyTransmitted) > xAvlSpace)
                {
                    xBytesToSend = xAvlSpace;
                }
                else
                {
                    xBytesToSend = (xTotalLengthToSend - xAlreadyTransmitted);
                }
                memcpy( pucTCPZeroCopyStrmBuffer, 
                        ( void * ) (( (uint8_t *) pcBufferToTransmit ) + xAlreadyTransmitted),  
                        xBytesToSend);
            }
            else
            {
                /* Error - break out of the loop for graceful socket close. */
                break;
            }

            /* Call the FreeRTOS_send with buffer as NULL indicating to the stack
               that it's a zero copy */
            xBytesSent = FreeRTOS_send( /* The socket being sent to. */
                                        xSocket,
                                        /* The data being sent. */
                                        NULL,
                                        /* The remaining length of data to send. */
                                        xBytesToSend,
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
*IPv6 Example using FreeRTOS_send() with the zero copy calling semantics*

[Back to the RTOS TCP networking tutorial index](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

