---
title: FreeRTOS_MatchingEndpoint()
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[以太网驱动程序移植 API](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/04-Porting-API/01-Network_interface_functions)]


FreeRTOS_Routing.h


```c
NetworkEndPoint_t * FreeRTOS_MatchingEndpoint( const NetworkInterface_t * pxNetworkInterface,
                                               const uint8_t * pucEthernetBuffer );
```

FreeRTOS_MatchingEndpoint() 用于查找传入以太网数据包的最佳匹配端点。

**参数：**

*pxInterface*
接收数据包的接口。
*pucEthernetBuffer*
刚刚接收到的以太网数据包。

**返回：**  

应处理传入以太网数据包的端点。

**用法示例：**  

有关示例，请参阅 
 [将 FreeRTOS 移植到不同的微控制器](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting)页面。 
 在该页面上搜索 FreeRTOS_MatchingEndpoint()，即可找到示例源代码。
