---
title: 发送 UDP 数据（标准接口）
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

[FreeRTOS-Plus-TCP 联网教程的一部分](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

经证明， [FreeRTOS_sendto()](API/sendto.md)
TCP/IP 堆栈 API 函数用于向 [UDP](UDP.md) 套接字发送数据。
只有在 [套接字](socket.md) 
[创建、配置并绑定](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/09-Creating-a-UDP-socket)到 
本地[端口号](port_number.md)后，才能接收数据。

正如 FreeRTOS_sendto() API 引用页面所述，FreeRTOS_sendto()
可以与标准调用语义或零拷贝调用语义一起使用。
本页演示的是标准调用语义。

下述源代码展示的是 RTOS 任务，该任务在进入循环之前创建了 UDP 套接字，
该循环每秒（1000 毫秒）向套接字发送一个字符串
（使用标准调用语义）。如需了解更多信息，请参阅源代码示例中的注释
。

```c
static void vUDPSendUsingStandardInterface( void *pvParameters )
{
Socket_t xSocket;
struct freertos_sockaddr xDestinationAddress;
uint8_t cString[ 50 ];
uint32_t ulCount = 0UL;
const TickType_t x1000ms = 1000UL / portTICK_PERIOD_MS;

   /* Send strings to port 10000 on IP address 192.168.0.50. */
   xDestinationAddress.sin_addr = FreeRTOS_inet_addr( "192.168.0.50" );
   xDestinationAddress.sin_port = FreeRTOS_htons( 10000 );

   /* Create the socket. */
   xSocket = FreeRTOS_socket( FREERTOS_AF_INET,
                              FREERTOS_SOCK_DGRAM,/*FREERTOS_SOCK_DGRAM for UDP.*/
                              FREERTOS_IPPROTO_UDP );

   /* Check the socket was created. */
   configASSERT( xSocket != FREERTOS_INVALID_SOCKET );

   /* NOTE: FreeRTOS_bind() is not called. This will only work if
      ipconfigALLOW_SOCKET_SEND_WITHOUT_BIND is set to 1 in FreeRTOSIPConfig.h. */

   for( ;; )
   {
       /* Create the string that is sent. */
       sprintf( cString,
                "Standard send message number %lurn",
                ulCount );

       /* Send the string to the UDP socket. ulFlags is set to 0, so the standard
          semantics are used. That means the data from cString[] is copied
          into a network buffer inside FreeRTOS_sendto(), and cString[] can be
          reused as soon as FreeRTOS_sendto() has returned. */
       FreeRTOS_sendto( xSocket,
                        cString,
                        strlen( cString ),
                        0,
                        &xDestinationAddress,
                        sizeof( xDestinationAddress ) );

       ulCount++;

       /* Wait until it is time to send again. */
       vTaskDelay( x1000ms );
   }
}

```
*使用 FreeRTOS_sendto() 与零拷贝（和标准相反）调用语义的示例*

[返回 RTOS TCP 联网教程索引](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

