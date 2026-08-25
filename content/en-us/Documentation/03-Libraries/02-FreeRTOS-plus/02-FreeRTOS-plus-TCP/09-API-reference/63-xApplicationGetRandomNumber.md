---
title: "xApplicationGetRandomNumber()"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-TCP API Reference](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS\_sockets.h
  
```c
BaseType_t xApplicationGetRandomNumber( uint32_t * pulNumber );
```

xApplicationGetRandomNumber is an application defined hook (or callback) function that is called by 
the FreeRTOS-Plus-TCP stack to get a random number. Applications should strive to provide a true random 
number. If at all possible, a hardware random number generator should be used. The quality of provided 
random numbers greatly effects the security of communication.

Callback functions are implemented by the application writer, but called by the TCP/IP stack. The prototype 
of the callback function must exactly match the prototype above (including the function name). The code in 
an application hook should not call FreeRTOS-Plus-TCP API's that are blocking. That could easily lead to 
a dead-lock.

When an application hook executes, it borrows the task priority and the stack of the IP-task. Therefore, 
we recommend that you keep application hooks short--it may want to wakeup some application task which 
will do further processing.


**Parameters:**

+ *pulNumber*
  
  If the random number generation is successful, then this pointer is filled with the generated 32-bit 
  random number.
  

**Return value:** 

If the random number is successfully generated, then a pdTRUE should be returned and a copy of the random 
number in the pulNumber parameter should be made. Otherwise a pdFALSE should be returned.
 
