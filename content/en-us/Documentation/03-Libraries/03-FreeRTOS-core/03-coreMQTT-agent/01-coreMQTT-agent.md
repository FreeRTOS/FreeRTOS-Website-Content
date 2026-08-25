---
title: "coreMQTT agent"
created: 2018-09-20
categories:
  - kernel
description: An introduction to the MQTT C client library
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: Beginner's guide to FreeRTOS
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: Download FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: FAQs
    link: /Why-FreeRTOS/FAQs
externalLinks:
  - title: coreMQTT agent API reference
    link: https://freertos.github.io/coreMQTT-Agent/v1.2.0/
---


Thread-safe MQTT C client library for small IoT devices (MCU or small MPU)


## Introduction

The coreMQTT Agent library is a high level API that adds thread safety to the [coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT) 
library. It lets you create a dedicated MQTT agent task that manages an MQTT connection in the background 
and doesn't need any intervention from other tasks. The library provides thread safe equivalents to the 
coreMQTT's APIs, so it can be used in multi-threaded environments.

The MQTT agent is an independent task (or thread of execution). It achieves thread safety by being the 
only task that is permitted to access the MQTT library's API. It serializes access by isolating all MQTT 
API calls to a single task, and it removes the need for semaphores or any other synchronization primitives.

The library uses a thread safe messaging queue (or other inter-process communication mechanism) to serialize 
all requests to call MQTT APIs. The messaging implementation is decoupled from the library through a messaging 
interface, which allows the library to be ported to other operating systems. The messaging interface is 
composed of functions to send and receive pointers to the agent's command structures, and functions to allocate
these command objects, which allows the application writer to decide the memory allocation strategy appropriate 
for their application.

The library is written in C and designed to be compliant with [ISO C90](https://en.wikipedia.org/wiki/ANSI_C#C90) 
and [MISRA C:2012](https://misra.org.uk/misra-c/). The library has no 
dependencies on any additional libraries other than [coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT) and the standard C library. The 
library has [proofs](https://www.cprover.org/cbmc/) that show safe memory use and no heap allocation, so it 
can be used for IoT microcontrollers, but is also fully portable to other platforms.

This library can be freely used and is distributed under the [MIT open source license](/Documentation/03-Libraries/01-Library-overview/04-Licensing).


**Code Size of coreMQTT Agent (example generated with GCC for ARM Cortex-M)**

| File | With -O1 Optimization | With -Os Optimization |
| --- | --- | --- |
| core\_mqtt\_agent.c | 1.7K | 1.5K |
| core\_mqtt\_agent\_command\_functions.c | 0.3K | 0.2K |
| core\_mqtt.c (coreMQTT) | 4.0K | 3.4K |
| core\_mqtt\_state.c (coreMQTT) | 1.7K | 1.3K |
| core\_mqtt\_serializer.c (coreMQTT) | 2.8K | 2.2K |
| Total estimates | 10.5K | 8.6K |

Memory Estimation includes [coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT) library
