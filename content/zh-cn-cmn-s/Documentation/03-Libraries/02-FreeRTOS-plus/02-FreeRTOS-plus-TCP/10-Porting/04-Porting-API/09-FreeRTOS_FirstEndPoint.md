---
title: FreeRTOS_FirstEndPoint()
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
NetworkEndPoint_t * FreeRTOS_FirstEndPoint( const NetworkInterface_t * pxInterface );
```

FreeRTOS_FirstEndPoint() 用于查找绑定到给定接口的第一个端点。如果给定接口为 NULL， 
 则返回任何接口的第一个端点。

**参数：**

*pxInterface*
新接口的地址。该对象必须继续存在，即使在 
 [`px${port_name}_FillInterfaceDescriptor()`](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting#pxport_name_FillInterfaceDescriptor)。

**返回：**  

当接口没有任何端点时，返回找到的第一个端点，否则返回 NULL。

**用法示例：**  

在[“将 FreeRTOS 移植到不同的微控制器”](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting)页面上提供了示例
 。在该页面上搜索 FreeRTOS_FirstEndPoint()，即可找到示例源代码。
