---
title: xStreamBufferIsFull()
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Stream Buffer API](/Documentation/02-Kernel/04-API-references/08-Stream-buffers/00-RTOS-stream-buffer-API)]

stream\_buffer.h

```c
BaseType_t xStreamBufferIsFull( StreamBufferHandle_t xStreamBuffer );
```

Queries a [stream buffer](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/02-Stream-buffer-example) to see if it is full.
A stream buffer is full if it does not have any free space, and therefore cannot
accept any more data.

Stream buffer functionality is enabled by including the FreeRTOS/source/stream\_buffer.c
source file in the build.


**Parameters:** 

+ *xStreamBuffer* 

  The handle of the stream buffer being queried.


**Returns:** 

If the stream buffer is full then pdTRUE is returned. Otherwise
pdFALSE is returned.
 
