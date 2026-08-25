---
title: "FreeRTOS_SetEndPointConfiguration()"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-TCP API Reference](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS\_IP.h

```c
void FreeRTOS_SetEndPointConfiguration( const uint32_t * pulIPAddress,
                                        const uint32_t * pulNetMask,
                                        const uint32_t * pulGatewayAddress,
                                        const uint32_t * pulDNSServerAddress,
                                        struct xNetworkEndPoint * pxEndPoint )
```

Set the current IPv4 network address configuration of the TCP/IP stack for a given IPv4 endpoint. Only non-NULL pointers will be used.

**Parameters:**

+ *`pulIPAddress`*

  Used to set the IP address being used by the IP stack. The IP address is represented as a 32-bit number in network byte order.
  
+ *`pulNetMask`*

  Used to set the net mask being used by the IP stack. The net mask is represented as a 32-bit number in network byte order.
  
+ *`pulGatewayAddress`* 

  Used to set the IP address of the gateway being used by the IP stack. The IP address is represented as a 32-bit number in network byte order.
  
+ *`pulDNSServerAddress`*

  Used to set the IP address of the DNS server being used by the IP stack. The IP address is represented as a 32-bit number in network byte order.
 
+ *`pxEndPoint`*

  The IPv4 end-point which is being set with the configuration.

**Returns:** 

No return value.
 
