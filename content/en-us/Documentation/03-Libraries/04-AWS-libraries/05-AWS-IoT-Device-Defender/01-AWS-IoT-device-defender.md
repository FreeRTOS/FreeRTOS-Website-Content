---
title: "AWS IoT Device Defender"
created: 2018-09-20
categories:
  - libraries
description: An introduction to the AWS IoT Device Defender library
relatedLinks: 
  - title: Device defender Github repository
    link: https://github.com/aws/Device-Defender-for-AWS-IoT-embedded-sdk
externalLinks: 
  - title: AWS IoT Device Defender Client Library
    link: https://aws.github.io/Device-Defender-for-AWS-IoT-embedded-sdk/v1.3.0/
 
---

## Introduction

The AWS IoT Device Defender library enables you to send security metrics from your IoT devices to the 
AWS IoT Device Defender service. The AWS IoT Device Defender service lets you continuously monitor these 
security metrics from devices for deviations from what you have defined as appropriate behavior for 
each device. If something doesn’t look right, AWS IoT Device Defender sends out an alert so you can 
take action to remediate the issue. More details about AWS IoT Device Defender can be found 
in [AWS IoT documentation](https://docs.aws.amazon.com/iot/latest/developerguide/device-defender.html). 
Interactions with the AWS IoT Device Defender service use [MQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT), a lightweight 
publish-subscribe protocol. This library provides a convenient API to compose and recognize the MQTT 
topic strings used by the AWS IoT Device Defender service. 

The library is written in C and designed to be compliant with [ISO C90](https://en.wikipedia.org/wiki/ANSI_C#C90) 
and [MISRA C:2012](https://misra.org.uk/misra-c/). The library 
has no dependencies on any additional libraries other than the standard C library. It also doesn’t 
have any platform dependencies, such as threading or synchronization. It can be used with any MQTT 
library and any [JSON](/Documentation/03-Libraries/03-FreeRTOS-core/07-coreJSON/02-coreJSON-terminology) or [CBOR](https://cbor.io/) library. The library 
has [proofs](https://www.cprover.org/cbmc/) showing safe memory use and no heap allocation, making it 
suitable for IoT microcontrollers, but also fully portable to other platforms.

AWS IoT Device Defender library can be freely used and is distributed under the [MIT open source license](/Documentation/03-Libraries/01-Library-overview/04-Licensing).


**Code Size of AWS IoT Device Defender (example generated with GCC for ARM Cortex-M)**

| File | With -O1 Optimization | With -Os Optimization |
| --- | --- | --- |
| defender.c | 1.1K | 0.6K |
| Total estimates | 1.1K | 0.6K |
