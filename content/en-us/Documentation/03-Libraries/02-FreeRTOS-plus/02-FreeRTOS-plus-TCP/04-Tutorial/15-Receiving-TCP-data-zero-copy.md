---
title: "Receiving Data Using a TCP Socket (zero copy interface)"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

Part of the [FreeRTOS-Plus-TCP Networking Tutorial](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

Refer to [Receiving UDP Data (zero copy interface)](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/13-Receiving-UDP-data-zero-copy) 
for receiving data using UDP zero copy interface.

[FreeRTOS\_recv()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/09-recv) is used to receive data from a TCP 
socket. FreeRTOS\_recv() cannot be called until the TCP socket has 
been [created, configured, bound](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/05-Creating-TCP-sockets) 
and connected to a remote socket.

The source code below demonstrates how to use FreeRTOS\_recv() to place received data into a buffer using 
the zero copy interface. In the example it is assumed that the socket has already been created and connected.


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

        uint8_t *pucZeroCopyRxBuffPtr = NULL;

        /* Receive data from the socket.  xFlags has the zero copy bit set
           (FREERTOS_ZERO_COPY) indicating to the stack that a reference to the
           received data should be passed out to this RTOS task using the second
           parameter to the FreeRTOS_recv() call.  When this is done the
           IP stack is no longer responsible for releasing the buffer, and
           the RTOS task must return the buffer to the stack when it is no longer
           needed using the FreeRTOS_ReleaseTCPPayloadBuffer() API. */
        lBytesReceived =  FreeRTOS_recv( xSocket, /* The socket being received from. */
                          &pucZeroCopyRxBuffPtr,  /* While using FREERTOS_ZERO_COPY flag, 
                                                     pvBuffer is taken as a double pointer which will 
                                                     be updated with pointer to TCP RX stream buffer. */
                          ipconfigTCP_MSS,        /* The size of the buffer provided to 
                                                     receive the data. */
                          FREERTOS_ZERO_COPY );   /* Use FREERTOS_ZERO_COPY flag to enable 
                                                     zero copy. */
        if( pucZeroCopyRxBuffPtr != NULL )
        {
            /* Copy the data to application buffer if its required to be processed later */
            memcpy(  &cRxedData, pucZeroCopyRxBuffPtr, lBytesReceived );
            
            /* Release the memory that was previously obtained by calling FreeRTOS_recv()
               with the flag 'FREERTOS_ZERO_COPY' */
            FreeRTOS_ReleaseTCPPayloadBuffer( xSocket, pucZeroCopyRxBuffPtr, lBytesReceived );
        }

        if( lBytesReceived > 0 )
        {
            /* Data was received, process it here. */
            prvProcessData( cRxedData, lBytesReceived );
        }
        else if( lBytesReceived == 0 )
        {
            /* No data was received, but FreeRTOS_recv() did not return an error.
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

    /* The RTOS task will get here if an error is received on a read.  Ensure the
       socket has shut down (indicated by FreeRTOS_recv() returning a -pdFREERTOS_ERRNO_EINVAL
       error before closing the socket). */

    while( FreeRTOS_recv( xSocket, pcBufferToTransmit, xTotalLengthToSend, 0 ) >= 0 )
    {
        /* Wait for shutdown to complete.  If a receive block time is used then
           this delay will not be necessary as FreeRTOS_recv() will place the RTOS task
           into the Blocked state anyway. */
        vTaskDelay( pdTICKS_TO_MS( 250 ) );

        /* Note - real applications should implement a timeout here, not just
           loop forever. */
    }

    /* Shutdown is complete and the socket can be safely closed. */
    FreeRTOS_closesocket( xSocket );

    /* Must not drop off the end of the RTOS task - delete the RTOS task. */
    xTaskDelete( NULL );
}
```
*Example using FreeRTOS_recv()*


[Back to the RTOS TCP networking tutorial index](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

