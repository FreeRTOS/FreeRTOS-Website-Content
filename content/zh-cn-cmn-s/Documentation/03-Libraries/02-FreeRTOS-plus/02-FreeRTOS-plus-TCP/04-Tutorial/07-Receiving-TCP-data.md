---
title: 使用 TCP 套接字接收数据
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

[FreeRTOS-Plus-TCP 联网教程的一部分](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

[**注意：**本页不介绍供专家用户使用的回调或零拷贝接口
。]

[FreeRTOS_recv()](API/recv.md)
用于从TCP [套接字](socket.md)接收数据。
FreeRTOS_recv()
在[创建、配置、绑定](TCP_Networking_Tutorial_TCP_Client_and_Server.md)TCP
套接字并将其连接到远程套接字后才能调用。

下述源代码演示了如何通过 FreeRTOS_recv()
将接收数据放入缓冲区。在本示例中，
假设套接字已创建并连接。

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

    /* The RTOS task will get here if an error is received on a read. Ensure the
 socket has shut down (indicated by FreeRTOS_recv() returning a -pdFREERTOS_ERRNO_EINVAL
 error before closing the socket). */

    while( FreeRTOS_recv( xSocket, pcBufferToTransmit, xTotalLengthToSend, 0 ) >= 0 )
    {
        /* Wait for shutdown to complete. If a receive block time is used then
           this delay will not be necessary as FreeRTOS_recv() will place the RTOS task
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
*使用 FreeRTOS_recv()* 的示例


[返回 RTOS TCP 联网教程索引](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

