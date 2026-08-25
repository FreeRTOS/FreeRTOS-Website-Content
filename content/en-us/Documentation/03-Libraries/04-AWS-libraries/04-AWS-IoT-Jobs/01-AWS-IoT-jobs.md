---
title: "AWS IoT Jobs"
created: 2018-09-20
categories:
  - kernel
description: An introduction to the AWS IoT Jobs library
relatedLinks: 
  - title: Jobs Github repository
    link: https://github.com/aws/Jobs-for-AWS-IoT-embedded-sdk
externalLinks: 
  - title: AWS IoT Jobs Client Library
    link: https://aws.github.io/Jobs-for-AWS-IoT-embedded-sdk/v1.3.0/
 
---

## Introduction

AWS IoT Jobs is a service that notifies one or more connected devices of a pending ["Job"](/Documentation/03-Libraries/04-AWS-libraries/04-AWS-IoT-Jobs/02-Jobs-terminology). 
You can use a Job to manage your fleet of devices, update firmware and security certificates on your 
devices, or perform administrative tasks such as restarting devices and performing diagnostics. For 
documentation of the service, please see [Jobs](https://docs.aws.amazon.com/iot/latest/developerguide/iot-jobs.html) 
in the *AWS IoT Core Developer Guide*. Interactions with the Jobs service use [MQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT), 
a lightweight publish-subscribe protocol. This library provides a convenient API to compose and recognize 
the MQTT topic strings used by the Jobs service. 

The AWS IoT Jobs library is written in C and designed to be compliant with [ISO C90](https://en.wikipedia.org/wiki/ANSI_C#C90) 
and [MISRA C:2012](https://misra.org.uk/misra-c/). The library 
has no dependencies on any additional libraries other than the standard C library. It can be used with 
any MQTT library and any JSON library. The library has [proofs](https://www.cprover.org/cbmc/) showing 
safe memory use and no heap allocation, making it suitable for IoT microcontrollers, but also fully 
portable to other platforms.

This library can be freely used and is distributed under the [MIT open source license](/Documentation/03-Libraries/01-Library-overview/04-Licensing).


**Code Size of AWS IoT Jobs (example generated with GCC for ARM Cortex-M)**

| File | With -O1 Optimization | With -Os Optimization |
| --- | --- | --- |
| jobs.c | 1.9K | 1.6K |
| Total estimates | 1.9K | 1.6K |
