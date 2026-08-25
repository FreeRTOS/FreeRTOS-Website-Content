---
title: "FreeRTOS_rx_size()"
created: 2024-09-18
categories:
  - kernel
description: TBD
relatedLinks: 
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-TCP API 参考](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS_Sockets.h

```c
BaseType_t FreeRTOS_rx_size ( ConstSocket_t xSocket );
```
返回可以从 RX 流缓冲区读取的字节数。

**Parameters:**

+ *xSocket*

    从套接字获取字节数。

**Returns:** 
返回可以读取的字节数。或者返回错误码。

**Example usage:**

```c
#include "FreeRTOS_Sockets.h"

/* 看看数据；处理它；如果处理成功，则删除数据。 */
BaseType_t xPeekAndProcessData( Socket_t xSocket, uint8_t * pucBuffer, size_t uxBufferLength )
{
    size_t uxSize = FreeRTOS_recvcount( xSocket );

    if( uxSize > uxBufferLength )
    {
        uxSize = uxBufferLength;
    }

    /* 通过传递 FREERTOS_MSG_PEEK 标志来查看数据。不会导致数据
     * 从套接字缓冲区中删除。 */
    BaseType_t xCount = FreeRTOS_recv( xSocket,
                                       pucBuffer,
                                       uxSize,
                                       FREERTOS_MSG_PEEK );

    /* 检查 pucBuffer 是否有整个数据包 “Hello FreeRTOS!” 不多也不少。 */
    if( strncmp( pucBuffer, "Hello FreeRTOS!", uxSize ) == 0 )
    {
        /* Remove the data from the socket buffer by reading it. */
        ( void ) FreeRTOS_recv( xSocket,
                                pucBuffer,
                                uxSize,
                                0 );
    }
    return xCount;
}
```
*FreeRTOS_recv() API 函数的使用示例*