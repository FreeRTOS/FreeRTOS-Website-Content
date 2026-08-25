---
title: ulApplicationGetNextSequenceNumber()
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-TCP API 引用](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/09-API-reference/01-FreeRTOS-plus-TCP-APIs)]

FreeRTOS_sockets.h

```c
uint32_t ulApplicationGetNextSequenceNumber( uint32_t ulSourceAddress,
                                             uint16_t usSourcePort,
                                             uint32_t ulDestinationAddress,
                                             uint16_t usDestinationPort );
```

ulApplicationGetNextSequenceNumber 是应用程序定义的钩子（或回调）函数， 
由 FreeRTOS-Plus-TCP 堆栈调用，以生成 4 值地址元组难以预测的序列号， 
用于 TCP 连接。

回调函数由应用程序写入程序实现，但由 TCP/IP 堆栈调用。回调函数的原型 
必须与上面的原型完全匹配（包括函数名称）。


**参数：**

+ *ulSourceAddress*
  
  设备的 IPv4 地址。

+ *usSourcePort*
  
  TCP 套接字绑定的设备端口号。

+ *ulDestinationAddress*
  
  对等方的 IPv4 地址。

+ *usDestinationPort*
  
  正在建立 TCP 连接的对等方端口。
  

**返回值：** 

此回调函数应返回一个难以预测的 32 位数字， 
用作 TCP 连接的初始序列号。

