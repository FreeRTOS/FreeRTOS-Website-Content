---
title: "FreeRTOS_FillEndPoint_IPv6()"
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-TCP API Reference](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS\_Routing.h

```c 
void FreeRTOS_FillEndPoint_IPv6( NetworkInterface_t * pxNetworkInterface,
                                 NetworkEndPoint_t * pxEndPoint,
                                 const IPv6_Address_t * pxIPAddress,
                                 const IPv6_Address_t * pxNetPrefix,
                                 size_t uxPrefixLength,
                                 const IPv6_Address_t * pxGatewayAddress,
                                 const IPv6_Address_t * pxDNSServerAddress, /* Not used yet. */
                                 const uint8_t ucMACAddress[ ipMAC_ADDRESS_LENGTH_BYTES ] );
```

Provide the IPv6 end-point information and append it to the FreeRTOS-Plus-TCP stack.


**Parameters:**

+ *pxNetworkInterface*

  The interface to which it belongs.

+ *pxEndPoint*

  Space for the new end-point. This memory is dedicated for the end-point and should not be freed or gotten any other purpose.

+ *pxIPAddress*

  The IP-address.

+ *pxNetPrefix*

  The prefix which will be used for this end-point.

+ *uxPrefixLength*

  The length of the above end-point.

+ *pxGatewayAddress*

  The IP-address of a device on the LAN which can serve as a gateway to the Internet.

+ *pxDNSServerAddress*

  The IP-address of a DNS server.

+ *ucMACAddress*

  The MAC address of the end-point.


**Returns:**

No return value.

