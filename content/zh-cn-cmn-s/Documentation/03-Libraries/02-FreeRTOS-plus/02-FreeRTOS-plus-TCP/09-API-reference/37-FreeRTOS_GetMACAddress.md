---
title: FreeRTOS_GetMACAddress()
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
const uint8_t * FreeRTOS_GetMACAddress( void );
```


**返回：** 

返回指向 NIC 使用的 MAC 地址的指针，该地址用六个单字节表示， 
每个字节位于一个连续的存储器位置。

