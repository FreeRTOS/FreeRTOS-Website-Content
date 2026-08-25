---
title: FreeRTOS_SetGatewayAddress()
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
void FreeRTOS_SetGatewayAddress( uint32_t ulGatewayAddress );
```
此函数可用于更新 FreeRTOS-Plus-TCP 设备使用的网关的 IPv4 地址， 
此前 TCP 堆栈应通过调用 [FreeRTOS_IPInit()](FreeRTOS_IPInit) 初始化。


**参数：**

+ *ulGatewayAddress*

  设备应使用的 32 位 IPv4 [网关](../router)地址（按网络内位顺序排列） 
  。 [FreeRTOS_htonl](https://www.freertos.org/FreeRTOS-Plus/FreeRTOS_Plus_TCP/API/htons_ntohs_htonl_ntohl.html)
  可用于获取 32 位网关地址的网络 endian 表示。
  

**注意事项： **

此函数不是线程安全的，应与 `taskENTER_CRITICAL`/`taskEXIT_CRITICAL` 对一起使用。 
只有在没有活动连接（UDP 或 TCP）时才应调用此函数，否则 
连接可能被切断。


**用法示例：**

有关示例，请参阅 [FreeRTOS_SetIPAddress](FreeRTOS_SetIPAddress) 页面。

