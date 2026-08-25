---
title: 从 FreeRTOS V10.4.5 升级到 V10.4.6
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

FreeRTOS V10.4.6 是 FreeRTOS V10.4.5 的升级版，
适用于除带有内存保护单元（MPU）支持的 ARMv7-M 移植以外的所有移植。


**ARMv7-M MPU 移植**

支持内存保护单元（MPU）的 FreeRTOS ARMv7-M (ARM Cortex-M3/4/7) 移植包含新的
配置选项 [configALLOW_UNPRIVILEGED_CRITICAL_SECTIONS](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configallow_unprivileged_critical_sections)。
在 FreeRTOSConfig.h 中将该常量设置为 0 可防止非特权应用程序任务
使用 [taskENTER_CRITICAL()](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/01-taskENTER_CRITICAL_taskEXIT_CRITICAL) 宏创建临界区。
将该常量设置为 1，或者不定义它，可保持与之前 FreeRTOS MPU 内核
版本的兼容性，可使特权和非特权任务创建临界区。注意：
建议将常量定义为 0 以获得最大安全性；因此，如果未定义常量，
会输出编译器警告。
