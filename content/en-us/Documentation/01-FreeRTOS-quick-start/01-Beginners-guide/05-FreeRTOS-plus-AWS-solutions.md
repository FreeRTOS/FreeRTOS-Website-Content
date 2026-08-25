---
title: "FreeRTOS + AWS IoT solutions"
created: 2018-09-20
categories:
  - kernel
description: A brief introduction to FreeRTOS kernel
relatedLinks:
  - title: AWS IoT OTA library
    link: /Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates
  - title: AWS IoT device shadow library
    link: /Documentation/03-Libraries/04-AWS-libraries/03-AWS-IoT-Device-Shadow/01-AWS-IoT-device-shadow
  - title: AWS IoT jobs library
    link: /Documentation/03-Libraries/04-AWS-libraries/04-AWS-IoT-Jobs/01-AWS-IoT-jobs
  - title: AWS IoT device defender library
    link: /Documentation/03-Libraries/04-AWS-libraries/05-AWS-IoT-Device-Defender/01-AWS-IoT-device-defender
  - title: AWS IoT fleet provisioning library
    link: /Documentation/03-Libraries/04-AWS-libraries/06-AWS-IoT-Fleet-Provisioning/01-AWS-IoT-fleet-provisioning
  - title: AWS IoT signature version 4 library
    link: /Documentation/03-Libraries/04-AWS-libraries/07-AWS-Signature-Version-4/01-AWS-signature-version-4
  - title: AWS IoT quick connect
    link: /Why-FreeRTOS/Quick-Connect
  - title: AWS partner device cataloge
    link: https://devices.amazonaws.com/search?page=1&sv=freertos

previous:
  title: FreeRTOS libraries and 3rd party tools
  link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/04-FreeRTOS-libraries-and-3rd-party-tools
next:
  title: Join the FreeRTOS community
  link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/06-Join-the-FreeRTOS-community
---

**How FreeRTOS + AWS bring you simple and secure IoT solutions.**

## Introduction
First, AWS IoT [ExpressLink](/Documentation/03-Libraries/08-Featured-integrations/06-STM32-Expresslink)
provides the simplest and fastest way to connect to AWS IoT.
If that is not a suitable path for your project, then read on....

[AWS IoT](https://aws.amazon.com/iot/) provides services
and solutions suitable for connecting and managing billions of IoT devices.

Two of the library categories described on the [libraries introduction page](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/04-FreeRTOS-libraries-and-3rd-party-tools)
are FreeRTOS Core, and FreeRTOS for AWS.  [FreeRTOS Core libraries](/Documentation/03-Libraries/03-FreeRTOS-core/01-Introduction)
implement standard and cloud agnostic functionality, such
as a [small MQTT client](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT).
These libraries are only dependent on a subset of the
standard C library, making them suitable for use in almost any system, with or without
an operating system.  If you use FreeRTOS Core libraries to connect to AWS IoT, or
any other library to do the same, then [FreeRTOS for AWS libraries](/Documentation/03-Libraries/04-AWS-libraries/01-Introduction) help you access
AWS IoT specific value add cloud services.

All the libraries are MIT open source licensed.

![FreeRTOS + AWS](/media/2024/FreeRTOS-Plus.png)


## Getting started

### Simple FreeRTOS projects

If you are new to FreeRTOS then it's recommended to familiarize yourself with the
kernel before using any additional libraries.  The quick start guide includes a
[build your first FreeRTOS project](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project)
page that describes how to do this even if you don't have hardware yet, as it describes
running demos in Windows, Linux, and using the free QEMU software emulator.

### Simple connectivity libraries

Once familiar with the kernel, experiment with one or two libraries at a time.
[Each library](/Documentation/03-Libraries/01-Library-overview/01-All-libraries)
has its own documentation page, with links to that libraries pre-configured
demo provided in the left menu.

You can progress in steps from adding just local TCP/IP connectivity, to unauthenticated
MQTT connectivity (this is just for learning, never use unauthenticated connections in production!), to authenticated
MQTT connections, and further.

### Progressing to AWS connectivity, first step

The pre-configured [AWS Quick Connect](/Why-FreeRTOS/Quick-connect) demos already
build the necessary AWS IoT libraries on top of the connectivity libraries, so provide
a good introduction to AWS connectivity.

### Explore AWS IoT libraries

Once you have an understanding of how an IoT device and AWS IoT work together, you can start
exploring FreeRTOS for AWS IoT libraries individually, ending up at the
[featured FreeRTOS IoT reference integrations](/Documentation/03-Libraries/08-Featured-integrations/01-Featured-integrations)
which are comprehensive, and demonstrate security best practices.

## Develop your AWS IoT applications

Follow these steps to create an AWS IoT connectivity project for a devices not
already supported by a pre-configured demo:

1. Download the latest FreeRTOS or Long Term Support (LTS) version, or clone from
   the [FreeRTOS-LTS](https://github.com/FreeRTOS/FreeRTOS-LTS) GitHub repository. You can also integrate
   the required FreeRTOS libraries into your project from
   the [MCU vendor's toolchain](/Community/Blogs/2021/freertos-lts-libraries-are-now-part-of-our-partner-toolchains)
   if available.

2. Follow the [FreeRTOS Porting guide](https://docs.aws.amazon.com/freertos/latest/portingguide/porting-guide.html)
   to create a project, set up the development environment, and integrate FreeRTOS libraries into your project.
   Use the [FreeRTOS-Libraries-Integration-Tests](https://github.com/FreeRTOS/FreeRTOS-Libraries-Integration-Tests)
   GitHub repository to validate the porting.
