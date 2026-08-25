---
title: 移植 FreeRTOS-Plus-TCP
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

更改嵌入式以太网驱动器和编译器


### 引言

大多数 FreeRTOS-Plus-TCP 源代码独立于用于构建代码的编译器
和运行代码的微控制器。C 编译器可以非常直接地被更改
非常直接的。在以太网 MAC 中
以太网 MAC 硬件依赖性的因素，但即使如此，更改
具有不同以太网 MAC 接口的微控制器仍然
相对直接。此页面可链接至描述如何同时执行这两项操作的页面。

本页内容：

* [使用不同的编译器](Embedded_Compiler_Porting.md)
* [创建简单的新嵌入式以太网驱动器](Embedded_Ethernet_Porting.md#creating_a_simple_network_interface_port_layer)
* [创建新的零拷贝嵌入式以太网驱动器](Embedded_Ethernet_Porting.md#creating_a_zero_copy_network_port_layer)


