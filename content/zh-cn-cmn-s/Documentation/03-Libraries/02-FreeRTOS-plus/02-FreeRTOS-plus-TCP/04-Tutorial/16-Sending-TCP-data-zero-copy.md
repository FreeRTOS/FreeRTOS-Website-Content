---
title: "使用 TCP 套接字（零拷贝接口）发送数据"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[FreeRTOS-Plus-TCP 联网教程的一部分](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

请参阅[发送 UDP 数据（零拷贝接口）](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/11-Sending-UDP-data-zero-copy) 
了解如何用 UDP 零拷贝接口接收数据。

[FreeRTOS_send()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/07-send) TCP/IP 堆栈 API 函数 
用于向 [TCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/10-TCP) 套接字发送数据。只有 
在 
[创建、配置、绑定](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/05-Creating-TCP-sockets)套接字 
并使用 
[FreeRTOS_connect()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/04-connect) 
API 函数连接到远程套接字后，才能发送数据，或者接受来自远程套接字的连接。

以下源代码片段显示了创建套接字、 
通过零拷贝接口向套接字发送数据，然后优雅地关闭套接字的函数。显示的是 IPv4 和 IPv6 用例 
。请注意，此套接字未显式绑定到移植号——导致它在 
FreeRTOS_connect() API 函数中自动绑定。


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
               that its a zero copy */
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
*使用 FreeRTOS_send() 和零拷贝调用语义的 IPv4 示例*


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
               that its a zero copy */
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
*使用 FreeRTOS_send() 和零拷贝调用语义的 IPv6 示例*

[返回 RTOS TCP 联网教程索引](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

