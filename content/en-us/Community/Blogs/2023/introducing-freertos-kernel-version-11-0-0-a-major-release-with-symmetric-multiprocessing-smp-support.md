---
title: "Introducing FreeRTOS Kernel version 11.0.0: A Major Release with Symmetric Multiprocessing (SMP) Support"
date: 15 Dec 2023
feature: blog
authors:
  - aggarg
---
FreeRTOS Kernel version 11.0.0 is now available for [download](https://github.com/FreeRTOS/FreeRTOS-Kernel/releases/tag/V11.0.0). This release includes the following features:

* While FreeRTOS introduced Asymmetric Multiprocessing (AMP) support in 2017, FreeRTOS version 11.0.0
 is the first to merge Symmetric Multiprocessing (SMP) support into the mainline release. SMP enables
 one instance of the FreeRTOS Kernel to schedule tasks across multiple identical processor cores.
 The simplest way to get started is to use one of the following pre-configured example projects:


	+ [XCORE AI](https://github.com/FreeRTOS/FreeRTOS-Community-Supported-Demos/tree/main/XCORE.AI_xClang)
	+ [Raspberry Pico](https://github.com/FreeRTOS/FreeRTOS-Community-Supported-Demos/tree/main/CORTEX_M0%2B_RP2040)
	+ [TI Sitara AM64x](https://github.com/FreeRTOS/FreeRTOS-Partner-Supported-Demos/tree/main/CORTEX_A53_64-BIT_TI_AM64_SMP)See the [FreeRTOS SMP webpage](/Documentation/02-Kernel/02-Kernel-features/13-Symmetric-multiprocessing-introduction) for details.
* Switched MISRA compliance checking from PC Lint to Coverity, and updated from MISRA C:2004 to MISRA C:2012.
* Several security enhancements to the FreeRTOS ports with Memory Protection Support (MPU) for greater security.
* Enhanced tracing support for enhanced integration with tracing tools.
* Several other enhancements and optimizations such as updates to `vTaskList` and
 `vTaskGetRunTimeStats` that protect against buffer overflows, heap hardening, CMake
 improvements etc.


FreeRTOS V11.0.0 is a drop-in replacement for FreeRTOS V10.6.x.


Refer the [release notes](/Documentation/04-Roadmap-and-release-note/02-Release-notes/00-Release-history) for a complete list of changes. We're looking forward to your
continued feedback. Visit the [FreeRTOS forums](https://forums.freertos.org/) if you have comments or requests!
