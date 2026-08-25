---
title: FreeRTOS-Plus-TCP with unified IPv4 and IPv6 functionalities and multi-interface support now generally available
date: 16 Aug 2023
feature: blog
authors:
  - stanmoy
---

We are excited to release FreeRTOS-Plus-TCP v4.0.0 with unified IPv4 and IPv6 functionalities and multi-interface 
support as generally available. Developers can now use the FreeRTOS-Plus-TCP library for IPv6-based embedded 
applications, design applications that use multiple network interfaces, and choose combinations of IPv6, IPv4, 
TCP, and UDP within the same library to optimize for memory footprint.

FreeRTOS-Plus-TCP has been checked for memory safety with the C Bounded Model 
Checker ([CBMC](/Community/Blogs/2020/ensuring-the-memory-safety-of-freertos-part-1)) 
automated reasoning tool, which is intended to help mitigate code security issues such as buffer overflow. 
In addition, FreeRTOS-Plus-TCP has been penetration tested and has undergone certain code quality checks 
including [MISRA-C](https://www.misra.org.uk/) compliance and [Coverity](https://scan.coverity.com/) static 
analysis, which are intended to help improve code safety, portability, and reliability in embedded 
systems (see [LTS Code Quality Checklist](/Documentation/03-Libraries/01-Library-overview/03-LTS-libraries/01-LTS-libraries#lts-code-quality-checklist)). 
To learn more and get started, refer to the FreeRTOS-Plus-TCP library introduction page 
on [freertos.org](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP), 
the [demo](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Demo/FreeRTOS_Plus_TCP_IPv6_Demo/IPv6_Multi_WinSim_demo), 
or the code on [GitHub](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP).

