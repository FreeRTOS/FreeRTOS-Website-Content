---
title: New FreeRTOS Long Term Support version released
date: 14 Oct 2022
feature: blog
categories:
  - Long term support
authors:
  - stanmoy
---
It has already been 18 months since we introduced FreeRTOS Long Term Support (LTS). With FreeRTOS LTS,
developers can rely on a FreeRTOS version that provides feature stability, and security patches and
critical bug fixes for two years from the release date. We released
the [first LTS version (FreeRTOS 202012 LTS)](https://github.com/FreeRTOS/FreeRTOS-LTS/tree/202012-LTS)
with all libraries needed for secure AWS IoT connectivity and over-the-air updates. In addition, each
FreeRTOS library was designed to be modular, with its own repository and minimal dependence on other
libraries from this first LTS version. This enabled our partners
to [integrate the FreeRTOS libraries into their toolchains](/Community/Blogs/2021/freertos-lts-libraries-are-now-part-of-our-partner-toolchains),
making it easier for customers to build, update, and validate FreeRTOS based projects.

Today, we are excited to announce the second release of FreeRTOS Long Term Support (LTS) - FreeRTOS
202210.00 LTS. This release includes new libraries such as AWS IoT Fleet Provisioning and a Cellular
LTE-M Interface for easier device provisioning and cellular connectivity. It also includes coreMQTT
and FreeRTOS-Plus-TCP libraries with improved modularity and connectivity robustness. All libraries
included in this FreeRTOS LTS version, summarized in the table below, will receive security and critical
bug fixes until October 2024. With an LTS release, you can continue to maintain your existing FreeRTOS
code base and avoid any potential disruptions resulting from FreeRTOS version upgrades.

| Library | LTS 202012 | LTS 202210 | Changes compared to previous LTS version |
| --- | --- | --- | --- |
| [FreeRTOS Kernel](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/01-FreeRTOS-kernel) | 10.4.3 | 10.5.0 | No API changes. |
| [FreeRTOS-Plus-TCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP) | 2.3.2 | 3.1.0 | No API changes. Existing project builds will be affected due to improvements to file and folder structure. |
| [coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT) | 1.1.0 | 2.1.0 | API changes. |
| [coreHTTP](/Documentation/03-Libraries/03-FreeRTOS-core/04-coreHTTP/01-coreHTTP) | 2.0.0 | 3.0.0 | No API changes. HTTP parser updates. |
| [corePKCS11](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/01-corePKCS11) | 3.0.0 | 3.5.0 | No API changes. |
| [coreJSON](/Documentation/03-Libraries/03-FreeRTOS-core/07-coreJSON/01-coreJSON) | 3.0.0 | 3.2.0 | No API changes. |
| [backoffAlgorithm](/Documentation/03-Libraries/02-FreeRTOS-plus/05-backoff-algorithm) | 1.0.0 | 1.3.0 | No API changes. |
| [AWS IoT Device Shadow](/Documentation/03-Libraries/04-AWS-libraries/03-AWS-IoT-Device-Shadow/01-AWS-IoT-device-shadow) | 1.0.2 | 1.3.0 | No API changes. |
| [AWS IoT OTA](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates) | 3.0.0 | 3.4.0 | No API changes. |
| [AWS IoT Jobs](/Documentation/03-Libraries/04-AWS-libraries/04-AWS-IoT-Jobs/01-AWS-IoT-jobs) | 1.1.0 | 1.3.0 | No API changes. |
| [AWS IoT Device Defender](/Documentation/03-Libraries/04-AWS-libraries/05-AWS-IoT-Device-Defender/01-AWS-IoT-device-defender) | 1.1.0 | 1.3.0 | No API changes. |
| [coreSNTP](/Documentation/03-Libraries/03-FreeRTOS-core/05-coreSNTP/01-coreSNTP) |  | 1.2.0 | New addition. |
| [AWS IoT SigV4](/Documentation/03-Libraries/04-AWS-libraries/07-AWS-Signature-Version-4/01-AWS-signature-version-4) |  | 1.2.0 | New addition. |
| [Cellular LTE-M Interface](/Documentation/03-Libraries/03-FreeRTOS-core/09-Cellular-interface/01-Cellular-interface) |  | 1.3.0 | New addition. |
| [AWS IoT Fleet Provisioning](/Documentation/03-Libraries/04-AWS-libraries/06-AWS-IoT-Fleet-Provisioning/01-AWS-IoT-fleet-provisioning) |  | 1.1.0 | New addition. |


Similar to the previous FreeRTOS LTS release, FreeRTOS 202210.00 LTS includes libraries that have been
validated for memory safety with the C Bounded Model
Checker ([CBMC](https://freertos.org/Community/Blogs/2020/ensuring-the-memory-safety-of-freertos-part-1))
automated reasoning tool to help mitigate code security issues such as buffer overflow. In addition,
all LTS libraries have undergone certain code quality checks including [MISRA-C](https://www.misra.org.uk/)
compliance and [Coverity](https://scan.coverity.com/) static analysis to help improve code safety, portability,
and reliability in embedded systems (see [LTS Code Quality Checklist](https://freertos.org/lts-libraries.html#checklist)).

The support period for the previous LTS release will end in March 2023, providing you a six-month overlap
between the LTS releases for easy migration of your project. See the [migration guide](/Documentation/03-Libraries/01-Library-overview/03-LTS-libraries/01-LTS-libraries)
and corresponding [validation tests](https://github.com/FreeRTOS/FreeRTOS-Libraries-Integration-Tests)
to upgrade your project to FreeRTOS 202210.00 LTS. If you prefer not to upgrade and want to continue
receiving critical fixes on the previous LTS version beyond its expiry, you can consider
the [FreeRTOS Extended Maintenance Plan](https://aws.amazon.com/freertos/features/#FreeRTOS_Extended_Maintenance_Plan).

To [qualify](https://aws.amazon.com/partners/programs/dqp/) your development board (or update a qualified
board) using the latest LTS version and list (or update) it in the [AWS Partner Device Catalog](https://devices.amazonaws.com/),
you can use the [AWS IoT Device Tester for FreeRTOS](https://aws.amazon.com/freertos/device-tester/) 202210.00 LTS.

To learn more and get started, refer to the [FreeRTOS LTS page](https://freertos.org/lts-libraries.html)
and [FreeRTOS LTS GitHub repository](https://github.com/FreeRTOS/FreeRTOS-LTS).

FreeRTOS forums: Get industry-leading support from experts and collaborate with peers around the
globe. [View Forums](https://forums.freertos.org/)
