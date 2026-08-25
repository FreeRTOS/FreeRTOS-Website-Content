---
title: Upgrading From FreeRTOS V10.4.5 to V10.4.6
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

FreeRTOS V10.4.6 is a drop in replacement for FreeRTOS V10.4.5 for all ports other than ARMv7-M ports
with Memory Protection Unit (MPU) support.


**ARMv7-M MPU Ports**

The FreeRTOS ARMv7-M (ARM Cortex-M3/4/7) ports with memory protection unit (MPU) support include a new
configuration option [configALLOW\_UNPRIVILEGED\_CRITICAL\_SECTIONS](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configallow_unprivileged_critical_sections).
Setting this constant to 0 in FreeRTOSConfig.h prevents unprivileged application tasks from using
the [taskENTER\_CRITICAL()](/Documentation/02-Kernel/04-API-references/04-RTOS-kernel-control/01-taskENTER_CRITICAL_taskEXIT_CRITICAL) macro to create a critical section.
Set the constant to 1, or leave it undefined, to maintain compatibility with previous FreeRTOS MPU kernel
versions, which allow both privileged and unprivileged tasks to create critical sections. Note: It is
recommended to set the constant to 0 for maximum security; because of this, a compiler warning is output
if the constant is left undefined.
