---
title: FreeRTOS_htons(), FreeRTOS_ntohs(), FreeRTOS_htonl() and FreeRTOS_ntohl()
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
uint16_t FreeRTOS_htons( uint16_t usValueToSwap );
uint16_t FreeRTOS_ntohs( uint16_t usValueToSwap );

uint32_t FreeRTOS_htonl( uint32_t ulValueToSwap );
uint32_t FreeRTOS_ntohl( uint32_t ulValueToSwap );
```

“嵌入式网络基础知识和术语表”页面的[字节顺序和端序 (Endian)](../endian) 部分 
解释了 IP 网络中的字节顺序注意事项。

FreeRTOSIPConfig.h 中 ipconfigBYTE_ORDER 的定义
必须与运行 FreeRTOS-Plus-TCP 的微控制器相对应。如果
微控制器采用大端序，则必须将 ipconfigBYTE_ORDER 设置为
pdFREERTOS_BIG_ENDIAN。如果微控制器采用小端序，
则必须将 ipconfigBYTE_ORDER 设置为 pdFREERTOS_LITTLE_ENDIAN。


ipconfigBYTE_ORDER 设置为 pdFREERTOS_LITTLE_ENDIAN 时：

* FreeRTOS_htons 和 FreeRTOS_ntohs() 返回 16 位参数值， 
  并将高字节和低字节交换。例如，如果 usValueToSwap 参数为 0x1122 ，则两个宏均返回 0x2211。

* FreeRTOS_htonl 和 FreeRTOS_ntohl() 返回 32 位参数值， 
  并反转字节顺序。例如，如果 ulValueToSwap 参数为 0x11223344 ，则两个宏均返回 0x44332211。

如果微控制器采用大端序（因此 ipconfigBYTE_ORDER 设置为 pdFREERTOS_BIG_ENDIAN）， 
则微控制器的字节顺序和网络的字节顺序一致，上述四个字节交换宏 
不会对结果产生任何影响。

字节交换宏主要用于指定组成套接字地址的 IP 地址和 
端口号。


**用法示例：** 

[FreeRTOS_socket()](socket)、[FreeRTOS_inet_addr()](inet_addr) 和 [FreeRTOS_sendto()](sendto) 文档页面上的示例 
演示了 FreeRTOS_htons() 的用法。

[FreeRTOS_recvfrom() 文档页面](recvfrom) 上的示例演示了 FreeRTOS_ntohs() 的用法。

