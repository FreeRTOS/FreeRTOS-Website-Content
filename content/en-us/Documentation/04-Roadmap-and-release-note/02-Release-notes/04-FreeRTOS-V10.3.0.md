---
title: "Upgrading From FreeRTOS V10.2.1 to V10.3.0"
created: 2018-09-20
categories:
  - roadmap and release notes
description: Information on Upgrading From FreeRTOS V10.2.1 to V10.3.0
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


### Backward Compatibility

FreeRTOS 10.3.0 contains the new configuration options described in the sections below. New
options that are left undefined will default to a value that ensures backward compatibility
with FreeRTOS V10.2.x. Therefore FreeRTOS 10.3.0 is a backward compatible drop-in replacement for
FreeRTOS V10.2.1.


### ARM Cortex-M Memory Protection Unit (MPU) Ports

The ARMv7-M (ARM Cortex-M3, ARM Cortex-M4F and ARM Cortex-M7) ports that use
the Memory Protection Unit (MPU) have the following new configuration option:

* configENFORCE\_SYSTEM\_CALLS\_FROM\_KERNEL\_ONLY

When configENFORCE\_SYSTEM\_CALLS\_FROM\_KERNEL\_ONLY is defined to 1 in
FreeRTOSConfig.h, privilege escalations can only occur from within FreeRTOS
kernel code (other than escalations performed by the hardware itself when an
interrupt is entered). It requires that all the functions with
freertos\_system\_calls attribute are placed in a separate section and the
following two additional variables are exported from linker scripts to inform
the location of this section:

* \_\_syscalls\_flash\_start\_\_
* \_\_syscalls\_flash\_end\_\_

Pre-configured examples are provided for GCC, Keil uVision and IAR Embedded
Workbench in the FreeRTOS/Demo/CORTEX\_MPU\_STM32L4\_Discovery\_GCC\_IAR\_Keil
and FreeRTOS/Demo/CORTEX\_MPU\_M3\_NUCLEO\_L152RE\_GCC directories.
See [FreeRTOS Memory Protection Unit (MPU) Support](/Security/04-FreeRTOS-MPU-memory-protection-unit) for more
details about how to use FreeRTOS-MPU ports.


### RISC-V Ports

The configCLINT\_BASE\_ADDRESS configuration setting is deprecated and
replaced by configMTIME\_BASE\_ADDRESS and configMTIMECMP\_BASE\_ADDRESS.
The new settings are described on the [Using FreeRTOS on RISC-V Microcontrollers](/Using-FreeRTOS-on-RISC-V)
documentation page.  Legacy applications that still use configCLINT\_BASE\_ADDRESS
will generate a compiler warning, but otherwise continue to build and function as
before.


### Other Changes

See the [change history](/Documentation/04-Roadmap-and-release-note/02-Release-notes/00-Release-history) for more details of new ports and other enhancements.
