---
title: "FreeRTOS LTS Libraries"
created: 2018-09-20
categories:
  - kernel
description: Basic information on the FreeRTOS Long Term Support (LTS) libraries
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


**NOTE**: FreeRTOS 202604.00 LTS libraries are now available in the [FreeRTOS-LTS](https://github.com/FreeRTOS/FreeRTOS-LTS/tree/202604.00-LTS) GitHub repository.

### Introduction

FreeRTOS long term support (LTS) releases receive security and critical bug fixes
(should any be necessary) for at least two years following their release.
That ongoing maintenance enables you to incorporate bug fixes throughout a development and
deployment cycle without the costly disruption of updating to a new major version of FreeRTOS libraries.
Long term support is provided courtesy of AWS for the benefit of the entire FreeRTOS community.

AWS also offers the FreeRTOS Extended Maintenance Plan (EMP) that provides you with security patches and critical
bug fixes on your chosen FreeRTOS LTS version for up to an additional 10 years. Visit the
[EMP page on the AWS site](https://aws.amazon.com/freertos/features/#FreeRTOS_Extended_Maintenance_Plan) for details.

FreeRTOS LTS libraries are also available from partner toolchains.
See the [blog post](/Community/Blogs/2021/freertos-lts-libraries-are-now-part-of-our-partner-toolchains).


**Note:**You can find example projects for the libraries included in this bundle in the [primary FreeRTOS download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS). Refer to the [FAQ](/Why-FreeRTOS/FAQs/Long-term-support) for details.

[Download LTS 202604 Libraries](https://github.com/FreeRTOS/FreeRTOS-LTS/releases/download/202604.00-LTS/FreeRTOSv202604.00-LTS.zip)

Download the previous version:
[LTS 202406 Libraries](https://github.com/FreeRTOS/FreeRTOS-LTS/releases/download/202406.05-LTS/FreeRTOSv202406.05-LTS.zip)


### Upgrading to version 202604.xx of FreeRTOS LTS from the previous version

FreeRTOS 202604 LTS libraries are backward compatible with 202406.xx LTS, except coreMQTT, coreSNTP, and AWS IoT Jobs libraries which have had major version updates. For coreMQTT, refer to the [coreMQTT migration guide](https://github.com/FreeRTOS/coreMQTT/blob/v5.0.2/MigrationGuide.md) for upgrading from v2.x to v5.x. For AWS IoT Jobs, refer to the [Jobs migration guide](https://github.com/aws/Jobs-for-AWS-IoT-embedded-sdk/blob/v2.0.1/MigrationGuide.md) for upgrading from v1.x to v2.x. For coreSNTP, refer to the [coreSNTP migration guide](https://github.com/FreeRTOS/coreSNTP/blob/v2.0.0/MigrationGuide.md) for upgrading from v1.x to v2.x.


### LTS Status

The following table lists the libraries that are part of FreeRTOS 202604 LTS. All meet the LTS modularity
and [Code Quality Checklist](#lts-code-quality-checklist) requirements other than the kernel and TCP stack, both of which
still comply with their original quality requirements.


**Last Updated: April 29, 2026**

| Library | Version | Maintained at least until |
| --- | --- | --- |
| [FreeRTOS Kernel](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/01-FreeRTOS-kernel) | 11.3.0 | April 30, 2028 |
| [FreeRTOS-Plus-TCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP) | 4.4.1 | April 30, 2028 |
| [coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT) | 5.0.2 | April 30, 2028 |
| [coreHTTP](/Documentation/03-Libraries/03-FreeRTOS-core/04-coreHTTP/01-coreHTTP) | 3.1.3 | April 30, 2028 |
| [corePKCS11](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/01-corePKCS11) | 3.6.4 | April 30, 2028 |
| [coreJSON](/Documentation/03-Libraries/03-FreeRTOS-core/07-coreJSON/01-coreJSON) | 3.3.1 | April 30, 2028 |
| [coreSNTP](/Documentation/03-Libraries/03-FreeRTOS-core/05-coreSNTP/01-coreSNTP) | 2.0.0 | April 30, 2028 |
| [FreeRTOS-Cellular-Interface](/Documentation/03-Libraries/03-FreeRTOS-core/09-Cellular-interface/01-Cellular-interface) | 1.4.2 | April 30, 2028 |
| [backoffAlgorithm](/Documentation/03-Libraries/02-FreeRTOS-plus/05-backoff-algorithm) | 1.4.2 | April 30, 2028 |
| [AWS IoT SigV4](/Documentation/03-Libraries/04-AWS-libraries/07-AWS-Signature-Version-4/01-AWS-signature-version-4) | 1.3.1 | April 30, 2028 |
| [AWS IoT Device Shadow](/Documentation/03-Libraries/04-AWS-libraries/03-AWS-IoT-Device-Shadow/01-AWS-IoT-device-shadow) | 1.4.2 | April 30, 2028 |
| [AWS IoT Device Defender](/Documentation/03-Libraries/04-AWS-libraries/05-AWS-IoT-Device-Defender/01-AWS-IoT-device-defender) | 1.4.1 | April 30, 2028 |
| [AWS IoT Jobs](/Documentation/03-Libraries/04-AWS-libraries/04-AWS-IoT-Jobs/01-AWS-IoT-jobs) | 2.0.1 | April 30, 2028 |
| [AWS IoT Fleet Provisioning](/Documentation/03-Libraries/04-AWS-libraries/06-AWS-IoT-Fleet-Provisioning/01-AWS-IoT-fleet-provisioning) | 1.2.2 | April 30, 2028 |
| [AWS IoT MQTT File Streams](/Documentation/03-Libraries/03-FreeRTOS-core/10-coreMQTT-Streams/01-coreMQTT-Streams) | 1.2.0 | April 30, 2028 |


For information on library versions for the previous LTS version, see
the [FreeRTOS 202406.xx-LTS repository](https://github.com/FreeRTOS/FreeRTOS-LTS/tree/202406-LTS) on GitHub.


### FreeRTOS LTS Patches

For the latest information, subscribe to GitHub Notifications by watching
the [FreeRTOS LTS repository](https://github.com/FreeRTOS/FreeRTOS-LTS).


| Patch Version | Updates | Post |
| --- | --- | --- |
| 202604.00 LTS | Initial release of FreeRTOS 202604 LTS. | [Changelog](https://github.com/FreeRTOS/FreeRTOS-LTS/blob/202604.00-LTS/CHANGELOG.md) |
| 202406.05 LTS | Include fixes for FreeRTOS-Plus-TCP (V4.2.6).| [Changelog](https://github.com/FreeRTOS/FreeRTOS-LTS/blob/202406.05-LTS/CHANGELOG.md) |
| 202406.04 LTS | Include fixes for FreeRTOS-Plus-TCP (V4.2.5).| [Changelog](https://github.com/FreeRTOS/FreeRTOS-LTS/blob/202406.04-LTS/CHANGELOG.md) |
| 202406.03 LTS | Include fixes for FreeRTOS-Plus-TCP (V4.2.4).| [Changelog](https://github.com/FreeRTOS/FreeRTOS-LTS/blob/202406.03-LTS/CHANGELOG.md) |
| 202406.02 LTS | Include fixes for corePKCS11 (v3.6.3) and FreeRTOS-Plus-TCP (V4.2.3).| [Changelog](https://github.com/FreeRTOS/FreeRTOS-LTS/blob/202406.02-LTS/CHANGELOG.md) |
| 202406.01 LTS | Include fixes for coreMQTT (v2.3.1) and FreeRTOS-Plus-TCP (V4.2.2).| [Changelog](https://github.com/FreeRTOS/FreeRTOS-LTS/blob/202406.01-LTS/CHANGELOG.md) |
| 202210.01 LTS | Includes critical fixes for the coreMQTT (V2.1.1) and FreeRTOS kernel (V10.5.1). | [Changelog](https://github.com/FreeRTOS/FreeRTOS-LTS/blob/202210.01-LTS/CHANGELOG.md) |
| 202012.05 LTS | Includes critical fixes for the FreeRTOS kernel (10.4.3-LTS-Patch-3). | [Release notes](https://github.com/FreeRTOS/FreeRTOS-Kernel/releases/tag/V10.4.3-LTS-Patch-3) |
| 202012.05 LTS | Includes security patches for the FreeRTOS kernel (10.4.3-LTS-Patch-3). | [Security Updates](/Security/03-Vulnerabilities) |
| 202012.04 LTS | Includes critical bug fixes for the FreeRTOS-Plus-TCP library (2.3.2-LTS-Patch-2). | [Release notes](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP/releases/tag/V2.3.2-LTS-Patch-2) |
| 202012.03 LTS | Includes security patches for the FreeRTOS kernel (10.4.3-LTS-Patch-2). | [Security Updates](/Security/03-Vulnerabilities) |
| 202012.02 LTS | Includes security patches for the FreeRTOS kernel (10.4.3-LTS-Patch-1) and TCP libraries (V2.3.2-LTS-Patch-1). | [Security Updates](/Security/03-Vulnerabilities) |
| 202012.01 LTS | Added AWS IoT OTA, AWS Device Defender, and AWS IoT Jobs library to 202012.00 LTS | [Blog Post](/Community/Blogs/2021/freertos-long-term-support-now-includes-aws-iot-over-the-air-update-aws-iot-device-defender-and-aws-iot-jobs-libraries) |


### LTS Code Quality Checklist

The table below documents the LTS release code quality requirements.


| # | Category | Checks |
| --- | --- | --- |
| 1 | Coding Standard | Functions shall comply with the [MISRA 2012 coding standard](/Documentation/02-Kernel/06-Coding-guidelines/02-FreeRTOS-Coding-Standard-and-Style-Guide/#coding-standard--misra-compliance). |
| 2 | Static Checking | Functions shall pass [Coverity](https://scan.coverity.com/) static checking. |
| 3 | APSEC review and pentest | Libraries must pass AWS security review. |
| 4 | Code Testing, including memory safety proofs | The code shall have extensive unit and function tests, with Gcov reports detailing test coverage,<br/> as well as CBMC memory safety proofs. |
| 5 | Requirements Documentation | Libraries shall have documented requirements, which may include resource, dependency, and porting requirements (as applicable). |
| 6 | Design Documentation | Libraries shall have design documentation, including application and cloud interface, state machines, and synchronization (as applicable). |
| 7 | Compiler Warning | The code shall compile with GCC using the -Wall and -Wextra command line options without generating compiler warnings. |