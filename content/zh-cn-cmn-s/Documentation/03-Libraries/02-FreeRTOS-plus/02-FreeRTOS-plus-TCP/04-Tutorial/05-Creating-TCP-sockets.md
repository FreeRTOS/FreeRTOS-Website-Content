---
title: 创建、配置和绑定 TCP 套接字
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

[FreeRTOS-Plus-TCP 联网教程的一部分](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

TCP [套接字](socket.md) 是：

- 使用 [FreeRTOS_socket()](API/socket.md)
  API 函数创建的，其中 xType（第二个）参数设置为 FREERTOS_SOCK_STREAM，并且 xProtocol（第三个）
  参数设置为 FREERTOS_IPPROTO_TCP。

- 使用 [FreeRTOS_setsockopt()](API/setsockopt.md) 函数配置的。

- 并使用 [FreeRTOS_bind()](API/bind.md) 函数绑定[到端口](bind.md)。

如果套接字用于实现[服务器](client_server.md)，则调用
[FreeRTOS_listen()](API/listen.md) 将套接字置于侦听状态，并调用
[FreeRTOS_accept()](API/accept.md)
接受传入连接。本页提供了源代码示例

要更改 TCP 套接字使用的接收和发送缓冲区的默认大小，
可分别通过以下参数调用 [FreeRTOS_setsockopt()](API/setsockopt.md)：
FREERTOS_SO_RCVBUF 和
FREERTOS_SO_SNDBUF。该操作必须在套接字创建后、
连接前立即完成。

如果 [ipconfigUSE_TCP_WIN](TCP_IP_Configuration.md#ipconfigUSE_TCP_WIN)
在 FreeRTOSIPConfig.h 中设置为 1，
套接字将使用[滑动窗口](http://en.wikipedia.org/wiki/Sliding_window)
最大限度地降低开销并最大限度地提高吞吐量。可以使用
FREERTOS_SO_WIN_PROPERTIES
参数将滑动窗口的默认大小更改为 FreeRTOS_setsockopt()。指定滑动窗口的大小以
MSS 为单位（因此，如果 MSS 设置为 200 字节，则滑动窗口大小为
2， 即 400 字节) ，
并且必须始终小于或等于两个方向上的内部缓冲区的大小。

默认情况下，可自动创建子套接字处理在侦听的
TCP/IP 套接字上接受的任何连接（可以通过调用
FreeRTOS_setsockopt() 的 FREERTOS_SO_REUSE_LISTEN_SOCKET 参数更改默认行为）。
子套接字继承其父套接字的缓冲区大小和滑动窗口大小
。

下述示例一演示了如何创建、配置并绑定
客户端套接字。下述示例二演示了如何创建、
配置并绑定服务器套接字，
以及如何在服务器套接字上接受新连接。

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
       it here!. (see the FreeRTOS\setsockopt() documentation. */

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
*创建、配置和绑定 TCP 客户端套接字*


```c
void vCreateTCPServerSocket( void )
{
struct freertos_sockaddr xClient, xBindAddress;
Socket_t xListeningSocket, xConnectedSocket;
socklen_t xSize = sizeof( xClient );
static const TickType_t xReceiveTimeOut = portMAX_DELAY;
const BaseType_t xBacklog = 20;

    /* Attempt to open the socket. */
    xListeningSocket = FreeRTOS_socket( PF_INET,
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
    xBindAddress.sin_port = ( uint16_t ) 10000;
    xBindAddress.sin_port = FreeRTOS_htons( xBindAddress.sin_port );

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
        [xTaskCreate](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate)( prvServerConnectionInstance,
                     "EchoServer",
                     usUsedStackSize,
                     ( void * ) xConnectedSocket,
                     tskIDLE_PRIORITY,
                     NULL );
    }
}

```
*创建、配置和绑定 TCP 服务器套接字*

[返回 RTOS TCP 联网教程索引](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

