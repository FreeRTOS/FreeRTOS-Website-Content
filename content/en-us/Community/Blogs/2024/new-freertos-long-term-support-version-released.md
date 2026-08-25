---
title: "New FreeRTOS Long Term Support version released"
date: 03 Jul 2024
feature: blog
authors:
  - luciodj
---

by [Lucio Di Jasio](../author/luciodj) on 03 Jul 2024

It has been another 18 months since we introduced our last FreeRTOS Long Term Support (FreeRTOS 202210 LTS). 
With FreeRTOS LTS, developers can rely on a FreeRTOS version that provides feature stability, security 
patches and critical bug fixes for two years from the release date. We released 
the [first LTS version (FreeRTOS 202012 LTS)](https://github.com/FreeRTOS/FreeRTOS-LTS/tree/202012-LTS) 
with all libraries needed for secure AWS IoT connectivity and over-the-air updates. In addition, each 
FreeRTOS library was designed to be modular, with its own repository and minimal dependence on other 
libraries.

Today, we are excited to announce the third release of FreeRTOS Long Term Support (LTS) - FreeRTOS 202406 
LTS. This release includes the 
latest [FreeRTOS kernel v11.1](/Community/Blogs/2023/introducing-freertos-kernel-version-11-0-0-a-major-release-with-symmetric-multiprocessing-smp-support)
that supports Symmetric Multiprocessing (SMP) 
and [Memory Protection Units (MPU)](/Security/04-FreeRTOS-MPU-memory-protection-unit). 
The [FreeRTOS-Plus-TCP v4.2.1](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP)
library provides improved IPv6 support (with backward compatibility mode) with a clean separation of 
the IPv4 and IPv6 files making it easy to optimize your application footprint. Finally the OTA library 
has been refactored for maximum flexibility. Learn more about the 
new [Modular Over the Air updates](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates) 
approach and the new [File Streaming Library](https://github.com/aws/aws-iot-core-mqtt-file-streams-embedded-c/tree/690fb2bd10020da916fe54f3e8c59f1e3f925e44), 
to support your most diverse OTA needs.

All libraries included in this FreeRTOS LTS version, summarized in the table below, will receive security 
and critical bug fixes until June 2026. With an LTS release, you can continue to maintain your existing 
FreeRTOS code base and avoid any potential disruptions resulting from FreeRTOS version upgrades.

| Library                | LTS 202406 | LTS 202210 | Changes compared to previous LTS version |
| ---------------------- | ---------- | ---------- | ---------------------------------------- |
| [FreeRTOS Kernel](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/01-FreeRTOS-kernel)        | 11.1.0     | 10.5.1     | Now including Symmetric Multiprocessing (SMP) and Memory Protection Units (MPU) support. |
| [FreeRTOS-Plus-TCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP)      | 4.2.1      | 3.1.0      | Now offering improved IPv6 support and backward compatibility mode. |
| [coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT)               | 2.3.0      | 2.1.1      | No API changes. |
| [coreHTTP](/Documentation/03-Libraries/03-FreeRTOS-core/04-coreHTTP/01-coreHTTP)               | 3.1.1      | 3.0.0      | No API changes. |
| [corePKCS11](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/01-corePKCS11)             | 3.6.1      | 3.5.0      | No API changes. |
| [coreJSON](/Documentation/03-Libraries/03-FreeRTOS-core/07-coreJSON/01-coreJSON)               | 3.3.0      | 3.2.0      | No API changes. |
| [coreSNTP](/Documentation/03-Libraries/03-FreeRTOS-core/05-coreSNTP/01-coreSNTP)               | 1.3.1      | 1.2.0      | No API changes. |
| [FreeRTOS-Cellular-Interface](/Documentation/03-Libraries/03-FreeRTOS-core/09-Cellular-interface/01-Cellular-interface) | 1.4.0 | 1.3.0      | No API changes. |
| [backoffAlgorithm](/Documentation/03-Libraries/02-FreeRTOS-plus/05-backoff-algorithm)       | 1.4.1      | 1.3.0      | No API changes. |
| [AWS IoT SigV4](/Documentation/03-Libraries/04-AWS-libraries/07-AWS-Signature-Version-4/01-AWS-signature-version-4)          | 1.3.0      | 1.2.0      | No API changes. |
| [AWS IoT Device Shadow](/Documentation/03-Libraries/04-AWS-libraries/03-AWS-IoT-Device-Shadow/01-AWS-IoT-device-shadow)  | 1.4.1      | 1.3.0      | No API changes. |
| [AWS IoT Device Defender](/Documentation/03-Libraries/04-AWS-libraries/05-AWS-IoT-Device-Defender/01-AWS-IoT-device-defender) | 1.4.0     | 1.3.0      | No API changes. |
| [AWS IoT Jobs](/Documentation/03-Libraries/04-AWS-libraries/04-AWS-IoT-Jobs/01-AWS-IoT-jobs)           | 1.5.1      | 1.3.0      | No API changes. |
| [AWS IoT Fleet Provisioning](/Documentation/03-Libraries/04-AWS-libraries/06-AWS-IoT-Fleet-Provisioning/01-AWS-IoT-fleet-provisioning) | 1.2.1  | 1.1.0      | No API changes. |
| [AWS IoT MQTT File Streams](/Documentation/03-Libraries/03-FreeRTOS-core/10-coreMQTT-Streams/01-coreMQTT-Streams) | 1.1.0   | -          | New library extending and simplifying the previous OTA library. |

Similar to the previous FreeRTOS LTS release, FreeRTOS 202406 LTS includes libraries that have been 
validated for memory safety with the C Bounded Model Checker (CBMC) automated reasoning tool to help 
mitigate code security issues such as buffer overflow. In addition, all LTS libraries have undergone 
code quality checks including [MISRA-C](https://www.misra.org.uk/) compliance 
and [Coverity](https://scan.coverity.com/) static analysis to help improve code safety, portability, 
and reliability in embedded systems (see 
the [LTS Code Quality Checklist](/Documentation/03-Libraries/01-Library-overview/03-LTS-libraries/01-LTS-libraries#lts-code-quality-checklist)).

The support period for the previous LTS release will end in October 2024, providing an overlap between 
the LTS releases for easy migration of your project. See 
the [migration guide](/Documentation/03-Libraries/01-Library-overview/03-LTS-libraries/01-LTS-libraries) and 
corresponding [validation tests](https://github.com/FreeRTOS/FreeRTOS-Libraries-Integration-Tests) 
to upgrade your project to FreeRTOS 202406 LTS. If you prefer not to upgrade and want to continue receiving 
critical fixes on the previous LTS version beyond its expiry, you can consider 
the [FreeRTOS Extended Maintenance Plan](https://aws.amazon.com/freertos/features/#FreeRTOS_Extended_Maintenance_Plan).

To learn more, refer to the [FreeRTOS LTS page](/Documentation/03-Libraries/01-Library-overview/03-LTS-libraries/01-LTS-libraries) 
and [FreeRTOS LTS GitHub repository](https://github.com/FreeRTOS/FreeRTOS-LTS).

