---
title: What's New in December 2021 FreeRTOS Releases
created: 2021-12-21
feature: blog
categories:
  - Long term support
authors: 
  - stanmoy
relatedLinks:
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
---

by [Tanmoy Sen](../author/stanmoy) on 21 Dec 2021

We're excited to share these latest updates: 

* FreeRTOS now includes a [MCUBoot demo project](/Documentation/03-Libraries/05-FreeRTOS-labs/05-FreeRTOS-MCUBoot) that can be used as a reference 
for a secure bootloader for FreeRTOS-based applications. [MCUBoot](https://github.com/mcu-tools/mcuboot) 
is a configurable secure bootloader for 32-bit microcontrollers. It can operate as the first or second 
stage bootloader, with support for cryptographic verification of software images.
  
* Additionally, the FreeRTOS download now includes the AWS Signature Version 4 (SigV4) library and the 
  AWS IoT Fleet Provisioning client library for IoT applications. 

  SigV4 is the process to authenticate requests to AWS services by adding authentication information to 
  HTTP requests. The SigV4 library provides an interface to generate a signature and authorization header 
  that complies with the [SigV4 signing process](https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html), 
  and helps authenticate IoT devices that send HTTP requests to AWS services such as Amazon S3. 

  The Fleet Provisioning library allows the provisioning of IoT devices 
  using [Fleet Provisioning for AWS IoT Core](https://docs.aws.amazon.com/iot/latest/developerguide/provision-wo-cert.html), 
  a feature in which [AWS IoT](https://aws.amazon.com/iot-core/)  generates and securely delivers device 
  certificates and private keys to your devices when they connect to AWS for the first time.

  The SigV4 and Fleet Provisioning libraries are optimized for memory usage and modularity, and have 
  undergone code quality checks (e.g. [MISRA-C compliance](https://www.misra.org.uk/misra-c/), [Coverity static analysis](https://scan.coverity.com/)). 
  To learn more and get started, visit the [SigV4](/Documentation/03-Libraries/04-AWS-libraries/07-AWS-Signature-Version-4/01-AWS-signature-version-4) 
  and [Fleet Provisioning](/Documentation/03-Libraries/04-AWS-libraries/06-AWS-IoT-Fleet-Provisioning/01-AWS-IoT-fleet-provisioning) webpages or the GitHub 
  repos ([SigV4](https://github.com/aws/SigV4-for-AWS-IoT-embedded-sdk), [Fleet Provisioning](https://github.com/aws/Fleet-Provisioning-for-AWS-IoT-embedded-sdk)).

* Finally, as another way of evaluating FreeRTOS before you have hardware, we added 
  a [FreeRTOS kernel demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/QEMU/freertos-on-qemu-mps2-an385-model) that targets the Arm 
  Cortex-M3 [mps2-an385  QEMU](https://qemu.readthedocs.io/en/latest/system/arm/mps2.html) model. 
  There are pre-configured build projects for both 
  the [IAR Embedded Workbench](https://www.iar.com/products/architectures/arm/iar-embedded-workbench-for-arm/) 
  and [arm-none-eabi-gcc](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads) 
  (GNU GCC) toolchains in the FreeRTOS download.

We're looking forward to your continued feedback. Visit the [FreeRTOS forums](https://forums.freertos.org/) if you have comments or requests! 


## About the author

![](https://secure.gravatar.com/avatar/4b004f93afe063d6b8444f0fafc89d00?s=200&d=mm&r=g)   
Tanmoy Sen is a Senior Product Manager at Amazon Web Services where he focuses on helping customers 
and embedded developers connect microcontroller-based devices to the cloud.   
[View articles by this author](../author/stanmoy) 

FreeRTOS forums: Get industry-leading support from experts and collaborate with peers around the 
globe. [View Forums](https://forums.freertos.org/)
