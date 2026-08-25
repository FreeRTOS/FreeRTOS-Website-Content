---
title: 接收 UDP 数据（标准接口）
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

[FreeRTOS-Plus-TCP 联网教程的一部分](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

用于查询时间的 [FreeRTOS_recvfrom()](API/recvfrom.md)
TCP/IP 堆栈 API 函数用于从 [UDP](UDP.md) 套接字接收数据。
当[套接字](socket.md)被 
[创建、配置并绑定](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/09-Creating-a-UDP-socket)到 
本地[端口号](port_number.md)后，才能接收数据。

正如 FreeRTOS_recvfrom() API 引用页面所述，FreeRTOS_recvfrom()
可以与标准调用语义或零拷贝调用语义一起使用。
本页演示的是标准调用语义。

下述源代码展示的是 RTOS 任务，
在进入使用标准调用语义（与零拷贝调用语义相反）
接收数据的循环之前，该任务会创建一个套接字。

```c
static void vUDPReceivingUsingStandardInterface( void *pvParameters )
{
long lBytes;
uint8_t cReceivedString[ 60 ];
struct freertos_sockaddr xClient, xBindAddress;
uint32_t xClientLength = sizeof( xClient );
Socket_t xListeningSocket;

   /* Attempt to open the socket. */
   xListeningSocket = FreeRTOS_socket( FREERTOS_AF_INET,
                                       FREERTOS_SOCK_DGRAM,   /* FREERTOS_SOCK_DGRAM for UDP */
                                       FREERTOS_IPPROTO_UDP );

   /* Check the socket was created. */
   configASSERT( xListeningSocket != FREERTOS_INVALID_SOCKET );

   /* Bind to port 10000. */
   xBindAddress.sin_port = FreeRTOS_htons( 10000 );
   FreeRTOS_bind( xListeningSocket, &xBindAddress, sizeof( xBindAddress ) );

   for( ;; )
   {
       /* Receive data from the socket. ulFlags is zero, so the standard
          interface is used. By default the block time is portMAX_DELAY, but it
          can be changed using FreeRTOS_setsockopt(). */
       lBytes = FreeRTOS_recvfrom( xListeningSocket,
                                   cReceivedString,
                                   sizeof( cReceivedString ),
                                   0,
                                   &xClient,
                                   &xClientLength );

       if( lBytes > 0 )
       {
           /* Data was received and can be process here. */
       }
   }
}

```
*使用 FreeRTOS_recvfrom() 与标准（和零拷贝相反）调用语义的示例*

[返回 RTOS TCP 联网教程索引](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

