---
title: Source Code Organisation
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

Part of the [FreeRTOS-Plus-TCP Networking Tutorial](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)

The RTOS's TCP source code is distributed with the directory structure shown
below. Pre-packaged projects may be delivered with a slightly different
structure.

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
          |   +-Compiler_x   [Contains structure packing header files for Compiler_x]
          |   +-Compiler_y   [Contains structure packing header files for Compiler_y]
          |   +-Compiler_z   [Contains structure packing header files for Compiler_z]
          |
          +-BufferManagement [Source files that implement various buffer allocation schemes]
          |
          +-NetworkInterface
              +-MCU_x        [Contains a network driver for the MCU_x family of microcontrollers]
              +-MCU_y        [Contains a network driver for the MCU_y family of microcontrollers]
              +-MCU_z        [Contains a network driver for the MCU_z family of microcontrollers]
```
*The FreeRTOS-Plus-TCP Directory Structure*

[Back to the RTOS TCP networking tutorial index](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/04-Tutorial/01-TCP-networking-tutorial)
