---
title: "FreeRTOS_rx_size()"
created: 2024-09-18
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-TCP API Reference](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS_Sockets.h

```c
BaseType_t FreeRTOS_rx_size ( ConstSocket_t xSocket );
```
Returns the number of bytes which can be read from the RX stream buffer.

**Parameters:**

+ *xSocket*

    the socket to get the number of bytes from.

**Returns:** 
Returns the number of bytes which can be read. Or an error code is returned.

**Example usage:**

```c
#include "FreeRTOS_Sockets.h"

/* Peek at the data; process it; then remove the data if processing is successful. */
BaseType_t xPeekAndProcessData( Socket_t xSocket, /* TCP socket. */
                                uint8_t * pucBuffer, /* Buffer to store the data. */
                                size_t uxBufferLength /* Length of the buffer. */ )
{
    size_t uxSize = FreeRTOS_recvcount( xSocket );
    BaseType_t xProcessed = pdFALSE;

    if( uxSize > uxBufferLength )
    {
        uxSize = uxBufferLength;
    }

    /* Peek at the data by passing the FREERTOS_MSG_PEEK flag. It will not lead to data
     * being removed from the socket buffer. */
    BaseType_t xCount = FreeRTOS_recv( xSocket,
                                       pucBuffer,
                                       uxSize,
                                       FREERTOS_MSG_PEEK );

    /* Check whether pucBuffer has entire packet "Hello FreeRTOS!" exactly - nothing more,
     * nothing less. */
    if( strncmp( pucBuffer, "Hello FreeRTOS!", uxSize ) == 0 )
    {
        /* Remove the data from the socket buffer by reading it. */
        ( void ) FreeRTOS_recv( xSocket,
                                pucBuffer,
                                uxSize,
                                0 );
        xProcessed = pdTRUE;
    }

    return xProcessed;
}
```
*Example use of the FreeRTOS_recv() API function*
