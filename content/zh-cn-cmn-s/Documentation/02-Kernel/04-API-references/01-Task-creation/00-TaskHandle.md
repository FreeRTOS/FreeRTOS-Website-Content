---
title: 创建任务
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

## 模块

- [xTaskCreate](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate/)
- [xTaskCreateStatic](/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic)
- [xTaskCreateRestrictedStatic](/Documentation/02-Kernel/04-API-references/13-FreeRTOS-MPU-specific/02-xTaskCreateRestrictedStatic)
- [vTaskDelete](/Documentation/02-Kernel/04-API-references/01-Task-creation/03-vTaskDelete/)


## 详细描述

### TaskHandle_t

task.h

任务引用的类型。例如，调用 `xTaskCreate`（通过指针参数） 
返回 `TaskHandle_t` 变量，然后可以将该变量用作 `vTaskDelete` 的参数来删除任务。
