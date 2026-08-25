---
title: FreeRTOS_GetNetmask()
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
uint32_t FreeRTOS_GetNetmask( void );
```


**返回：** 

返回以网络字节顺序表示的[网络掩码](../subnet)。  [FreeRTOS_inet_ntoa()](inet_ntoa)
可用于将 IP 地址转换成以点分十进制表示的更易读的 ASCII 字符串。

