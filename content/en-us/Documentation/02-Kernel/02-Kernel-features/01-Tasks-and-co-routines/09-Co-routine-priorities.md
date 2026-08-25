---
title: "FreeRTOS co-routines"
created: 2018-09-20
categories:
  - kernel
description: FreeRTOS scheduling algorithm for single-core, asymmetric multicore (AMP), and symmetric multicore (SMP) RTOS configurations
relatedLinks: 
  - title: API reference - Co-routines
    link: /Documentation/02-Kernel/04-API-references/14-Co-routines/00-Co-routine API/
  - title: Co-routine example
    link: /Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/11-Co-routine-example/
---

[[More about co-routines...](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/06-Co-routine-overview)]


### Co-Routine Priorities

Each co-routine is assigned a priority from 0 to ( configMAX\_CO\_ROUTINE\_PRIORITIES - 1 ). 
configMAX\_CO\_ROUTINE\_PRIORITIES is defined within FreeRTOSConfig.h and can be set on an application 
by application basis.

Low priority numbers denote low priority co-routines.

Co-routine priorities are only with respect to other co-routines. Tasks will always take priority over 
co-routines should you mix tasks and co-routines within the same application.
