---
title: 发送 UDP 数据（零拷贝接口）
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
只有在[创建、配置[套接字](socket.md)并将其
绑定到](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/09-Creating-a-UDP-socket)[本地端口号](port_number.md)后（可选），才能发送数据。

正如 FreeRTOS_sendto() API 引用页面所述，FreeRTOS_sendto()
可以与标准调用语义或零拷贝调用语义一起使用。
本页演示的是零拷贝调用语义。

下述源代码显示了 RTOS 任务，该任务在进入循环之前创建了 UDP 套接字，
该循环每秒（1000 毫秒）向套接字发送一个字符串
（使用标准调用语义）。源代码示例中的注释
提供了有关在使用零拷贝接口时如何使用网络缓冲区的
重要信息。

```c
static void vUDPSendingUsingZeroCopyInterface( void *pvParameters )
{
Socket_t xSocket;
uint8_t *pucBuffer;
struct freertos_sockaddr xDestinationAddress;
BaseType_t lReturned;
uint32_t ulCount = 0UL;
const uint8_t *pucStringToSend = "Zero copy send message number ";
const TickType_t x1000ms = 1000UL / portTICK_PERIOD_MS;
/* 15 is added to ensure the number, rn and terminating zero fit. */
const size_t xStringLength = strlen( ( char * ) pucStringToSend ) + 15;

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
       /* This RTOS task is going to send using the zero copy interface. The
          data being sent is therefore written directly into a buffer that is
          passed into, rather than copied into, the FreeRTOS_sendto()
          function.

          First obtain a buffer of adequate length from the TCP/IP stack into which
          the string will be written. */
       pucBuffer = [FreeRTOS_GetUDPPayloadBuffer](API/FreeRTOS_GetUDPPayloadBuffer.md)( xStringLength, portMAX_DELAY );

       /* Check a buffer was obtained. */
       configASSERT( pucBuffer );

       /* Create the string that is sent. */
       memset( pucBuffer, 0x00, xStringLength );
       sprintf( pucBuffer, "%s%lurn", ucStringToSend, ulCount );

       /* Pass the buffer into the send function. ulFlags has the
          FREERTOS_ZERO_COPY bit set so the TCP/IP stack will take control of the
          buffer rather than copy data out of the buffer. */
       lReturned = FreeRTOS_sendto( xSocket,
                                   ( void * ) pucBuffer,
                                   strlen( ( const char * ) pucBuffer ) + 1,
                                   FREERTOS_ZERO_COPY,
                                   &xDestinationAddress,
                                   sizeof( xDestinationAddress ) );

       if( lReturned == 0 )
       {
           /* The send operation failed, so this RTOS task is still responsible
              for the buffer obtained from the TCP/IP stack. To ensure the buffer
              is not lost it must either be used again, or, as in this case,
              returned to the TCP/IP stack using FreeRTOS_ReleaseUDPPayloadBuffer().
              pucBuffer can be safely re-used after this call. */
           FreeRTOS_ReleaseUDPPayloadBuffer( ( void * ) pucBuffer );
       }
       else
       {
           /* The send was successful so the TCP/IP stack is now managing the
              buffer pointed to by pucBuffer, and the TCP/IP stack will
              return the buffer once it has been sent. pucBuffer can
              be safely re-used. */
       }

       ulCount++;

       /* Wait until it is time to send again. */
       vTaskDelay( x1000ms );
   }
}

```
*使用 FreeRTOS_sendto() 和零拷贝调用语义的示例*

[返回 RTOS TCP 联网教程索引](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

