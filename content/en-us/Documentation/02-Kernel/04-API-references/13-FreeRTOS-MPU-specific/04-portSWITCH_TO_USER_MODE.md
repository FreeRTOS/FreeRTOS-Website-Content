---
title: "portSWITCH_TO_USER_MODE"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-MPU Specific](/Documentation/02-Kernel/04-API-references/13-FreeRTOS-MPU-specific/00-FreeRTOS-MPU-specific)]

task.h

```c
void portSWITCH_TO_USER_MODE( void );
```

Sets the calling task into User mode. Once in User mode a task cannot return to Privileged mode.

portSWITCH\_TO\_USER\_MODE() is intended for use with [FreeRTOS-MPU](/Security/04-FreeRTOS-MPU-memory-protection-unit),
the [demo applications](/Security/04-FreeRTOS-MPU-memory-protection-unit#FreeRTOS-MPU-Demos) for which contain
an example of portSWITCH\_TO\_USER\_MODE() being used.
