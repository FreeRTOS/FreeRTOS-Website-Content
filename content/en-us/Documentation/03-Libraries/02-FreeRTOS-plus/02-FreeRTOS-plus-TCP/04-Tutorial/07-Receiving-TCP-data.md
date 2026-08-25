---
title: Receiving Data Using a TCP Socket
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

Part of the [FreeRTOS-Plus-TCP Networking Tutorial](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

[**Note:** This page does not describe the callback or zero copy interfaces,
which are available for expert users.]

[FreeRTOS_recv()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/09-recv)
is used to receive data from a TCP [socket](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket).
FreeRTOS_recv() cannot be
called until the TCP socket has been [created, configured, bound](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/05-Creating-TCP-sockets)
and connected to a remote socket.

The source code below demonstrates how to use FreeRTOS_recv() to place
received data into a buffer. In the example it is assumed that the
socket has already been created and connected.

```c
#define BUFFER_SIZE 512
static void prvEchoClientRxTask( void *pvParameters )
{
Socket_t xSocket;
static char cRxedData[ BUFFER_SIZE ];
BaseType_t lBytesReceived;

    /* It is assumed the socket has already been created and connected before
 being passed into this RTOS task using the RTOS task's parameter. */
    xSocket = ( Socket_t ) pvParameters;

    for( ;; )
    {
        /* Receive another block of data into the cRxedData buffer. */
        lBytesReceived = FreeRTOS_recv( xSocket, &cRxedData, BUFFER_SIZE, 0 );

        if( lBytesReceived > 0 )
        {
            /* Data was received, process it here. */
            prvProcessData( cRxedData, lBytesReceived );
        }
        else if( lBytesReceived == 0 )
        {
            /* No data was received, but FreeRTOS\_recv() did not return an error.
               Timeout? */
        }
        else
        {
            /* Error (maybe the connected socket already shut down the socket?).
               Attempt graceful shutdown. */
            FreeRTOS_shutdown( xSocket, FREERTOS_SHUT_RDWR );
            break;
        }
    }

    /* The RTOS task will get here if an error is received on a read. Ensure the
 socket has shut down (indicated by FreeRTOS\_recv() returning a -pdFREERTOS\_ERRNO\_EINVAL
 error before closing the socket). */

    while( FreeRTOS_recv( xSocket, pcBufferToTransmit, xTotalLengthToSend, 0 ) >= 0 )
    {
        /* Wait for shutdown to complete. If a receive block time is used then
           this delay will not be necessary as FreeRTOS\_recv() will place the RTOS task
           into the Blocked state anyway. */
        vTaskDelay( pdTICKS_TO_MS( 250 ) );

        /* Note - real applications should implement a timeout here, not just
           loop forever. */
    }

    /* Shutdown is complete and the socket can be safely closed. */
    FreeRTOS_closesocket( xSocket );

    /* Must not drop off the end of the RTOS task - delete the RTOS task. */
    [xTaskDelete](/Documentation/02-Kernel/04-API-references/01-Task-creation/03-vTaskDelete)( NULL );

}
```
*Example using FreeRTOS_recv()*


[Back to the RTOS TCP networking tutorial index](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)
