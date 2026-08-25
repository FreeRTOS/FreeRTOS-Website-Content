---
title: FreeRTOS_OutputARPRequest()
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
void FreeRTOS_OutputARPRequest( uint32_t ulIPAddress );
```

强制向给定的 IP 地址发送 [ARP](../ARP) 请求。


**参数：** 

+ *ulIPAddress*

  将发送 ARP 请求的 IP 地址。


**返回：** 

void

