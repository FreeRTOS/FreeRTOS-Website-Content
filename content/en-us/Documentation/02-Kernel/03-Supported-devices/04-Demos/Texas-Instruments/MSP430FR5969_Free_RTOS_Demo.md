---
title: "TI MSP430FR5969 (MSP430X) RTOS Demo Supporting IAR, and TI (CCS) compilers"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![Texas Instruments MSP430 MSP-EXP430FR5969 Launchpad Development Kit](/media/2018/MSP-EXP430FR5969.jpg)

**The MSP-EXP430FR5969 LaunchPad Development Kit**

### Introduction

This page documents the RTOS demo application that targets the
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

### A note on low power support

The [Idle hook](/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions) is used to place the MSP430 MCU into a low
power mode as a crude method of saving power. The provision of a
[tickless idle](/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support)
implementation would significantly improve the power saving that could be
achieved, but is not configured in this demonstration.

|  |
| --- |
| [![FreeRTOS kernel aware debugger used with the IAR compiler](/media/2018/FreeRTOS-Kernel-Aware-Plug-In-Cortex-M0.jpg)](/media/2018/FreeRTOS-Kernel-Aware-Plug-In-Cortex-M0.jpg)<br/><br/><br/><br/>**Screen shot of the FreeRTOS state viewer plug-in<br/> <br/> that ships with the IAR IDE. Click to enlarge.** <br/><br/> |
