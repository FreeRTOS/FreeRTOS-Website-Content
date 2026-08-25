---
title: "使用 TCP 套接字（零拷贝接口）接收数据"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[FreeRTOS-Plus-TCP 网络教程](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)节选

请参阅[接收 UDP 数据（零拷贝接口）](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/13-Receiving-UDP-data-zero-copy)， 
了解如何用 UDP 零拷贝接口接收数据。

[FreeRTOS_recv()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/09-recv) 用于接收 TCP 套接字的数据。 
在调用 FreeRTOS_recv() 之前，必须确保 TCP 套接字 
已正确[创建、配置、绑定](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/05-Creating-TCP-sockets) 
并连接至远程套接字。

下述源代码演示了如何使用 FreeRTOS_recv()，通过零拷贝接口 
将接收的数据放入缓冲区中。本例中假定已正确创建并连接套接字。


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
*FreeRTOS_recv() 用法示例*

[返回 RTOS TCP 网络教程索引](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)
