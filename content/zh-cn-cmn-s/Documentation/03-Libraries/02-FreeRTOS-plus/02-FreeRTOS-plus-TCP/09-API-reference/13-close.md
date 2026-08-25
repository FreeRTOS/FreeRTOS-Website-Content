---
title: FreeRTOS_closesocket()
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[FreeRTOS-Plus-TCP API 引用](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS_sockets.h

```c
BaseType_t FreeRTOS_closesocket( Socket_t xSocket );
```

关闭套接字。

该函数被命名为 FreeRTOS_closesocket()，而非单纯地命名为 FreeRTOS_close()， 
以免与 FreeRTOS-Plus-IO 中的函数发生潜在的名称空间冲突。

在关闭套接字之前，应该以合理的方式[关停](shutdown)它， 
且关闭后无法再使用该套接字。


**参数：** 

+ *xSocket*

  正在停用的套接字句柄。套接字必须已成功创建， 
  （请参阅 [FreeRTOS_socket()](socket)），且在关闭后无法再使用。  


**返回：** 

始终返回 0。

虽然 FreeRTOS-Plus-TCP [当前]并未以有意义的方式使用返回值， 
返回值包含在函数原型中，以确保与预期的标准伯克利套接字原型保持一致， 
并确保与 FreeRTOS-Plus-TCP 的未来版本兼容。


**用法示例：** 

```c
/* FreeRTOS-Plus-TCP sockets include. */  
#include "FreeRTOS_sockets.h"  
  
void aFunction( void )  
{  
Socket_t xSocket;  
  
    /* Create a socket. */  
    xSocket = FreeRTOS_socket( FREERTOS_AF_INET, FREERTOS_SOCK_STREAM, FREERTOS_IPPROTO_TCP );  
  
    if( xSocket != FREERTOS_INVALID_SOCKET )  
    {  
        /*  
         * The socket can now be used...  
         */  
  
         /* . . . */  
  
         /* Initialise a shutdown before closing the socket. */  
         FreeRTOS_shutdown( xSocket );  
  
        /* Wait for the socket to disconnect gracefully (indicated by FreeRTOS_recv()  
           returning a FREERTOS_EINVAL error) before closing the socket. */  
        while( FreeRTOS_recv( xSocket, pcBufferToTransmit, xTotalLengthToSend, 0 ) >= 0 )  
        {  
            /* Wait for shutdown to complete. If a receive block time is used then  
               this delay will not be necessary as FreeRTOS_recv() will place the RTOS task  
               into the Blocked state anyway. */  
            [vTaskDelay](/Documentation/02-Kernel/04-API-references/02-Task-control/01-vTaskDelay)( pdTICKS_TO_MS( 250 ) );  
  
            /* Note - real applications should implement a timeout here, not just  
               loop forever. */  
        }  
  
         /* Close the socket again. */  
         FreeRTOS_closesocket( xSocket );  
    }  
}  
```
*FreeRTOS_closesocket() API 函数用法示例*

