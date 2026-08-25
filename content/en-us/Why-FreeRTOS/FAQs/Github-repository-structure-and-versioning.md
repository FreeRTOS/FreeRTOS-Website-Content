---
title: FreeRTOS FAQ - GitHub Repository Structure & Versioning
created: 2018-09-20
description: Frequently asked questions about the FreeRTOS GitHub repository structure and versioning
---

## How are FreeRTOS Git repositories structured?

There are two types of repositories, **single library** repositories and **package repositories**.
Each single library repository contains the source code for one library without any build projects or
examples. Package repositories contain multiple libraries, and may contain pre-configured projects that
demonstrate the library’s use.

While package repositories contain multiple libraries, they do not contain copies of those libraries.
Instead, package repositories reference the libraries they contain
as [git sub-modules](https://git-scm.com/book/en/v2/Git-Tools-Submodules). Using sub-modules ensures
there is a single source of truth for each individual library.

The individual library git repositories are split between two GitHub organisations. Repositories containing
FreeRTOS specific libraries (such as FreeRTOS-Plus-TCP) or generic libraries (such as coreMQTT, which is cloud
agnostic because it works with any MQTT broker) are in the [FreeRTOS GitHub organisation](https://www.github.com/FreeRTOS).
Repositories containing AWS IoT specific libraries (such as the AWS IoT over-the-air
update client) are in the [AWS GitHub organisation](https://github.com/AWS).

The following diagram demonstrates the structure.

[![](/media/2021/gsv-faq-image1.png)](/media/2021/gsv-faq-image1.png)
*GitHub Repository Structure - click to enlarge*


## How are FreeRTOS libraries versioned?

[Individual libraries](#how-are-freertos-git-repositories-structured) use *x.y.z* style version numbers, similar
to [semantic versioning](https://semver.org/). *x* is the major version number, *y* the minor version
number, and (from 2022) *z* is a patch number. Prior to 2022, *z* was a point release number, meaning
patches to the first [LTS libraries](/Community/Blogs/2021/freertos-aws-reference-integrations-now-include-freertos-202012-01-lts-libraries) required a separate patch number of the
form *"x.y.z LTS Patch 2"*.

The LTS version of a FreeRTOS library will reserve the *z* in *x.y.z* for LTS patches. For example,
if *3.1.0* is the LTS version of a FreeRTOS library, *3.1.1* will be a patch to the LTS version. This
implies that a non-LTS point release of the library from the *3.1.z* release commit will have to increment
the *minor* (i.e *y*) number rather than the *z* number. This is so that patches to the LTS version
can be extended.

The reservation of *z* applies only to LTS versions of a library. Non-LTS versions of a library will
increment z for point releases. For example, in subsequent releases from mainline, a future version
of a FreeRTOS library, say *3.3.0*, can make a point release of *3.3.1* while *3.1.0* continues to be
the LTS version.

[Library packages](#how-are-freertos-git-repositories-structured) use *yyyymm.x* style date stamp version numbers. *yyyy* is the
year, *mm* the month of the release, and *x* is a sequential patch number. The individual libraries
contained in a package are whatever the latest version of that library was on that date (or, in the
case of the LTS package, the latest patch version of the LTS libraries originally released as an LTS
version on that date).


## Which library packages are available?

There are four library packages.

1. Primary FreeRTOS distribution (from the FreeRTOS GitHub organization):

   This contains many pre-configured projects that demonstrate the FreeRTOS kernel running on different
   processors and using different compilers, as well as projects that demonstrate other FreeRTOS
   libraries (such as FreeRTOS-Plus-TCP) running in emulated environments.

1. Featured FreeRTOS IoT reference integrations (from the FreeRTOS GitHub organization):

   [Featured FreeRTOS IoT integrations](/Documentation/03-Libraries/08-Featured-integrations/01-Featured-integrations)
   are pre-configured projects that demonstrate best practices to make IoT device software more secure and
   robust. These FreeRTOS IoT integrations are designed for improved security using a combination of FreeRTOS
   software and a partner-provided board with hardware security features.

1. AWS IoT Embedded C SDK for devices (from the AWS GitHub organization):

   This contains many pre-configured projects that demonstrate the integration of FreeRTOS and AWS libraries
   running on a POSIX operating system instead of FreeRTOS.

1. LTS versions of FreeRTOS libraries (from the FreeRTOS GitHub organization):

   This is for reference and convenience only. It contains just the
   [Long Term Support (LTS) versions](/Community/Blogs/2021/freertos-aws-reference-integrations-now-include-freertos-202012-01-lts-libraries) of the FreeRTOS libraries, with no example projects.


## How do I obtain and use individual FreeRTOS libraries?

The recommended way to use individual libraries in your application is to sub-module them directly from
GitHub into your application project. Alternatively, you can copy an individual library into your application
by downloading a zip file of the library from the GitHub repository's Releases area. The following table
contains links to individual libraries. The package downloads contain examples.

| Library | Git repo (including zip download) |
| ------- | --------------------------------- |
| [FreeRTOS Kernel](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/01-FreeRTOS-kernel) (RTOS kernel)  | https://github.com/FreeRTOS/FreeRTOS-Kernel |
| [FreeRTOS-Plus-TCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP) (TCP/IP stack)  | https://github.com/FreeRTOS/FreeRTOS-Plus-TCP |
| [coreMQTT-Agent](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT) (multi-threaded MQTT client)  | https://github.com/FreeRTOS/coreMQTT-Agent (includes coreMQTT) |
| [coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT) (base MQTT client)  | https://github.com/FreeRTOS/coreMQTT |
| [coreHTTP](/Documentation/03-Libraries/03-FreeRTOS-core/04-coreHTTP/01-coreHTTP) (HTTP client)  | https://github.com/FreeRTOS/coreHTTP |
| [corePKCS11](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/01-corePKCS11) (software mock of PKCS#11)  | https://github.com/FreeRTOS/corePKCS11 |
| [coreJSON](/Documentation/03-Libraries/03-FreeRTOS-core/07-coreJSON/01-coreJSON) (JSON)  | https://github.com/FreeRTOS/coreJSON |
| [coreSNTP](/Documentation/03-Libraries/03-FreeRTOS-core/05-coreSNTP/01-coreSNTP) (SNTP)  | https://github.com/FreeRTOS/coreSNTP |
| [AWS IoT Device Shadow](/Documentation/03-Libraries/04-AWS-libraries/03-AWS-IoT-Device-Shadow/01-AWS-IoT-device-shadow) | https://github.com/aws/device-shadow-for-aws-iot-embedded-sdk |
| [AWS IoT OTA](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates) | https://github.com/aws/ota-for-aws-iot-embedded-sdk |
| [AWS IoT Jobs](/Documentation/03-Libraries/04-AWS-libraries/04-AWS-IoT-Jobs/01-AWS-IoT-jobs) | https://github.com/aws/jobs-for-aws-iot-embedded-sdk |
| [AWS IoT Device Defender](/Documentation/03-Libraries/04-AWS-libraries/05-AWS-IoT-Device-Defender/01-AWS-IoT-device-defender) | https://github.com/aws/device-defender-for-aws-iot-embedded-sdk |


## How do I obtain a FreeRTOS distribution package?

Here are instructions for each package. Note, if using git to obtain a library package then additionally
follow the repository cloning instructions in the package’s readme file to ensure you also initialize
and sync sub-module references:

1. Primary FreeRTOS distribution:

   Most people use the [download button on the FreeRTOS.org website](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)
   to obtain a zip file. The package distribution is also available from GitHub as either
   a [git repository](https://github.com/FreeRTOS/FreeRTOS)
   or [zip file](https://github.com/FreeRTOS/FreeRTOS/releases).

1. Featured FreeRTOS IoT integrations:

   Each featured integration is distributed in a separate repository under FreeRTOS github organization
   with the "iot-reference-targetplatform" name format. Check for the list of the latest projects from
   the [Featured FreeRTOS IoT Integration pages](/Documentation/03-Libraries/08-Featured-integrations/01-Featured-integrations).

1. AWS IoT Embedded C SDK for devices:

   This package is available from GitHub as either a [git repository](https://github.com/aws/aws-iot-device-sdk-embedded-C)
   or [zip file](https://github.com/aws/aws-iot-device-sdk-embedded-C/releases).

1. LTS versions of FreeRTOS libraries:

   Similar to the primary FreeRTOS distribution, most people use
   the [download button on the FreeRTOS.org website](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) to obtain a zip
   file. The distribution is also available from GitHub as either a [git repository](https://github.com/FreeRTOS/FreeRTOS-LTS)
   or [zip file](https://github.com/FreeRTOS/FreeRTOS-LTS/releases).
