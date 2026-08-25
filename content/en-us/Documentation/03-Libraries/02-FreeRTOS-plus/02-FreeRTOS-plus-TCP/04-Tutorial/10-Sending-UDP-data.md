---
title: Sending UDP Data (standard interface)
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

Part of the [FreeRTOS-Plus-TCP Networking Tutorial](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

The [FreeRTOS_sendto()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/08-sendto)
TCP/IP stack API function is used to send data to a [UDP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/09-UDP) socket.
Data can only be sent after the [socket](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket) has
been [created, configured, and optionally bound](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/09-Creating-a-UDP-socket) to a
local [port number](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/12-Port-number).

As detailed on the FreeRTOS_sendto() API reference page, FreeRTOS_sendto()
can be used with standard calling semantics, or zero copy calling semantics.
This page demonstrates the standard calling semantics.

The source code below shows a RTOS task that creates a UDP socket before entering
a loop that sends a string to the socket (using the standard calling
semantics) every 1 second (1000ms). The comments in the source code
example provide more information.

```c
static void vUDPSendUsingStandardInterface( void *pvParameters )
{
Socket_t xSocket;
struct freertos_sockaddr xDestinationAddress;
uint8_t cString[ 50 ];
uint32_t ulCount = 0UL;
const TickType_t x1000ms = 1000UL / portTICK_PERIOD_MS;

   /* Send strings to port 10000 on IP address 192.168.0.50. */
   memset( &xDestinationAddress, 0, sizeof(xDestinationAddress) );
   xDestinationAddress.sin_address.ulIP_IPv4 = FreeRTOS_inet_addr( "192.168.0.50" );
   xDestinationAddress.sin_family = FREERTOS_AF_INET4;
   xDestinationAddress.sin_port = FreeRTOS_htons( 10000 );

   /* Create the socket. */
   xSocket = FreeRTOS_socket( FREERTOS_AF_INET, /* Used for IPv4 UDP socket. */
                                 /* FREERTOS_AF_INET6 can be used for IPv6 UDP socket. */
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
*Example using FreeRTOS_sendto() with the standard (as opposed to zero copy) calling semantics*

[Back to the RTOS TCP networking tutorial index](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)
