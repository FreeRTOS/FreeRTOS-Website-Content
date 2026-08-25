---
title: Backoff Algorithm
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


## Introduction


The [backoffAlgorithm](https://github.com/FreeRTOS/backoffAlgorithm) library is a utility library to space 
out repeated retransmissions of the same block of data, to avoid network congestion. This library calculates 
backoff period for retrying network operations (like failed network connection with server) using 
an [exponential backoff with jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/) 
algorithm. 


Exponential backoff with jitter is typically used when retrying a failed connection or network request to 
the server. An exponential backoff with jitter helps to mitigate the failed network operations with servers, 
that are caused due to network congestion or high load on the server, by spreading out retry requests across 
multiple devices attempting network connections. Besides, in an environment with poor connectivity, a client 
can get disconnected at any time. A backoff strategy helps the client to conserve battery by not repeatedly 
attempting reconnections when they are unlikely to succeed. 


The library is written in C and designed to be compliant with [ISO C90](https://en.wikipedia.org/wiki/ANSI_C#C90) 
and [MISRA C:2012](https://misra.org.uk/misra-c/). The library has 
no dependencies on any additional libraries other than the standard C library and has no heap allocation, 
making it suitable for IoT microcontrollers, but also fully portable to other platforms.

See the backoffAlgorithm library [API Reference](https://freertos.github.io/backoffAlgorithm/v1.3.0/).

This library can be freely used and is distributed under the [MIT open source license](/Documentation/03-Libraries/01-Library-overview/04-Licensing).


**Code Size of backoffAlgorithm (example generated with GCC for ARM Cortex-M)**

| File | With -O1 Optimization | With -Os Optimization |
| --- | --- | --- |
| backoff\_algorithm.c | 0.1K | 0.1K |
| Total estimates | 0.1K | 0.1K |
