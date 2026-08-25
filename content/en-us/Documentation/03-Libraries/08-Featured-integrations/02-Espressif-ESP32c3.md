---
title: "Featured FreeRTOS IoT Integration "
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

#### Targeting an Espressif ESP32-C3 RISC-V MCU with Digital Signature Peripheral

*This featured reference integration gives you great flexibility to adapt their functionality and utilize 
your hardware features. Or, to trade that flexibility for simplicity, also consider 
the [ExpressLink featured integration](06-STM32-Expresslink).*


## Introduction

The demo project documented on this page demonstrates how to integrate modular FreeRTOS software
with hardware enforced security to help create secure cloud connected applications. The project is pre-configured to
run on the [ESP32-C3-DevKitM-1](https://www.espressif.com/en/products/devkits) IoT development board which includes
an [ESP32-C3](https://www.espressif.com/en/products/socs/esp32-c3) microcontroller (MCU).


The ESP32-C3 is a single-core [RISC-V](https://en.wikipedia.org/wiki/RISC-V) MCU with Wi-Fi and Bluetooth
5 (LE) connectivity. It comes with
the [Digital Signature (DS)](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/api-reference/peripherals/ds.html)
peripheral and [HMAC](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/api-reference/peripherals/hmac.html)
(Hashed-based Message Authentication Code) peripherals for more secure device identity.


[Secure Boot](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/security/secure-boot-v2.html)
on the ESP32-C3 helps ensure only trusted software runs on the device,
and [flash encryption](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/security/flash-encryption.html)
protects information by converting the contents of the ESP32-C3's off-chip flash memory into a secret form
(encryption) that cannot be understood without correctly transforming it back into its original construction
(decryption).

[![](/media/2022/ESP32-C3-DevKitM-1.png) ESP32-C3-DevKitM-1](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/hw-reference/esp32c3/user-guide-devkitm-1.html)


## Demonstrated security best practices

### Preventing unauthorized software from running on the device

Ensuring that a device boots using only software that is trusted by the Original Equipment Manufacturer (OEM)
helps keep a device secure. Secure Boot protects a device from running any unauthorized (i.e. unsigned) code;
it checks that each piece of software that is being booted is trusted by the OEM. The demo uses
Espressif's [Secure Boot V2](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/security/secure-boot-v2.html).
Secure Boot on the ESP32-C3 involves a first stage bootloader (which is stored in unchangeable ROM) and a second stage
bootloader. The first stage bootloader loads the second stage bootloader, which in turn loads the application binary.
An [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem)) private key is utilized to sign the second stage bootloader
and the application binary. Signing the bootloader image with this private key ensures that the image has not been
tampered with after it was signed because, if it were, signature verification using the corresponding public key would
fail.


This RSA private key must be kept secret as malicious actors who gain access to the key can use it to provide
unauthorized binaries. The RSA private key is generated and stored outside the device on the OEM's premises (which
could be a secure build machine or a remote signing server) and is never accessed by the device. The corresponding
public key is stored in the signature blocks that are appended to the bootloader and application images. A hash of
the public key is stored in an [eFuse](https://en.wikipedia.org/wiki/EFuse).

An eFuse can be programmed only once and provides a way to store information in an unchangeable manner. The ESP32-C3 has
a number of eFuse blocks which can be used by the OEM to store system and security parameters. Each signature block
contains the signature of the corresponding image, in addition to the public key. The hash of the public key in the
eFuse is used to verify that the public key in the image's signature block is valid.

Secure Boot consists of the following steps:

1. When the first stage bootloader loads the second stage bootloader, it verifies the second stage bootloader's signature
   block and image. Image verification includes comparison of the hash of the public key embedded in the second stage
   bootloader's signature block with the public key hash stored in eFuse, as well as using the public key to verify the
   signature of the bootloader image. If verification is successful, the second stage bootloader is executed.
1. When the second stage bootloader loads an application image, it similarly verifies the application's signature
   block and image in the manner described above. If the verification is successful, the application image is
   executed. Refer to the
   ESP-IDF [programming guide on Secure Boot V2](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/security/secure-boot-v2.html)
   for more details.


### Keeping device identity and secrets secure

Secure [Transport Layer Security (TLS)](https://en.wikipedia.org/wiki/Transport_Layer_Security) communication requires
senders and receivers to be authenticated by establishing their identity. A device's unique private key and its corresponding
client certificate are used to identify and authenticate a device. The private key must be kept secret to prevent unauthorized
access and communication. Securing the identity of a device during secure TLS communication is made possible in
the ESP32-C3 via
the [Digital Signature (DS) peripheral](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/api-reference/peripherals/ds.html)
which allows use of the unique [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem)) private key employed in a TLS connection,
while keeping it secret by not making it accessible by software outside of the DS peripheral.

In order to prevent its exposure, the private key used in a TLS connection
is [AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)-encrypted and stored in flash, and
can only be read by the DS peripheral, i.e. only by hardware. The DS peripheral utilizes
the [Hash-based Message Authentication Code](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/api-reference/peripherals/hmac.html) (HMAC)
module and an [eFuse](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/efuse.html)
to generate the key required to encrypt the private key. HMAC is used for key derivation and in turn
it utilizes a selected eFuse block as its input key. This key in the eFuse is a randomly generated, 256 bit
value (generated on the OEM's host system) which is burned into a chosen eFuse block during the operation
to [configure the DS peripheral](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/api-reference/peripherals/ds.html#configure-the-ds-peripheral-for-a-tls-connection)
by the OEM. Refer to the
ESP-IDF [programming guide on the DS peripheral](https://docs.espressif.com/projects/esp-idf/en/latest/esp32c3/api-reference/peripherals/ds.html)
as well as this [DS technical reference manual](https://www.espressif.com/sites/default/files/documentation/esp32s2_technical_reference_manual_en.pdf#digsig)
for a detailed description of how the DS peripheral works.


### Secure TLS communication with mutual authentication

Communication between the device and the AWS IoT Core MQTT broker is encrypted by
using [TLS version 1.2](https://en.wikipedia.org/wiki/Transport_Layer_Security#TLS_1.2).
See [Transport security in AWS IoT](https://docs.aws.amazon.com/iot/latest/developerguide/transport-security.html) for details.
The demo uses the DS Peripheral, encrypted flash, the HMAC module, and the eFuse integrated in the ESP32-C3 SoC to store
and use the [X.509](https://en.wikipedia.org/wiki/X.509) TLS client certificate and its associated RSA private key. These
are used to establish a TLS connection with the AWS IoT Core MQTT broker using the [coreMQTT/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT) library.


### Secure over-the-air updates (OTA)

To enable remote patching of security vulnerabilities and bug fixes, the demo includes Over the Air (OTA) updates using
the [AWS IoT OTA service](https://docs.aws.amazon.com/freertos/latest/userguide/freertos-ota-dev.html) for FreeRTOS, which
includes [Code Signing for AWS IoT](https://docs.aws.amazon.com/signer/latest/developerguide/Welcome.html). A firmware
image must be digitally signed with a private key before an OTA update to ensure that it is from a reliable source and has
not been tampered with. The private key is generated as part of the OTA setup process and stored
with [AWS Certificate Manager](https://aws.amazon.com/certificate-manager/) which is accessible only to the OEM.
The corresponding public key certificate, which is used to verify the signed image, is embedded in the application binary
that runs on the device and thus cannot be altered.

The OTA client software on the ESP32-C3 uses the [AWS IoT OTA library](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates). When it receives notification of a
pending OTA update, the device downloads the new image into a secondary OTA flash partition on the ESP32-C3. The OTA client
then performs code signature verification of the entire image to confirm the
author by using the public key certificate, and to guarantee that the code was not tampered with or
corrupted since it was signed. Refer to the
ESP-IDF [programming guide on OTA](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/ota.html)
for more details.


## Libraries used by this demo

This demo uses:

* the [ESP-IDF FreeRTOS Kernel](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/freertos.html) which
  is Espressif's port of the  [FreeRTOS Kernel](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/01-FreeRTOS-kernel).
* the [coreMQTT Agent](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/01-coreMQTT-agent), including [coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT)
  with [backOffAlgorithm](https://github.com/FreeRTOS/backoffAlgorithm).
* [coreJSON](/Documentation/03-Libraries/03-FreeRTOS-core/07-coreJSON/01-coreJSON)
* [AWS IoT Over the Air (OTA)](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates)

The "core" and "FreeRTOS for AWS" libraries meet the [LTS](/Community/Blogs/2021/freertos-aws-reference-integrations-now-include-freertos-202012-01-lts-libraries) code quality standards,
including memory safety proofs.


## Getting started with the demo

Visit the [FreeRTOS/iot-reference-esp32c3](https://github.com/FreeRTOS/iot-reference-esp32c3) GitHub repository to get
started. The example source code, list of features, and instructions on how to build and run the demo
can be found in the repository.
