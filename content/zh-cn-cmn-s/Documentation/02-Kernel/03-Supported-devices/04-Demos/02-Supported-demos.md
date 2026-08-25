---
title: "支持的演示"
created: 2018-09-20 00:00:00.0 UTC
feature: standard
categories:
  - 内核
description: 面向受支持设备的演示列表
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: FreeRTOS 简介
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: FreeRTOS 初学者指南
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: 下载 FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: 常见问题
    link: /Why-FreeRTOS/FAQs
---

[[支持的设备](/Documentation/02-Kernel/03-Supported-devices/00-Supported-devices)]

**没看到与您的微控制器部件号和所选择的编译器供应商完全匹配的演示？**本文提供的演示能够适配受支持微控制器系列中的各种
微控制器。请参阅[创建新的 FreeRTOS 应用程序](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project)以及[改编 FreeRTOS 演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)文档页面。

**还没有硬件？**别担心，请参阅[演示快速入门页面](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project#getting-started-with-simple-freertos-demo-projects)，其中提供了 Windows 和 Linux 移植以及 Arm Cortex-M3 QEMU 项目相关链接。

[“官方支持”和“贡献”的 FreeRTOS 代码](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party)页面详细解释了
官方支持的和贡献的 FreeRTOS 移植之间的区别。我们针对目标为以下供应商的微控制器提供了官方支持的 FreeRTOS 演示：

1. [Altera](#针对-altera-产品的演示)
2. [ARMv8-M](#针对-armv8-m-产品和模拟器的演示)
3. [Atmel（现为 Microchip)](#针对-atmel现为-microchip-产品的演示)
4. [Cadence](#针对-cadence-tensilica-产品的演示)
5. [CEVA](#针对-ceva-dsp-产品的演示)
6. [Cortus](#针对-cortus-产品的演示)
7. [Cypress](#针对-cypress-产品的演示)
8. [Energy Micro（见 Silicon Labs）](#针对-silicon-labs-产品的演示)
9. [Freescale](#针对-freescale-产品的演示)
10. [Imagination/MIPS](#imaginationmips)
11. [Infineon](#针对-infineon-产品的演示)
12. [Luminary Micro](#针对-texas-instruments-产品的演示)
13. [Microchip](#针对-atmel现为-microchip-产品的演示)
14. [Microsemi（现为 Microchip)](#针对-microsemi现为-microchip-产品的演示)
15. [NEC](#针对-nec-产品的演示)
16. [NXP](#针对-nxp-产品的演示)
17. [Nuvoton](#针对-nuvoton-产品的演示)
18. [Raspberry Pi (Pico)](#针对-raspberry-pi-产品的演示)
19. [Renesas](#针对-renesas-产品的演示)
20. [RISC-V](#针对-risc-v-的演示) [贡献的移植，目前也有[官方移植](/Using-FreeRTOS-on-RISC-V)]
21. [SiFive](#针对-sifive-产品的演示)
22. [Silicon Labs](#针对-silicon-labs-产品的演示)
23. [Spansion（原为 Fujitsu）](#针对-spansion-产品的演示)
24. [ST Microelectronics](#针对-st-microelectronics-产品的演示)
25. [Synopsys ARC](#针对-synopsys-designware-arc-产品的演示)
26. [Texas Instruments](#针对-texas-instruments-产品的演示)
27. [Xilinx](#针对-xilinx-产品的演示)
28. [XMOS](#针对-xmos-产品的演示)
29. [x86（实模式）](#针对-intel-ia32-和各种-x86-产品的演示)
30. [模拟器和仿真器](#模拟器和仿真器)

### 针对 Altera 产品的演示

- Nios II

  - [Cycle III FPGA 上的 Nios II 软核处理器](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Altera/FreeRTOS-Nios2)

    该移植和演示应用程序针对 EBV Elektronik 提供的 DBC3C40 参考设计。

- Cyclone V SoC (ARM Cortex-A9)

  - [Cyclone V SoC 上的 Cortex-A9 HPS（硬处理器系统）](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Altera/RTOS_Altera_SoC_ARM_Cortex-A9)

    此 RTOS 演示在 Cyclone V SoC 硬接线 Cortex-A9 处理器的一个核心上运行。该演示使用了 Atlera SoC 嵌入式设计套件 (EDS)，
    其中包含一个特殊版本的基于 ARM DS-5 Eclipse 的开发环境，该环境集成了 GCC 工具链。

### 针对 ARMv8-M 产品和模拟器的演示

- Keil 模拟器

  - [ARM Cortex-M23 (ARMv8-M) 演示，适用于 Nuvoton NuMaker-PFM-M2351 板](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Nuvoton/RTOS-Cortex-M23-NuMaker-PFM-M2351-Keil)

    预配置的 FreeRTOS 项目，针对 Nuvoton NuMaker-PFM-M2351 板上的 ARM Cortex-M23 核心。

  - [ARMv8-M/ARM Cortex-M33 模拟器](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Arm-Virtual-Hardware/RTOS-Cortex-M33-Keil-Simulator)

    预配置的 FreeRTOS 项目，针对 Keil uVision ARM Cortex-M33 模拟器，并使用 armclang 编译器构建 FreeRTOS ARMv8-M GCC 移植。
    该项目演示了如何使用 ARM Cortex-M33 TrustZone 和 ARM Cortex-M33 内存保护单元 (MPU)。

  - [ARM Cortex-M33 (ARMv8-M) 演示，适用于 NXP LPCXpresso55S69 开发板](/Documentation/02-Kernel/03-Supported-devices/04-Demos/NXP/RTOS-Cortex-M33-LPC55S69-MCUXpresso-GCC)

    预配置的 FreeRTOS 项目，针对 NXP LPCXpresso55S69 开发板上的 ARM Cortex-M33 核心
    。

### 针对 Atmel(现为 Microchip) 产品的演示

**这些演示能够适配同一系列中具有足够 ROM/RAM 的各种微控制器。请参阅[创建新应用程序](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project)
以及[改编演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos) 页面。**

- 基于 ATSAMD20 ARM Cortex-M0+ 的微控制器

  - [Atmel ATSAMD20 Xplained Pro，使用 Atmel Studio](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/Atmel_SAMD20_RTOS)

    此演示包括一个简单的 blinky 示例和一个全面演示，后者包含 FreeRTOS-Plus-CLI。命令行接口使用 Atmel Software Framework 的 UART
    驱动程序进行字符输入和输出。

- 基于 SAMV7 和 SAME7 ARM Cortex-M7 的微控制器

  - [Atmel SAMV7 和 SAME7 Xplained Ultra，使用 IAR、Keil 和 GCC](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/Atmel_SAMV7_Cortex-M7_RTOS_Demo)

    [SAMV7 ARM Cortex-M7 微控制器](http://www.microchip.com/design-centers/32-bit/sam-32-bit-mcus/sam-v-mcus)演示可使用 IAR、Keil 或 Atmel
    Studio (GCC) 工具进行构建，目标平台是 [SAM V71 Xplained Ultra 评估套件](http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=ATSAMV71-XULT)。

    [SAME7 ARM Cortex-M7 微控制器](http://www.microchip.com/design-centers/32-bit/sam-32-bit-mcus/sam-e-mcus)演示可使用 Atmel Studio (GCC) 进行构建，
    目标平台是 [SAM E70 Xplained Ultra 评估套件](http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=ATSAME70-XPLD)。

    同样的 RTOS 移植也可以用于 [SAM S70](http://www.microchip.com/design-centers/32-bit/sam-32-bit-mcus/sam-s-mcus) ARM Cortex-M7 微控制器。

- 基于 AT91SAM4 ARM Cortex-M4 的微控制器
  - [Atmel SAM4L-EK 低功耗无滴答演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/Atmel_SAM4L-EK_Low_Power_Tick-less_RTOS_Demo)

    此应用程序演示了如何使用 FreeRTOS 滴答抑制功能最大限度地减少
    在 Atmel SAM4L ARM Cortex-M4 微控制器上运行的应用程序的功耗。SAM4L 专为需要极低功耗的应用程序设计。

  - [Atmel SAM4S-EK 演示，使用 Atmel Studio 和 GCC](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/Atmel_SAM4_SAM4S-EK_RTOS_Demo)

    该项目针对 SAM4S ARM Cortex-M4 微控制器，经过预配置可使用免费的 Atmel Studio IDE 进行构建，并在 SAM4S-EK 评估套件上运行。

- 基于 AT91SAM3 ARM Cortex-M3 的微控制器

  - [Atmel SAM3S-EK2 和 Atmel SAM3X-EK 演示，使用 Atmel Studio](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/Atmel_SAM3_SAM3X-EK_SAM3S-EK2_RTOS_Demo)

    该页面展示了两个运行相同演示应用程序的项目。第一个项目针对
    [SAM3S-EK2](http://www.microchip.com/developmenttools/productdetails.aspx?partno=atsam3s-ek2) 评估板上的 SAM3S 微控制器，第二个项目
    针对 [SAM3X-EK](http://www.microchip.com/developmenttools/productdetails.aspx?partno=atsam3x-ek) 评估板上的 SAM3X 微控制器。两个项目均使用
    免费的 [Atmel Studio IDE](https://www.microchip.com/en-us/tools-resources/develop/microchip-studio) 进行构建和调试。

  - [Atmel SAM3U-EK 演示，使用 IAR](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/Free-RTOS-for-Atmel-SAM3-Cortex-M3)

    该页面的演示应用程序经过预配置可在官方的 Atmel SAM3U-EK 评估套件上执行。此演示使用 FreeRTOS IAR ARM
    Cortex-M3 移植，可直接在 IAR Embedded Workbench for ARM 中进行编译和调试。

- 基于 ATSAMA5 ARM Cortex-A5 的微控制器

  - [Atmel SAMA5D3，使用 IAR](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/Atmel_SAMA5D3_Cortex-A5_IAR)

    该页面展示了一个针对低成本 [Atmel SAMA5 Xplained 板](http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=ATSAMA5D3-XPLD) 的 RTOS 演示项目。

  - [Atmel SAMA5D4，使用 IAR](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/Atmel_SAMA5D4_Cortex-A5_IAR)

    SAMA5D4 ARM Cortex-A5 RTOS 演示针对 [Atmel SAMA5D4 评估套件](http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=ATSAMA5D4-EK) (EK)。

- 基于 AT91SAM7S 和 AT91SAM7X ARM7 的微控制器

  - [Atmel SAM7S ARM7，使用 IAR 开发工具](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/portsam7iar)

    此演示使用 AT91SAM7S64-IAR 评估套件的所有组件，包括
    [AT91SAM7S-EK 开发/原型板](http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=AT91SAM7S-EK)以及
    [面向 ARM 的 IAR Embedded Workbench 开发工具](http://www.iar.com/ewarm)。此演示还包括一个 USB HID 类驱动程序示例。

  - [Atmel SAM7X ARM7，使用 GCC 和 Rowley 开发工具](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/portsam7xlwIP)

    使用 FreeRTOS GCC ARM7 移植、[Rowley CrossStudio](http://www.rowley.co.uk/arm/index.htm)、[lwIP](http://savannah.nongnu.org/projects/lwip/) 和 Atmel AT91SAM7X-EK
    开发板在完全抢占式多任务项目中创建嵌入式 Web 服务器。此演示还包括一个 USB CDC 类驱动程序（USB 转串口）示例。

  - [Atmel SAM7X ARM7，使用 GCC（命令行）](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/portsam7xlwIP#building-the-demo-using-gcc-command-line-version)

    SAM7X lwIP 项目也可以使用简单的 makefile 和标准命令行 GCC 编译器进行构建。

  - [Atmel AT91FR40008，使用 GCC 开发工具](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/portat91fr40008)

    针对 AT91 微控制器的 GCC ARM7 移植。此演示经过预配置可在 [Embest ATEB40X](http://www.embedinfo.com/English/Product/ateb40x.asp)
    原型板（Atmel AT91EB40A 克隆版）上运行。

- 基于 AT91SAM9 ARM9 的微控制器

  - [Atmel AT91SAM9XE，使用 IAR](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/ARM9-AT91SAM9-RTOS-Demo)

    此 IAR 演示在 [AT91SAM9XE-EK 评估板](http://www.microchip.com/Developmenttools/ProductDetails.aspx?PartNO=AT91SAM9XE-EK)上运行，
    支持 ARM 和 THUMB 模式。

- AVR32

  - [AVR32 AT32UC3A，使用 GCC 和 IAR 工具，随附 TCP/IP 示例](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/portAVR32)

    标准演示已移植到 GCC 和 IAR 开发工具。此演示还提供了嵌入式 Web 服务器和 TFTP 服务器示例。

- AVR/ATMegaAVR

  - [ATmega323/ATmega32 和 ATmega128，使用 WinAVR (AVR GCC) 开发工具](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/Atmel_AVR_Mega_AVR)

    此演示经过预配置可在 [STK500 原型板](http://www.microchip.com/developmenttools/productdetails.aspx?partno=atstk500)上运行，
    使用 [ATMega323 微控制器](http://www.microchip.com/wwwproducts/en/atmega32)。此演示使用[基于 GNU 的 WinAVR 开发工具](http://winavr.sourceforge.net/)进行编译，
    并为此提供了预配置的 makefile。可执行文件可以使用 AVR Studio 模拟器进行调试。

  - [ATmega323/ATmega32 和 ATmega128，使用 IAR 开发工具](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/AVR_IAR)

    与 WinAVR 移植类似，但采用 [IAR Embedded Workbench 开发工具](http://www.iar.com/)。

  - [ATmega-0，使用 XC8、AVR-GCC 和 IAR EWAVR 编译器](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/microchip-atmega-0-demo)

    此演示在 [ATmega4809 Curiosity Nano 评估套件](https://www.microchip.com/DevelopmentTools/ProductDetails/PartNO/DM320115)上运行，并且已移植到
    MPLAB X (XC8)、Atmel Studio (AVR-GCC) 和 IAR EWAVR 开发工具。

  - [AVR Dx，使用 XC8、AVR-GCC 和 IAR EWAVR 编译器](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/microchip-avr-dx-demo)

    此演示在 [AVR128DA48 Curiosity Nano 评估套件](https://www.microchip.com/DevelopmentTools/ProductDetails/PartNO/DM164151)上运行，并且已移植到
    MPLAB X (XC8)、Atmel Studio (AVR-GCC) 和 IAR EWAVR 开发工具。

### 针对 Cadence Tensilica 产品的演示

- [Xtensa 处理器](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Cadence/Tensilica_Xtensa_Free_RTOS_Demo)  **使用[[第三方](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party) RTOS 移植]**

  运行所有 RTOS 测试，使用 XCC 编译器，并通过 Xtensa Xplorer IDE 构建。

### 针对 CEVA DSP 产品的演示

这是一个[第三方](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party) RTOS 移植。有关详细信息，请访问 [https://www.ceva-dsp.com](https://www.ceva-dsp.com)。

### 针对 Cortus 产品的演示

- [Cortus APS3](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Cortus/Cortus-APS3-Free-RTOS-Demo)

  该移植和演示应用程序针对在 Spartan-3 入门板上运行的 APS3 处理器。

### 针对 Cypress 产品的演示

**这些演示能够适配同一系列中具有足够 ROM/RAM 的各种微控制器。请参阅
[创建新应用程序](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project)以及[改编演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)页面。**

- [Cypress PSoC5 CY8C5588 ARM Cortex-M3](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Cypress/FreeRTOS-port-and-demo-for-Cypress-PSoC5-CY8C5588-Cortex-M3)

  此 FreeRTOS 演示针对 PSoC5，目标平台是 [CY8CKIT-001 PSoC® 开发套件](http://www.cypress.com/?rID=37464)，
  使用 [CY8CKIT- 010 PSoC® CY8C55 系列处理器模块套件](http://www.cypress.com/?rID=43673)。此 PSoC5 演示提供了集成多种外围设备的原理图设计，
  以演示这些外围设备与 RTOS 的集成。集成的外围设备包括 UART、LCD 字符显示器和两种不同类型的定时器实现。此演示
  提供了针对 GCC 和 ARM Keil/RVDS 编译器的 PSoC Creator 项目。

### 针对 Freescale 产品的演示

**这些演示能够适配同一系列中具有足够 ROM/RAM 的各种微控制器。请参阅
[创建新应用程序](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project)以及[改编演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)页面。**

- Kinetis ARM Cortex-M0+

  - [Freescale Kinetis KL0，使用 FreeRTOS CodeWarrior Processor Expert 组件](http://mcuoneclipse.wordpress.com/2012/09/29/tutorial-freedom-with-freertos-and-kinetis-l/)  
    **[[非官方](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party)第三方演示，链接到外部网站]**

    在 FRDM-KL25Z Freedom 板上使用 FreeRTOS 的优秀第三方演示。该网页包含 FreeRTOS Processor Expert 插件链接以及如何在 Freescale CodeWarrior IDE 中使用该插件的教程。

- HCS12

  - [Motorola/Freescale MC9S12C32，使用 CodeWarrior](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Freescale-product-demos/porthcs12)

    此演示经过预配置可在 [PK-HCS12C32](http://www.softecmicro.com/products.html?type=detail&title=PK-HCS12C32) 入门套件
    （由 [SofTec Microsystems](http://www.softecmicro.com/) 提供）上运行，并使用 [CodeWarrior HC(S)12 开发工具](http://www.codewarrior.com/MW/Develop/Embedded/HC12/Default.htm)。
    该项目演示了如何在小内存模型下使用 FreeRTOS。

- [Motorola/Freescale MC9S12DP256B，使用 CodeWarrior](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Freescale-product-demos/port68hcs12)

  此演示经过预配置可在 [M68KIT912DP256](http://www.freescale.com/webapp/sps/site/prod_summary.jsp?code=M68KIT912DP256&parentCode=MC9S12A512&nodeId=0162468636K100)
  开发板（由 Freescale 提供）上运行，并使用 [CodeWarrior HC(S)12 开发工具](http://www.codewarrior.com/MW/Develop/Embedded/HC12/Default.htm)。该项目演示了如何
  在分页内存模型下使用 FreeRTOS。

- Coldfire V2
  - [Motorola/Freescale ColdFire V2，使用 CodeWarrior](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Freescale-product-demos/Free-RTOS-for-ColdFire-MCF5222x-using-CodeWarrior)

    经过预配置可在 FreeScale 提供的 [M52221DEMO 评估板](http://www.freescale.com/webapp/sps/site/prod_summary.jsp?code=M52221DEMO)上运行，
    使用 CodeWarrior for ColdFire 免费特别版。

  - [Motorola/Freescale MCF523x GCC](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Freescale-product-demos/portcoldfire)

### Fujitsu

Fujitsu 微控制器业务已被 Spansion 收购。请参阅下文的 [Spansion](#针对-spansion-产品的演示)。

### Imagination/MIPS

FreeRTOS 下载中不包含官方 MIPS 支持，但在 FreeRTOS Interactive 网站上，Imagination 直接提供并支持以下选项：

- 适用于以下核心的 GCC 移植：

  1. 传统核心：24K、34K、74K、1004K、1074K、M4K、M14K
  2. Aptiv 核心：microAptiv、interAptiv、proAptiv
  3. Warrior 核心：M5100、M5150、M6200、M6250、P5600

### 针对 Infineon 产品的演示

**这些演示能够适配同一系列中具有足够 ROM/RAM 的各种微控制器。请参阅[创建新应用程序](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project)
以及[改编演示](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party)页面。**

- AURIX™ TC3xx
  - [AURIX™ TC375，使用 AURIX™ Development Studio (ADS)](https://github.com/FreeRTOS/FreeRTOS-Partner-Supported-Demos/tree/main/AURIX_TC375_ADS)

    该演示应用程序旨在使用 [AURIX™ Development Studio (ADS)](https://www.infineon.com/cms/en/product/promopages/aurix-development-studio/) 在 Infineon 提供的 [AURIX™ TC375 lite 套件](https://www.infineon.com/cms/en/product/evaluation-boards/kit_a2g_tc375_lite/)上运行。ADS 包括一个功能齐全的集成开发环境，内含免费编译器、调试器和其他工具/库。

- XMC1000 ARM Cortex-M0

  - [XMC1100、XMC1200 和 XMC1300 启动套件，使用 IAR、GCC 和 Keil 编译器](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Infineon/Infineon-ARM-Cortex-M0-XMC1000-RTOS)

    与 XMC4000 等效产品一样，XMC1000 ARM Cortex-M0 演示经过配置可创建简单的 blinky 演示或全面的测试和演示应用程序。

- XMC4000 ARM Cortex-M4

  - [XMC4200、XMC4400 和 XMC4500 Hexagon 应用程序板演示，使用 IAR、Keil、Dave/GCC 和 Tasking 编译器](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Infineon/Infineon-ARM-Cortex-M4-XMC4000-RTOS)

    此页面的演示可构建为简单的 blinky 演示或全面的测试和演示应用程序。

  - [Hexagon 评估板上的 XMC4500，使用 IAR 和 Keil 开发工具](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Infineon/Infineon-XMC45xx-Cortex-M4_GCC_Atollic)

    此演示提供了 IAR Embedded Workbench 和 Keil uVision 项目，均针对 Infineon hexagon MXC4500 评估套件中的 CPU 板。

    **[此演示现已被[同样支持 XMC4200 和 XMC4400 设备的演示]取代](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Infineon/Infineon-ARM-Cortex-M4-XMC4000-RTOS)**

  - [Hexagon 评估板上的 XMC4500，使用 GCC 和 Atollic](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Infineon/Infineon-XMC45xx-Cortex-M4_GCC_Atollic)

    此演示提供了一个使用 GCC 编译器的 Atollic 项目，针对 Infineon hexagon MXC4500 评估套件中的 CPU 板。

    **[此演示现已被[同样支持 XMC4200 和 XMC4400 设备的演示]取代](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Infineon/Infineon-ARM-Cortex-M4-XMC4000-RTOS)**

  - [Hexagon 评估板上的 XMC4500，使用 ARM Tasking VX-toolset](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Infineon/Infineon-XMC4500-Cortex-M4-Tasking-VX-For-ARM)

    另一个针对 Infineon hexagon MXC4500 评估套件的项目，本次使用的是 ARM Tasking VX-toolset。

    **[此演示现已被[同样支持 XMC4200 和 XMC4400 设备的演示]取代](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Infineon/Infineon-ARM-Cortex-M4-XMC4000-RTOS)**

### 针对 Luminary Micro 产品的演示

在 Texas Instruments 收购 Luminary Micro 后，针对 Stellaris 微控制器的演示应用程序现列在 [Texas Instruments](#针对-texas-instruments-产品的演示) 标题下。

### 针对 Microchip  产品的演示

另请参阅 [Atmel（现为 Microchip)](#针对-atmel现为-microchip-产品的演示) 和 [Microsemi（现为 Microchip)](#针对-microsemi现为-microchip-产品的演示)

**PIC32 演示能够适配同一系列中具有足够 ROM/RAM 的各种微控制器。请参阅
[创建新应用程序](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project)以及[改编演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)页面。**

- PIC32 (MIPS)

  - [PIC32（基于 MIPS M14K 核心的 PIC32MZ 和 PIC32MZ EF）MPLAB GCC](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Microchip/PIC32MZ_RTOS_MIPS_M14K)

    此移植和演示应用程序适用于 Microchip. 提供的基于 MIPS M14K 的 PIC32MZ 和 PIC32MZ EF（带浮点）。此演示使用 XC32 编译器、MPLAB X 以及
    PIC32MZ 和 PIC32MZ EF入门套件。

  - [PIC32（基于 MIPS M4K 核心的 PIC32MX）MPLAB GCC](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Microchip/port_PIC32_MIPS_MK4)

    此移植和演示应用程适用于 Microchip. 提供的基于 MIPS M14K 的 PIC32。此演示使用 XC32 编译器和 MPLAB X，
    针对 Explorer16 开发板和 PIC32 USB II 入门套件提供了构建配置。

- MEC14xx、CEC13xx、CEC17xx、MEC17xx、MEC51xx (ARM Cortex-M4F)

  - [CEC1302 ARM Cortex-M4F、GCC、Keil、MikroC](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Microchip/Microchip_CEC1302_ARM_Cortex-M4F_Low_Power_Demo)

    这些全面的低功耗无滴答演示适用于 Microchip. 提供的基于 CEC1302 ARM Cortex-M4F 的微控制器。此项目演示了 CEC1302
    在聚合和非聚合中断方案中的使用。

- PIC24 & dsPIC

  - [Microchip PIC24 和 dsPIC33 MPLABX](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Microchip/portpic24_dspic)

    适用于 Microchip PIC24 和 dsPIC33 MCU 的移植和演示应用程序。大多数演示都针对 Explorer16 评估板
    并使用 MPLAB&reg XC16 或 XC-DSC 编译器。有关目标板和所用编译器的详细信息，请参阅各个演示的自述文件。

- PIC18

  请注意，PIC18 因采用分段内存，不适合与 RTOS 一起使用。

  - [Microchip PIC18 MPLAB](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Microchip/PIC18-with-c18-compiler)

    此演示经过预配置可在 Forest Electronic Developments 提供的 [40 引脚 PICmicro 原型板](https://www.fored.co.uk/)
    （配备了 PIC18F452 微控制器）上运行。此平台成本极低，具备系统内编程功能。此演示还使用了 MPLAB 开发工具，
    包括 [MPLAB IDE](http://www.microchip.com/stellent/idcplg?IdcService=SS_GET_PAGE&nodeId=1406&dDocName=en019469) 和
    [MPLAB C18 编译器](http://www.microchip.com/stellent/idcplg?IdcService=SS_GET_PAGE&nodeId=1406&dDocName=en010014)。

  - [Microchip PIC18 wizC](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Microchip/portwizc)

    此移植使用 [wizC 集成开发环境](http://www.fored.co.uk/html/wiz_c_-__pic_c_compiler.HTM)
    （由 [Forest Electronic Developments](http://www.fored.co.uk/) 提供）创建。此移植还可与
    同样由 Forest Electronic Developments 提供的 [FED C 编译器](http://www.fored.co.uk/html/c_compilers.html)一起使用。

### 针对 Microsemi（现为 Microchip) 产品的演示

**这些演示能够适配同一系列中具有足够 ROM/RAM 的各种微控制器。请参阅
[创建新应用程序](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project)以及[改编演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)页面。**

- 基于 RISC-V 的微控制器

  - [MiFive M2GL025 创意板和 Renode，使用 GCC 和 SoftConsole IDE](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Microsemi-now-Microchip/RTOS-RISC-V-SoftConsole-Renode-SiFive)

    此演示最初目标为 Future Electronics 提供的 Microchip （原为 MicroSemi）M2GL025 创意板上的 MiFive RISC-V 核心。目标现已改为
    同一创意板的 Renode 软件仿真。

### 针对 NEC 产品的演示

在 NEC 与 Renesas 合并为 Renesas 品牌后，针对 NEC 微控制器的演示应用程序现列在 [Renesas](#针对-renesas-产品的演示) 标题下。

### 针对 Nuvoton 产品的演示

**这些演示能够适配同一系列中具有足够 ROM/RAM 的各种微控制器。请参阅
[创建新应用程序](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project)以及[改编演示](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party)页面。**

- 基于 ARM Cortex-M23 的微控制器

  - [Nuvoton NuMaker-PFM-M2351 板演示，使用 Keil uVision 和 IAR Embedded Workbench](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Nuvoton/RTOS-Cortex-M23-NuMaker-PFM-M2351-Keil)

    此演示针对 Nuvoton NuMaker-PFM-M2351 板上的 ARM Cortex-M23 核心。这些预配置项目演示了如何使用 ARM Cortex-M23 TrustZone 和
    ARM Cortex-M23 内存保护单元 (MPU)。

### 针对 NXP 产品的演示

**这些演示能够适配同一系列中具有足够 ROM/RAM 的各种微控制器。请参阅
[创建新应用程序](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project)以及[改编演示](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party)页面。**

- 基于 RISC-V 的微控制器

  - [VEGAboard PULP RI5CY 演示，使用 GCC 和 Eclipse](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Others/RTOS-RISC-V-Vegaboard_Pulp)

    此演示针对 VEGAboard 多核（两个 Arm 核心、两个 RISC-V 核心）RV32M1 MCU 上的 RI5CY 核心。

- 基于 ARM Cortex-M33 的微控制器

  - [NXP LPCXpresso55S69 开发板演示，使用 GCC 和 MCUXpresso](/Documentation/02-Kernel/03-Supported-devices/04-Demos/NXP/RTOS-Cortex-M33-LPC55S69-MCUXpresso-GCC)

    此演示针对 LPCXpresso55S69 开发板上的 ARM Cortex-M33 核心。此预配置项目演示了如何使用 ARM Cortex-M33
    TrustZone 和 ARM Cortex-M33 内存保护单元 (MPU)。

- 基于 ARM Cortex-M4F 的微控制器

  - [NXP LPC4350 演示，使用 Keil/RVDS](/Documentation/02-Kernel/03-Supported-devices/04-Demos/NXP/FreeRTOS-for-LPC4350-Cortex-M4F-and-Cortex-M0-Keil)

    此应用程序演示了在双核 LPC4350 的 ARM Cortex-M4 核心上运行的 FreeRTOS ARM Cortex-M4F RVDS 移植。此演示经过预配置
    可在 Hitex LPC4350 评估板上运行。LPC4300 微控制器配置为以 204 MHz 运行。此演示包括基础的 LED 闪烁配置
    和全面配置。全面配置可创建超过 40 项任务，包括测试 FreeRTOS 移植本身的任务。

- 基于 ARM Cortex-M3 的微控制器

  - NXP LPC1830，演示 FreeRTOS-Plus-UDP

    此演示在 NGX Technologies 提供的 LPC1830 XPlorer 板上运行 [FreeRTOS-Plus-UDP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP)。此项目
    使用基于 FreeRTOS LPCXpresso Eclipse 的 IDE 构建。

  - [NXP LPC1768，演示 FreeRTOS-Plus-IO 和 FreeRTOS-Plus-CLI](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/01-FreeRTOS_Plus_IO)

    使用 FreeRTOS-Plus-CLI 与 FreeRTOS-Plus-IO 以及托管在 SD 卡上的 FatFS 文件系统进行交互的全面演示。FreeRTOS-Plus-IO 管理 UART、
    I2C 和 SPI 移植。此演示使用免费的 LPCXPresso IDE 构建并在 LPCXpresso 基板上运行。

- 基于 ARM Cortex-M0 的微控制器

  - [NXP LPC1114 LPCXpresso](/Documentation/02-Kernel/03-Supported-devices/04-Demos/NXP/FreeRTOS-for-Cortex-M0-LPC1114-LPCXpresso)

    此应用程序演示了如何在低成本 LPCXpresso LPC1114 硬件上使用 FreeRTOS ARM Cortex-M0 GCC 移植。演示中使用的是免费版 LPCXpresso IDE。

  - [NXP LPC51U68 低功耗演示，使用 LPCXpresso (GCC)、Keil 和 IAR](/Documentation/02-Kernel/03-Supported-devices/04-Demos/NXP/FreeRTOS_LPCXpresso51U68_IAR_Keil_GCC)

    演示了如何在 ARM Cortex-M0+ LPC51U68 上使用三种不同的编译器实现无滴答低功耗模式。

- 基于 LPC2000 ARM7 的微控制器

  - [NXP ARM7，使用 Keil 开发工具](/Documentation/02-Kernel/03-Supported-devices/04-Demos/NXP/portlpckeil)

    此演示经过预配置可在 [MCB2100 开发/原型板](http://www.keil.com/mcb2100)上运行。开发工具提供了出色的调试器
    和外围设备模拟器，允许在模拟器内执行整个演示应用程序。这是了解 FreeRTOS 的极佳途径！

  - [NXP ARM7，使用 IAR 开发工具](/Documentation/02-Kernel/03-Supported-devices/04-Demos/NXP/portlpciar)

    [IAR](http://www.iar.com/ewarm) LPC2000 演示同样经过预配置可在 MCB21000 开发板上执行。

  - [NXP ARM7，使用 GCC](/Documentation/02-Kernel/03-Supported-devices/04-Demos/NXP/portlpc2106)

    此演示经过预配置可在配备 LPC2106 微控制器的 LPC-P2106 原型板上运行。此原型版成本极低，具备系统内
    编程功能。此移植使用 Win32 版本的 [ARM7 GNU 开发工具](http://www.gnuarm.com/)。

  - [NXP ARM7，使用 Rowley 开发工具和 Rowley 开发板](/Documentation/02-Kernel/03-Supported-devices/04-Demos/NXP/portlpc2138)

    此演示基于 GCC 移植，使用 [Rowley Associates](http://www.rowley.co.uk/) 的 CrossWorks 集成开发环境，
    针对 [CrossFire LPC2138 嵌入式评估套件](http://www.rowley.co.uk/crossfire/crossfire_lpc2138.htm)

  - [NXP ARM7，使用 Rowley 开发工具和 Olimex 开发板](/Documentation/02-Kernel/03-Supported-devices/04-Demos/NXP/portrowleylpc2124)

    此演示基于 GCC 移植，使用 [Rowley Associates](http://www.rowley.co.uk/) 的 CrossWorks 集成开发环境，并包含嵌入式 TCP/IP 堆栈和嵌入式 Web 服务器。

### 针对 Raspberry Pi 产品的演示

- [Pico](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Raspberry-Pi/smp-demos-for-the-raspberry-pi-pico-board)

  这些演示使用 FreeRTOS 对称多处理 (SMP) 版本的内核，针对 Raspberry Pi Pico 板，该板使用
  Raspberry Pi 提供的 RP2040 微控制器，具有双核 ARM Cortex M0+ 处理器。

### 针对 Renesas 产品的演示

**这些演示能够适配同一系列中具有足够 ROM/RAM 的各种微控制器。请参阅
[创建新应用程序](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project)以及[改编演示](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party)页面。**

- RZ/A (ARM Cortex-A9)
  - RZ 嵌入式处理器（ARM Cortex-A9 核心），使用 GCC 开发工具

    **[[非官方](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party)第三方演示，链接到 FreeRTOS Interactive 网站]**

    另一个针对 Renesas RZ/A1 嵌入式处理器的 FreeRTOS 演示应用程序，本次使用的是 GCC 工具链。

- RZ/T (ARM Cortex-R4F)

  - [RZ/T 嵌入式处理器（ARM Cortex-R4F 核心），使用 Renesas、GCC 和 IAR 编译器](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Renesas/Renesas_RZ-T_Cortex-R4F-RTOS)

    针对 Renesas RZ/T 嵌入式处理器（具有 ARM Cortex-R 核心）的 FreeRTOS 演示应用程序。目前提供三个项目，都可以使用
    IAR、GCC 和 Renesas 编译器构建演示。GCC 和 Renesas 编译器项目使用 e2studio IDE。此演示包括使用 FreeRTOS-Plus-CLI 实现的命令行接口。

- RX700

  - [RX700 RX71M（RXv2 核心），使用 Renesas、GCC 和 IAR 编译器](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Renesas/RX700_RX71M_Renesas_GCC_IAR)

    针对 Renesas RX71M 微控制器（具有 RXv2 核心）的 FreeRTOS 演示应用程序。目前提供三个项目，都可以使用 IAR、
    GCC 和 Renesas 编译器构建演示。GCC 和 Renesas 编译器项目使用 e2studio IDE。此演示包括使用 FreeRTOS-Plus-CLI 实现的命令行接口。

- RX600

  - [RX64M（RXv2 核心），使用 e2studio](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Renesas/RX64M_RTOS_Renesas_GCC_e2studio)

    目前提供两个 e2studio 项目，均针对 RX64M RSK（Renesas 入门套件）。一个项目使用 Renesas RX 编译器，另一个项目使用 GCC 编译器。

- RX200

  - [RX231，使用 Renesas、GCC 和 IAR 编译器](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Renesas/RX231_RTOS_Renesas_GCC_IAR)

    针对 Renesas RX231 微控制器（具有 RXv2 核心）的 FreeRTOS 演示应用程序。目前提供三个项目，都可以使用 IAR、
    GCC 和 Renesas 编译器构建演示。GCC 和 Renesas 编译器项目使用 e2studio IDE。

  - [RX210，使用 Renesas 编译器和 HEW IDE](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Renesas/Free_RTOS_For_Renesas_RX210_HEW)

    记录了 [Renesas RX210](http://www.renesas.eu/products/mpumcu/rx/rx200/rx210/rx210_root.jsp) FreeRTOS 移植和演示应用程序
    （使用 [Renesas RX](http://www.renesas.com/compiler) 编译器和 [HEW IDE](http://www.renesas.com/hew)）。此项目经过预配置可在 RSKRX210 入门套件上运行。

- RX100

  - [RX113，使用 Renesas、GCC 和 IAR 编译器](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Renesas/RX113_RTOS_Renesas_GCC_IAR)

    针对 Renesas RX113 微控制器的 FreeRTOS 演示应用程序。目前提供三个项目，都可以使用 IAR、GCC 和 Renesas 编译器构建演示。
    GCC 和 Renesas 编译器项目使用 e2studio IDE。此演示包括使用 FreeRTOS-Plus-CLI 实现的命令行接口。

  - [针对 RX100 的无滴答低功耗演示，使用 IAR、GCC 和 Renesas 编译器](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Renesas/RX100_RSK_Low_Power_Tick-less_RTOS_Demo)

    该应用程序演示了如何在 RX100 微控制器上使用 FreeRTOS 滴答抑制功能来减少功耗。此演示针对
    IAR、带 GCC 的 e2studio 和带 Renesas 编译器的 e2studio 提供了相关项目。

- RL78 16 位微控制器

  - [RL78/G13、RL78/G14、RL78/G1C、RL78/L13 和 RL78/G1A，使用 IAR](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Renesas/RTOS_RL78_IAR_Demos)

    IAR 演示，具有针对以下 RL78 芯片和硬件的构建配置：YRPBRL78G13 RL78/G13 推广板、YRDKRL78G14 RL78/G14 开发板、
    RSKRL78G1C RL78/G1C 入门套件、RSKRL78L13 RL78/L13 入门套件、RL78/G1A TB RL78/G1A 目标板。支持远内存模型和近内存模型。

  - [RL78/G13 推广板](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Renesas/FreeRTOS-port-and-demo-for-Renesas-RL78-YRPBRL78G13-Promo-Board)

    针对 RL78/G13 推广板的 IAR 演示。支持远内存模型和近内存模型。

- [H8/S](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Renesas/porth8s)

  此演示经过预配置
  可直接在 [EDK2329 原型嵌入式计算机](http://america.renesas.com/fmwk.jsp?cnt=edk_2329_software_tools_root.jsp&fp=/products/tools/introductory_evaluation_tools/starterkits_evaluation_boards/edk2329/)
  （由 [Renesas (Hitachi)](http://www.renesas.com/) 提供）上运行。该计算机配备
  [H8/S2329 处理器](http://america.renesas.com/fmwk.jsp?cnt=h8s2329_h8s2328_root.jsp&fp=/products/mpumcu/h8s_family/h8s2300_series/h8s2329_h8s2328_group/)。
  此移植使用 [GNU H8 编译器](http://www.gnuh8.com/) 和 HEW GUI。

- [V850ES 32 位微控制器](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Renesas/NEC-V850-RTOS)

  IAR 演示，包含多个不同 Renesas 目标板和 V850ES/Fx3 入门板的配置。支持大型和小型内存模型。

- [78K0R 16 位微控制器](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Renesas/NEC-78K-RTOS)

  IAR 演示，包含不同 Renesas 目标板的配置。支持远内存模型和近内存模型。

### 针对 RISC-V 的演示

- RISC-V Spike 模拟器 GCC

  **[[非官方](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party)第三方演示，链接到 FreeRTOS Interactive 网站。
  目前也有[官方移植](/Using-FreeRTOS-on-RISC-V)]**

  此移植自动根据 GCC 设置的宏定义进行自配置，以适应 32 位和 64 位 RISC-V 架构。此演示应用程序
  在 [Spike 模拟器](http://riscv.org/software-tools/risc-v-isa-simulator/)上以 64 位模式运行，需要安装 riscv GCC 编译器和 Spike 模拟器
  才能成功构建。

### 针对 SiFive 产品的演示

- [SiFive HiFive1 RevB，使用 Freedom Studio (GCC) 和 IAR](/Documentation/02-Kernel/03-Supported-devices/04-Demos/SiFive/RTOS-RISC-V-FreedomStudio-IAR-HiFive-RevB)

  两个为 HiFive1 RevB 评估板上的 RISC-V 核心创建演示应用程序的预配置项目：一个项目使用 SiFive 的 Freedom Studio 与 GCC，
  另一个项目使用 IAR 提供的 Embedded Workbench for IAR。预配置的 SiFive Freedom Studio 项目，在 sifive_e QEMU 模型中使用 GCC 和 GDB 构建并运行 FreeRTOS RISC-V 演示
  。

### 针对 Silicon Labs 产品的演示

**FreeRTOS ARM Cortex-M 移植可以在所有 Silicon Labs ARM Cortex-M 微控制器上运行。请参阅[创建新应用程序](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project)
以及[改编演示](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party)页面。**

- [EFM Giant Gekco 和 Pearl Gecko，使用 Simplicity Studio 和 GCC](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Silicon-labs/EFM32-Giant-Gecko-Pearl-Gecko-tickless-RTOS-demo)

  此页面上的演示展示了 FreeRTOS 滴答抑制功能，该功能可用于降低 EFM32 Giant Gecko 和 EFM32 Pearl Gecko 入门套件的
  功耗。这两个演示都使用免费的基于 Eclipse 的 Simplicity Studio IDE 和 GCC 构建。

- [EFM32G890F128 (ARM Cortex-M3)，使用 IAR](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Silicon-labs/EFM32)

  旧版移植和演示应用程序，使用 IAR Embedded Workbench 开发工具，针对基于 ARM Cortex-M3 的 EFM32G890F128 微控制器。

  **[此演示现已被 [Giant 和 Pearl Gecko 入门套件演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Silicon-labs/EFM32-Giant-Gecko-Pearl-Gecko-tickless-RTOS-demo)取代，这两个演示还展示了
  如何使用 FreeRTOS 无滴答闲置模式降低功耗]**

- [Cygnal 8051](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Energy-Micro-see-Silicon-Labs/portcygn)

  此移植使用直接由 [Silicon Labs](http://www.silabs.com/) 提供的原型板，并使用开源 [SDCC 编译器](http://sdcc.sourceforge.net/)。

### 针对 Spansion 产品的演示

**这些演示能够适配同一系列中具有足够 ROM/RAM 的各种微控制器。请参阅[创建新应用程序](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project)
以及[改编演示](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party)页面。**

- 32 位微控制器

  - [Spansion FM3 ARM Cortex-M3 MCU](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Spasion-was-Fujitsu/FreeRTOS-for-Fujitsu-FM3-MB9BF500-microcontrollers)

    针对 Spansion [FM3 微控制器](http://mcu.emea.fujitsu.com/mcu_product/overview_32FM3.htm) 的 FreeRTOS ARM Cortex-M3 演示应用程序。此演示提供了 IAR 和 Keil 两个项目，
    均经过预配置，可分别在 [SK-FM3-100PMC](http://mcu.emea.fujitsu.com/mcu_tool/detail/SK-FM3-100PMC.htm)
    和 [SK-FM3-64PMC1](http://mcu.emea.fujitsu.com/mcu_tool/detail/SK-FM3-64PMC1.htm) 入门套件评估板上运行。

  - [Spansion MB91460 32 位 MCU](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Spasion-was-Fujitsu/RTOS-port-Fujitsu-FR-MCU-MB91460)

    针对 Spansion 提供的 MB91460 系列 32 位 MCU 的演示。此移植经过预配置可在
    [SK-91F467-FLEXRAY](http://mcu.emea.fujitsu.com/mcu_tool/detail/SK-91F467-FLEXRAY.htm) 入门套件上运行，并使用
    [Softune](http://mcu.emea.fujitsu.com/mcu_tool/detail/SWB_(FR)_V6.htm) 编译器、IDE 和调试器。

- 16 位 16FX 微控制器

  - [Spansion MB96340 16 位 MCU](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Spasion-was-Fujitsu/RTOS-port-Fujitsu-16FX-MB96340)

    针对 Spansion 提供的 MB96340 系列 16 位 MCU (16FX)  的演示。此移植经过预配置可在
    [SK-16FX-EUROScope](http://mcu.emea.fujitsu.com/mcu_tool/detail/SK-16FX-EUROSCOPE.htm) 入门套件上运行，并使用
    [Softune](http://mcu.emea.fujitsu.com/mcu_tool/detail/SWB_(F2MC-16)_V3.htm) 编译器、IDE 以及 Euroscope 调试器。

### 针对 ST Microelectronics 产品的演示

**这些演示能够适配同一系列中具有足够 ROM/RAM 的各种微控制器。请参阅
[创建新应用程序](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project)以及[改编演示](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party)页面。**

- 基于 STM32F7 ARM Cortex-M7 的微控制器

  - [STM32H745 双核 (AMP) 演示，使用 IAR EWARM](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ST-Microelectronics/STM32H7_Dual_Core_AMP_RTOS_demo)

    此双核 RTOS 演示是一个简单的非对称多处理 (AMP) 核间通信项目，
    使用 [FreeRTOS 消息缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers)实现。该演示随附了
    [一篇文章](/Community/Blogs/2020/simple-multicore-core-to-core-communication-using-freertos-message-buffers)，专门描述
    一些内部实现细节。

    此演示经过预配置可在 [STM32H745I 发现板](https://www.st.com/en/evaluation-tools/stm32h745i-disco.html)上运行，并使用 IAR 编译器
    和 [Embedded Workbench IDE](https://www.iar.com/products/architectures/arm/) 构建。STM32H7xx 有一个 ARM Cortex-M4 核心和一个 ARM Cortex-M7 核心。这两个核心运行同一个 ARMv7-M FreeRTOS 移植。

  - [STM32F7 演示，使用 IAR EWARM 和 Keil uVision](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ST-Microelectronics/ST_STM32F7_Cortex-M7_RTOS_Demo)

    此 RTOS 演示针对 STM32756G-EVAL 评估套件，该套件包含一个 [STM32F7 ARM Cortex-M7 微控制器](http://www.st.com/web/en/catalog/mmc/SC1169/SS1858)。
    该演示针对 [IAR](http://www.iar.com/ewarm) 和 ARM Keil 工具提供了预配置的构建项目。

- 基于 STM32F4 ARM Cortex-M4F 的微控制器

  - [STM32F407 演示，使用 IAR EWARM](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ST-Microelectronics/FreeRTOS-for-STM32F4xx-Cortex-M4F-IAR)

    此应用程序演示了如何在基于 ARM Cortex-M4 的 STM32F407 上使用 FreeRTOS ARM Cortex-M4F IAR 移植。此演示经过预配置可在 STM32F407ZF-SK 入门
    套件评估板上运行。此演示包括基础的 LED 闪烁配置和全面配置。全面配置可创建超过 40 项任务，
    包括测试 FreeRTOS 移植本身的任务。

- 基于 STM32 ARM Cortex-M3 的微控制器

  - [STM32L 上的极低功耗无滴答操作](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ST-Microelectronics/STM32L-discovery-low-power-tickless-RTOS-demo)

    此项目演示了如何使用 FreeRTOS 滴答抑制功能最大限度地减少在 ST 的 STM32L 低功耗 ARM Cortex-M3 微控制器上
    运行的应用程序的功耗。STM32L 专为需要极低功耗的应用程序设计。

  - [低功耗 ST STM32 (STM32L152)，使用 IAR Embedded Workbench](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ST-Microelectronics/Free-RTOS-for-Cortex-M3-STM32-STM32L152-EVAL)

    此 FreeRTOS 演示应用程序针对 [STMicroelectronics](http://www.st.com/) 提供的低功耗 [STM32L152 微控制器](http://www.st.com/internet/mcu/product/248824.jsp)。
    此演示使用 IAR Systems 提供的 [IAR Embedded Workbench for ARM V6.10](http://www.iar.com/ewarm)，针对 STMicroelectronics 提供的 STM32L152-EVAL 官方评估板。

  - [ST STM32 Value Line 演示，使用 Atollic TrueStudio](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ST-Microelectronics/FreeRTOS-for-Cortex-M3-STM32-STM32F100-Discovery)

    使用 ARM Cortex-M3 GCC 移植以及
    [Atollic TrueStudio IDE](https://www.st.com/content/st_com/en/products/development-tools/software-development-tools/stm32-software-development-tools/stm32-ides/truestudio.html)。
    此演示经过预配置可在 [STM32 Value Line 发现板](http://www.st.com/stm32-discovery)上运行，该发现板配备了
    [STM32F100 微控制器](http://www.st.com/internet/mcu/product/216844.jsp)。

  - [ST STM32 ARM Cortex-M3，使用 IAR 开发工具](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ST-Microelectronics/portstm32iar)

    使用 ARM Cortex-M3 IAR 移植在 STM32 评估板上创建演示应用程序。

  - [ST STM32 ARM Cortex-M3，使用 GCC 编译器和 RIDE IDE](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ST-Microelectronics/RTOS_Demo_STM32_Primer_Ride)

    此演示使用新型 STM32 Primer 评估板。

- 基于 STM32F0 ARM Cortex-M0 的微控制器

  - [STM32F051 演示，使用 IAR EWARM](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ST-Microelectronics/FreeRTOS-for-STM32F051-Cortex-M0-IAR)

    此应用程序演示了如何在 ST 提供的 STM320518-EVAL 板上使用 FreeRTOS ARM Cortex-M0 IAR 移植，该板配备了 STM32F051 微控制器。

- 基于 STR7 ARM7 的微控制器

  - [ST Microelectronics STR75x ARM7，使用 IAR 开发工具](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ST-Microelectronics/portstr75xiar)

    此应用程序经过预配置可在 STMicroelectronics 提供的 [STR750 EVAL](http://www.st.com/internet/evalboard/product/132197.jsp) 评估板上运行，
    演示了如何在 ST STR750 ARM7TDMI 微控制器上使用 FreeRTOS，该微控制器配备了[面向 ARM 的 IAR Embedded Workbench 开发工具](http://www.iar.com/ewarm)。

  - [ST Microelectronics STR75x ARM7，使用 Raisonance RIDE 开发工具](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ST-Microelectronics/portstr75xiar)

    此应用程序同样经过预配置可在 STMicroelectronics 提供的 [STR750 EVAL](http://www.st.com/internet/evalboard/product/132197.jsp) 评估板上运行，
    演示了如何在 ST STR750 ARM7TDMI 微控制器上使用 FreeRTOS，该微控制器配备了 [Raisonance RIDE IDE](https://www.raisonance.com/ride7.html)
    与 [GNUARM GCC 工具链](http://www.gnuarm.org/)进行交互的接口。

  - [ST Microelectronics STR71x ARM7，使用 IAR 开发工具](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ST-Microelectronics/portstr71xiar)

    此演示经过预配置可在 [IAR STR712 KickStart 开发套件](http://www.st.com/internet/evalboard/product/152464.jsp)上运行，使用 KickStart 原型板、
    USB JTAG 调试器接口和[面向 ARM 的 IAR Embedded Workbench 开发工具](http://www.iar.com/ewarm)。

- 基于 STR9 ARM9 的微控制器

  - [STMicroelectronics STR9 ARM9，使用 IAR 开发工具](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ST-Microelectronics/portstr912iar)

    这是首个 FreeRTOS ARM9 移植。此演示应用程序经过预配置可在 STR910-EVAL 开发板上运行。它包括使用 uIP v1.0 的 Web 服务器演示。

### 针对 Synopsys DesignWare ARC 产品的演示

FreeRTOS 下载中不包含官方 ARC 支持，但希望在 DesignWare ARC 微控制器上运行 RTOS 的用户可以使用以下选项：

- [embARC](https://embarc.org/) 开放软件平台包含软件和文档，有助于加速开发基于 DesignWare ARC 处理器的嵌入式系统和 IoT 系统。
- 我们的官方合作伙伴公司 WITTENSTEIN high integrity systems 可提供适用于各种 ARC 处理器的 [OPENRTOS](http://www.highintegritysystems.com/openrtos)。

### 针对 Texas Instruments 产品的演示

**这些演示能够适配同一系列中具有足够 ROM/RAM 的各种微控制器。请参阅
[创建新应用程序](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project)以及[改编演示](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party)页面。**

在 Texas Instruments 收购 Luminary Micro 后，此部分现包括针对 Stellaris 微控制器的演示。

- SimpleLink IoT 微控制器

  - [CC3220，使用 Code Composer Studio (CCS)](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Texas-Instruments/TI_CC3220_SimpleLink_FreeRTOS_Demo)

    针对 SimpleLink CC3220SF 无线 (WiFi) 微控制器 LaunchPad 开发套件。

- 基于 MSP432 ARM Cortex-M4F 的微控制器

  - [MSP432P401R，使用 IAR、Keil、CCS](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Texas-Instruments/TI_MSP432_Free_RTOS_Demo)

    此演示应用程序针对 Texas Instruments MSP432 微控制器，该微控制器是使用 ARM Cortex-M4F 核心的 MSP430 低功耗微控制器的变体。
    提供的预配置 MSP432 项目针对 MSP432P401R Launchpad 开发套件，使用了 IAR、Keil 和 CCS 开发工具。

- 基于 MSP430 和 MSP430X 的微控制器

  - [MSP430FR5969，使用 IAR Embedded Workbench 和 Code Composer Studio](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Texas-Instruments/MSP430FR5969_Free_RTOS_Demo)

    此演示针对 [Texas Instruments MSP430FR5969](http://www.ti.com/product/msp430fr5969) 低功耗微控制器，该微控制器具有 16 位 MSP430X 核心。
    提供的预配置项目针对 [MSP-EXP430FR5969](http://www.ti.com/tool/msp-exp430fr5969#0) Launchpad 开发套件，
    使用了 [IAR](https://www.iar.com/iar-embedded-workbench/texas-instruments/msp430/) 和 [Code Composer Studio](http://www.ti.com/ccs) (CCS) MSP430 编译器。

  - [MSP430X 核心 (MSP430F5438)，使用 IAR Embedded Workbench](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Texas-Instruments/Free-RTOS-for-MSP430X-MSP430F5438-Experimenter-Board-using-IAR)

    此 FreeRTOS 演示应用程序适用于 [MSP430X/MSP430F5438 微控制器](http://focus.ti.com/docs/prod/folders/print/msp430f5438.html)
    （由 [Texas Instruments](http://www.ti.com/) 提供）。此演示使用 IAR Systems 提供的[面向 MSP430 的 IAR Embedded Workbench](https://www.iar.com/products/architectures/iar-embedded-workbench-for-msp430/)，针对
    TI 提供的官方 [MSP-EXP430F5438](http://focus.ti.com/docs/toolsw/folders/print/msp-exp430f5438.html) 实验板。

  - [MSP430X 核心 (MSP430F5438)，使用 Code Composer Studio 4](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Texas-Instruments/Free-RTOS-for-MSP430X-MSP430F5438-Experimenter-Board-using-CCS)

    此版本的 FreeRTOS MSP430X 演示应用程序同样针对 [MSP430X/MSP430F5438 微控制器](http://focus.ti.com/docs/prod/folders/print/msp430f5438.html)
    （由 [Texas Instruments](http://www.ti.com/) 提供），但使用 TI 自有的 [Code Composer Studio 4](http://focus.ti.com/docs/toolsw/folders/print/ccstudio.html) 开发工具。
    **此演示现已被取代，请参阅上文的 MSP-EXP430FR5969 演示**

  - [MSP430，使用 Rowley CrossWorks](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Texas-Instruments/portmspcrossworks)

    此演示经过预配置可在 [SoftBaugh](http://www.softbaugh.com/) 提供的 [ES449 原型板](http://www.softbaugh.com/ProductPage.cfm?strPartNo=ES449)上运行，
    该原型板配备了 [MSP430F449](http://focus.ti.com/docs/prod/folders/print/msp430f449.html) 微控制器。该原型板包括内置 LCD，非常适合
    调试。此移植使用 Rowley Associates 的 [CrossWorks](http://www.rowley.co.uk/) 工具套件以及 FETP JTAG 调试器，包括两个略有不同的移植
    实现。

  - [MSP430，使用 MSPGCC (GCC)](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Texas-Instruments/portmspgcc)

    与 MSP430 CrossWorks 移植类似，但使用的是 [MSPGCC 开发工具](http://mspgcc.sourceforge.net/)，其中包括预构建的 Win32 版 GCC。

- 基于 Stellaris ARM Cortex-M3 的微控制器

  - [针对 QEMU LM3S6965 模型的 FreeRTOS 演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Texas-Instruments/cortex-m3-qemu-lm3S6965-demo)

    预配置的 Eclipse 项目，在 LM3S6965 QEMU 模型中构建并运行 FreeRTOS ARM Cortex-M3 GCC 移植。

  - [LM3S102，使用 Keil 开发工具](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Texas-Instruments/portcortexkeil)

    此移植和演示应用程序针对 [Texas Instruments](https://www.ti.com/microcontrollers-mcus-processors/arm-based-microcontrollers/arm-cortex-m4-mcus/overview.html) 基于 Stellaris ARM Cortex-M3 的处理器，该处理器使用新版 ARM Keil 开发工具 (RVDS)。
    此演示应用程序经过预配置可用于 DK-LMS102 开发，并使用协程和任务。

  - [LM3S811，使用 Keil 开发工具](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Texas-Instruments/portlm3s811keil)

    另一个适用于 Texas Instruments Stellaris ARM Cortex-M3 Keil 移植的演示应用程序，本次针对 LM3S811 评估板。

  - [LM3S102，使用 GCC](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Texas-Instruments/portcortexgcc)

    另一个适用于 [Texas Instruments](https://www.ti.com/microcontrollers-mcus-processors/arm-based-microcontrollers/arm-cortex-m4-mcus/overview.html) 基于 Stellaris ARM Cortex-M3 的处理器的移植和演示应用程序，但本次使用的是 GCC 开发工具。

  - [LM3S102，使用 CrossWorks](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Texas-Instruments/portcortexcrossworks)

    此移植和演示应用程序适用于 [Texas Instruments](https://www.ti.com/microcontrollers-mcus-processors/arm-based-microcontrollers/arm-cortex-m4-mcus/overview.html) 基于 Stellaris ARM Cortex-M3 的处理器，包括两个针对 Texas Instruments 开发板的演示，
    以及一个针对 Rowley Associates 提供的新版低成本 [CrossFire LM3S102](http://www.rowley.co.uk/crossfire/crossfire_lm3s102.htm) 的简单协程演示。
    所有演示都可以使用[面向 ARM 的 CrossWorks](http://www.rowley.co.uk/arm/index.htm) 进行编译和调试。

  - [LM3S316，使用 IAR](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Texas-Instruments/portcortexiar)

    另一个 Stellaris 移植，本次演示应用程序针对 LM3S316 并使用 [IAR 开发工具](http://www.iar.com/)。

- Hercules 安全微控制器

  - [RM48 和 TMS570，使用 Code Composer Studio](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Texas-Instruments/Free_RTOS_for_TI_RM48_and_TMS570)

    两个项目功能相同。其中一个项目针对 RM48 USB 盘评估平台，另一个项目针对 TMS570 USB 盘。两者都使用 FreeRTOS ARM Cortex-R4F CCS 移植。

  - TMS470M 和 TMS470MF06607，使用 USB 盘

    **[[非官方](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party)第三方演示，链接到 FreeRTOS Interactive 网站]**  
    此演示使用 Code Composer Studio V5。

### 针对 Xilinx 产品的演示

**这些演示能够适配同一系列中具有足够 ROM/RAM 的各种微控制器。请参阅[创建新应用程序](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project)
以及[改编演示](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party)页面。**

- Zynq

  - [Zynq，使用官方 FreeRTOS Cortex-A9 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Xilinx/RTOS-Xilinx-Zynq)

    此演示使用官方 Cortex-A9 RTOS 移植通过 Xilinx SDK 和 GCC 在 ZC702 评估板上运行 FreeRTOS。此演示使用独立 BSP，
    并将 FreeRTOS 构建到应用程序中。

  - [Zynq，使用 FreeRTOS BSP](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Xilinx/RTOS-Xilinx-SDK-BSP)

    演示如何使用 Xilinx SDK 创建 FreeRTOS BSP。在 BSP 中包含 FreeRTOS 可为应用程序编写者提供预配置的 FreeRTOS 环境，
    无需手动添加任何源文件，也无需应用程序代码提供任何回调函数，并且可在 IDE 中编辑 FreeRTOSConfig.h
    。

- Zynq UltraScale MPSoC

  - [在 UltraScale ARM Cortex-A53（64 位）核心上使用 FreeRTOS](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Xilinx/RTOS-Xilinx-UltraScale_MPSoC_64-bit)

    首个运行原生 64 位核心的 FreeRTOS 移植和演示应用程序。此演示经过预配置可在 ZCU102 评估板上运行。提供的 FreeRTOS 支持适用于
    多核 Xilinx Zynq UltraScale+ MPSoC 上的所有核心（ARM 和 Microblaze）。

  - [在 UltraScale ARM Cortex-R5 核心上使用 FreeRTOS](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Xilinx/RTOS-ARM-Cortex-R5-Xilinx-UltraScale_MPSoC)

    在 Zynq UltraScale+ MPSoC 的一个 ARM Cortex-R5 核心上运行的简单 blinky 演示和全面演示。此演示经过预配置可在 ZCU102 评估板上运行。
    提供的 FreeRTOS 支持适用于多核 Xilinx Zynq UltraScale+ MPSoC 上的所有核心（ARM 和 Microblaze）。

- Microblaze

  - [Xilinx Microblaze](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Xilinx/RTOS-Xilinx-Microblaze-KC705) [最新演示]

    此 MicroBlaze 演示使用 Xilinx 提供的 [Vivado Design Suite](http://www.xilinx.com/products/design-tools/vivado.html/) 2014.4 版本制作而成，支持 8.x 版本的
    [MicroBlaze 软核处理器](http://www.xilinx.com/tools/microblaze.htm)，
    并在基于 Kintex FPGA 的 [KC705 评估套件](http://www.xilinx.com/products/boards-and-kits/ek-k7-kc705-g.html)板上进行开发和测试。

  - [Xilinx Microblaze](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Xilinx/Free-RTOS-for-Xilinx-MicroBlaze-on-Spartan-6-FPGA)

    此 MicroBlaze 移植使用 [Xilinx 提供的 ISE Design Suite（嵌入式版本）](http://www.xilinx.com/products/design-tools/ise-design-suite/)13.1 版本生成，
    支持 8.10 版本的 [MicroBlaze 软核处理器](http://www.xilinx.com/tools/microblaze.htm)，并在基于 Spartan-6 FPGA 的
    [SP605 评估套件](http://www.xilinx.com/products/boards-and-kits/EK-S6-SP605-G.htm)上进行开发和测试。**此演示现已被取代，请参阅上文的 Kintex 演示。**

  - [Xilinx Microblaze](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Xilinx/portmicroblaze)

    在 Virtex4 FPGA 上运行的 [Microblaze 软核处理器](http://www.xilinx.com/products/design_resources/proc_central/microblaze.htm)移植。此演示经过预配置
    可在 [ML403 开发板](http://www.xilinx.com/products/boards/ml403/docs.htm)上执行。**此移植和演示现已被取代，请参阅上文的 Kintex 演示。**

- PowerPC 405

  - [Xilinx Virtex-4 PowerPC (PPC405)](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Xilinx/Free-RTOS-PPC405-Xilinx-Virtex4)

    在 Virtex4 FPGA 上运行的 PowerPC 可配置处理器核心。此演示同样经过预配置
    可在 [ML403 开发板](http://www.xilinx.com/products/boards/ml403/docs.htm)上执行。

- PowerPC 440

  - [Xilinx Virtex-5 PowerPC (PPC440)](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Xilinx/PPC440-Xilinx-Virtex5)

    在 Virtex5 FPGA 上运行的 PowerPC 可配置处理器核心。此演示提供了没有 FPU、单精度 FPU 和双精度 FPU 等配置。

### 针对 XMOS 产品的演示

- [XCORE.AI Explorer](/Documentation/02-Kernel/03-Supported-devices/04-Demos/XMOS/smp-demo-for-xmos-xcore-ai-explorer-board)

  此演示使用 FreeRTOS 内核的对称多处理 (SMP) 版本，针对 16 核
  XCORE.AI。此演示项目使用 XMOS XTC 工具构建 FreeRTOS XCOREAI
  移植，展示了对内核中 FreeRTOS 对称多处理 (SMP) 的支持。

### 针对 Intel IA32 和各种 x86 产品的演示

- [32 位模式下的 IA32/Intel Quark SoC X1000](/Documentation/02-Kernel/03-Supported-devices/04-Demos/x86/RTOS_Intel_Quark_Galileo_GCC)

  本页演示使用 GCC 和 Eclipse 在 [Intel Galileo](https://software.intel.com/iot/hardware/galileo) 单板计算机上运行 FreeRTOS。

- [工业 PC 单板计算机](/Documentation/02-Kernel/03-Supported-devices/04-Demos/x86/Industrial-PC-Port)

  此演示可在多种 PC/AT 兼容的工业和单板计算机上运行，包括 PC/104 系统；可以使用
  [Open Watcom](http://www.openwatcom.org/) 或 Borland 开发工具，并针对这两个工具提供了预配置的项目文件。请参阅“工具”页面。

- [基于 RDC8822 的单板计算机](/Documentation/02-Kernel/03-Supported-devices/04-Demos/x86/RDC8822)

  此演示在 [JK Microsystems](http://www.jkmicro.com/) 提供的 Flashlite 186 单板计算机上运行，该单板计算机极具价格优势。RDC8822 是 AMD 嵌入式 186 的
  克隆版 (AM186ED)。此演示可以使用 [Open Watcom](http://www.openwatcom.org/) 或 Borland 开发工具（请参阅“工具”页面），并针对这两个编译器
  提供了预配置的项目文件。

- [基于 RDC R1120 的单板计算机](/Documentation/02-Kernel/03-Supported-devices/04-Demos/x86/portternee)

  包括一个简单的 Web 服务器演示，运行在 [Tern](http://www.tern.com/) E-Engine 控制器上，使用内存映射的 WizNET TCP/IP 协处理器。RDC1120 是 AMD
  嵌入式 186 的克隆版 (AM186ES)。此演示应用程序使用 Paradigm C/C++ 编译器构建，可以在编译器 IDE 内进行远程调试。

### 模拟器和仿真器

- [Windows 模拟器，适用于 Visual Studio 以及集成了 MinGW (GCC) 的 Eclipse](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)

  这允许 FreeRTOS 在 Windows 环境中运行，但无法实现真正的实时操作。提供的演示项目适用于集成了 MinGW (GCC) 的 Eclipse
  和 Visual Studio 社区版。这两个工具链都免费，但 Visual Studio Express 需要注册才能用于
  评估以外的其他目的。此演示的文档页面描述了模拟操作的原理。

- [在 Linux 上运行的 POSIX 移植 (GCC)](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Linux/FreeRTOS-simulator-for-Linux)

  这允许 FreeRTOS 在 Linux 上运行，但无法实现真正的实时操作。此演示的文档页面描述了模拟操作的原理。

- [QEMU Cortex-M3 模型，使用 IAR 或 GCC（makefile 和 Eclipse）](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/QEMU/freertos-on-qemu-mps2-an385-model)

  针对 Arm Cortex-M3 mps2-an385 QEMU 模型的 FreeRTOS 内核演示。此演示针对 IAR Embedded Workbench
  和 arm-none-eabi-gcc (GNU GCC) 编译器提供了预配置的构建项目。该 GCC 项目使用了一个简单的 makefile，此文件可通过命令行或提供的 Eclipse CDT IDE 项目构建。
