---
title: "FreeRTOS 202604 LTS now available with enhanced security and MQTT v5.0"
date: 06 May 2026
feature: blog
authors:
  - lesau
---

by [Victor Lesau](../author/lesau) on 06 May 2026

FreeRTOS 202604 LTS, a new Long Term Support release of the open-source real-time operating system for embedded devices, is now available. This release provides embedded systems developers and Internet of Things (IoT) device manufacturers with feature stability, security updates, and critical bug fixes for two years. It addresses key challenges in embedded systems, including memory safety, code quality, and protocol support.

FreeRTOS kernel v11.3.0 introduces new hardware ports, security hardening, and expanded Memory Protection Unit (MPU) support, reducing the number of MPU regions claimed by FreeRTOS and allowing developers to reserve hardware regions for application-specific memory protection. Additionally, coreMQTT v5.0.2 adds MQTT v5.0 protocol support, enabling features like topic aliases for bandwidth-constrained devices and request/response patterns for interactive IoT applications. coreSNTP v2.0.0 brings year 2038 readiness, so devices deployed today can validate TLS certificates and timestamp data correctly throughout their operational lifetime.

This release offers libraries verified for memory safety and MISRA-C compliance. The libraries improve robustness, portability, and reliability in embedded systems.

The release also provides long-term support for all included libraries, summarized in the table below, with security and critical bug fixes until April 30, 2028. With an LTS release, you can maintain your existing FreeRTOS code base without changes from version upgrades.

| Library | 202604 LTS | 202406 LTS | Changes compared to previous LTS version |
| --- | --- | --- | --- |
| FreeRTOS Kernel | 11.3.0 | 11.1.0 | New hardware ports, security hardening, and expanded MPU support for application-specific memory protection |
| FreeRTOS-Plus-TCP | 4.4.1 | 4.2.5 | No API changes |
| coreMQTT | 5.0.2 | 2.3.1 | Support for MQTT v5.0 |
| coreHTTP | 3.1.3 | 3.1.1 | No API changes |
| corePKCS11 | 3.6.4 | 3.6.3 | No API changes |
| coreJSON | 3.3.1 | 3.3.0 | No API changes |
| coreSNTP | 2.0.0 | 1.3.1 | Adds year 2038 readiness, extending time support to 2106 |
| FreeRTOS-Cellular-Interface | 1.4.2 | 1.4.0 | No API changes |
| backoffAlgorithm | 1.4.2 | 1.4.1 | No API changes |
| AWS IoT SigV4 | 1.3.1 | 1.3.0 | No API changes |
| AWS IoT Device Shadow | 1.4.2 | 1.4.1 | No API changes |
| AWS IoT Device Defender | 1.4.1 | 1.4.0 | No API changes |
| AWS IoT Jobs | 2.0.1 | 1.5.1 | Support for custom metadata in job status updates, enabling richer OTA progress reporting |
| AWS IoT Fleet Provisioning | 1.2.2 | 1.2.1 | No API changes |
| AWS IoT MQTT File Streams | 1.2.0 | 1.1.0 | No API changes |

Migration guides for [coreMQTT](https://github.com/FreeRTOS/coreMQTT/blob/main/MQTTv5Guide.md) and [coreSNTP](https://github.com/FreeRTOS/coreSNTP/blob/main/MigrationGuide.md) provide detailed guidance for updating to FreeRTOS 202604 LTS. For projects requiring critical fixes on the previous LTS version beyond its expiry, the [FreeRTOS Extended Maintenance Plan](https://aws.amazon.com/freertos/features/#freertos-extended-maintenance-plan--oxjb3r) is available. To learn more, visit the [FreeRTOS LTS page](https://freertos.org/Documentation/03-Libraries/01-Library-overview/03-LTS-libraries/01-LTS-libraries) and [FreeRTOS LTS GitHub repository](https://github.com/FreeRTOS/FreeRTOS-LTS).
