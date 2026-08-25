---
title: "SNTP C client library for small IoT devices (MCU or small MPU)"
created: 2018-09-20
categories:
  - kernel
description: An introduction to the coreSNTP library
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
externalLinks:
  - title: coreSNTP API reference
    link: https://freertos.github.io/coreSNTP/v1.2.0/
---


## Introduction

The coreSNTP library provides a client for the **Simple Network Time Protocol (SNTP)** to allow devices
to synchronize their system clocks with time servers. This library implements the SNTPv4 specification
defined in [RFC 4330](https://tools.ietf.org/html/rfc4330). An SNTP client can request the time from
both NTP and SNTP servers.

The library provides two API layers to provide different levels of development flexibility to application
developers. Either of these layers can be used by the application developer to create an SNTP client in
their application:

1. **Serializer/Deserializer and Utilities** - This layer provides functions to serialize SNTP time
   requests and deserialize SNTP response packets, as well as some utility functions that are helpful when
   you set up an SNTP client in an application.

2. **Client** - This layer provides additional ***managed*** functionality for network operations including
   DNS resolution, sending and receiving SNTP packets over UDP, authenticating servers for security (if enabled),
   notifying the system to correct its time with information from the server, as well as handling rejection
   of time requests by servers. This layer calls the Serializer/De-Serializer layer to serialize and deserialize
   SNTP packets sent and received on the network. (Note: This layer performs network and authentication operations
   through a user-defined implementation of the interfaces exposed by the library.)

The **Serializer/De-serializer layer** does not have a dependency on any interface. It can be integrated
in an application for use as-is, whereas the **Client layer** decouples from platform-specific calls by
exposing the interface operations of network I/O, cryptographic calculations and getting and updating system time. If
you develop against the **Client** layer, you must implement these interfaces for your platform. For more
information on the interfaces, refer to the [Porting Guide](https://freertos.github.io/coreSNTP/main/sntp_porting.html).

The library is written in C and designed to be compliant
with [ISO C90](https://en.wikipedia.org/wiki/ANSI_C#C90) and [MISRA C:2012](https://www.misra.org.uk/).
The library has no dependencies on any additional libraries other than the standard C library. The library
has [proofs](https://www.cprover.org/cbmc/) showing safe memory use and no heap allocation, making it
suitable for IoT microcontrollers, but also fully portable to other platforms.

When you design an SNTP client for time synchronization in your application, we recommend that you use
authentication to communicate with the SNTP/NTP servers you have chosen. Mutual authentication provides
protection against malicious modification or spoofing of server responses, and thereby prevents malicious
corruption of time in devices. For an example of using authentication with coreSNTP library, refer to the
coreSNTP demo.

This library can be freely used and is distributed under the [MIT open source license](/Documentation/03-Libraries/01-Library-overview/04-Licensing).

**Code Size of coreSNTP (example generated with GCC for ARM Cortex-M)**

| File | With -O1 Optimization | With -Os Optimization |
| --- | --- | --- |
| core\_sntp\_client.c | 1.5K | 1.2K |
| core\_sntp\_serializer.c | 1.0K | 0.8K |
| Total estimates | 2.5K | 2.0K |
