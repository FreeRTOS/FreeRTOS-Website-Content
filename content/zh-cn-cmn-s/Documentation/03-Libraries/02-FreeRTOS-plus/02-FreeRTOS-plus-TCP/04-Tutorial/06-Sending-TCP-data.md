---
title: 使用 TCP 套接字发送数据
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[FreeRTOS-Plus-TCP 网络教程](/Documentation/03-Libraries/03-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)节选

[**注意：**本页不介绍供专家用户使用的回调或零拷贝接口
。]

TCP [套接字](/Documentation/03-Libraries/03-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket)[创建、配置并绑定后](/Documentation/03-Libraries/03-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/05-Creating-TCP-sockets)，
即可通过 [FreeRTOS_connect()](/Documentation/03-Libraries/03-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/04-connect) API
函数连接到远程套接字，或[接受](/Documentation/03-Libraries/03-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/06-accept)
来自远程套接字的连接。一旦连接，
数据将通过 [FreeRTOS_send()](/Documentation/03-Libraries/03-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/07-send) API 函数
发送到远程套接字。

以下源代码显示了创建套接字、
向套接字发送数据，然后有序关闭套接字的函数。IPv4 和 
IPv6 用例如下所示。请注意，此套接字未显式绑定到端口号， 
而是在 
FreeRTOS_connect() API 函数内部自动绑定。

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

    /* Wait for the socket to disconnect gracefully (indicated by FreeRTOS_recv()
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
*FreeRTOS_send() 用法示例*


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
*FreeRTOS_send() 用法示例*

[返回 RTOS TCP 网络教程索引](/Documentation/03-Libraries/03-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)
