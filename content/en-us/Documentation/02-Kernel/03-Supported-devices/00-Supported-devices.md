---
title: "Supported Devices"
created: 2018-09-20
categories:
  - kernel
description: FreeRTOS supported MCUs
relatedLinks: 
  - title: FreeRTOS porting guide
    link: /Documentation/02-Kernel/03-Supported-devices/01-FreeRTOS-porting-guide/
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: Beginner's guide to FreeRTOS
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: Download FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: FAQs
    link: /Why-FreeRTOS/FAQs/Why-FreeRTOS/FAQs
---

**Don't see an exact match for your microcontroller part number and compiler vendor choice?**  These 
demos can be adapted to any microcontroller within a supported microcontroller family. See 
the [Creating a new FreeRTOS application](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project) 
and [Adapting a FreeRTOS Demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos) documentation pages. As 
many IDEs are now based on Eclipse, also see the page that 
describes [how to use virtual and linked paths in the Eclipse project explorer](/Documentation/02-Kernel/03-Supported-devices/04-Demos/IDE/Project_Workspace_Relative_File_Paths_Eclipse)
to ensure you do not need to copy the RTOS source files into an Eclipse project directory.

FreeRTOS ports are categorised as either being officially supported, or contributed. 
The [Official and Contributed Definitions](/Documentation/02-Kernel/03-Supported-devices/03-Official-vs-3rd-party) 
page describes the categories, and the rationale for making the distinction. This page only lists the official RTOS ports.

**No hardware yet?** Don't worry - see the [Demo Quick Start page](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project#getting-started-with-simple-freertos-demo-projects) for links to Windows and 
Linux ports, as well as Arm Cortex-M3 QEMU projects.
 

| Hardware Partner | Supported Processor Families | Supported Tools |
| --- | --- | --- |
| __A__ |
| [Altera](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-altera-products) | Cyclone V SoC (ARM Cortex-A9), Nios II | Altera SoC EDS (ARM DS-5 with GCC), Nios II IDE with GCC |
| [ARMv8-M](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-armv8-m-products-and-simulators) <br/>Note this category is just for simulated targets. Other ARMv8-M targets are in their respective vendor categories. | ARM Cortex-M33 simulator | GCC (and ARMclang building the FreeRTOS ARMv8-M GCC port) |
| [Armv8-R](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-armv8-r-products-and-simulators) | Cortex-R82 | GCC, ArmClang |
| [Atmel](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-atmel-now-microchip-products) | SAMV7 (ARM Cortex-M7), SAM3 (ARM Cortex-M3), SAM4 (ARM Cortex-M4 ), SAMD20 (ARM Cortex-M0+), SAMA5 (ARM Cortex-A5), SAM7 (ARM7), SAM9 (ARM9), AT91, AVR and AVR32 UC3 | IAR, GCC, Keil, Rowley CrossWorks |
| __C__ |
| [Cadence](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-cadence-tensilica-products) | Tensilica Xtensa | XCC with the Xtensa Xplora IDE |
| [CEVA](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-ceva-dsp-products) | SensPro, SensPro2, CEVA-BX1, CEVA-BX2, CEVA-X1, CEVA-X2, CEVA-XC16, CEVA-XM6, CEVA-XM4, CEVA-XC12, CEVA-XC4500 <br /> | LLVM |
| [Cortus](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-cortus-products) | APS3 | Cortus IDE with GCC |
| [Cypress](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-cypress-products) | PSoC 5 ARM Cortex-M3 | GCC, ARM Keil and RVDS - all in the PSoC Creator IDE |
| __F__ |
| [Freescale](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-freescale-products) | Kinetis ARM Cortex-M4, Coldfire V2, Coldfire V1, other Coldfire families, HCS12, PPC405 & PPC440 (Xilinx implementations) (small and banked memory models), plus contributed ports | Codewarrior, GCC, Eclipse, IAR |
| __I__ |
| [Infineon](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-infineon-products) | AURIX™ TC3xx, XMC4000 (ARM Cortex-M4F), XMC1000 (ARM Cortex-M0) | GCC, Keil, Tasking, IAR |
| [Fujitsu (Now](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#fujitsu) [Spansion](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-spansion-products)[)](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#fujitsu) | FM3 ARM Cortex-M3, 32bit (for example MB91460) and 16bit (for example MB96340 16FX) | Softune, IAR, Keil |
| __L__ |
| [Luminary Micro / Texas Instruments](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-luminary-micro-products). See also [TI](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-texas-instruments-products). | All Luminary Micro ARM Cortex-M3 and ARM Cortex-M4 based Stellaris microcontrollers | Keil, IAR, Code Red, CodeSourcery GCC, Rowley CrossWorks |
| __M__ |
| [Microchip](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-microchip-products). <br/>See also [Microsemi (now Microchip)](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-microsemi-now-microchip-products). | PIC32MX, PIC32MZ, PIC32MZ EF, PIC24, dsPIC33C, dsPIC33E, dsPIC33F, MEC14xx, CEC13xx, CEC17xx, MEC17xx, MEC51xx | [XC Compilers](https://www.microchip.com/xc) |
| [Microsemi](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-microsemi-now-microchip-products) | MiFive (RISC-V), SmartFusion, SmartFusion2 | IAR, Keil, SoftConsole (GCC with Eclipse) |
| __N__ |
| [NEC (now Renesas)](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-renesas-products) | V850 (32bit), 78K0R (16bit) | IAR |
| [Nuvoton](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-nuvoton-products) | NuMicro M2351 (ARM Cortex-M23) | IAR, Keil |
| [NXP](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-nxp-products) | VEGAboard (RISC-V), LPC55S6x(ARM Cortex-M33), LPC1500 (ARM Cortex-M3), LPC1700 (ARM Cortex-M3), LPC1800 (ARM Cortex-M3), LPC1100 (ARM Cortex-M0), LPC2000 (ARM7), LPC4000 (ARM Cortex-M4F/ ARM Cortex-M0) | GCC, Rowley CrossWorks, IAR, Keil, LPCXpresso IDE, Eclipse, MCUXpresso IDE |
| __R__ |
| [Renesas](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-renesas-products) | RZ/A1 / RZ/A2M, (ARM Cortex-A9), RZ/T, RX700 / RX71M, RX600 / RX64M / RX62N / RX63N / RX65N, RX200, RX100, SuperH, RL78, H8/S plus contributed ports | GCC, e2 studio, IAR Embedded Workbench, HEW (High Performance Embedded Workbench) |
| __S__ |
| [SiFive](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-sifive-products) | RISC-V RV32 | Freedom Studio (GCC), IAR |
| [Silicon Labs [ex Energy Micro]](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-silicon-labs-products) | EFM32 Gecko (Cortex-M3 and Cortex-M4F), 8051 compatible microcontrollers. | Simplicity Studio (GCC), IAR, SDCC |
| [Spansion](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-spansion-products) | FM3 ARM Cortex-M3, 32bit (for example MB91460) and 16bit (for example MB96340 16FX) | Softune, IAR, Keil |
| [ST](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-st-microelectronics-products) | STM32 (ARM Cortex-M0, ARM Cortex-M7, ARM Cortex-M3 and ARM Cortex-M4F), STR7 (ARM7), STR9 (ARM9) | IAR, Atollic TrueStudio, GCC, Keil, Rowley CrossWorks |
| __T__ |
| [TI](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-texas-instruments-products) | RM48, TMS570, ARM Cortex-M4F MSP432, MSP430, MSP430X, SimpleLink, Stellaris (ARM Cortex-M3, ARM Cortex-M4F) | Rowley CrossWorks, IAR, GCC, Code Composer Studio |
| __X__ |
| [Xilinx](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-xilinx-products) | Zynq, Zynq UltraScale+ MPSoC (64-bit ARM Cortex-A53 and 32-bit ARM Cortex-R5), Microblaze, PPC405 running on a Virtex4 FPGA, PPC440 running on a Virtex5 FPGA. | GCC |
| [Intel/x86](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#demos-targeting-intel-ia32-and-any-x86-products) | IA32 (32-bit flat memory model), Quark SoC X1000 (32-bit flat memory model), any x86 compatible running in Real mode only, plus a [Win32 port](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW). A port for the [Linux Simulator](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Linux/FreeRTOS-simulator-for-Linux)  is available as well.  | GCC, Visual Studio 2010 Express, MingW, Open Watcom, Borland, Paradigm |
| Tricore, MICO32, Blackfin, Jennic, eZ80, SuperH and others. | *Contributed Ports* | Contributed ports are provided "as is" and are not supported directly. |
