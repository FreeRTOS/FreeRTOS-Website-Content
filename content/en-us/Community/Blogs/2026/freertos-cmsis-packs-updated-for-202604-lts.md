---
title: "FreeRTOS CMSIS Packs updated for 202604.00-LTS"
date: 03 Jun 2026
feature: blog
categories:
  - Long term support
  - What's new
authors:
  - lesau
---

by [Victor Lesau](../author/lesau) on 03 Jun 2026

[FreeRTOS](https://aws.amazon.com/freertos/) now provides its latest Long Term Support (202604.00-LTS) libraries as CMSIS Packs. Embedded teams building on Arm Cortex-M microcontrollers can now manage FreeRTOS dependencies directly through their IDE's built-in pack manager, eliminating manual source integration.

This release includes FreeRTOS kernel v11.3.0 with new hardware port support and security hardening, and AWS IoT connectivity libraries including MQTT v5.0 protocol support for bandwidth-efficient device communication. Developers using any IDE or toolchain that supports the CMSIS-Pack format, such as Keil MDK, Keil Studio, or IAR Embedded Workbench, can add these libraries directly from their pack manager.

For source files and release notes, see [FreeRTOS CMSIS-Packs on GitHub](https://github.com/FreeRTOS/CMSIS-Packs). To browse available packs, see the [official pack index](https://www.keil.arm.com/packs/?q=&pack-search=&vendor=aws&contents=software_only&sort_by=name).
