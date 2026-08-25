---
title: "Featured FreeRTOS IoT Integration "
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

#### Targeting an Arm Corstone-3xx platform based on Arm Cortex-M MCU

*This featured reference integration gives you great flexibility to adapt their functionality and utilize 
your hardware features. Or, to trade that flexibility for simplicity, also consider 
the [ExpressLink featured integration](06-STM32-Expresslink).*


## Introduction

This reference integration demonstrates how to develop cloud connected applications and update them
securely by integrating the modular FreeRTOS [kernel](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/01-FreeRTOS-kernel) and
[libraries](/Documentation/03-Libraries/01-Library-overview/Library-categories) and utilizing hardware-enforced security based
on [Arm TrustZone (Armv8-M)](https://www.arm.com/architecture/learn-the-architecture/m-profile).


To utilize the hardware-enforced security, this integration uses PSA Certified reference implementation
[Trusted Firmware-M](https://www.trustedfirmware.org/projects/tf-m/). Trusted Firmware-M provides various Secure services
such as Secure boot, Crypto, Secure Storage, Attestation and Update services meeting
[PSA Certified requirements](https://www.psacertified.org/blog/psa-certified-10-security-goals-explained/). This integration
is based on the [Corstone-300](https://developer.arm.com/Processors/Corstone-300) platform.


Developers and partners can use this integration as a starting point to build the FreeRTOS kernel and
libraries-based software stack on top of Arm Cortex-M based platforms. All the components are put together
in a modular manner to make porting this integration across platforms easy.

[![](/media/2022/example-integration-corstone3xx.png) Corstone-300](https://developer.arm.com/Processors/Corstone-300)


## Demonstrated security features and function

Trusted Firmware-M (TF-M) leverages the Arm TrustZone technology to provide a Non-Secure Processing Environment
(NSPE) and a Secure Processing Environment (SPE) which are isolated from each other. The FreeRTOS kernel,
middleware and application run in the NSPE while TF-M runs in the SPE. TF-M provides the PSA RoT secure services
through the PSA Certified Functional APIs to the NSPE. The isolation ensures TF-M code, assets (keys, certificates,
and so on) and data are protected from any vulnerabilities present in the NSPE.


The demo showcases how a Secure TLS connection between the Corstone-300 and AWS IoT Core can be established making
use of the TF-M's PSA Crypto and Secure Storage functions. In addition, it demonstrates a secure OTA update of the
platform using TF-M's Firmware Update Service.


### Secure TLS Connection

The Corstone-300 communicates with AWS IoT Core over a secure TLS connection. Mbed TLS running on the NSPE is used
to establish the TLS connection. Mbed TLS makes use of the PSA Crypto APIs provided by TF-M to perform Crypto
operations and [PKCS#11](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/01-corePKCS11) APIs
to perform TLS client authentication and import the TLS client certificate and private key into the device.


PKCS#11 has been integrated with TF-M using a thin shim. In the integration, the PKCS#11 APIs invoke the appropriate
PSA Secure Storage API or Cryptographic API via the shim. This ensures the keys and certificates are protected and
the cryptographic operations are performed securely within the SPE of TF-M and are isolated from the kernel,
libraries, and applications in the Non-secure Processing Environment. Keys and certificates are securely stored.
This is enabled by TF-M's Internal Trusted Storage (ITS) and Protected Storage (PS) services. Signing during TLS
client authentication is performed by TF-M's Crypto service.


### Secure OTA Updates


The FreeRTOS OTA Agent provides an OTA PAL layer for platforms to integrate and enable OTA updates. The demo integrates
an OTA PAL implementation that makes use of the PSA Certified Firmware Update API that is implemented in TF-M. This
allows the Corstone-300 to receive a new image from AWS IoT Core, authenticate it using TF-M, before deploying it
as the active image. The secure (TF-M) and the non-secure (FreeRTOS kernel and application) images can be updated
separately.


Every time the device boots, MCUBoot (the bootloader) verifies that the image signature is valid before it boots
the image. Since the secure (TF-M) and the non-secure (FreeRTOS kernel and application) images are signed separately,
MCUBoot verifies that both image signatures are valid before it boots. If either of the verification fails, then
MCUBoot stops the booting process.


### Memory safety proofs

The "core" FreeRTOS libraries comply with documented code quality criteria, including memory safety proofs that run
on each code check-in.


## Getting started with the demo

There are two examples: "blinky" and "aws-iot-example". The "blinky" example demonstrates FreeRTOS
kernel and TF-M integration, whereas the "aws-iot-example" demonstrates connectivity to AWS IoT core
using the [coreMQTT-agent](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/01-coreMQTT-agent)
library and secure OTA using the [OTA agent](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates).
The source code and the getting started guide can be found at
[FreeRTOS/iot-reference-arm-corstone3xx](https://github.com/FreeRTOS/iot-reference-arm-corstone3xx) on GitHub.
