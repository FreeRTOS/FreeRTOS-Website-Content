---
title: Receiving UDP Data (zero copy interface)
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

Part of the [FreeRTOS-Plus-TCP Networking Tutorial](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

The [FreeRTOS_recvfrom()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/10-recvfrom)
TCP/IP stack API function is used to receive from a [UDP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/09-UDP) socket.
Data can only be received after the [socket](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket) has
been [created, configured, and bound](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/09-Creating-a-UDP-socket) to a
local [port number](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/12-Port-number).

As detailed on the FreeRTOS_recvfrom() API reference page, FreeRTOS_recvfrom()
can be used with standard calling semantics, or zero copy calling semantics.
This page demonstrates the zero copy calling semantics.

The source code below shows a RTOS task that creates a socket before entering
a loop that receives data using the zero copy calling semantics. The
comments in the source code provide important information on how to use
network buffers when the zero copy option is used.

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
                                          /* FREERTOS_AF_INET6 to be used for IPv6 */
                                       FREERTOS_SOCK_DGRAM, 
                                          /*FREERTOS_SOCK_DGRAM for UDP.*/
                                       FREERTOS_IPPROTO_UDP );

   /* Check the socket was created. */
   configASSERT( xListeningSocket != FREERTOS_INVALID_SOCKET );

   /* Bind to port 10000. */
   memset( &xBindAddress, 0, sizeof(xBindAddress) );
   xBindAddress.sin_port = FreeRTOS_htons( 10000 );
   xBindAddress.sin_family = FREERTOS_AF_INET4; /* FREERTOS_AF_INET6 to be used for IPv6 */
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
*Example using FreeRTOS_recvfrom() with the zero copy (as opposed to standard) calling semantics*

[Back to the RTOS TCP networking tutorial index](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)
