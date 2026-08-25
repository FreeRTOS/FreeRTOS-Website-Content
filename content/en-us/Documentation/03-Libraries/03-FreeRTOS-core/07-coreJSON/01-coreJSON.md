---
title: "coreJSON"
created: 2018-09-20
categories:
  - kernel
description: An introduction to the coreJSON library
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/

external links:
  - title: coreJSON API reference
    link: https://freertos.github.io/coreJSON/v3.2.0/
---


Parser library that strictly enforces the ECMA-404 JSON standard


## Introduction

JSON (JavaScript Object Notation) is a human-readable data serialization format which comes from JavaScript. 
It is widely used to exchange data, such as with the [AWS IoT Device Shadow service](/Documentation/03-Libraries/04-AWS-libraries/03-AWS-IoT-Device-Shadow/01-AWS-IoT-device-shadow), and 
is part of many APIs, such as the [GitHub REST API](https://developer.github.com/v3/). JSON is maintained as 
a standard by Ecma International.

The coreJSON library provides a parser that supports [key lookups](/Documentation/03-Libraries/03-FreeRTOS-core/07-coreJSON/02-coreJSON-terminology) while strictly enforcing 
the standard ([ECMA-404: The JSON Data Interchange Standard](http://www.ecma-international.org/publications/files/ECMA-ST/ECMA-404.pdf)). 
The library is written in C and designed to comply with [ISO C90](https://en.wikipedia.org/wiki/ANSI_C#C90) 
and  [MISRA C:2012](https://misra.org.uk/misra-c/). 
It has [proofs](https://www.cprover.org/cbmc/)  showing safe memory use and no heap allocation, making it 
suitable for IoT microcontrollers, but also fully portable to other platforms. 


### Source Code Organization and Demos

The coreJSON library can be found in the [main FreeRTOS download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) in 
the [FreeRTOS/FreeRTOS-Plus/Source/coreJSON](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Source) 
directory. A demonstration of the coreJSON library can viewed in 
the [IoT Device Shadow demo](/Documentation/03-Libraries/04-AWS-libraries/03-AWS-IoT-Device-Shadow/04-Device-shadow-demo). 


### Memory Usage

The coreJSON library uses an internal stack to track nested structures in a JSON document. The stack 
exists for the duration of a single function call; it is not preserved. Stack size may be specified by 
defining the macro JSON\_MAX\_DEPTH, which defaults to 32 levels. Each level consumes a single byte. 


**Code Size of coreJSON (example generated with GCC for ARM Cortex-M)**

| File | With -O1 Optimization | With -Os Optimization |
| --- | --- | --- |
| core\_json.c | 2.9K | 2.4K |
| Total estimates | 2.9K | 2.4K |
