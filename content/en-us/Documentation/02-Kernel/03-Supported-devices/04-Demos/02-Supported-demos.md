---
title: "Supported Demos"
created: 2018-09-20
feature: standard
categories:
  - kernel
description: A listing of demos for supported devices
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: Beginner's guide to FreeRTOS
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: Download FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: FAQs
    link: /Why-FreeRTOS/FAQs
---

[[Supported Devices](/Documentation/02-Kernel/03-Supported-devices/00-Supported-devices)]

**Don't see an exact match for your microcontroller part number and compiler vendor choice?** These demos can be adapted to any microcontroller within a supported microcontroller
family. See the [Creating a new FreeRTOS application](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project) and [Adapting a FreeRTOS Demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)
documentation pages.

**No hardware yet?** Don't worry - see the [Demo Quick Start page](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project#getting-started-with-simple-freertos-demo-projects) for links to Windows and Linux ports, as well as Arm Cortex-M3 QEMU projects.

The ['Officially Supported' and 'Contributed' FreeRTOS Code](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party) page provides a detailed explanation of
the differences between officially supported and contributed FreeRTOS ports. Officially supported FreeRTOS demos are provided that target microcontrollers from the following
manufacturers:

1. [Altera](#demos-targeting-altera-products)
2. [ARMv8-M](#demos-targeting-armv8-m-products-and-simulators)
3. [Armv8-R](#demos-targeting-armv8-r-products-and-simulators)
4. [Atmel (now Microchip)](#demos-targeting-atmel-now-microchip-products)
5. [Cadence](#demos-targeting-cadence-tensilica-products)
6. [CEVA](#demos-targeting-ceva-dsp-products)
7. [Cortus](#demos-targeting-cortus-products)
8. [Cypress](#demos-targeting-cypress-products)
9. [Energy Micro (see Silicon Labs)](#demos-targeting-silicon-labs-products)
10. [Freescale](#demos-targeting-freescale-products)
11. [Imagination/MIPS](#imaginationmips)
12. [Infineon](#demos-targeting-infineon-products)
13. [Luminary Micro](#demos-targeting-texas-instruments-products)
14. [Microchip](#demos-targeting-atmel-now-microchip-products)
15. [Microsemi (now Microchip)](#demos-targeting-microsemi-now-microchip-products)
16. [NEC](#demos-targeting-nec-products)
17. [NXP](#demos-targeting-nxp-products)
18. [Nuvoton](#demos-targeting-nuvoton-products)
19. [Raspberry Pi (Pico)](#demos-targeting-raspberry-pi-products)
20. [Renesas](#demos-targeting-renesas-products)
21. [RISC-V](#demos-targeting-risc-v) [contributed, there is now an [official port](/Using-FreeRTOS-on-RISC-V) too]
22. [SiFive](#demos-targeting-sifive-products)
23. [Silicon Labs](#demos-targeting-silicon-labs-products)
24. [Spansion (ex Fujitsu)](#demos-targeting-spansion-products)
25. [ST Microelectronics](#demos-targeting-st-microelectronics-products)
26. [Synopsys ARC](#demos-targeting-synopsys-designware-arc-products)
27. [Texas Instruments](#demos-targeting-texas-instruments-products)
28. [Xilinx](#demos-targeting-xilinx-products)
29. [XMOS](#demos-targeting-xmos-products)
30. [x86 (real mode)](#demos-targeting-intel-ia32-and-any-x86-products)
31. [Simulators and emulators](#simulators-and-emulators)

### Demos targeting Altera products

- Nios II

  - [Nios II Soft Core on a Cycle III FPGA](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Altera/FreeRTOS-Nios2)

    A port and demo application targeting the DBC3C40 reference design from EBV Elektronik.

- Cyclone V SoC (ARM Cortex-A9)

  - [Cortex-A9 HPS (Hard Processor System) on a Cyclone V SoC](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Altera/RTOS_Altera_SoC_ARM_Cortex-A9)

    This RTOS demo runs on one core of the hard wired Cortex-A9 processor on a Cyclone V SoC. The demo uses the Atlera SoC Embedded Design Suite (EDS) which
    includes a special version of ARM's DS-5 Eclipse based development environment with the GCC toolchain.

### Demos targeting ARMv8-M Products and Simulators

- Keil Simulator

  - [ARM Cortex-M23 (ARMv8-M) Demo for the Nuvoton NuMaker-PFM-M2351 Board](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Nuvoton/RTOS-Cortex-M23-NuMaker-PFM-M2351-Keil)

    Pre-configured FreeRTOS projects that target the ARM Cortex-M23 core on the Nuvoton NuMaker-PFM-M2351 board.

  - [ARMv8-M/ARM Cortex-M33 Simulator](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Arm-Virtual-Hardware/RTOS-Cortex-M33-Keil-Simulator)

    A pre-configured FreeRTOS project that targets the Keil uVision ARM Cortex-M33 Simulator and uses the armclang compiler to build the FreeRTOS ARMv8-M GCC port.
    The project demonstrates using the ARM Cortex-M33 TrustZone and the ARM Cortex-M33 Memory Protection Unit (MPU).

  - [ARM Cortex-M33 (ARMv8-M) Demo for the NXP LPCXpresso55S69 Development Board](/Documentation/02-Kernel/03-Supported-devices/04-Demos/NXP/RTOS-Cortex-M33-LPC55S69-MCUXpresso-GCC)

    A pre-configured FreeRTOS project that targets the ARM Cortex-M33 core on the NXP
    LPCXpresso55S69 Development Board.

### Demos targeting Armv8-R Products and Simulators

- Arm Cortex-R82 (Armv8-R AArch64)

  - [FreeRTOS SMP port for Armv8-R AArch64 on Cortex-R82](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Arm/FreeRTOS-SMP-port-for-Armv8-R-AArch64-on-Cortex-R82)

    A FreeRTOS SMP port targeting Arm Cortex-R82 in AArch64 state, with reference applications running on the FVP_BaseR_AEMv8R Fixed Virtual Platform. Supports GCC and ArmClang toolchains.

  - [Arm Cortex-R82 Non-MPU SMP application](https://github.com/FreeRTOS/FreeRTOS-Partner-Supported-Demos/blob/main/CORTEX_R82_SMP_FVP_GCC_ARMCLANG/README.md)

    Minimal SMP demo with two tasks pinned to different cores, validating tick, yield SGI, and coherency assumptions.

  - [Arm Cortex-R82 SMP MPU application](https://github.com/FreeRTOS/FreeRTOS-Partner-Supported-Demos/blob/main/CORTEX_R82_SMP_MPU_FVP_GCC_ARMCLANG/README.md)

    MPU-backed privilege separation demo with unprivileged tasks communicating via queue and a privileged logger task.

  - [Arm Cortex-R82 SMP Extended MPU application](https://github.com/FreeRTOS/FreeRTOS-Partner-Supported-Demos/blob/main/CORTEX_R82_SMP_EXTENDED_MPU_FVP_GCC_ARMCLANG/README.md)

    Extends the MPU demo with explicit fault injection and handling to validate robustness patterns.

### Demos targeting Atmel (now Microchip) products

**These demos can be adapted to any microcontroller within the same family that has sufficient ROM/RAM. See the [Creating a new application](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project)
and [Adapting a Demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos) pages.**

- ATSAMD20 ARM Cortex-M0+ based microcontrollers

  - [Atmel ATSAMD20 Xplained Pro with Atmel Studio](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/Atmel_SAMD20_RTOS)

    This demo includes a simple blinky example, and a comprehensive demo that includes FreeRTOS-Plus-CLI. The command line interface uses the Atmel Software Framework UART
    drivers for its character input and output.

- SAMV7 and SAME7 ARM Cortex-M7 based microcontrollers

  - [Atmel SAMV7 and SAME7 Xplained Ultra with IAR, Keil and GCC](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/Atmel_SAMV7_Cortex-M7_RTOS_Demo)

    The [SAMV7 ARM Cortex-M7 microcontroller](http://www.microchip.com/design-centers/32-bit/sam-32-bit-mcus/sam-v-mcus) demo can be build with either the IAR, Keil or Atmel
    Studio (GCC) tools, and targets the [SAM V71 Xplained Ultra Evaluation Kit](http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=ATSAMV71-XULT).

    The [SAME7 ARM Cortex-M7 microcontroller](http://www.microchip.com/design-centers/32-bit/sam-32-bit-mcus/sam-e-mcus) demo can be build with Atmel Studio (GCC), and targets
    the [SAM E70 Xplained Ultra Evaluation Kit](http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=ATSAME70-XPLD).

    The same RTOS port can be used with the [SAM S70](http://www.microchip.com/design-centers/32-bit/sam-32-bit-mcus/sam-s-mcus) ARM Cortex-M7 microcontrollers.

- AT91SAM4 ARM Cortex-M4 based microcontrollers
  - [Atmel SAM4L-EK low power tickless demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/Atmel_SAM4L-EK_Low_Power_Tick-less_RTOS_Demo)

    The application demonstrates how the FreeRTOS tick suppression features can be used to minimise the power consumption of an application running on a SAM4L ARM Cortex-M4
    microcontroller from Atmel. The SAM4L is designed specifically for use in applications that require extremely low power consumption.

  - [Atmel SAM4S-EK demo using Atmel Studio and GCC](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/Atmel_SAM4_SAM4S-EK_RTOS_Demo)

    A project targeting a SAM4S ARM Cortex-M4 microcontroller that is pre-configured to build with the free Atmel Studio IDE and run on the SAM4S-EK evaluation kit.

- AT91SAM3 ARM Cortex-M3 based microcontrollers

  - [Atmel SAM3S-EK2 and Atmel SAM3X-EK demo using Atmel Studio](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/Atmel_SAM3_SAM3X-EK_SAM3S-EK2_RTOS_Demo)

    This page presents two projects that both run the same demo application. The first targets the SAM3S microcontroller on
    the [SAM3S-EK2](http://www.microchip.com/developmenttools/productdetails.aspx?partno=atsam3s-ek2) evaluation board, and the second the SAM3X microcontroller
    on the [SAM3X-EK](http://www.microchip.com/developmenttools/productdetails.aspx?partno=atsam3x-ek) evaluation board. Both are built and debugged using the
    free [Atmel Studio IDE](https://www.microchip.com/en-us/tools-resources/develop/microchip-studio).

  - [Atmel SAM3U-EK demo using IAR](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/Free-RTOS-for-Atmel-SAM3-Cortex-M3)

    The demo application presented on this page is pre-configured to execute on the official SAM3U-EK evaluation kit from Atmel. The demo uses the FreeRTOS IAR ARM
    Cortex-M3 port and can be compiled and debugged directly from the IAR Embedded Workbench for ARM.

- ATSAMA5 ARM Cortex-A5 based microprocessors

  - [Atmel SAMA5D3 using IAR](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/Atmel_SAMA5D3_Cortex-A5_IAR)

    This page presents an RTOS demo project that targets the low cost [Atmel SAMA5 Xplained board](http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=ATSAMA5D3-XPLD).

  - [Atmel SAMA5D4 using IAR](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/Atmel_SAMA5D4_Cortex-A5_IAR)

    The SAMA5D4 ARM Cortex-A5 RTOS demo targets the [Atmel SAMA5D4 Evaluation Kit](http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=ATSAMA5D4-EK) (EK).

- AT91SAM7S and AT91SAM7X ARM7 based microcontrollers

  - [Atmel SAM7S ARM7 with IAR development tools](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/portsam7iar)

    This demo uses all the components of the AT91SAM7S64-IAR evaluation kit - including
    an [AT91SAM7S-EK development/prototyping board](http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=AT91SAM7S-EK), and
    the [IAR Embedded Workbench development tools for ARM](http://www.iar.com/ewarm). It includes a sample USB HID class driver.

  - [Atmel SAM7X ARM7 with GCC and Rowley development tools](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/portsam7xlwIP)

    Uses the FreeRTOS GCC ARM7 port, [Rowley CrossStudio](http://www.rowley.co.uk/arm/index.htm), [lwIP](http://savannah.nongnu.org/projects/lwip/) and the Atmel AT91SAM7X-EK
    development board to create an embedded web server within a fully preemptive multitasking project. This demo also includes a sample USB CDC class driver (USB to serial).

  - [Atmel SAM7X ARM7 with GCC (command line)](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/portsam7xlwIP#building-the-demo-using-gcc-command-line-version)

    The SAM7X lwIP project can also be built using a simple makefile and the standard command line GCC compiler.

  - [Atmel AT91FR40008 with GCC development tools](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/portat91fr40008)

    A GCC ARM7 port for the AT91 microcontroller. The demo is preconfigured to run on the [Embest ATEB40X](http://www.embedinfo.com/English/Product/ateb40x.asp)
    prototyping board (Atmel AT91EB40A clone).

- AT91SAM9 ARM9 based microcontrollers

  - [Atmel AT91SAM9XE using IAR](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/ARM9-AT91SAM9-RTOS-Demo)

    An IAR demo that runs on the [AT91SAM9XE-EK Evaluation Board](http://www.microchip.com/Developmenttools/ProductDetails.aspx?PartNO=AT91SAM9XE-EK).
    Supports both ARM and THUMB modes.

- AVR32

  - [AVR32 AT32UC3A using GCC and IAR tools - including TCP/IP examples](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/portAVR32)

    The standard demo has been ported for both the GCC and IAR development tools. An embedded web server and TFTP server example is also provided

- AVR / ATMegaAVR

  - [ATmega323/ATmega32 and ATmega128 with WinAVR (AVR GCC) development tools](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/Atmel_AVR_Mega_AVR)

    The demo is pre-configured to run on the [STK500 prototyping board](http://www.microchip.com/developmenttools/productdetails.aspx?partno=atstk500) utilising
    an [ATMega323 microcontroller](http://www.microchip.com/wwwproducts/en/atmega32). It is compiled using the [GNU based WinAVR development tools](http://winavr.sourceforge.net/),
    for which a pre-configured make file is provided. Executables can be debugged using the AVR Studio simulator.

  - [ATmega323/ATmega32 and ATmega128 with IAR development tools](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/AVR_IAR)

    As per the WinAVR port, but uses the [IAR Embedded Workbench development tools](http://www.iar.com/).

  - [ATmega-0 with XC8, AVR-GCC and IAR EWAVR Compiler](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/microchip-atmega-0-demo)

    The demo runs on [ATmega4809 Curiosity Nano evaluation kit](https://www.microchip.com/DevelopmentTools/ProductDetails/PartNO/DM320115) and has been ported
    to MPLAB X (XC8), Atmel Studio (AVR-GCC), and IAR EWAVR development tools.

  - [AVR Dx with XC8, AVR-GCC and IAR EWAVR Compiler](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/microchip-avr-dx-demo)

    The demo runs on [AVR128DA48 Curiosity Nano evaluation kit](https://www.microchip.com/DevelopmentTools/ProductDetails/PartNO/DM164151) and has been ported to
    MPLAB X (XC8), Atmel Studio (AVR-GCC), and IAR EWAVR development tools.

### Demos targeting Cadence Tensilica products

- [Xtensa Processors](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Cadence/Tensilica_Xtensa_Free_RTOS_Demo)  **Uses a [[third party](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party) RTOS port]**

  Running all the RTOS tests, using the XCC compiler and builds using the Xtensa Xplorer IDE.

### Demos targeting CEVA DSP products

This is a [third party](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party) RTOS port. Visit [https://www.ceva-dsp.com](https://www.ceva-dsp.com) for details.

### Demos targeting Cortus products

- [Cortus APS3](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Cortus/Cortus-APS3-Free-RTOS-Demo)

  A port and demo application targeting an APS3 processor running on a Spartan-3 Starter Board.

### Demos targeting Cypress products

**These demos can be adapted to any microcontroller within the same family that has sufficient ROM/RAM. See
the [Creating a new application](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project) and [Adapting a Demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos) pages.**

- [Cypress PSoC5 CY8C5588 ARM Cortex-M3](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Cypress/FreeRTOS-port-and-demo-for-Cypress-PSoC5-CY8C5588-Cortex-M3)

  A FreeRTOS demo for the PSoC5 that targets the [CY8CKIT-001 PSoC® Development Kit](http://www.cypress.com/?rID=37464), using
  a [CY8CKIT- 010 PSoC® CY8C55 Family Processor Module Kit](http://www.cypress.com/?rID=43673). The PSoC5 demo includes a schematic design with several peripherals
  to demonstrate their integration with the RTOS. The included peripherals are the UART, LCD Character Display and two different types of timer implementations. PSoC
  Creator projects are provided for GCC, as well as the ARM Keil/RVDS compilers.

### Demos targeting Freescale products

**These demos can be adapted to any microcontroller within the same family that has sufficient ROM/RAM. See
the [Creating a new application](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project) and [Adapting a Demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos) pages.**

- Kinetis ARM Cortex-M0+

  - [Freescale Kinetis KL0 With FreeRTOS CodeWarrior Processor Expert Component](http://mcuoneclipse.wordpress.com/2012/09/29/tutorial-freedom-with-freertos-and-kinetis-l/)
    **[[Unofficial](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party) third party demo, links to an external site]**

    A great third party demo using FreeRTOS on a FRDM-KL25Z Freedom board. The web page includes a link to, and a tutorial on using, a FreeRTOS Processor Expert plug-in to the Freescale CodeWarrior IDE.

- HCS12

  - [Motorola / Freescale MC9S12C32 using CodeWarrior](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Freescale-product-demos/porthcs12)

    The demo is pre-configured to run on the [PK-HCS12C32](http://www.softecmicro.com/products.html?type=detail&title=PK-HCS12C32) starter kit
    from [SofTec Microsystems](http://www.softecmicro.com/), and uses the [CodeWarrior HC(S)12 Development Tools](http://www.codewarrior.com/MW/Develop/Embedded/HC12/Default.htm).
    It demonstrated using FreeRTOS with the small memory model.

- [Motorola / Freescale MC9S12DP256B using CodeWarrior](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Freescale-product-demos/port68hcs12)

  The demo is pre-configured to run on the [M68KIT912DP256](http://www.freescale.com/webapp/sps/site/prod_summary.jsp?code=M68KIT912DP256&parentCode=MC9S12A512&nodeId=0162468636K100)
  development board from Freescale, and uses the [CodeWarrior HC(S)12 Development Tools](http://www.codewarrior.com/MW/Develop/Embedded/HC12/Default.htm). It demonstrated using
  FreeRTOS with the banked memory model.

- Coldfire V2
  - [Motorola / Freescale ColdFire V2 using CodeWarrior](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Freescale-product-demos/Free-RTOS-for-ColdFire-MCF5222x-using-CodeWarrior)

    Pre-configured to run on the [M52221DEMO evaluation board](http://www.freescale.com/webapp/sps/site/prod_summary.jsp?code=M52221DEMO) from FreeScale, using the
    free special edition of CodeWarrior for ColdFire.

  - [Motorola / Freescale MCF523x GCC](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Freescale-product-demos/portcoldfire)

### Fujitsu

Fujitsu microcontrollers were acquired by Spansion. See [Spansion](#demos-targeting-spansion-products) below.

### Imagination/MIPS

The FreeRTOS download does not contain official MIPS support, but the following options are made available and supported directly by Imagination in the FreeRTOS Interactive site:

- A GCC port for the following cores:

  1. Legacy Cores: 24K, 34K,74K,1004K,1074K,M4K,M14K
  2. Aptiv Cores: microAptiv, interAptiv, proAptiv
  3. Warrior Cores: M5100, M5150, M6200, M6250, P5600

### Demos targeting Infineon products

**These demos can be adapted to any microcontroller within the same family that has sufficient ROM/RAM. See the [Creating a new application](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project)
and [Adapting a Demo](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party) pages.**

- AURIX™ TC3xx
  - [AURIX™ TC375 using AURIX™ Development Studio (ADS)](https://github.com/FreeRTOS/FreeRTOS-Partner-Supported-Demos/tree/main/AURIX_TC375_ADS)

    The demo application is meant to run on the [AURIX™ TC375 lite kit](https://www.infineon.com/cms/en/product/evaluation-boards/kit_a2g_tc375_lite/) from Infineon using [AURIX™ Development Studio (ADS)](https://www.infineon.com/cms/en/product/promopages/aurix-development-studio/). ADS includes a fully functional IDE with a free compiler, debugger, and other tools/libraries.

- TriCore TC1782 using the Free TriCore Entry Toolchain
  - [TriCore TC1782 using the Free TriCore Entry Toolchain](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Infineon/FreeRTOS-for-Infineon-TriCore-TC1782-using-HighTec-GCC)

    The demo application is pre-configured to run on the TriBoard TC1782 starter kit from Infineon. The free tool chain includes an Eclipse integration.

- XMC1000 ARM Cortex-M0

  - [XMC1100, XMC1200 and XMC1300 Boot Kits with IAR, GCC and Keil compilers](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Infineon/Infineon-ARM-Cortex-M0-XMC1000-RTOS)

    Like the XMC4000 equivalent, the XMC1000 ARM Cortex-M0 demo can be configured to create either a simple blinky or a comprehensive test and demo application.

- XMC4000 ARM Cortex-M4

  - [XMC4200, XMC4400 and XMC4500 Hexagon Application Board demos for IAR, Keil, Dave/GCC and Tasking compilers](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Infineon/Infineon-ARM-Cortex-M4-XMC4000-RTOS)

    The demo presented on this page can be built as a simple blinky demo, or as a comprehensive test and demo application.

  - [XMC4500 on the Hexagon Eval Board Using IAR and Keil development tools](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Infineon/Infineon-XMC45xx-Cortex-M4_GCC_Atollic)

    Both IAR Embedded Workbench and a Keil uVision projects are provided that targets the CPU board from the Infineon hexagon MXC4500 evaluation kit.

    **[This demo has now been superseded by [the demo that also supports the XMC4200 and XMC4400 devices]](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Infineon/Infineon-ARM-Cortex-M4-XMC4000-RTOS)**

  - [XMC4500 on the Hexagon Eval Board Using GCC and Atollic](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Infineon/Infineon-XMC45xx-Cortex-M4_GCC_Atollic)

    An Atollic project is provided that uses the GCC compiler, and targets the CPU board from the Infineon hexagon MXC4500 evaluation kit.

    **[This demo has now been superseded by [the demo that also supports the XMC4200 and XMC4400 devices]](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Infineon/Infineon-ARM-Cortex-M4-XMC4000-RTOS)**

  - [XMC4500 on the Hexagon Eval Board Using the Tasking VX-toolset for ARM](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Infineon/Infineon-XMC4500-Cortex-M4-Tasking-VX-For-ARM)

    Another project that targets the Infineon hexagon MXC4500 evaluation kit - this time using the Tasking VX-toolset for ARM.

    **[This demo has now been superseded by [the demo that also supports the XMC4200 and XMC4400 devices]](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Infineon/Infineon-ARM-Cortex-M4-XMC4000-RTOS)**

### Demos targeting Luminary Micro products

Following the acquisition of Luminary Micro by Texas Instruments, demo applications that target Stellaris microcontrollers are now listed under the [Texas Instruments](#demos-targeting-texas-instruments-products) heading.

### Demos targeting Microchip products

See also [Atmel (now Microchip)](#demos-targeting-atmel-now-microchip-products) and [Microsemi (now Microchip)](#demos-targeting-microsemi-now-microchip-products)

**PIC32 demos can be adapted to any microcontroller within the same family that has sufficient ROM/RAM. See
the [Creating a new application](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project) and [Adapting a Demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos) pages.**

- PIC32 (MIPS)

  - [PIC32 (PIC32MZ and PIC32MZ EF with MIPS M14K core) MPLAB GCC](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Microchip/PIC32MZ_RTOS_MIPS_M14K)

    Port and demo application for the MIPS M14K based PIC32MZ and PIC32MZ EF (with floating point) from Microchip. The demo utilises the XC32 compiler, MPLAB X and the
    PIC32MZ and PIC32MZ EF Starter Kits.

  - [PIC32 (PIC32MX with MIPS M4K core) MPLAB GCC](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Microchip/port_PIC32_MIPS_MK4)

    Port and demo application for the MIPS M4K based PIC32 from Microchip. The demo utilises the XC32 compiler and MPLAB X. Build configurations are provided for the
    Explorer16 development board and the PIC32 USB II starter kit.

- MEC14xx, CEC13xx, CEC17xx, MEC17xx, MEC51xx (ARM Cortex-M4F)

  - [CEC1302 ARM Cortex-M4F, GCC, Keil, MikroC](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Microchip/Microchip_CEC1302_ARM_Cortex-M4F_Low_Power_Demo)

    Comprehensive and low power tick-less demos for the CEC1302 ARM Cortex-M4F based microcontroller from Microchip. The project demonstrates the CEC1302 being used
    with both aggregated and disaggregated interrupt schemes.

- PIC24 & dsPIC

  - [Microchip PIC24 and dsPIC33 MPLABX](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Microchip/portpic24_dspic)

    Ports and demo applications for Microchip PIC24 and dsPIC33 MCUs. Majority of the demos are targeted at the Explorer 16 evaluation board
    and use the MPLAB&reg XC16 or XC-DSC compilers. Please refer the README of individual demos for the details about the target board and the compilers used.

- PIC18

  Please note that the segmented memory on the PIC18 makes it a less than ideal candidate for use with an RTOS.

  - [Microchip PIC18 MPLAB](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Microchip/PIC18-with-c18-compiler)

    The demo is pre-configured to run on the [40 pin PICmicro prototyping board](https://www.fored.co.uk/) from Forest Electronic Developments, with
    a PIC18F452 microcontroller. This is a very low cost platform that has an in system programming capability. The MPLAB development tools are also utilised,
    comprising of the [MPLAB IDE](http://www.microchip.com/stellent/idcplg?IdcService=SS_GET_PAGE&nodeId=1406&dDocName=en019469) and
    the [MPLAB C18 compiler](http://www.microchip.com/stellent/idcplg?IdcService=SS_GET_PAGE&nodeId=1406&dDocName=en010014).

  - [Microchip PIC18 wizC](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Microchip/portwizc)

    The port is created using the [wizC Integrated Development Environment](http://www.fored.co.uk/html/wiz_c_-__pic_c_compiler.HTM)
    from [Forest Electronic Developments](http://www.fored.co.uk/). The port can also be used with
    the [FED C-compiler](http://www.fored.co.uk/html/c_compilers.html), also from Forest Electronic Developments.

### Demos targeting Microsemi (now Microchip) products

**These demos can be adapted to any microcontroller within the same family that has sufficient ROM/RAM. See
the [Creating a new application](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project) and [Adapting a Demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos) pages.**

- RISC-V based microcontrollers

  - [MiFive M2GL025 Creative Board and Renode using GCC and the SoftConsole IDE](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Microsemi-now-Microchip/RTOS-RISC-V-SoftConsole-Renode-SiFive)

    This demo originally targeted the MiFive RISC-V core on the Microchip (previously MicroSemi) M2GL025 Creative Board from Future Electronics. The target was switched
    to the Renode software emulation of the same board.

### Demos targeting NEC products

Following the merger of NEC and Renesas under the Renesas brand, demo applications that target what were NEC microcontrollers are now listed under the [Renesas](#demos-targeting-renesas-products) heading.

### Demos targeting Nuvoton products

**These demos can be adapted to any microcontroller within the same family that has sufficient ROM/RAM. See
the [Creating a new application](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project) and [Adapting a Demo](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party) pages.**

- ARM Cortex-M23 based microcontrollers

  - [Nuvoton NuMaker-PFM-M2351 Board Demo using Keil uVision and IAR Embedded Workbench](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Nuvoton/RTOS-Cortex-M23-NuMaker-PFM-M2351-Keil)

    This demo targets the ARM Cortex-M23 core on the Nuvoton NuMaker-PFM-M2351 Board. The pre-configured projects demonstrate using the ARM Cortex-M23 TrustZone and the
    ARM Cortex-M23 Memory Protection Unit (MPU).

### Demos targeting NXP products

**These demos can be adapted to any microcontroller within the same family that has sufficient ROM/RAM. See
the [Creating a new application](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project) and [Adapting a Demo](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party) pages.**

- RISC-V based microcontrollers

  - [VEGAboard PULP RI5CY Demo using GCC and Eclipse](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Others/RTOS-RISC-V-Vegaboard_Pulp)

    This demo targets the RI5CY core on the VEGAboards multi-cored (two Arm cores, two RISC-V cores) RV32M1 MCU.

- ARM Cortex-M33 based microcontrollers

  - [NXP LPCXpresso55S69 Development Board Demo using GCC and MCUXpresso](/Documentation/02-Kernel/03-Supported-devices/04-Demos/NXP/RTOS-Cortex-M33-LPC55S69-MCUXpresso-GCC)

    This demo targets the ARM Cortex-M33 core on the LPCXpresso55S69 Development Board. The pre-configured project demonstrates using the ARM Cortex-M33
    TrustZone and the ARM Cortex-M33 Memory Protection Unit (MPU).

- ARM Cortex-M4F based microcontrollers

  - [NXP LPC4350 demo using Keil/RVDS](/Documentation/02-Kernel/03-Supported-devices/04-Demos/NXP/FreeRTOS-for-LPC4350-Cortex-M4F-and-Cortex-M0-Keil)

    This application demonstrates the FreeRTOS ARM Cortex-M4F RVDS port on the ARM Cortex-M4 core of the dual core LPC4350. The demo is pre-configured to
    run on the Hitex LPC4350 evaluation board. The LPC4300 microcontroller is configured to run at 204MHz. The demo includes a basic LED flashing configuration,
    and a comprehensive configuration. The comprehensive configuration creates more than 40 tasks, including tasks that test the FreeRTOS port itself.

- ARM Cortex-M3 based microcontrollers

  - NXP LPC1830 demonstrating FreeRTOS-Plus-UDP

    The demo runs [FreeRTOS-Plus-UDP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP) on an LPC1830 XPlorer board from NGX Technologies. The project builds
    with the FreeRTOS LPCXpresso Eclipse based IDE.

  - [NXP LPC1768 demonstrating FreeRTOS-Plus-IO and FreeRTOS-Plus-CLI](/Documentation/03-Libraries/02-FreeRTOS-plus/04-FreeRTOS-plus-IO/01-FreeRTOS_Plus_IO)

    A comprehensive demo that uses FreeRTOS-Plus-CLI to interact with FreeRTOS-Plus-IO and the FatFS file system hosted on an SD card. FreeRTOS-Plus-IO manages the UART,
    I2C and SPI ports. The demo builds with the free LPCXPresso IDE and runs on the LPCXpresso base board.

- ARM Cortex-M0 based microcontrollers

  - [NXP LPC1114 LPCXpresso](/Documentation/02-Kernel/03-Supported-devices/04-Demos/NXP/FreeRTOS-for-Cortex-M0-LPC1114-LPCXpresso)

    This application demonstrates the FreeRTOS ARM Cortex-M0 GCC port on low cost LPCXpresso LPC1114 hardware. The free LPCXpresso IDE is used.

  - [NXP LPC51U68 low power demo using LPCXpresso (GCC), Keil and IAR](/Documentation/02-Kernel/03-Supported-devices/04-Demos/NXP/FreeRTOS_LPCXpresso51U68_IAR_Keil_GCC)

    Demonstrates using the tickless low power mode on an ARM Cortex-M0+ LPC51U68 using three different compilers.

- LPC2000 ARM7 based microcontrollers

  - [NXP ARM7 with the Keil development tools](/Documentation/02-Kernel/03-Supported-devices/04-Demos/NXP/portlpckeil)

    The demo is pre-configured to run on the [MCB2100 development/prototyping board](http://www.keil.com/mcb2100). The development tools provide an excellent debugger
    and peripheral simulator - allowing the entire demo application to be executed within the simulator. An excellent way to learn FreeRTOS!

  - [NXP ARM7 with the IAR development tools](/Documentation/02-Kernel/03-Supported-devices/04-Demos/NXP/portlpciar)

    The [IAR](http://www.iar.com/ewarm) LPC2000 demo is also preconfigured to execute on the MCB21000 development board.

  - [NXP ARM7 with GCC](/Documentation/02-Kernel/03-Supported-devices/04-Demos/NXP/portlpc2106)

    The demo is pre-configured to run on the LPC-P2106 prototyping board, with a LPC2106 microcontroller. This is a very low cost prototyping board that has an in system
    programming capability. The port uses a Win32 build of the [ARM7 GNU development tools](http://www.gnuarm.com/).

  - [NXP ARM7 with Rowley Development tools and Rowley development board](/Documentation/02-Kernel/03-Supported-devices/04-Demos/NXP/portlpc2138)

    Based on the GCC port, this demo uses the [Rowley Associates](http://www.rowley.co.uk/) CrossWorks integrated development environment and is targeted at
    the [CrossFire LPC2138 embedded evaluation kit](http://www.rowley.co.uk/crossfire/crossfire_lpc2138.htm)

  - [NXP ARM7 with Rowley Development tools and Olimex development board](/Documentation/02-Kernel/03-Supported-devices/04-Demos/NXP/portrowleylpc2124)

    Based on the GCC port, this demo uses the [Rowley Associates](http://www.rowley.co.uk/) CrossWorks integrated development environment and includes an embedded TCP/IP stack and embedded web server.

### Demos targeting Raspberry Pi products

- [Pico](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Raspberry-Pi/smp-demos-for-the-raspberry-pi-pico-board)

  These demos use the FreeRTOS symmetric multiprocessing (SMP) version of the kernel. The demos target the Raspberry Pi Pico board, which uses the
  RP2040 microcontroller from Raspberry Pi that features a Dual-core ARM Cortex M0+ processor.

### Demos targeting Renesas products

**These demos can be adapted to any microcontroller within the same family that has sufficient ROM/RAM. See
the [Creating a new application](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project) and [Adapting a Demo](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party) pages.**

- RZ/A (ARM Cortex-A9)
  - RZ Embedded Processor (ARM Cortex-A9 core) with GCC development tools

    **[[Unofficial](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party) third party demo, links to the FreeRTOS Interactive site]**

    Another FreeRTOS demo application for the Renesas RZ/A1 embedded processor, this time using the GCC tool chain.

- RZ/T (ARM Cortex-R4F)

  - [RZ/T Embedded Processor (ARM Cortex-R4F core) with Renesas, GCC and IAR compilers](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Renesas/Renesas_RZ-T_Cortex-R4F-RTOS)

    A FreeRTOS demo application for the Renesas RZ/T embedded processor, which has an ARM Cortex-R core. Three projects are provided, allowing the demo to be built
    with the IAR, GCC and Renesas compilers. The GCC and Renesas compiler projects use the e2studio IDE. The demo includes a command line interface implemented with FreeRTOS-Plus-CLI.

- RX700

  - [RX700 RX71M (RXv2 core) with Renesas, GCC and IAR compilers](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Renesas/RX700_RX71M_Renesas_GCC_IAR)

    A FreeRTOS demo application for the Renesas RX71M microcontroller, which has an RXv2 core. Three projects are provided, allowing the demo to be built with the IAR,
    GCC and Renesas compilers. The GCC and Renesas compiler projects use the e2studio IDE. The demo includes a command line interface implemented with FreeRTOS-Plus-CLI.

- RX600

  - [RX64M (RXv2 core) using e2studio](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Renesas/RX64M_RTOS_Renesas_GCC_e2studio)

    Two e2studio projects are provided, both of which target the RX64M RSK (Renesas Starter Kit). One project users the Renesas RX compiler, and the other the GCC compiler.

- RX200

  - [RX231 with Renesas, GCC and IAR compilers](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Renesas/RX231_RTOS_Renesas_GCC_IAR)

    A FreeRTOS demo application for the Renesas RX231 microcontroller, which as an RXv2 core. Three projects are provided, allowing the demo to be built with the IAR,
    GCC and Renesas compilers. The GCC and Renesas compiler projects use the e2studio IDE.

  - [RX210 using the Renesas compiler and HEW IDE](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Renesas/Free_RTOS_For_Renesas_RX210_HEW)

    Documents the [Renesas RX210](http://www.renesas.eu/products/mpumcu/rx/rx200/rx210/rx210_root.jsp) FreeRTOS port and demo application that uses
    the [Renesas RX](http://www.renesas.com/compiler) compiler, and [HEW IDE](http://www.renesas.com/hew). The project is pre-configured to run on the RSKRX210 starter kit.

- RX100

  - [RX113 with Renesas, GCC and IAR compilers](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Renesas/RX113_RTOS_Renesas_GCC_IAR)

    A FreeRTOS demo application for the Renesas RX113 microcontroller. Three projects are provided, allowing the demo to be built with the IAR, GCC and Renesas compilers.
    The GCC and Renesas compiler projects use the e2studio IDE. The demo includes a command line interface implemented with FreeRTOS-Plus-CLI.

  - [Tickless low power demo for RX100 (IAR, GCC and Renesas compilers)](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Renesas/RX100_RSK_Low_Power_Tick-less_RTOS_Demo)

    An application that demonstrates how to use FreeRTOS tick suppression functionality to reduce power consumption on an RX100 microcontroller. Projects are provided for
    IAR, e2studio with GCC and e2studio with the Renesas compiler.

- RL78 16-bit microcontroller

  - [RL78/G13, RL78/G14, RL78/G1C, RL78/L13 and RL78/G1A using IAR](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Renesas/RTOS_RL78_IAR_Demos)

    An IAR demo with build configurations to target the following RL78 chips and hardware: YRPBRL78G13 RL78/G13 promotion board, YRDKRL78G14 RL78/G14 development board,
    RSKRL78G1C RL78/G1C starter kit, RSKRL78L13 RL78/L13 starter kit, RL78/G1A TB RL78/G1A target board. Far and near memory models are supported.

  - [RL78/G13 promotion board](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Renesas/FreeRTOS-port-and-demo-for-Renesas-RL78-YRPBRL78G13-Promo-Board)

    An IAR demo that targets the RL78/G13 promotion board. Far and near memory models are supported.

- [H8/S](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Renesas/porth8s)

  The demo is pre-configured to run on the
  [EDK2329 prototyping embedded computer](http://america.renesas.com/fmwk.jsp?cnt=edk_2329_software_tools_root.jsp&fp=/products/tools/introductory_evaluation_tools/starterkits_evaluation_boards/edk2329/)
  direct from [Renesas (Hitachi)](http://www.renesas.com/), fitted with
  an [H8/S2329 processor](http://america.renesas.com/fmwk.jsp?cnt=h8s2329_h8s2328_root.jsp&fp=/products/mpumcu/h8s_family/h8s2300_series/h8s2329_h8s2328_group/).
  The port uses the [GNU H8 compiler](http://www.gnuh8.com/) and HEW GUI.

- [V850ES 32bit microcontroller](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Renesas/NEC-V850-RTOS)

  An IAR demo that contains configurations for many different Renesas target boards and the V850ES/Fx3 Starter Board. Large and small memory models are supported.

- [78K0R 16bit microcontroller](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Renesas/NEC-78K-RTOS)

  An IAR demo that contains configurations for different Renesas target boards. Far and near memory models are supported.

### Demos targeting RISC-V

- RISC-V Spike Simulator GCC

  **[[Unofficial](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party) third party demo, links to the FreeRTOS Interactive site.
  There is now an [official port](/Using-FreeRTOS-on-RISC-V) too]**

  The port automatically configures itself for 32-bit and 64-bit RISC-V architectures on basis of #defines set by GCC. The demo application runs on
  the [spike simulator](http://riscv.org/software-tools/risc-v-isa-simulator/) in 64-bit mode, and needs the riscv GCC compiler and spike simulator to be installed
  somewhere for the build to succeed.

### Demos targeting SiFive products

- [SiFive HiFive1 RevB using Freedom Studio (GCC) and IAR](/Documentation/02-Kernel/03-Supported-devices/04-Demos/SiFive/RTOS-RISC-V-FreedomStudio-IAR-HiFive-RevB)

  Two pre-configured projects that create demo applications for the RISC-V core on the HiFive1 RevB evaluation board - one project uses SiFive's Freedom Studio with
  GCC, the other IAR's Embedded Workbench for IAR. A pre-configured SiFive Freedom Studio project that builds and runs a FreeRTOS RISC-V demo in the sifive_e QEMU
  model using GCC and GDB.

### Demos targeting Silicon Labs products

**The FreeRTOS ARM Cortex-M ports will run on all Silicon Labs ARM Cortex-M microcontrollers. See the [Creating a new application](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project)
and [Adapting a Demo](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party) pages.**

- [EFM Giant Gekco and Pearl Gecko using Simplicity Studio and GCC](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Silicon-labs/EFM32-Giant-Gecko-Pearl-Gecko-tickless-RTOS-demo)

  The demos presented on this page demonstrate the FreeRTOS tick suppression feature being used to save power on both an EFM32 Giant Gecko and an EFM32 Pearl Gecko starter
  kit. Both demos build using the free Eclipse based Simplicity Studio IDE and GCC.

- [EFM32G890F128 (ARM Cortex-M3) using IAR](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Silicon-labs/EFM32)

  An older port and demo application that uses the IAR Embedded Workbench development tools, and targets the ARM Cortex-M3 based EFM32G890F128 microcontroller.

  **[This demo has now been superseded by the [Giant and Pearl Gecko starter kit demos](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Silicon-labs/EFM32-Giant-Gecko-Pearl-Gecko-tickless-RTOS-demo), which also demonstrate
  the FreeRTOS tickless idle mode to save power]**

- [Cygnal 8051](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Energy-Micro-see-Silicon-Labs/portcygn)

  This port uses a prototyping board supplied directly from [Silicon Labs](http://www.silabs.com/), and uses the open source [SDCC compiler](http://sdcc.sourceforge.net/).

### Demos targeting Spansion products

**These demos can be adapted to any microcontroller within the same family that has sufficient ROM/RAM. See the [Creating a new application](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project)
and [Adapting a Demo](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party) pages.**

- 32bit microcontrollers

  - [Spansion FM3 ARM Cortex-M3 MCU](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Spasion-was-Fujitsu/FreeRTOS-for-Fujitsu-FM3-MB9BF500-microcontrollers)

    A FreeRTOS ARM Cortex-M3 demo application that targets a Spansion [FM3 microcontroller](http://mcu.emea.fujitsu.com/mcu_product/overview_32FM3.htm). Two IAR and Keil
    projects are provided that are already pre-configured to run on the [SK-FM3-100PMC](http://mcu.emea.fujitsu.com/mcu_tool/detail/SK-FM3-100PMC.htm)
    and [SK-FM3-64PMC1](http://mcu.emea.fujitsu.com/mcu_tool/detail/SK-FM3-64PMC1.htm) starter kit evaluation boards respectively.

  - [Spansion MB91460 32bit MCU](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Spasion-was-Fujitsu/RTOS-port-Fujitsu-FR-MCU-MB91460)

    A demo for the MB91460 series of 32bit MCUs from Spansion. The port is pre-configured to run on
    the [SK-91F467-FLEXRAY](http://mcu.emea.fujitsu.com/mcu_tool/detail/SK-91F467-FLEXRAY.htm) starter kit and uses
    the [Softune](http://mcu.emea.fujitsu.com/mcu_tool/detail/SWB_(FR)_V6.htm) compiler, IDE and debugger.

- 16bit 16FX microcontrollers

  - [Spansion MB96340 16bit MCU](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Spasion-was-Fujitsu/RTOS-port-Fujitsu-16FX-MB96340)

    A demo for the MB96340 series of 16bit MCUs from Spansion (16FX). The port is pre-configured to run on
    the [SK-16FX-EUROScope](http://mcu.emea.fujitsu.com/mcu_tool/detail/SK-16FX-EUROSCOPE.htm) starter kit and uses
    the [Softune](http://mcu.emea.fujitsu.com/mcu_tool/detail/SWB_(F2MC-16)_V3.htm) compiler and IDE along with the Euroscope debugger.

### Demos targeting ST Microelectronics products

**These demos can be adapted to any microcontroller within the same family that has sufficient ROM/RAM. See
the [Creating a new application](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project) and [Adapting a Demo](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party) pages.**

- STM32F7 ARM Cortex-M7 based microcontrollers

  - [STM32H745 dual core (AMP) demo using IAR EWARM](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ST-Microelectronics/STM32H7_Dual_Core_AMP_RTOS_demo)

    This dual core RTOS demo is a simple Asymmetric Multi Processing (AMP) core to core communication project implemented
    using [FreeRTOS message buffers](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers). It is accompanies by
    a [separate article](/Community/Blogs/2020/simple-multicore-core-to-core-communication-using-freertos-message-buffers) that describes
    some of the internal implementation details.

    The demo is preconfigured to run on the [STM32H745I Discovery Board](https://www.st.com/en/evaluation-tools/stm32h745i-disco.html) and build with the IAR compiler
    and [Embedded Workbench IDE](https://www.iar.com/products/architectures/arm/). The STM32H7xx has one ARM Cortex-M4 core and one ARM Cortex-M7 core. Both cores run the same ARMv7-M FreeRTOS port.

  - [STM32F7 demo using IAR EWARM and Keil uVision](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ST-Microelectronics/ST_STM32F7_Cortex-M7_RTOS_Demo)

    This RTOS demo targets the STM32756G-EVAL Evaluation Kit, which incorporates an [STM32F7 ARM Cortex-M7 microcontroller](http://www.st.com/web/en/catalog/mmc/SC1169/SS1858).
    Pre-configured build projects are provided for both the [IAR](http://www.iar.com/ewarm) and ARM Keil tools.

- STM32F4 ARM Cortex-M4F based microcontrollers

  - [STM32F407 demo using IAR EWARM](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ST-Microelectronics/FreeRTOS-for-STM32F4xx-Cortex-M4F-IAR)

    This application demonstrates the FreeRTOS ARM Cortex-M4F IAR port on the ARM Cortex-M4F based STM32F407. The demo is pre-configured to run on the STM32F407ZF-SK starter
    kit evaluation board. The demo includes a basic LED flashing configuration, and a comprehensive configuration. The comprehensive configuration creates more than 40 tasks,
    including tasks that test the FreeRTOS port itself.

- STM32 ARM Cortex-M3 based microcontrollers

  - [Extreme low power tickless operation on an STM32L](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ST-Microelectronics/STM32L-discovery-low-power-tickless-RTOS-demo)

    This project demonstrates how the FreeRTOS tick suppression features can be used to minimise the power consumption of an application running on an STM32L low power ARM
    Cortex-M3 microcontroller from ST. The STM32L is designed specifically for use in applications that require extremely low power consumption.

  - [Low power ST STM32 (STM32L152) using the IAR Embedded Workbench](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ST-Microelectronics/Free-RTOS-for-Cortex-M3-STM32-STM32L152-EVAL)

    The FreeRTOS demo application for the low power [STM32L152 microcontroller](http://www.st.com/internet/mcu/product/248824.jsp) from [STMicroelectronics](http://www.st.com/).
    The demo uses the [IAR Embedded Workbench for ARM V6.10](http://www.iar.com/ewarm) from IAR Systems, and targets the official STM32L152-EVAL evaluation board from STMicroelectronics.

  - [ST STM32 Value Line demo using Atollic TrueStudio](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ST-Microelectronics/FreeRTOS-for-Cortex-M3-STM32-STM32F100-Discovery)

    Uses the ARM Cortex-M3 GCC port along with
    the [Atollic TrueStudio IDE](https://www.st.com/content/st_com/en/products/development-tools/software-development-tools/stm32-software-development-tools/stm32-ides/truestudio.html).
    The demo is preconfigured to run on the [STM32 value line Discovery board](http://www.st.com/stm32-discovery), fitted with
    an [STM32F100 microcontroller](http://www.st.com/internet/mcu/product/216844.jsp).

  - [ST STM32 ARM Cortex-M3 using the IAR development tools](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ST-Microelectronics/portstm32iar)

    Uses the ARM Cortex-M3 IAR port to create a demo application on the STM32 evaluation board.

  - [ST STM32 ARM Cortex-M3 using the GCC compiler with the RIDE IDE](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ST-Microelectronics/RTOS_Demo_STM32_Primer_Ride)

    Demo that uses the novel STM32 Primer evaluation board.

- STM32F0 ARM Cortex-M0 based microcontrollers

  - [STM32F051 demo using IAR EWARM](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ST-Microelectronics/FreeRTOS-for-STM32F051-Cortex-M0-IAR)

    This application demonstrates the FreeRTOS ARM Cortex-M0 IAR port on the STM320518-EVAL board from ST, which is fitted with an STM32F051 microcontroller.

- STR7 ARM7 based microcontrollers

  - [ST Microelectronics STR75x ARM7 with IAR development tools](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ST-Microelectronics/portstr75xiar)

    Preconfigured to run on the [STR750 EVAL](http://www.st.com/internet/evalboard/product/132197.jsp) evaluation board from STMicroelectronics, this application
    demonstrates FreeRTOS on the ST STR750 ARM7TDMI microcontroller with the [IAR Embedded Workbench development tools for ARM](http://www.iar.com/ewarm).

  - [ST Microelectronics STR75x ARM7 with Raisonance RIDE development tools](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ST-Microelectronics/portstr75xiar)

    Also preconfigured to run on the [STR750 EVAL](http://www.st.com/internet/evalboard/product/132197.jsp) evaluation board from STMicroelectronics, this application
    demonstrates FreeRTOS on the ST STR750 ARM7TDMI microcontroller with the [Raisonance RIDE IDE interface](https://www.raisonance.com/ride7.html) to
    the [GNUARM GCC toolchain](http://www.gnuarm.org/).

  - [ST Microelectronics STR71x ARM7 with IAR development tools](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ST-Microelectronics/portstr71xiar)

    This demo is preconfigured to run on the [IAR STR712 KickStart development kit](http://www.st.com/internet/evalboard/product/152464.jsp). It uses the KickStart
    prototyping board, USB JTAG debugger interface and the [IAR Embedded Workbench development tools for ARM](http://www.iar.com/ewarm).

- STR9 ARM9 based microcontrollers

  - [STMicroelectronics STR9 ARM9 with the IAR development tools](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ST-Microelectronics/portstr912iar)

    This is the first FreeRTOS ARM9 port. The demo application is pre-configured to run on the STR910-EVAL development. It includes web server demos using lwIP.

### Demos targeting Synopsys DesignWare ARC Products

The FreeRTOS download does not contain official ARC support, but the following options are available to users wishing to run the RTOS on DesignWare ARC microcontrollers:

- The [embARC](https://embarc.org/) Open Software Platform consists of software and documentation to accelerate the development of embedded and IoT systems based on DesignWare ARC processors.
- Our official partner company, WITTENSTEIN high integrity systems, can provide [OPENRTOS for various ARC processors](http://www.highintegritysystems.com/openrtos).

### Demos targeting Texas Instruments products

**These demos can be adapted to any microcontroller within the same family that has sufficient ROM/RAM. See
the [Creating a new application](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project) and [Adapting a Demo](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party) pages.**

Following the acquisition of Luminary Micro by Texas Instruments this section now includes demos that target Stellaris microcontrollers.

- SimpleLink IoT microcontrollers

  - [CC3220 using Code Composer Studio (CCS)](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Texas-Instruments/TI_CC3220_SimpleLink_FreeRTOS_Demo)

    Targets the SimpleLink CC3220SF Wireless (WiFi) Microcontroller LaunchPad Development Kit.

- MSP432 ARM Cortex-M4F based microcontrollers

  - [MSP432P401R IAR, Keil, CCS](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Texas-Instruments/TI_MSP432_Free_RTOS_Demo)

    The demo application targets the Texas Instruments MSP432 microcontroller - which is a variant of the MSP430 low power microcontroller that uses an ARM Cortex-M4F core.
    Pre-configured MSP432 projects that target the MSP432P401R Launchpad Development Kit are provided for the IAR, Keil and CCS development tools.

- MSP430 and MSP430X based microcontrollers

  - [MSP430FR5969 IAR Embedded Workbench and Code Composer Studio](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Texas-Instruments/MSP430FR5969_Free_RTOS_Demo)

    This demo targets the [Texas Instruments MSP430FR5969](http://www.ti.com/product/msp430fr5969) low power microcontroller, which has a 16-bit MSP430X core.
    Pre-configured projects that target the [MSP-EXP430FR5969](http://www.ti.com/tool/msp-exp430fr5969#0) Launchpad Development Kit are provided for both
    the [IAR](https://www.iar.com/iar-embedded-workbench/texas-instruments/msp430/) and [Code Composer Studio](http://www.ti.com/ccs) (CCS) MSP430 compilers.

  - [MSP430X core (MSP430F5438) IAR Embedded Workbench](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Texas-Instruments/Free-RTOS-for-MSP430X-MSP430F5438-Experimenter-Board-using-IAR)

    This is a FreeRTOS demo application for the [MSP430X / MSP430F5438 microcontroller](http://focus.ti.com/docs/prod/folders/print/msp430f5438.html)
    from [Texas Instruments](http://www.ti.com/). The demo uses the [IAR Embedded Workbench for MSP430](https://www.iar.com/products/architectures/iar-embedded-workbench-for-msp430/) from IAR Systems, and targets
    the official [MSP-EXP430F5438](http://focus.ti.com/docs/toolsw/folders/print/msp-exp430f5438.html) experimenter board from TI.

  - [MSP430X core (MSP430F5438) Code Composer Studio 4](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Texas-Instruments/Free-RTOS-for-MSP430X-MSP430F5438-Experimenter-Board-using-CCS)

    This version of the FreeRTOS MSP430X demo application also targets the [MSP430X / MSP430F5438 microcontroller](http://focus.ti.com/docs/prod/folders/print/msp430f5438.html)
    from [Texas Instruments](http://www.ti.com/), but uses TI's own [Code Composer Studio 4](http://focus.ti.com/docs/toolsw/folders/print/ccstudio.html) development tools.
    **This demo has now been superseded, see the MSP-EXP430FR5969 demo above**

  - [MSP430 Rowley CrossWorks](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Texas-Instruments/portmspcrossworks)

    The demo is pre-configured to run on the [ES449 prototyping board](http://www.softbaugh.com/ProductPage.cfm?strPartNo=ES449) from [SoftBaugh](http://www.softbaugh.com/),
    with a [MSP430F449](http://focus.ti.com/docs/prod/folders/print/msp430f449.html) microcontroller. The prototyping board includes a built in LCD - which is great for
    debugging. The port uses the Rowley Associates [CrossWorks](http://www.rowley.co.uk/) tool suite along with a FETP JTAG debugger. Two slightly different port
    implementations are included.

  - [MSP430 MSPGCC (GCC)](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Texas-Instruments/portmspgcc)

    As per the MSP430 CrossWorks port, but using the [MSPGCC development tools](http://mspgcc.sourceforge.net/) which includes a prebuilt Win32 build of GCC.

- Stellaris ARM Cortex-M3 based microcontrollers

  - [FreeRTOS Demo for QEMU LM3S6965 Model](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Texas-Instruments/cortex-m3-qemu-lm3S6965-demo)

    A pre-configured Eclipse project that builds and runs the FreeRTOS ARM Cortex-M3 GCC port in the LM3S6965 QEMU model.

  - [LM3S102 with the Keil development tools](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Texas-Instruments/portcortexkeil)

    Port and demo application for [Texas Instruments](https://www.ti.com/microcontrollers-mcus-processors/arm-based-microcontrollers/arm-cortex-m4-mcus/overview.html) Stellaris ARM Cortex-M3 based processor that uses the new ARM Keil development tools (RVDS).
    The demo application is pre-configured for the DK-LMS102 development, and uses both co-routines and tasks.

  - [LM3S811 with the Keil development tools](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Texas-Instruments/portlm3s811keil)

    Another demo application for the Texas Instruments Stellaris ARM Cortex-M3 Keil port, this time target at an LM3S811 evaluation board.

  - [LM3S102 with GCC](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Texas-Instruments/portcortexgcc)

    Another port and demo application for [Texas Instruments](https://www.ti.com/microcontrollers-mcus-processors/arm-based-microcontrollers/arm-cortex-m4-mcus/overview.html) Stellaris ARM Cortex-M3 based processor, but this time using the GCC development tools.

  - [LM3S102 with CrossWorks](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Texas-Instruments/portcortexcrossworks)

    This port and demo application for [Texas Instruments](https://www.ti.com/microcontrollers-mcus-processors/arm-based-microcontrollers/arm-cortex-m4-mcus/overview.html) Stellaris ARM Cortex-M3 based processor includes two demos for the Texas Instruments
    development board, and a simple co-routine demo for the new low cost [CrossFire LM3S102](http://www.rowley.co.uk/crossfire/crossfire_lm3s102.htm) from Rowley Associates.
    All demos can be compiled and debugged using [CrossWorks for ARM](http://www.rowley.co.uk/arm/index.htm).

  - [LM3S316 with IAR](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Texas-Instruments/portcortexiar)

    Another Stellaris port, this time with the demo application targeted at an LM3S316 and using the [IAR development tools](http://www.iar.com/).

- Hercules Safety Microcontrollers

  - [RM48 and TMS570 Code Composer Studio](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Texas-Instruments/Free_RTOS_for_TI_RM48_and_TMS570)

    Two projects with identical functionality. One targets the RM48 USB stick evaluation platform, and the other the TMS570 USB stick. Both use the FreeRTOS ARM Cortex-R4F CCS port.

  - TMS470M TMS470MF06607 USB stick

    **[[Unofficial](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party) third party demo, links to the FreeRTOS Interactive site]**
    Uses Code Composer Studio V5.

### Demos targeting Xilinx products

**These demos can be adapted to any microcontroller within the same family that has sufficient ROM/RAM. See the [Creating a new application](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project)
and [Adapting a Demo](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party) pages.**

- Zynq

  - [Zynq using the official FreeRTOS Cortex-A9 port](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Xilinx/RTOS-Xilinx-Zynq)

    A demo that uses the official Cortex-A9 RTOS port to run FreeRTOS on a ZC702 evaluation board using the Xilinx SDK and GCC. This demo uses a stand alone BSP and
    builds FreeRTOS as part of the application.

  - [Zynq using a FreeRTOS BSP](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Xilinx/RTOS-Xilinx-SDK-BSP)

    A demonstration of how the Xilinx SDK can be used to create a FreeRTOS BSP. Including FreeRTOS in the BSP presents the application writer with a pre-configured FreeRTOS
    environment that does not require any source files to be added manually, any callback functions to be provided by the application code, and allows FreeRTOSConfig.h to
    be edited within the IDE.

- Zynq UltraScale MPSoC

  - [Using FreeRTOS on an UltraScale ARM Cortex-A53 (64-bit) Core](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Xilinx/RTOS-Xilinx-UltraScale_MPSoC_64-bit)

    The first FreeRTOS port and demo application to run native 64-bit! The demo is pre-configured to run on the ZCU102 evaluation board. FreeRTOS support is provided for all the
    cores (ARM and Microblaze) found on the many-core Xilinx Zynq UltraScale+ MPSoC.

  - [Using FreeRTOS on an UltraScale ARM Cortex-R5 Core](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Xilinx/RTOS-ARM-Cortex-R5-Xilinx-UltraScale_MPSoC)

    Simply blinky and comprehensive demos that run on one of the ARM Cortex-R5 cores on the Zynq UltraScale+ MPSoC. The demo is pre-configured to run on the ZCU102 evaluation board.
    FreeRTOS support is provided for all the cores (ARM and Microblaze) found on the many-core Xilinx Zynq UltraScale+ MPSoC.

- Microblaze

  - [Xilinx Microblaze](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Xilinx/RTOS-Xilinx-Microblaze-KC705) [most recent demo]

    This MicroBlaze demo was produced using version 2014.4 of Xilinx's [Vivado Design Suite](http://www.xilinx.com/products/design-tools/vivado.html/), supports version 8.x of
    the [MicroBlaze soft processor core](http://www.xilinx.com/tools/microblaze.htm), and was developed and tested on a Kintex FPGA on
    a [KC705 Evaluation Kit](http://www.xilinx.com/products/boards-and-kits/ek-k7-kc705-g.html) board.

  - [Xilinx Microblaze](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Xilinx/Free-RTOS-for-Xilinx-MicroBlaze-on-Spartan-6-FPGA)

    This MicroBlaze port is produced using version 13.1 of the [Xilinx ISE Design Suite (Embedded Edition)](http://www.xilinx.com/products/design-tools/ise-design-suite/),
    supports version 8.10 of the [MicroBlaze soft processor core](http://www.xilinx.com/tools/microblaze.htm), and was developed and tested on a Spartan-6 FPGA
    based [SP605 Evaluation Kit](http://www.xilinx.com/products/boards-and-kits/EK-S6-SP605-G.htm). **This demo has now been superseded, see the Kintex demo above.**

  - [Xilinx Microblaze](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Xilinx/portmicroblaze)

    A [Microblaze soft processor core](http://www.xilinx.com/products/design_resources/proc_central/microblaze.htm) port running on a Virtex4 FPGA. The demo is preconfigured
    to execute on an [ML403 development board](http://www.xilinx.com/products/boards/ml403/docs.htm). **This port and demo has now been superseded, see the Kintex demo above.**

- PowerPC 405

  - [Xilinx Virtex-4 PowerPC (PPC405)](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Xilinx/Free-RTOS-PPC405-Xilinx-Virtex4)

    A PowerPC configurable processor core running on a Virtex4 FPGA. The demo is also preconfigured to execute on
    an [ML403 development board](http://www.xilinx.com/products/boards/ml403/docs.htm).

- PowerPC 440

  - [Xilinx Virtex-5 PowerPC (PPC440)](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Xilinx/PPC440-Xilinx-Virtex5)

    A PowerPC configurable processor core running on a Virtex5 FPGA. Configurations are provided with no FPU, single precision FPU and double precision FPU.

### Demos targeting XMOS products

- [XCORE.AI Explorer](/Documentation/02-Kernel/03-Supported-devices/04-Demos/XMOS/smp-demo-for-xmos-xcore-ai-explorer-board)

  This demo uses the Symmetric Multiprocessing (SMP) version of the FreeRTOS kernel. It targets the
  XCORE.AI, which has 16 cores. The demo project uses XMOS XTC Tools to build the FreeRTOS XCOREAI
  port. It demonstrates support for FreeRTOS symmetric multiprocessing (SMP) in the kernel.

### Demos targeting Intel IA32 and any x86 products

- [IA32 / Intel Quark SoC X1000 in 32-bit mode](/Documentation/02-Kernel/03-Supported-devices/04-Demos/x86/RTOS_Intel_Quark_Galileo_GCC)

  The demo presented on this page used GCC and Eclipse to run FreeRTOS on an [Intel Galileo](https://software.intel.com/iot/hardware/galileo) single board computer.

- [Industrial PC Single Board Computer](/Documentation/02-Kernel/03-Supported-devices/04-Demos/x86/Industrial-PC-Port)

  This will run on a huge variety of PC/AT compatible industrial and single board computers, including PC/104 systems. It can use
  the [Open Watcom](http://www.openwatcom.org/) or Borland development tools, for both of which a pre-configured project file is provided. See the Tools page.

- [RDC8822 Based Single Board Computer](/Documentation/02-Kernel/03-Supported-devices/04-Demos/x86/RDC8822)

  This runs on the very competitively priced Flashlite 186 single board computer from [JK Microsystems](http://www.jkmicro.com/). The RDC8822 is an AMD embedded 186
  clone (AM186ED). It can use the [Open Watcom](http://www.openwatcom.org/) or Borland development tools (see Tools). Again a pre-configured project file is provided
  for both compilers.

- [RDC R1120 Based Single Board Computer](/Documentation/02-Kernel/03-Supported-devices/04-Demos/x86/portternee)

  Includes a simple web server demo running on a [Tern](http://www.tern.com/) E-Engine controller using a memory mapped WizNET TCP/IP co-processor. The RDC1120 is an AMD
  embedded 186 clone (AM186ES). The demo application builds with the Paradigm C/C++ compiler and can be remotely debugged from within the compiler IDE.

### Simulators and emulators

- [Windows Simulator for Visual Studio and Eclipse with MingW (GCC)](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)

  This allows FreeRTOS to be run in a Windows environment - although true real time behaviour cannot be achieved. Demo projects are provided for both Eclipse with
  MingW (GCC) and Visual Studio community edition. Both these tool chains are free, although Visual Studio Express requires registration if it is to be used for
  anything other than evaluation purposes. The demo's documentation page describes the principle of the simulated operation.

- [POSIX port that runs on Linux (GCC)](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Linux/FreeRTOS-simulator-for-Linux)

  This allows FreeRTOS to run on Linux - although true real time behaviour cannot be achieved. The demo's documentation page describes the principle of the simulated operation.

- [QEMU Cortex-M3 model using IAR or GCC (makefile and Eclipse)](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/QEMU/freertos-on-qemu-mps2-an385-model)

  A FreeRTOS kernel demo that targets the Arm Cortex-M3 mps2-an385 QEMU model. Preconfigured build projects are provided for both the IAR Embedded Workbench
  and arm-none-eabi-gcc (GNU GCC) compilers. The GCC project uses a simple makefile that can be built from the command line or the provided Eclipse CDT IDE project.
