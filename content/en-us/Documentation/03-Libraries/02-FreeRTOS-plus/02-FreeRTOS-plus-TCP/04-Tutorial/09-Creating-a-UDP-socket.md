---
title: Create, Configure and Bind a [UDP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/09-UDP) Socket
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

Part of the [FreeRTOS-Plus-TCP Networking Tutorial](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

UDP [Sockets](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket) are created using the [FreeRTOS_socket()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket)
API function with the xType (second) parameter set to FREERTOS_SOCK_DGRAM and the xProtocol (third) parameter
set to FREERTOS_IPPROTO_UDP. They are configured using the [FreeRTOS_setsockopt()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/11-setsockopt)
function, and [bound to a port](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/03-bind)
(if necessary) using the [FreeRTOS_bind()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/03-bind) function.

```c
static void prvSimpleUDPServerTask( void *pvParameters )
{
long lBytes;
struct freertos_sockaddr xBindAddress;
Socket_t xListeningSocket;
const TickType_t xSendTimeOut = 200 / portTICK_PERIOD_MS;

   /* Attempt to open the UDP socket. */
   xListeningSocket = FreeRTOS_socket( FREERTOS_AF_INET,
                                          /* Use FREERTOS_AF_INET6 for IPv6 UDP socket */
                                       FREERTOS_SOCK_DGRAM,
                                          /*FREERTOS_SOCK_DGRAM for UDP.*/
                                       FREERTOS_IPPROTO_UDP );

   /* Check for errors. */
   configASSERT( xListeningSocket != FREERTOS_INVALID_SOCKET );

   /* Ensure calls to FreeRTOS\_sendto() timeout if a network buffer cannot be
      obtained within 200ms. */
   FreeRTOS_setsockopt( xListeningSocket,
                        0,
                        FREERTOS_SO_SNDTIMEO,
                        &xSendTimeOut,
                        sizeof( xSendTimeOut ) );

   /* Bind the socket to port 0x1234. */
   memset( &xBindAddress, 0, sizeof(xBindAddress) );
   xBindAddress.sin_port = FreeRTOS_htons( 0x1234 );
   xBindAddress.sin_family = FREERTOS_AF_INET4; /* FREERTOS_AF_INET6 to be used for IPv6 */
   FreeRTOS_bind( xListeningSocket, &xBindAddress, sizeof( xBindAddress ) );

   for( ;; )
   {
       /*
        * The socket can now send and receive data here.
        */
   }
}
```
*Creating, configuring and binding a UDP socket*

[Back to the RTOS TCP networking tutorial index](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)
