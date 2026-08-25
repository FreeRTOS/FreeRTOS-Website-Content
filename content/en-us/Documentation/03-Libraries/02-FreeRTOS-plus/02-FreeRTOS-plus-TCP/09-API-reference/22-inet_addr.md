---
title: "FreeRTOS_inet_addr()"
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
uint32_t FreeRTOS_inet_addr( const uint8_t * pucIPAddress );
```

FreeRTOS\_inet\_addr() is a function that converts an IP address expressed
in decimal dot notation (for example "192.168.0.100") into a 32-bit IP
address in network byte order.
 
[FreeRTOS\_inet\_addr\_quick()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/21-inet_addr_quick) is a macro that converts an IP address expressed 
as four separate numeric octets (for example 192, 168, 0, 100) into a an IP address expressed as a 
32-bit number in network byte order
 
FreeRTOS\_inet\_addr\_quick() is the preferred method because of its smaller size and faster execution. 
FreeRTOS\_inet\_addr() is provided because it conforms to the expected Berkeley sockets function prototype.
 
ipconfigINCLUDE\_FULL\_INET\_ADDR must be set to 1 in FreeRTOSIPConfig.h for FreeRTOS\_inet\_addr() to 
be available. FreeRTOS\_inet\_addr\_quick() is always available.
 

**Parameters:** 

+ *pucIPAddress*

  A pointer to a string that contains the IP address being converted in decimal dot format.  


**Returns:** 

If the format of the string pointed to by the pucIPAddress parameter is valid then the same IP address 
expressed as a 32-bit number in network byte order is returned. In all other cases 0 is returned.
 

**Example usage:** 

This example sends a string to port 5000 of IP address 192.168.0.100, using FreeRTOS\_inet\_addr() to 
convert the IP address from a string to the necessary 32-bit format. The socket is passed in as the 
function parameter, and is assumed to have already been created using a call 
to [FreeRTOS\_socket()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket). If ipconfigALLOW\_SOCKET\_SEND\_WITHOUT\_BIND is not set to 1 in
FreeRTOSIPConfig.h, then the socket is also assumed to have been bound to a port number 
using [FreeRTOS\_bind()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/03-bind).
 

```c
/* FreeRTOS-Plus-TCP sockets include. */  
#include "FreeRTOS_sockets.h"  
  
void aFunction( Socket_t xSocket )  
{  
struct freertos_sockaddr xDestinationAddress;  
const int8_t *pcMessageToSend = "String being sent";  
  
    /* Generate the destination address. */  
    xDestinationAddress.sin_addr = FreeRTOS_inet_addr( "192.168.0.100" );  
    xDestinationAddress.sin_port = FreeRTOS_htons( 5000 );  
  
    /* Send the message. */  
    iReturned = FreeRTOS_sendto(  
                                    /* The socket being send to. */  
                                    xSocket,  
                                    /* The data being sent. */  
                                    pcMessageToSend,  
                                    /* The length of the data being sent. */  
                                    strlen( pcMessageToSend ),  
                                    /* ulFlags with the FREERTOS\_ZERO\_COPY bit clear. */  
                                    0,  
                                    /* Where the data is being sent. */  
                                    &xDestinationAddress,  
                                    /* Not used but should be set as shown. */  
                                    sizeof( xDestinationAddress )  
                               );  
}  
```
*Example use of the FreeRTOS\_inet\_addr\_quick() API function*
