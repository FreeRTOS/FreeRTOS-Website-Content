---
title: FreeRTOS_GetIPAddress()
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
uint32_t FreeRTOS_GetIPAddress( void );
```


**返回：** 

按网络字节顺序返回 NIC 的 IP 地址。  [FreeRTOS_inet_ntoa()](inet_ntoa) 
可用于将 IP 地址转换成更易读的十进制点符号 ASCII 字符串。

