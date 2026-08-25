---
title: FreeRTOS_NextEndPoint()
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
NetworkEndPoint_t * FreeRTOS_NextEndPoint( const NetworkInterface_t * pxInterface,
                                           NetworkEndPoint_t * pxEndPoint );
```

FreeRTOS_NextEndPoint() 用于查找绑定到给定接口的下一个端点。如果指定接口为 NULL， 
 则返回与任何接口的当前 pxEndPoint 相连的下一个端点。

**参数：**

*pxInterface*
新接口的地址。该对象必须继续存在，即使在 
 [`px${port_name}_FillInterfaceDescriptor()`](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting#pxport_name_FillInterfaceDescriptor) 之后。
*pxEndPoint*
指当前端点。

**返回：**  

找到接口的下一个端点，或者当列表中没有更多端点时，返回 NULL。


**用法示例：**  

有关示例，请参阅 
 [移植 FreeRTOS 到不同的微控制器](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting)页面。 
 在该页面上搜索 FreeRTOS_NextEndPoint()，即可找到示例源代码。
