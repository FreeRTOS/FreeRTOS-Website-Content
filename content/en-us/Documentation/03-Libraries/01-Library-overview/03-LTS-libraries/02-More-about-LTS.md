---
title: "FreeRTOS LTS Roadmap"
created: 2018-09-20
categories:
  - kernel
description: The FreeRTOS development roadmap
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
---

This page captures the status of each library in our Long Term Support (LTS) release roadmap. All libraries
listed on this page have or are being refactored to meet the modularity and code quality criteria
stated [below](#lts-code-quality-checklist). Libraries are moved into the main FreeRTOS download as they meet the criteria (each
library also has its [own Github repository](https://github.com/FreeRTOS)). When all the libraries are in
the main FreeRTOS download they, and the FreeRTOS kernel, will be released with Long Term Support.

## LTS Status

**Last Updated: 11/10/2020**

| Library | Stage |
| ------- | ----- |
| [FreeRTOS-Plus-TCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP) | In the main [download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) |
| [coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT) (works with any TCP/IP stack) | In the main [download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) |
| [corePKCS11](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/01-corePKCS11) | In the main [download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) |
| [coreJSON](/Documentation/03-Libraries/03-FreeRTOS-core/07-coreJSON/01-coreJSON) | In the main [download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) |
| [AWS IoT Device Shadow](/Documentation/03-Libraries/04-AWS-libraries/03-AWS-IoT-Device-Shadow/01-AWS-IoT-device-shadow) | In the main [download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) |
| OTA                                                        | In progress                                                                                                  |
| HTTPS                                                      | In progress                                                                                                  |
| AWS IoT Jobs                                               | In progress                                                                                                  |

## LTS Code Quality Checklist

| #   | Category                   | Checks |
| --- | -------------------------- | ------ |
| 1   | Complexity Score | All functions will have a [GNU Complexity](https://www.gnu.org/software/complexity/manual/complexity.html) score of 8 or lower |
| 2   | Coding Standard | All functions will comply with the [MISRA coding standard](/Documentation/02-Kernel/06-Coding-guidelines/02-FreeRTOS-Coding-Standard-and-Style-Guide/#coding-standard--misra-compliance) |
| 3   | Static Checking | All code will be statically checked with [Coverity](https://scan.coverity.com/) |
| 4   | Function Returns | All functions will have a single exit point |
| 5   | Code Testing | All code will have extensive unit tests. Gcov reports will be used to report the test coverage, and each library will have extended functional tests. |
| 6   | Requirements Documentation | All libraries will have documented requirements, which may include resource requirements, listing all dependencies, and porting requirements (as applicable) |
| 7   | Design Documentation | All libraries will have a design document, which may include application and cloud interface, state machines, and synchronization (as applicable). |
| 8   | Compiler Warning | Code will compile without generating any compiler warnings when the gcc -Wall -Wextra compiler options are used. |
