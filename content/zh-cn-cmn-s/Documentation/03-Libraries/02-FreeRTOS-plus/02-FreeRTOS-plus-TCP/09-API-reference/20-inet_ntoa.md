---
title: FreeRTOS_inet_ntoa()
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
void FreeRTOS_inet_ntoa( uint32_t ulIPAddress, uint8_t *pucBuffer )
```

将按网络字节顺序表示的 32 位数字的 IP 地址
转换为以点分十进制（例如 192.168.0.200）表示的字符串的宏。

标准的伯克利套接字 inet_ntoa() 函数返回一个
指向通常存储在全局缓冲区中的字符串的指针。FreeRTOS_inet_ntoa() 偏离了正常语义，
把字符串所写入的缓冲区当成了参数
。此偏差是为了确保宏是可重入和线程感知的。


**参数：** 

+ *ulIPAddress*

  按网络字节顺序表示的 32 位值的 IP 地址。  

+ *pucBuffer*

  指向缓冲区的指针，IP 地址将以十进制点符号写入该缓冲区。  


**用法示例：** 

[FreeRTOS_recvfrom() 文档页面](recvfrom)上的示例演示了
如何使用 FreeRTOS_inet_ntoa() 打印接收消息的 IP 地址。

[FreeRTOS_GetAddressConfiguration() 文档页面](FreeRTOS_GetAddressConfiguration)上的示例演示了
如何使用 FreeRTOS_inet_ntoa() 打印网络配置， 
包括节点的 IP 地址和网络掩码，以及网关和 DNS 服务器的 IP 地址。

