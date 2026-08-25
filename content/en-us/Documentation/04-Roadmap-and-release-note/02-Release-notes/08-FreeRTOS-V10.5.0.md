---
title: Upgrading From FreeRTOS V10.4.6 to V10.5.0
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

FreeRTOS V10.5.0 is a drop in replacement for FreeRTOS V10.4.6 for all ports other than ARMv7-M and 
ARMv8-M ports with Memory Protection Unit (MPU) support. 


**ARMv7-M and ARMv8-M MPU Ports**

The FreeRTOS ARMv7-M (ARM Cortex-M3/4/7) and ARMv8-M (ARM Cortex-M23/33/55) ports with memory protection 
unit (MPU) support can no longer create privileged tasks from unprivileged tasks using xTaskCreate or 
xTaskCreateStatic APIs. Also, unprivileged tasks can no longer call the following APIs:

* xTimerCreate
* xTimerCreateStatic
* xTimerPendFunctionCall

The application writer needs to perform these operations either before starting the scheduler, or from 
a privileged task.
