---
title: FreeRTOS Library Categories
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


## Introduction

Each library documented on this website falls into one of the categories described below. All the libraries
are [MIT (open source) licensed](/Documentation/03-Libraries/01-Library-overview/04-Licensing) and are designed for resource constrained devices such as
microcontrollers and small microprocessors. FreeRTOS core and FreeRTOS for AWS libraries do not have any
dependencies other than on the standard C library – they are not even dependent on an RTOS.


### Category Descriptions

**The FreeRTOS kernel**
The FreeRTOS kernel itself. This library includes the RTOS kernel, intertask communication primitives and
intertask synchronisation primitives.
[Learn More](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/01-FreeRTOS-kernel)


**FreeRTOS Plus**
Libraries that implement additional functionality and, unlike the core libraries (see below), have a dependency
on the FreeRTOS RTOS kernel.
[Learn More](/Documentation/03-Libraries/02-FreeRTOS-plus/01-Introduction)


**FreeRTOS Core**
Libraries that implement open standards based connectivity, security, and related functionality. These
libraries are suitable for building smart microcontroller-based devices that connect to the cloud. Unlike
the FreeRTOS-Plus libraries (see above), FreeRTOS Core libraries have no dependencies other than on the
standard C libraries, so FreeRTOS Core libraries are not dependent on the FreeRTOS RTOS kernel.
[Learn More](/Documentation/03-Libraries/03-FreeRTOS-core/01-Introduction)


**FreeRTOS for AWS IoT**
Libraries that implement clients for AWS IoT specific value add cloud services, including over the air
updates (OTA). These libraries are suitable for building smart microcontroller-based devices that connect
to the AWS IoT cloud. Like the FreeRTOS core libraries, they have no dependencies on anything other than
the standard C library, so are not dependent on the FreeRTOS RTOS kernel.
[Learn More](/Documentation/03-Libraries/04-AWS-libraries/01-Introduction)


**FreeRTOS Labs**
FreeRTOS Labs libraries are functional but either incomplete, experimental, or simply provided for open
source community interest. See the individual library documentation pages for a description of which
criteria applies to that library.
[Learn More](/Documentation/03-Libraries/05-FreeRTOS-labs/01-Introduction)
