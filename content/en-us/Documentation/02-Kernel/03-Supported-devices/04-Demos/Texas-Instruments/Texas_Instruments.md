---
title: FreeRTOS For TI Embedded MCUs
---

## Introduction
This page links to documentation pages for the most up-to-date RTOS projects
that target Texas Instruments embedded processors. Links to older RTOS projects
can be found on the main [RTOS ports page](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#TI).

## MSP432 (ARM Cortex-M4F core)
Supporting IAR, ARM (Keil), and TI (CCS) compilers

![Texas Instruments MSP432 Launchpad Development Kit](/media/2018/MSP432_Launchpad_Development_Kit.jpg)

The MSP-EXP432P401R LaunchPad Development Kit

[This page](TI_MSP432_Free_RTOS_Demo) documents the demo application that targets the
[Texas Instruments MSP432 microcontroller](http://www.ti.com/MSP432)
 - which is a variant of the MSP430 low power microcontroller
that uses an ARM Cortex-M4F core.

Pre-configured MSP432 projects that target the MSP432P401R Launchpad Development
Kit are provided for the IAR, ARM and TI (CCS) compilers.

Each project can be compiled to create either a simple blinky demo,
or a comprehensive test and demo application.

The comprehensive demo uses [FreeRTOS-Plus-CLI](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI)
 to create a simple command line interface through a UART.

The blinky demo uses FreeRTOS's tickless idle mode to reduce power consumption.

[Read More About the MSP432 Demo . . .](TI_MSP432_Free_RTOS_Demo)

## MSP430FR5969 (MSP430X core)
Supporting IAR, and TI (CCS) compilers
![Texas Instruments MSP430 MSP-EXP430FR5969 Launchpad Development Kit](/media/2018/MSP-EXP430FR5969.jpg)

### The MSP-EXP430FR5969 LaunchPad Development Kit
[This page](MSP430FR5969_Free_RTOS_Demo) documents the RTOS demo
application that targets the
[Texas Instruments MSP430FR5969](http://www.ti.com/product/msp430fr5969)
low power microcontroller, which has a 16-bit MSP430X core.

Pre-configured projects that target the
[MSP-EXP430FR5969](http://www.ti.com/tool/msp-exp430fr5969#0) Launchpad Development
Kit are provided for both the [IAR](https://www.iar.com/iar-embedded-workbench/texas-instruments/msp430/)
and [Code Composer Studio](http://www.ti.com/ccs) (CCS) MSP430 compilers:

Each project can be compiled to create either a simple blinky demo,
or a comprehensive test and demo application that includes a
[FreeRTOS-Plus-CLI](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI)
 command line interface. Further, build configurations are provided that use both
 the large and small data models.

[Read More About the MSP430FR5969 Demo . . .](MSP430FR5969_Free_RTOS_Demo)
