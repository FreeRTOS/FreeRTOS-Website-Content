---
title: FreeRTOS_AddNetworkInterface()
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
NetworkInterface_t * FreeRTOS_AddNetworkInterface( NetworkInterface_t * pxInterface );
```

FreeRTOS_AddNetworkInterface() 用于添加新的物理网络接口。“pxInterface”指向的对象
 必须继续存在。仅网络接口函数 
 [`px${port_name}_FillInterfaceDescriptor()`](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting)
 才应调用此函数。

**参数：**

*pxInterface*
新接口的地址。该对象必须继续存在，即使在 
 [`px${port_name}_FillInterfaceDescriptor()`](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting)

**返回：**  

指向接口本身的指针。

**用法示例：**  

有关示例，请参阅 
[将 FreeRTOS 移植到不同的微控制器](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/10-Porting/03-Embedded_Ethernet_Porting) 
页面。在该页面上搜索 FreeRTOS_AddNetworkInterface()，即可找到示例源代码。

