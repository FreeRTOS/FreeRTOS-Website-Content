---
title: 从 FreeRTOS V10.4.6 升级到 V10.5.0
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

FreeRTOS V10.5.0 是 FreeRTOS V10.4.6 的升级版，适用于除 ARMv7-M 
以及支持内存保护单元（MPU）的 ARMv8-M 移植以外的所有移植。 


**ARMv7-M 和 ARMv8-M MPU 移植**

FreeRTOS ARMv7-M (ARM Cortex-M3/4/7) 和 ARMv8-M (ARM Cortex-M23/33/55) 移植 
（带有内存保护单元 (MPU) 支持）不再能够使用 xTaskCreate 
或 xTaskCreateStatic API 从非特权任务创建特权任务。此外非特权任务也无法再调用以下 API：

* xTimerCreate
* xTimerCreateStatic
* xTimerPendFunctionCall

应用程序写入器需要在启动调度器之前 
或从一个特权任务中执行这些操作。
