---
title: Receiving UDP Data (standard interface)
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

Part of the [FreeRTOS-Plus-TCP Networking Tutorial](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

The [FreeRTOS\_recvfrom()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/10-recvfrom)
TCP/IP stack API function is used to receive from a [UDP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/09-UDP) socket.
Data can only be received after the [socket](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket) has
been [created, configured, and bound](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/09-Creating-a-UDP-socket) to a
local [port number](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/12-Port-number).

As detailed on the FreeRTOS\_recvfrom() API reference page, FreeRTOS\_recvfrom()
can be used with standard calling semantics, or zero copy calling semantics.
This page demonstrates the standard calling semantics.

The source code below shows a RTOS task that creates a socket before entering
a loop that receives data using the standard (as opposed to zero copy)
calling semantics. Both IPv4 and IPv6 use cases are shown.

**IPv4**

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
   memset( &xBindAddress, 0, sizeof(xBindAddress) );
   xBindAddress.sin_port = FreeRTOS_htons( 10000 );
   xBindAddress.sin_family = FREERTOS_AF_INET4;
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
*Example using FreeRTOS_recvfrom() with the standard (as opposed to zero copy) calling semantics*


**IPv6**

```c
static void vUDPReceivingUsingStandardInterface( void *pvParameters )
{
    long lBytes;
    uint8_t cReceivedString[ 60 ];
    struct freertos_sockaddr xClient, xBindAddress;
    uint32_t xClientLength = sizeof( xClient );
    Socket_t xListeningSocket;

   /* Attempt to open the socket. */
   xListeningSocket = FreeRTOS_socket( FREERTOS_AF_INET6, /* FREERTOS_AF_INET6 for IPv6 socket */
                                       FREERTOS_SOCK_DGRAM, /*FREERTOS_SOCK_DGRAM for UDP.*/
                                       FREERTOS_IPPROTO_UDP );

   /* Check the socket was created. */
   configASSERT( xListeningSocket != FREERTOS_INVALID_SOCKET );

   /* Bind to port 10000. */
   memset( &xBindAddress, 0, sizeof(xBindAddress) );
   xBindAddress.sin_port = FreeRTOS_htons( 10000 );
   xBindAddress.sin_family = FREERTOS_AF_INET6;
   FreeRTOS_bind( xListeningSocket, &xBindAddress, sizeof( xBindAddress ) );

   for( ;; )
   {
       /* Receive data from the socket.  ulFlags is zero, so the standard
          interface is used.  By default the block time is portMAX_DELAY, but it
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
*Example using FreeRTOS_recvfrom() with the standard (as opposed to zero copy) calling semantics*

[Back to the RTOS TCP networking tutorial index](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)
