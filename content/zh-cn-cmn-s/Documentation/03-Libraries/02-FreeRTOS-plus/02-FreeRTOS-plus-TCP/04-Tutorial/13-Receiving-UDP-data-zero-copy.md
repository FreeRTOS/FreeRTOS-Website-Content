---
title: 接收 UDP 数据（零拷贝接口）
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
本页演示的是零拷贝调用语义。

下方源代码所述的 RTOS 任务在进入
使用零拷贝调用语义接收数据的循环前创建了套接字。源代码中的
注释提供了采用零拷贝方案时如何使用
网络缓冲区的重要信息。

```c
static void vUDPReceivingUsingZeroCopyInterface( void *pvParameters )
{
int32_t lBytes;
uint8_t *pucUDPPayloadBuffer;
struct freertos_sockaddr xClient, xBindAddress;
uint32_t xClientLength = sizeof( xClient ), ulIPAddress;
Socket_t xListeningSocket;

   /* Attempt to open the socket. */
   xListeningSocket = FreeRTOS_socket( FREERTOS_AF_INET,
                                       FREERTOS_SOCK_DGRAM, /*FREERTOS_SOCK_DGRAM for UDP.*/
                                       FREERTOS_IPPROTO_UDP );

   /* Check the socket was created. */
   configASSERT( xListeningSocket != FREERTOS_INVALID_SOCKET );

   /* Bind to port 10000. */
   xBindAddress.sin_port = FreeRTOS_htons( 10000 );
   FreeRTOS_bind( xListeningSocket, &xBindAddress, sizeof( xBindAddress ) );

   for( ;; )
   {
       /* Receive data from the socket. ulFlags has the zero copy bit set
          (FREERTOS_ZERO_COPY) indicating to the stack that a reference to the
          received data should be passed out to this RTOS task using the second
          parameter to the FreeRTOS_recvfrom() call. When this is done the
          IP stack is no longer responsible for releasing the buffer, and
          the RTOS task **must** return the buffer to the stack when it is no longer
          needed. By default the block time is portMAX_DELAY but it can be
          changed using FreeRTOS_setsockopt(). */
       lBytes = FreeRTOS_recvfrom( xListeningSocket,
                                   &pucUDPPayloadBuffer,
                                   0,
                                   FREERTOS_ZERO_COPY,
                                   &xClient,
                                   &xClientLength );

       if( lBytes > 0 )
       {
           /* Data was received and can be processed here. */
       }

       if( lBytes >= 0 )
       {
           /* The receive was successful so this RTOS task is now responsible for
              the buffer. The buffer **must** be freed once it is no longer
              needed. */

           /*
            * The data can be processed here.
            */

           /* Return the buffer to the TCP/IP stack. */
           FreeRTOS_ReleaseUDPPayloadBuffer( pucUDPPayloadBuffer );
       }
   }
}

```
*使用 FreeRTOS_recvfrom() 与零拷贝（和标准相反）调用语义的示例*

[返回 RTOS TCP 联网教程索引](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

