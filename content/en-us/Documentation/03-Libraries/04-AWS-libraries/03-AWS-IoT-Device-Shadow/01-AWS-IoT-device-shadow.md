---
title: "AWS IoT Device Shadow"
created: 2018-09-20
categories:
  - kernel
description: An introduction to the AWS IoT Device Shadow library
relatedLinks: 
  - title: Device shadow Github repository
    link: https://github.com/aws/Device-Shadow-for-AWS-IoT-embedded-sdk
externalLinks: 
  - title: AWS IoT Device Shadow Library
    link: https://aws.github.io/Device-Shadow-for-AWS-IoT-embedded-sdk/v1.3.0/
---


## Introduction

The AWS IoT Device Shadow library enables you to store and retrieve the current 
state (the ["shadow"](/Documentation/03-Libraries/04-AWS-libraries/03-AWS-IoT-Device-Shadow/03-Shadow-terminology)) of every IoT device registered in 
your [AWS IoT](https://aws.amazon.com/iot/) account. The device's shadow is a persistent, virtual 
representation of your IoT device that you can interact with in your applications even if the device 
is offline. The device state captured as its "shadow" is itself represented as a [JSON](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/01-corePKCS11) 
document. You can send commands to the AWS IoT Device Shadow service over MQTT or HTTP to query the 
latest known device state, or to change the state. Each IoT device's shadow is uniquely identified by 
the name of the corresponding "thing". A "thing" is a representation of a specific IoT device or logical 
entity in the AWS Cloud. 
See [Managing Devices with AWS IoT](https://docs.aws.amazon.com/iot/latest/developerguide/iot-thing-management.html) 
for more information. More details about shadows can be found 
in [AWS IoT documentation](https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-shadows.html).

AWS IoT Device Shadow library is written in C and designed to be compliant 
with [ISO C90](https://en.wikipedia.org/wiki/ANSI_C#C90) 
and  [MISRA C:2012](https://misra.org.uk/misra-c/). It has no 
dependencies on additional libraries other than the standard C library. It also doesn't have any platform 
dependencies, such as threading or synchronization. It can be used with any MQTT library and any JSON 
library. This library has [proofs](https://www.cprover.org/cbmc/) showing safe memory use, and does 
not perform any dynamic memory allocation, making it suitable for IoT microcontrollers, but also fully 
portable to other platforms.

The AWS IoT Device Shadow library can be freely used and is distributed under the [MIT open source license](/Documentation/03-Libraries/01-Library-overview/04-Licensing).

**Code Size of AWS IoT Device Shadow (example generated with GCC for ARM Cortex-M)**

| File | With -O1 Optimization | With -Os Optimization |
| --- | --- | --- |
| shadow.c | 1.2K | 0.9K |
| Total estimates | 1.2K | 0.9K |
