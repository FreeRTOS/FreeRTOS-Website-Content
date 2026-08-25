---
title: "coreMQTT"
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

external links:
  - title: coreMQTT API reference
    link: https://freertos.github.io/coreMQTT/v2.1.1/
---

**MQTT C client library for small IoT devices (MCU or small MPU)**


## Introduction

The coreMQTT library is a client implementation of the [MQTT](https://en.wikipedia.org/wiki/MQTT) standard. 
The MQTT standard provides a lightweight [publish/subscribe](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern) 
messaging protocol that runs on top of TCP/IP and is often used in Machine to Machine (M2M) and Internet of 
Things (IoT) use cases.

The coreMQTT library is compliant with the [MQTT 3.1.1](http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/mqtt-v3.1.1.html) 
protocol standard. This library has been optimized for a low memory footprint. The design of this library embraces 
different use-cases, ranging from resource-constrained platforms using 
only [QoS 0 (Quality of Service level 0) MQTT PUBLISH messages](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/01-MQTT-terminology), to resource-rich platforms 
using [QoS 2 MQTT PUBLISH](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/01-MQTT-terminology) over [TLS (Transport Layer Security)](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/03-TLS-terminology) connections. 
The library provides a menu of composable functions, a combination of which can be chosen to precisely 
fit a specific use case.

The library provides a high-level API to connect to an MQTT broker, subscribe or unsubscribe to a topic, 
publish a message to a topic and receive incoming messages. The library also exposes a low-level serializer/deserializer 
API. This low-level API handles formatting and parsing messages, leaving the application full, zero-overhead 
control over the network connection to the MQTT broker.

The library is decoupled from the underlying network drivers through 
a [two-function send and receive transport interface](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/01-Transport-interface). The application writer can 
select an existing transport interface or implement their own, as appropriate for their application.

The library is written in C and designed to be compliant with [ISO C90](https://en.wikipedia.org/wiki/ANSI_C#C90) 
and [MISRA C:2012](https://misra.org.uk/misra-c/). The library has 
no dependencies on any additional libraries other than the standard C library. The library 
has [proofs](https://www.cprover.org/cbmc/) showing safe memory use and no heap allocation, making it suitable 
for IoT microcontrollers, but also fully portable to other platforms.

When using MQTT connections in IoT applications, we recommend that you use a secure transport interface, 
such as one that uses the TLS protocol as demonstrated in the [MQTT TLS](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication) demo.

This library can be freely used and is distributed under the [MIT open source license](/Documentation/03-Libraries/01-Library-overview/04-Licensing).


**Code Size of coreMQTT (example generated with GCC for ARM Cortex-M)**
| File | With -O1 Optimization | With -Os Optimization |
| ---- | --------------------- | --------------------- |
| core\_mqtt.c | 4.0K | 3.4K |
| core\_mqtt\_state.c | 1.7K | 1.3K |
| core\_mqtt\_serializer.c | 2.8K | 2.2K |
| Total estimates | 8.5K | 6.9K |
