---
title: "coreHTTP"
created: 2018-09-20
categories:
  - kernel
description: An introduction to the coreHTTP library
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/

external links:
  - title: coreHTTP API reference
    link: https://freertos.github.io/coreHTTP/v3.0.0/
---

coreHTTP
 
HTTP C client library for small IoT devices (MCU or small MPU)


## Introduction

The coreHTTP library is a client implementation of a subset of 
the [HTTP/1.1](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol) standard. The HTTP standard 
provides a stateless protocol that runs on top of TCP/IP and is often used in distributed, collaborative, 
hypertext information systems.

The coreHTTP library implements a subset of the [HTTP/1.1](https://tools.ietf.org/html/rfc2616) protocol 
standard. This library has been optimized for a low memory footprint. The library provides a fully synchronous 
API to allow applications to completely manage their concurrency. The library also operates only on fixed 
buffers, so that applications have complete control of their memory allocation strategy.

The library provides a high-level simple API to serialize request headers, send the request, and receive the response.

The library is decoupled from the underlying network drivers through 
a [two-function send and receive transport interface](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/01-Transport-interface). The application writer 
can select an existing transport interface or implement their own, as appropriate for their application.

The library is written in C and designed to be compliant 
with [ISO C90](https://en.wikipedia.org/wiki/ANSI_C#C90) 
and [MISRA C:2012](https://misra.org.uk/misra-c/). The 
library's only dependencies are the standard C library 
and [LTS version (v12.19.1) of http-parser](https://github.com/nodejs/node/tree/v12.19.1/deps/http_parser) 
from Node.js. The library has [proofs](https://www.cprover.org/cbmc/) showing safe memory use and no heap 
allocation, making it suitable for IoT microcontrollers, but also fully portable to other platforms.

When using HTTP connections in IoT applications, we recommend that you use a secure transport interface, 
such as one that uses the TLS protocol as demonstrated in the [HTTP TLS](/Documentation/03-Libraries/03-FreeRTOS-core/04-coreHTTP/03-coreHTTP-demos/02-Mutual-authentication)
demo.

This library can be freely used and is distributed under the [MIT open source license](/Documentation/03-Libraries/01-Library-overview/04-Licensing).


**Code Size of coreHTTP (example generated with GCC for ARM Cortex-M)**

| File | With -O1 Optimization | With -Os Optimization |
| --- | --- | --- |
| core\_http\_client.c | 3.2K | 2.6K |
| api.c (llhttp) | 2.6K | 2.0K |
| http.c (llhttp) | 0.3K | 0.3K |
| llhttp.c (llhttp) | 17.9 | 15.9 |
| Total estimates | 23.9K | 20.7K |
