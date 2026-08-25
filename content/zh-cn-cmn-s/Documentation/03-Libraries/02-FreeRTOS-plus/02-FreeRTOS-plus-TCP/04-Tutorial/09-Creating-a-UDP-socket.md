---
title: 创建、配置和绑定 [UDP](UDP.md) 套接字
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

[FreeRTOS-Plus-TCP 联网教程的一部分](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

UDP [套接字](socket.md) 是使用 [FreeRTOS_socket()](API/socket.md)
创建的，其中函数的 xType（第二个）参数设置为 FREERTOS_SOCK_DGRAM，xProtocol （第三个）参数
设置为 FREERTOS_IPPROTO_UDP。它们使用 [FreeRTOS_setsockopt()](API/setsockopt.md) 函数
进行配置，并[绑定到端口](bind.md)
——使用 [FreeRTOS_bind()](API/bind.md) 函数绑定（如有必要）。

```c
static void prvSimpleUDPServerTask( void *pvParameters )
{
long lBytes;
struct freertos_sockaddr xBindAddress;
Socket_t xListeningSocket;
const TickType_t xSendTimeOut = 200 / portTICK_PERIOD_MS;

   /* Attempt to open the UDP socket. */
   xListeningSocket = FreeRTOS_socket( FREERTOS_AF_INET,
                                       FREERTOS_SOCK_DGRAM,/*FREERTOS_SOCK_DGRAM for UDP.*/
                                       FREERTOS_IPPROTO_UDP );

   /* Check for errors. */
   configASSERT( xListeningSocket != FREERTOS_INVALID_SOCKET );

   /* Ensure calls to FreeRTOS_sendto() timeout if a network buffer cannot be
      obtained within 200ms. */
   FreeRTOS_setsockopt( xListeningSocket,
                        0,
                        FREERTOS_SO_SNDTIMEO,
                        &xSendTimeOut,
                        sizeof( xSendTimeOut ) );

   /* Bind the socket to port 0x1234. */
   xBindAddress.sin_port = [FreeRTOS_htons](API/htons_ntohs_htonl_ntohl.md)( 0x1234 );
   FreeRTOS_bind( xListeningSocket, &xBindAddress, sizeof( xBindAddress ) );

   for( ;; )
   {
       /*
        * The socket can now send and receive data here.
        */
   }
}

```
*创建、配置和绑定 UDP 套接字*

[返回 RTOS TCP 联网教程索引](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

