---
title: "FreeRTOS_FillEndPoint()"
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
void FreeRTOS_FillEndPoint( NetworkInterface_t * pxNetworkInterface,
                            NetworkEndPoint_t * pxEndPoint,
                            const uint8_t ucIPAddress[ ipIP_ADDRESS_LENGTH_BYTES ],
                            const uint8_t ucNetMask[ ipIP_ADDRESS_LENGTH_BYTES ],
                            const uint8_t ucGatewayAddress[ ipIP_ADDRESS_LENGTH_BYTES ],
                            const uint8_t ucDNSServerAddress[ ipIP_ADDRESS_LENGTH_BYTES ],
                            const uint8_t ucMACAddress[ ipMAC_ADDRESS_LENGTH_BYTES ] );
```

Provide the IPv4 end-point information and append it to the FreeRTOS-Plus-TCP stack.


**Parameters:**

+ *pxNetworkInterface*

  The interface to which it belongs.

+ *pxEndPoint*

  Space for the new end-point. This memory is dedicated for the end-point and should not be freed or get any other purpose.

+ *ucIPAddress*

  The IP-address.

+ *ucNetMask*

  The prefix which shall be used for this end-point.

+ *ucGatewayAddress*

  The IP-address of a device on the LAN which can serve as a gateway to the Internet.

+ *ucDNSServerAddress*

  The IP-address of a DNS server.

+ *ucMACAddress*

  The MAC address of the end-point.


**Returns:**

No return value. 

