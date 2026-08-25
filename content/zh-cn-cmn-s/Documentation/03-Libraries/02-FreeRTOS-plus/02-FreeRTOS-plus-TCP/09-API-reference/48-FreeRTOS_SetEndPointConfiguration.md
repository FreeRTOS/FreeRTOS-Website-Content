---
title: "FreeRTOS_SetEndPointConfiguration()"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-TCP API 引用](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS_IP.h

```c
void FreeRTOS_SetEndPointConfiguration( const uint32_t * pulIPAddress,
                                        const uint32_t * pulNetMask,
                                        const uint32_t * pulGatewayAddress,
                                        const uint32_t * pulDNSServerAddress,
                                        struct xNetworkEndPoint * pxEndPoint )
```

为给定的 IPv4 端点设置 TCP/IP 堆栈的当前 IPv4 网络地址配置。仅使用非空指针。

**参数：**

+ *`pulIPAddress`*

  用于设置 IP 堆栈使用的 IP 地址。IP 地址是一个按网络字节顺序排列的 32 位数字。
  
+ *`pulNetMask`*

  用于设置 IP 堆栈使用的网络掩码。网络掩码是一个按网络字节顺序排列的 32 位数字。
  
+ *`pulGatewayAddress`* 

  用于设置 IP 堆栈使用的网关 IP 地址。IP 地址是一个按网络字节顺序排列的 32 位数字。
  
+ *`pulDNSServerAddress`*

  用于设置 IP 堆栈使用的 DNS 服务器的 IP 地址。IP 地址是一个按网络字节顺序排列的 32 位数字。

+ *`pxEndPoint`*

  正在使用配置设置的 IPv4 端点。

**返回：** 

无返回值。

