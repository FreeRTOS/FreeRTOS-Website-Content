---
title: "FreeRTOS_htons(), FreeRTOS_ntohs(), FreeRTOS_htonl() and FreeRTOS_ntohl()"
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
uint16_t FreeRTOS_htons( uint16_t usValueToSwap );
uint16_t FreeRTOS_ntohs( uint16_t usValueToSwap );

uint32_t FreeRTOS_htonl( uint32_t ulValueToSwap );
uint32_t FreeRTOS_ntohl( uint32_t ulValueToSwap );
```

The [Byte Order and Endian](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/02-Networking-basics/25-Endian) section of the Embedded Networking Basics and Glossary page 
provides an explanation of byte order considerations in IP networks.
 
The definition of ipconfigBYTE\_ORDER in FreeRTOSIPConfig.h must be
correct for the microcontroller on which FreeRTOS-Plus-TCP will run. If the
microcontroller is big endian then ipconfigBYTE\_ORDER must be set to
pdFREERTOS\_BIG\_ENDIAN. If the microcontroller is little endian then
ipconfigBYTE\_ORDER must be set to pdFREERTOS\_LITTLE\_ENDIAN.
 

When ipconfigBYTE\_ORDER is set to pdFREERTOS\_LITTLE\_ENDIAN:
 
* FreeRTOS\_htons and FreeRTOS\_ntohs() return the value of their 16-bit parameter with the high and 
  low bytes swapped. For example, if the usValueToSwap parameter is 0x1122, then both macros return 0x2211.

* FreeRTOS\_htonl and FreeRTOS\_ntohl() return the value of their 32-bit parameter with the byte order 
  reversed. For example, if the ulValueToSwap parameter is 0x11223344, then both macros return 0x44332211.

If the microcontroller is big endian (and therefore ipconfigBYTE\_ORDER set to pdFREERTOS\_BIG\_ENDIAN) 
then the byte order of the microcontroller and the byte order of the network already match, and all four 
byte swapping macros are defined to have no effect.
 
Byte swapping macros are primarily used when specifying the IP address and port number that make up a 
socket address.


**Example usage:** 

The examples on the [FreeRTOS\_socket()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/52-FreeRTOS_SignalSocket), [FreeRTOS\_inet\_addr()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/22-inet_addr) [FreeRTOS\_sendto()](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/08-sendto) 
documentation pages demonstrate the use of FreeRTOS\_htons().
 
The example on the [FreeRTOS\_recvfrom() documentation page](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/10-recvfrom) demonstrates the use of FreeRTOS\_ntohs().
