---
title: "FreeRTOS_GetAddressConfiguration()"
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
void FreeRTOS_GetAddressConfiguration( uint32_t *pulIPAddress,
                                       uint32_t *pulNetMask,
                                       uint32_t *pulGatewayAddress,
                                       uint32_t *pulDNSServerAddress );
```

Obtains the network address configuration from the TCP/IP stack.
 

**Parameters:** 

+ *pulIPAddress* 
  
  Used to return the IP address being used by the IP stack.
 
  The IP address is represented as a 32-bit number in network byte order.
 
+ *pulNetMask* 
  
  Used to return the net mask being used by the IP stack.
 
  The net mask is represented as a 32-bit number in network byte order.
 
+ *pulGatewayAddress* 
  
  Used to return the IP address of the gateway being used by the IP stack.
 
  The IP address is represented as a 32-bit number in network byte order.
 
+ *pulDNSServerAddress* 
  
  Used to return the IP address of the DNS server being used by the IP stack.
 
  The IP address is represented as a 32-bit number in network byte order.
 
 
**Example usage:** 

```c
/* FreeRTOS-Plus-TCP sockets include. */  
#include "FreeRTOS_sockets.h"  
  
void vApplicationIPNetworkEventHook( eIPCallbackEvent_t eNetworkEvent )  
{  
uint32_t ulIPAddress, ulNetMask, ulGatewayAddress, ulDNSServerAddress;  
int8_t cBuffer[ 16 ];  
  
    if( eNetworkEvent == eNetworkUp )  
    {  
        /* The network is up and configured. Print out the configuration  
           obtained from the DHCP server. */  
        FreeRTOS_GetAddressConfiguration( &ulIPAddress,  
                                          &ulNetMask,  
                                          &ulGatewayAddress,  
                                          &ulDNSServerAddress );  
  
        /* Convert the IP address to a string then print it out. */  
        FreeRTOS_inet_ntoa( ulIPAddress, cBuffer );  
        printf( "IP Address: %srn", cBuffer );  
  
        /* Convert the net mask to a string then print it out. */  
        FreeRTOS_inet_ntoa( ulNetMask, cBuffer );  
        printf( "Subnet Mask: %srn", cBuffer );  
  
        /* Convert the IP address of the gateway to a string then print it out. */  
        FreeRTOS_inet_ntoa( ulGatewayAddress, cBuffer );  
        printf( "Gateway IP Address: %srn", cBuffer );  
  
        /* Convert the IP address of the DNS server to a string then print it out. */  
        FreeRTOS_inet_ntoa( ulDNSServerAddress, cBuffer );  
        printf( "DNS server IP Address: %srn", cBuffer );  
    }  
}  
```
*Example use of the FreeRTOS\_GetAddressConfiguration() API function*
