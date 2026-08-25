---
title: "Featured FreeRTOS IoT Integration "
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

#### Targeting an STM32U5 Arm Cortex-M33 MCU

*This featured reference integration gives you great flexibility to adapt their functionality and utilize 
your hardware features. Or, to trade that flexibility for simplicity, also consider 
the [ExpressLink featured integration](06-STM32-Expresslink).*


## Introduction

This demo shows how to integrate modular FreeRTOS software
with hardware enforced security to help create more secure cloud connected applications. The projects
are preconfigured to run on the [B-U585-IOT02A](https://www.st.com/en/evaluation-tools/b-u585i-iot02a.html)
IoT discovery kit which includes an [STM32U5](https://www.st.com/en/microcontrollers-microprocessors/stm32u5-series.html)
microcontroller (MCU).

The STM32U5 is an Arm® Cortex®-M33 MCU and
includes [Arm TrustZone technology](https://www.arm.com/technologies/trustzone-for-cortex-m) to help protect
critical security code and data with hardware-enforced isolation built into the CPU. There are two projects, one
without and one with TrustZone enabled. The MCU also provides built-in security functions, some of which are used
in this demo such as secure boot, secure storage, and
a [True Random Number Generator](https://en.wikipedia.org/wiki/Hardware_random_number_generator) (TRNG). The STM32U5
has been independently certified to [PSA Level 3](https://www.psacertified.org/getting-certified/silicon-vendor/overview/level-3/)
and [SESIP Level 3](https://www.trustcb.com/iot/sesip/).

[![B-U585-IOT02A discovery kit](/media/2022/b-u585-iot02a.jpeg) B-U585-IOT02A discovery kit](https://www.st.com/en/evaluation-tools/b-u585i-iot02a.html)


## Demonstrated security features and functions

### Reducing the potential for attack by isolating critical security firmware and data

Isolating security critical components from normal application firmware and data helps to
reduce [the potential for attack](https://developer.arm.com/documentation/100690/0201/Security-of-TrustZone-technology-for-Armv8M-against-different-attack-scenarios).
The TrustZone enabled project
utilizes [ARM Trusted Firmware M](https://www.trustedfirmware.org/projects/tf-m/) (TF-M),
leveraging [Arm TrustZone technology](https://developer.arm.com/documentation/100690/0201/Arm-TrustZone-technology)
and providing isolation between code running in the Non-Secure Processing Environment (NSPE) and code running in the
Secure Processing Environment (SPE).

In the TrustZone enabled project, the secure environment runs the following services, which are critical to the security
of the system as described in the [Featured FreeRTOS Integrations](01-Featured-integrations) page:

* Secure boot
* Private key and secrets storage
* Crypto operations such as key generation and signing

The remaining applications, FreeRTOS kernel, and other tasks such as OTA and the MQTT Agent
are run in the non-secure environment. The OTA library interacts with the secure TF-M firmware update
APIs to install new images.

The STM32CubeIDE provides build support for the TrustZone project, which generates two separate
secure and non-secure binaries which are individually signed and verified using separate keys.


### Keeping device identity and secrets secure

Secure [Transport Layer Security (TLS)](https://en.wikipedia.org/wiki/Transport_Layer_Security)
communication requires senders and receivers to be
authenticated by establishing their identity. A device's unique private key and its corresponding
client certificate are used to identify and authenticate a device. The private key must be kept
secret to prevent unauthorized access and communication.

The device [ECDSA](https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm) public/private key
pair is generated using the built-in [NIST SP 800-90B](https://en.wikipedia.org/wiki/NIST_SP_800-90B)
compliant TRNG to achieve uniqueness. The key pair is used to generate TLS client certificate. The key pair and the
certificate are stored in the Internal Trusted Storage within TF-M, with the private key is created with a flag that
prevents exporting it from the SPE. Private key generation and verification operations are performed via calls to
the [ARM PSA Cryptography APIs](https://armmbed.github.io/mbed-crypto/html/), allowing cryptographic operations to be
performed on the key stored in secure storage and is isolated from the application running in non-secure environment.


### Secure TLS communication with mutual authentication

Communication between the device and the AWS IoT Core MQTT broker is encrypted
using [TLS version 1.2](https://en.wikipedia.org/wiki/Transport_Layer_Security#TLS_1.2).
See [Transport security in AWS IoT](https://docs.aws.amazon.com/iot/latest/developerguide/transport-security.html)
for details. The [ARM PSA Cryptography APIs](https://armmbed.github.io/mbed-crypto/html/) allow TLS code to run in the
NSPE without direct access to the TLS client certificate's associated private key.


### Secure over the air updates (OTA)

The STM32U5 platform has a dual bank flash memory with a total size two megabytes. Available flash
memory is divided into two banks of size 1MB each, with one bank used for current firmware
images, and the second bank used to stage the new firmware images. Each bank of the
memory is further partitioned into secure and non-secure regions, with separate read and write
protected flash areas for secure side access.

Firmware updates for TrustZone enabled projects are implemented by integrating the FreeRTOS OTA
library with the [PSA Trusted Firmware Update API](https://developer.arm.com/documentation/ihi0093/0000)
as the PAL. Secure and non-secure executables are updated separately. Anti-rollback protection and root of trust
validation are done in the unchangeable (immutable) BL2 bootloader.

Each of the secure image and non-secure image partitions are divided into primary and
secondary slots. The new image is downloaded, validated, and staged into the secondary slot
initially. On the next reset following the new image installation, the bootloader performs a swap of
the current image running in the primary slot with the new image in the secondary slot. The swap is
performed by copying a few chunks at a time, using a scratch area as a temporary buffer. Following the
swap and a successful signature verification, the new image boots up and performs tests for
sanity. These tests include successfully connecting to AWS IoT and a version upgrade validation
for anti-rollback protection. If the tests are successful, the new image is confirmed and the old image
in the secondary slot is erased to prevent any rollback. If the test fails, the bootloader rolls back to
the old image to bring the system back to a known good state.


### Anti-Rollback protection

Anti-Rollback protection prevents downgrading the device to an older version of its
software that has been deprecated due to security concerns. Anti-rollback protection is
achieved using the MCUboot and
TF-M [Security Counter](https://tf-m-user-guide.trustedfirmware.org/design_docs/booting/tfm_secure_boot.html)
Implementation.

For each secure and non-secure region, updates must have a security counter value which is
greater than or equal to the current security counter for that region.
During a firmware update, an image with a security counter lower than the current image's
security counter will result in rejection of the update, and the bootloader will revert to the
previous image for that region. The security counter is incremented after a successful firmware
update.


### Memory safety proofs

The "core" FreeRTOS libraries comply with documented code quality criteria, including
memory safety proofs that run on each code check-in.


## Getting started with the demo

The demos connect to AWS IoT using Wi-Fi, and then use the [coreMQTT-Agent](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT) library to
publish environment and motion sensor data that is available on the development board. They
demonstrate use of the [OTA](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates) service for FreeRTOS, [Device Shadow](/Documentation/03-Libraries/04-AWS-libraries/03-AWS-IoT-Device-Shadow/01-AWS-IoT-device-shadow),
and [Device Defender](/Documentation/03-Libraries/04-AWS-libraries/05-AWS-IoT-Device-Defender/01-AWS-IoT-device-defender) AWS
IoT services. The example source code, list of features, and instructions on how to build and run the demo can
be found in the [FreeRTOS/iot-reference-stm32u5 GitHub repository](https://github.com/FreeRTOS/iot-reference-stm32u5).
