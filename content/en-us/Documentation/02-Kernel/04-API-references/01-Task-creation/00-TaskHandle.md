---
title: Task Creation
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

## Modules

- [xTaskCreate](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate/)
- [xTaskCreateStatic](/Documentation/02-Kernel/04-API-references/01-Task-creation/02-xTaskCreateStatic)
- [xTaskCreateRestrictedStatic](/Documentation/02-Kernel/04-API-references/13-FreeRTOS-MPU-specific/02-xTaskCreateRestrictedStatic)
- [vTaskDelete](/Documentation/02-Kernel/04-API-references/01-Task-creation/03-vTaskDelete/)


## Detailed Description

### TaskHandle_t

task.h

Type by which tasks are referenced. For example, a call to `xTaskCreate` returns (via a pointer parameter) 
an `TaskHandle_t` variable that can then be used as a parameter to `vTaskDelete` to delete the task.
