---
title: 源代码组织
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

[FreeRTOS-Plus-TCP 网络教程](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)节选

RTOS 的 TCP 源代码源代码按如下目录结构分布
。交付的预先打包项目结构可能稍有不同
。

```c
FreeRTOS-Plus-TCP
  |
  +-source                   [Contains the source files that implement the TCP/IP stack]
      |
      +-include              [Contains the header files for the TCP/IP stack]
      |
      +-portable
          |
          +-Compiler
          |   +-Compiler_x   [Contains [structure packing header files](Embedded_Compiler_Porting.md) for Compiler_x]
          |   +-Compiler_y   [Contains structure packing header files for Compiler_y]
          |   +-Compiler_z   [Contains structure packing header files for Compiler_z]
          |
          +-BufferManagement [Source files that implement various [buffer allocation schemes](Embedded_Ethernet_Buffer_Management.md)]
          |
          +-NetworkInterface
              +-MCU_x        [Contains a [network driver](Embedded_Ethernet_Porting.md) for the MCU_x family of microcontrollers]
              +-MCU_y        [Contains a network driver for the MCU_y family of microcontrollers]
              +-MCU_z        [Contains a network driver for the MCU_z family of microcontrollers]

```
*FreeRTOS-Plus-TCP 目录结构*

[返回 RTOS TCP 网络教程索引](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

