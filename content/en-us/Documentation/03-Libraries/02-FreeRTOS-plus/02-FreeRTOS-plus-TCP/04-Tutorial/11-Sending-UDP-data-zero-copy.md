---
title: Sending UDP Data (zero copy interface)
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
Data can only be sent after the [socket](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket) has been [created, configured, and
optionally bound](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/09-Creating-a-UDP-socket) to a local [port number](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/12-Port-number).

As detailed on the FreeRTOS_sendto() API reference page, FreeRTOS_sendto()
can be used with standard calling semantics, or zero copy calling semantics.
This page demonstrates the zero copy calling semantics.

The source code below shows a RTOS task that creates a UDP socket before entering
a loop that sends a string to the socket (using the standard calling
semantics) every 1 second (1000ms). The comments in the source code
example provide important information on how to use network buffers when
the zero copy interface is used.

**IPv4**

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
   memset( &xDestinationAddress, 0, sizeof(xDestinationAddress) );
   xDestinationAddress.sin_address.ulIP_IPv4 = FreeRTOS_inet_addr( "192.168.0.50" );
   xDestinationAddress.sin_family = FREERTOS_AF_INET4;
   xDestinationAddress.sin_port = FreeRTOS_htons( 10000 );

   /* Create the socket. */
   xSocket = FreeRTOS_socket( FREERTOS_AF_INET,
                              FREERTOS_SOCK_DGRAM,/*FREERTOS_SOCK_DGRAM for UDP.*/
                              FREERTOS_IPPROTO_UDP );

   /* Check the socket was created. */
   configASSERT( xSocket != FREERTOS_INVALID_SOCKET );

   /* NOTE: FreeRTOS_bind() is not called.  This will only work if
   ipconfigALLOW_SOCKET_SEND_WITHOUT_BIND is set to 1 in FreeRTOSIPConfig.h. */

   for( ;; )
   {
       /* This RTOS task is going to send using the zero copy interface.  The
          data being sent is therefore written directly into a buffer that is
          passed into, rather than copied into, the FreeRTOS_sendto()
          function.

          First obtain a buffer of adequate length from the TCP/IP stack into which
          the string will be written. */
       pucBuffer = FreeRTOS_GetUDPPayloadBuffer_Multi( xStringLength, 
                                                       portMAX_DELAY, 
                                                       ipTYPE_IPv4 );

       /* Check a buffer was obtained. */
       configASSERT( pucBuffer );

       /* Create the string that is sent. */
       memset( pucBuffer, 0x00, xStringLength );
       sprintf( pucBuffer, "%s%lurn", ucStringToSend, ulCount );

       /* Pass the buffer into the send function.  ulFlags has the
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
              for the buffer obtained from the TCP/IP stack.  To ensure the buffer
              is not lost it must either be used again, or, as in this case,
              returned to the TCP/IP stack using FreeRTOS_ReleaseUDPPayloadBuffer().
              pucBuffer can be safely re-used after this call. */
           FreeRTOS_ReleaseUDPPayloadBuffer( ( void * ) pucBuffer );
       }
       else
       {
           /* The send was successful so the TCP/IP stack is now managing the
              buffer pointed to by pucBuffer, and the TCP/IP stack will
              return the buffer once it has been sent.  pucBuffer can
              be safely re-used. */
       }

       ulCount++;

       /* Wait until it is time to send again. */
       vTaskDelay( x1000ms );
   }
}
```
*Example using FreeRTOS_sendto() with the zero copy calling semantics*


**IPv6**

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

    /* Send strings to port 10000 on IP address 2001::1234. */
    memset( &xDestinationAddress, 0, sizeof(xDestinationAddress) );
    BaseType_t rc = FreeRTOS_inet_pton( FREERTOS_AF_INET6, "2001::1234", 
                                        ( void * ) xDestinationAddress.sin_address.xIP_IPv6.ucBytes );
    xDestinationAddress.sin_port = FreeRTOS_htons( 10000 );
    xDestinationAddress.sin_family = FREERTOS_AF_INET6;

    if( rc == pdPASS )
    {
        /* Create the socket. */
        xSocket = FreeRTOS_socket( FREERTOS_AF_INET6,
                                   FREERTOS_SOCK_DGRAM,/*FREERTOS_SOCK_DGRAM for UDP.*/
                                   FREERTOS_IPPROTO_UDP );

        /* Check the socket was created. */
        configASSERT( xSocket != FREERTOS_INVALID_SOCKET );
 
        /* NOTE: FreeRTOS_bind() is not called.  This will only work if
        ipconfigALLOW_SOCKET_SEND_WITHOUT_BIND is set to 1 in FreeRTOSIPConfig.h. */
 
        for( ;; )
        {
            /* This RTOS task is going to send using the zero copy interface.  The
               data being sent is therefore written directly into a buffer that is
               passed into, rather than copied into, the FreeRTOS_sendto()
               function.
 
               First obtain a buffer of adequate length from the TCP/IP stack into which
               the string will be written. */
            pucBuffer = FreeRTOS_GetUDPPayloadBuffer_Multi( xStringLength, 
                                                            portMAX_DELAY, 
                                                            ipTYPE_IPv6);
 
            /* Check a buffer was obtained. */
            configASSERT( pucBuffer );
 
            /* Create the string that is sent. */
            memset( pucBuffer, 0x00, xStringLength );
            sprintf( pucBuffer, "%s%lurn", ucStringToSend, ulCount );
 
            /* Pass the buffer into the send function.  ulFlags has the
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
                   for the buffer obtained from the TCP/IP stack.  To ensure the buffer
                   is not lost it must either be used again, or, as in this case,
                   returned to the TCP/IP stack using FreeRTOS_ReleaseUDPPayloadBuffer().
                   pucBuffer can be safely re-used after this call. */
                FreeRTOS_ReleaseUDPPayloadBuffer( ( void * ) pucBuffer );
            }
            else
            {
                /* The send was successful so the TCP/IP stack is now managing the
                   buffer pointed to by pucBuffer, and the TCP/IP stack will
                   return the buffer once it has been sent.  pucBuffer can
                   be safely re-used. */
            }
 
            ulCount++;

            /* Wait until it is time to send again. */
            vTaskDelay( x1000ms );
        }
    }
}
```
*IPv6 Example using FreeRTOS_sendto() with the zero copy calling semantics*

[Back to the RTOS TCP networking tutorial index](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)
