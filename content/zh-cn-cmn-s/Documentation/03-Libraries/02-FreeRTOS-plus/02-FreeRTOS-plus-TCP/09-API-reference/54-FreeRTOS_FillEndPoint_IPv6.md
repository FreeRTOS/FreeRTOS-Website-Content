---
title: "FreeRTOS_FillEndPoint_IPv6()"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-TCP API 引用](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS_Routing.h

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

提供 IPv6 端点信息并将其附加到 FreeRTOS-Plus-TCP 堆栈。


**参数：**

+ *pxNetworkInterface*

  它所属的接口。

+ *pxEndPoint*

  新端点的空间。该内存专用于终点，不得释放或用于其他目的。

+ *pxIPAddress*

  IP 地址。

+ *pxNetPrefix*

  该端点将使用的前缀。

+ *uxPrefixLength*

  上述端点的长度。

+ *pxGatewayAddress*

  局域网中可作为互联网网关的设备的 IP 地址。

+ *pxDNSServerAddress*

  DNS 服务器的 IP 地址。

+ *ucMACAddress*

  端点的 MAC 地址。


**返回：**

无返回值。

