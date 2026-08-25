---
title: "FreeRTOS_bind()"
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
BaseType_t FreeRTOS_bind( Socket_t xSocket,
                          struct freertos_sockaddr *pxAddress,
                          socklen_t xAddressLength );
```

Binds a socket to a local port number. Binding a socket associates a socket with a port number on the 
local IP address, resulting in the socket receiving all the data that is sent to that IP address and 
port number combination.
 
The Network Addressing and Binding sections of the [Embedded Networking Basics and Glossary](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/01-Networking-basics)
page provide an introduction to the topic of socket binding.
 
Port numbers above 49408 (0xC100) to 65280 (0xff00) are considered private numbers available to the IP 
stack for dynamic allocation, and should therefore be avoided. Specifying a port number of 0 or passing
pxAddress as NULL will result in the socket being bound to a port number from the private range.
 
For convenience, if ipconfigALLOW\_SOCKET\_SEND\_WITHOUT\_BIND is set to 1 in FreeRTOSIPConfig.h, then 
calling [FreeRTOS\_send()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/07-send) on a socket that has not first been bound to a port number will also
result in the socket being bound to a port number from the private range.

FreeRTOS-Plus-TCP does not [currently] use all the function parameters. The parameters that are not used 
are retained in the function's prototype to ensure consistency with the expected standard Berkeley sockets 
API, and to ensure compatibility with future versions of FreeRTOS-Plus-TCP.
 

**Parameters:** 

+ *xSocket*

  The handle of the socket that is being bound to an address. The socket must have previously been 
  created by a successful call to [FreeRTOS\_socket()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket). 

+ *pxAddress*

   A pointer to a freertos\_sockaddr structure that contains the details of the port number being bound 
   to. See the provided example. 

+ *xAddressLength*

   Not currently used, but should be set to sizeof( struct freertos\_sockaddr ) to ensure future 
   compatibility. 


**Returns:** 

If the bind was successful then 0 is returned (0 is the standard Berkeley sockets success return value, 
contrary to the FreeRTOS standard where 0 means fail!).
 
 + -pdFREERTOS\_ERRNO\_EINVAL is returned if the socket did not get bound, probably because the specified 
   port number was already in use.
 
 + -pdFREERTOS\_ERRNO\_ECANCELED is returned if the calling RTOS task did not get a response from the IP 
   RTOS task to the bind request.
 

**Example usage:** 

See [the examples on the FreeRTOS-Plus-TCP networking tutorial](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/05-Creating-TCP-sockets)
page, and on the [FreeRTOS\_socket()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket) API documentation page.
 
