---
title: "支持的设备"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: FreeRTOS 支持的 MCU
relatedLinks:
  - title: FreeRTOS 移植指南
    link: /Documentation/02-Kernel/03-Supported-devices/01-FreeRTOS-porting-guide/
  - title: FreeRTOS 简介
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: FreeRTOS 初学者指南
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: 下载 FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: 常见问题
    link: /Why-FreeRTOS/FAQs/Why-FreeRTOS/FAQs
---

**没看到与您的微控制器部件号和所选择的编译器供应商完全匹配的演示？**  本文提供的 
演示能够适配受支持微控制器系列中的各种微控制器。请参阅 
[创建新的 FreeRTOS 应用程序](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project) 
以及[改编 FreeRTOS 演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)文档页面。由于 
现在许多 IDE 都基于 Eclipse，因此还请参阅 
描述[如何在 Eclipse 项目资源管理器中使用虚拟路径和链接路径](/Documentation/02-Kernel/03-Supported-devices/04-Demos/IDE/Project_Workspace_Relative_File_Paths_Eclipse)的页面，
以确保无需将 RTOS 源文件复制到 Eclipse 项目目录中。

FreeRTOS 移植分为“官方支持”或“贡献”两类。 
[“官方”和“贡献”的定义](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party) 
页面描述了这两种类别以及作出区分的理由。本页仅列出了官方 RTOS 移植。

**还没有硬件？**别担心，请参阅[演示快速入门页面](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project#getting-started-with-simple-freertos-demo-projects)，其中提供了 Windows 
和 Linux 移植以及 Arm Cortex-M3 QEMU 项目相关链接。
 

| 硬件合作伙伴 | 支持的处理器系列 | 支持的工具 |
| --- | --- | --- |
| __A__ |
| [Altera](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-altera-products) | Cyclone V SoC (ARM Cortex-A9)、Nios II | Altera SoC EDS（配备 GCC 的 ARM DS-5）、配备 GCC 的 Nios II IDE |
| [ARMv8-M](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-armv8-m-products-and-simulators) <br/>请注意，此类别仅适用于模拟目标。其他 ARMv8-M 目标属于其各自的供应商类别。| ARM Cortex-M33 模拟器 | GCC（和构建 FreeRTOS ARMv8-M GCC 移植的 ARMclang） |
| [Atmel](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-atmel-now-microchip-products) | SAMV7 (ARM Cortex-M7)、SAM3 (ARM Cortex-M3)、SAM4 (ARM Cortex-M4)、SAMD20 (ARM Cortex-M0+)、SAMA5 (ARM Cortex-A5)、SAM7 (ARM7)、SAM9 (ARM9)、AT91、AVR 和 AVR32 UC3 | IAR、GCC、Keil、Rowley CrossWorks |
| __C__ |
| [Cadence](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-cadence-tensilica-products) | Tensilica Xtensa | 配备 Xtensa Xplora IDE 的 XCC |
| [CEVA](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-ceva-dsp-products) | SensPro、SensPro2、CEVA-BX1、CEVA-BX2、CEVA-X1、CEVA-X2、CEVA-XC16、CEVA-XM6、CEVA-XM4、CEVA-XC12、CEVA-XC4500 <br /> | LLVM |
| [Cortus](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-cortus-products) | APS3 | 配备 GCC 的 Cortus IDE |
| [Cypress](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-cypress-products) | PSoC 5 ARM Cortex-M3 | GCC、ARM Keil 和 RVDS - 都包含在 PSoC Creator IDE 中 |
| __F__ |
| [Freescale](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-freescale-products) | Kinetis ARM Cortex-M4、Coldfire V2、Coldfire V1、其他 Coldfire 系列、HCS12、PPC405 和 PPC440（Xilinx 实现）（小型分页内存模型），以及其他贡献的移植 | Codewarrior、GCC、Eclipse、IAR |
| __I__ |
| [Infineon](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-infineon-products) | TriCore、XMC4000 (ARM Cortex-M4F)、XMC1000 (ARM Cortex-M0) | GCC、Keil、Tasking、IAR |
| [Fujitsu（现为 ](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#fujitsu) [Spansion](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-spansion-products)[）](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#fujitsu) | FM3 ARM Cortex-M3 32 位（例如 MB91460）和 16 位（例如 MB96340 16FX） | Softune、IAR、Keil |
| __L__ |
| [Luminary Micro/Texas Instruments](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-luminary-micro-products)。另请参阅 [TI](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-texas-instruments-products)。 | 所有基于 Luminary Micro ARM Cortex-M3 和 ARM Cortex-M4 的 Stellaris 微控制器 | Keil、IAR、Code Red、CodeSourcery GCC、Rowley CrossWorks |
| __M__ |
| [Microchip](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-microchip-products)。 <br/>另请参阅 [Microsemi（现为 Microchip)](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-microsemi-now-microchip-products)。 | PIC32MX、PIC32MZ、PIC32MZ EF、PIC24、dsPIC33C、dsPIC33E、dsPIC33F、MEC14xx、CEC13xx、CEC17xx、MEC17xx、MEC51xx | [XC 编译器](https://www.microchip.com/xc) |
| [Microsemi](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-microsemi-now-microchip-products) | MiFive (RISC-V)、SmartFusion、SmartFusion2 | IAR、Keil、SoftConsole（使用  Eclipse 的 GCC） |
| __N__ |
| [NEC（现为 Renesas）](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-renesas-products) | V850（32 位）、78K0R（16 位） | IAR |
| [Nuvoton](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-nuvoton-products) | NuMicro M2351 (ARM Cortex-M23) | IAR、Keil |
| [NXP](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-nxp-products) | VEGAboard (RISC-V)、LPC55S6x(ARM Cortex-M33)、LPC1500 (ARM Cortex-M3)、LPC1700 (ARM Cortex-M3)、LPC1800 (ARM Cortex-M3)、LPC1100 (ARM Cortex-M0)、LPC2000 (ARM7)、LPC4000 (ARM Cortex-M4F/ARM Cortex-M0) | GCC、Rowley CrossWorks、IAR、Keil、LPCXpresso IDE、Eclipse、MCUXpresso IDE |
| __R__ |
| [Renesas](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-renesas-products) | RZ/A1 / RZ/A2M (ARM Cortex-A9)、RZ/T、RX700 / RX71M、RX600 / RX64M / RX62N / RX63N / RX65N、RX200、RX100、SuperH、RL78、H8/S 以及贡献的移植 | GCC、e2 studio、IAR Embedded Workbench、HEW（高性能 Embedded Workbench） |
| __S__ |
| [SiFive](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-sifive-products) | RISC-V RV32 | Freedom Studio (GCC)、IAR |
| [Silicon Labs [原为 Energy Micro]](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-silicon-labs-products) | EFM32 Gecko（Cortex-M3 和 Cortex-M4F）、8051 兼容微控制器 | Simplicity Studio (GCC)、IAR、SDCC |
| [Spansion](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-spansion-products) | FM3 ARM Cortex-M3 32 位（例如 MB91460）和 16 位（例如 MB96340 16FX） | Softune、IAR、Keil |
| [ST](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-st-microelectronics-products) | STM32（ARM Cortex-M0、ARM Cortex-M7、ARM Cortex-M3 和 ARM Cortex-M4F）、STR7 (ARM7)、STR9 (ARM9) | IAR、Atollic TrueStudio、GCC、Keil、Rowley CrossWorks |
| __T__ |
| [TI](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-texas-instruments-products) | RM48、TMS570、ARM Cortex-M4F MSP432、MSP430、MSP430X、SimpleLink、Stellaris（ARM Cortex-M3、ARM Cortex-M4F） | Rowley CrossWorks、IAR、GCC、Code Composer Studio |
| __X__ |
| [Xilinx](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-xilinx-products) | Zynq、Zynq UltraScale+ MPSoC（64 位 ARM Cortex-A53 和 32 位 ARM Cortex-R5）、Microblaze、在 Virtex4 FPGA 上运行的 PPC405、在 Virtex5 FPGA 上运行的 PPC440 | GCC |
| [Intel/x86](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-intel-ia32-and-any-x86-products) | IA32（32 位平面内存模型）、Quark SoC X1000（32 位平面内存模型）、各种仅可在实模式下运行的 x86 兼容计算机，以及 [Win32 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)。[Linux 模拟器](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Linux/FreeRTOS-simulator-for-Linux)的移植  也可用。  | GCC、Visual Studio 2010 Express、MingW、Open Watcom、Borland、Paradigm |
| Tricore、MICO32、Blackfin、Jennic、eZ80、SuperH 等 | *贡献的移植* | 贡献的移植以“原样”提供，且无法获得直接支持。 |


