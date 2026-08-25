---
title: FreeRTOS FAQ - Scheduling
created: 2018-09-20
description: Information on FreeRTOS scheduling
---


## What is the FreeRTOS scheduling policy?

See the [page dedicated to describing](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/04-Task-scheduling) both the single core 
and multicore scheduling policies.


## How are tasks of equal priority scheduled?

Round robin - Ready state tasks that share a priority "take turns" to run.


## How are tasks that share the idle priority scheduled?

As per tasks that share any other priority. However, the [configIDLE\_SHOULD\_YIELD](/Documentation/02-Kernel/03-Supported-devices/02-Customization) 
configuration constant can be used to force the idle task to yield after a single iteration of its loop 
if other idle priority application tasks are able to run.
