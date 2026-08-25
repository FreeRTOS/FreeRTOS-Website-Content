---
title: "portSWITCH_TO_USER_MODE"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-MPU 特定](/Documentation/02-Kernel/04-API-references/13-FreeRTOS-MPU-specific/00-FreeRTOS-MPU-specific)]

task. h

```c
void portSWITCH_TO_USER_MODE( void );
```

将调用任务设置为用户模式。一旦进入用户模式，任务就无法返回特权模式。

portSWITCH_TO_USER_MODE() 适用于 [FreeRTOS-MPU](/Security/04-FreeRTOS-MPU-memory-protection-unit)，
其[演示应用程序](/Security/04-FreeRTOS-MPU-memory-protection-unit#FreeRTOS-MPU-Demos)包含
使用 portSWITCH_TO_USER_MODE() 的示例。
