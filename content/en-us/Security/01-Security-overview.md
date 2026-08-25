---
title: Security overview
date: Jan.2022
---

FreeRTOS follows a strict coding standard, and has undergone a number of
code quality checks including [MISRA-C](https://www.misra.org.uk/publications/) compliance
and [Coverity](https://scan.coverity.com/) static analysis to ensure code
safety, portability, and reliability in embedded systems (see the list
in the [LTS Code Quality Checklist](/Community/Blogs/2021/freertos-aws-reference-integrations-now-include-freertos-202012-01-lts-libraries#checklist)).
Non-trivial updates to the FreeRTOS libraries must pass AWS Application
Security (AppSec) and AWS Penetration Testing (pentest) reviews prior to
release.


### Memory Safety

FreeRTOS is designed for resource-constrained devices that do not
provide all the hardware mechanisms richer operating systems utilize to
protect the system from external adversaries. On such small devices,
security depends on simpler memory protection and execution privilege
level hardware, and on the operating system code itself. We work with
the [Automated Reasoning Group](https://aws.amazon.com/security/provable-security/)
at AWS to apply mathematically driven, provable security techniques to FreeRTOS.
FreeRTOS libraries have been validated for memory safety with the C
Bounded Model Checker ([CBMC](https://www.cprover.org/cbmc/)) automated
reasoning tool to mitigate code security issues such as buffer overflow.

To learn more \>\> read the blogs "Ensuring the Memory Safety of
FreeRTOS": ([Part 1](/Community/Blogs/2020/ensuring-the-memory-safety-of-freertos-part-1), [Part 2](/Community/Blogs/2020/ensuring-the-memory-safety-of-freertos-part-2).)


### Threat Model

See the [FreeRTOS Kernel Threat Model](/Security/02-Kernel-threat-model) page on this website.


### Security Certification

FreeRTOS provides foundational connectivity libraries such
as [FreeRTOS-Plus-TCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP)
and [coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT) that help developers confidently and
securely connect IoT devices to the cloud. FreeRTOS has demonstrated
safety and security through
the [Security Evaluation Standard for IoT Platforms (SESIP™)](https://trustcb.com/iot/sesip/)
Level 3 and PSA Level 1 certifications. SESIP™ derives its fundamental tenets from the
industry established [Common Criteria](https://en.wikipedia.org/wiki/Common_Criteria)
framework. [PSA Certified](https://www.psacertified.org/) offers a framework for
securing connected devices, from analysis through to security assessment
and certification.

Learn more \>\> [SESIP Level 3](/Community/Blogs/2024/freertos-is-now-sesip-level3-certified), [PSA level 1](/Community/Blogs/2021/secure-ota-updates-for-cortex-m-devices-with-freertos).
