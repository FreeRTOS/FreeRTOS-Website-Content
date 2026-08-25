---
title: Security for Arm Cortex-M devices with FreeRTOS
created: 2020-07-17
feature: blog
categories:
  - Long term support
authors:
  - arm-author
relatedLinks:
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
---

by [Shebu Varghese Kuriakose](../author/arm-author) on 17 Jul 2020

Securing microcontrollers is a challenge, hampered in part by lack of hardware enforced security domains.
Creating two security domains typically requires two microprocessors each with a separate Memory Protection
Unit (MPU). Arm TrustZone, introduced with the Armv8-M architecture, enables two security processing
environments on a single Cortex-M processor
(see [Using FreeRTOS on Armv8-M Microcontrollers](/Community/Blogs/2020/using-freertos-on-armv8-m-microcontrollers).
Once you have separate secure and non-secure processing environments, what do you do with them?


## Introducing Trusted Firmware-M

[Trusted Firmware-M](https://www.trustedfirmware.org/) (TF-M) implements a Secure Processing Environment (SPE)
for Armv8-M architecture (e.g. the Cortex-M55, Cortex-M33 and Cortex-M23 processors) and dual-core Cortex-M
devices. It is the PSA reference implementation aligning
with [PSA Certified guidelines,](https://www.psacertified.org/about/developing-psa-certified/) enabling
chips, Real Time Operating Systems, and devices to become PSA Certified. As an Open Source project distributed
under BSD-3 Clause license hosted in Trusted Firmware Open Governance community project, it is supported
on several Cortex-M based Microcontrollers such as NXP LPC55S69, ST STM32L5, and Cypress PSoC 64. FreeRTOS
has achieved [PSA Functional API Certification](https://www.psacertified.org/products/freertos/) using TF-M.

TF-M provides a set of secure services – Crypto, Attestation and Secure Storage. It also provides secure
boot through a 2nd stage bootloader based on mcuboot for authenticating runtime images and updates of
the platform. Applications and Libraries in the Non-secure Processing Environment (NSPE) can utilize
these secure services with a standardized set of PSA Functional APIs. On Armv8-M devices, TF-M uses
Arm TrustZone technology to isolate the NSPE and the Secure Processing Environment (SPE) code and data.
Applications running on Cortex-M devices can leverage TF-M services to ensure secure connection with
edge gateways and IoT cloud services. It also protects the critical security assets such as sensitive
data, keys and certificates on the platform.

![](/media/2020/07/Figure-1.png)
*Figure 1: Armv8-M based Cortex-M processor with TF-M*

TF-M has completed an initial integration with FreeRTOS. This enables applications running FreeRTOS
on Cortex-M devices to utilize secure services provided by TF-M via the PSA Functional APIs. The integration
has been verified on the
Arm [Musca-B1](https://developer.arm.com/tools-and-software/development-boards/iot-test-chips-and-boards/musca-b-test-chip-board)
reference platform and is expected to be available on several Cortex-M platforms with TF-M.


## Integration with FreeRTOS Kernel

As shown in the figure below, FreeRTOS kernel runs in NSPE and TF-M runs in SPE. FreeRTOS tasks can utilize
any TF-M secure services (e.g. Crypto, Secure Storage and Attestation) via the PSA Functional APIs.
A Non-Secure Dispatcher forwards the PSA Functional API calls from the tasks to TF-M. The integration
with an example can be found on [Github](https://github.com/Linaro/amazon-freertos/pull/1/commits).
The NSPE can communicate with TF-M using an IPC or function call mechanism which provide different levels
of security and isolation. FreeRTOS can use any one of these mechanisms for communication with TF-M
depending on the application needs.

![](/media/2020/Figure-2.png)
*Figure 2: Armv8-M based Cortex-M processor with FreeRTOS and TF-M*


## Integration with PKCS#11

FreeRTOS’s reference IoT integrations provide various libraries and APIs such as Secure Socket, TLS,
OTA agent and PKCS#11 (Public Key Cryptography Standard #11) to improve the security of applications.

[PKCS#11](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/01-corePKCS11) APIs are used in FreeRTOS to perform TLS client authentication and import
TLS client certificate and private key into the device. PKCS#11 has been integrated with TF-M using a
thin shim and verified on the Arm Musca-B1 reference platform. In the integration, the PKCS#11 APIs
invoke the appropriate PSA Functional Secure Storage API or Cryptographic API via the shim. This ensures
the keys and certificates are protected and the cryptographic operations are performed securely within
the SPE of TF-M and is isolated from the kernel, libraries and applications in the Non-secure Processing
Environment. Keys and certificates are securely stored on chip storage and external flash respectively.
This is enabled by TF-M’s Internal Trusted Storage (ITS) and Protected Storage (PS) services. Signing
during TLS client authentication is performed by TF-M’s Crypto service. The example integration on Arm
Musca-B1 reference platform as shown in the below picture can be
found [here](https://github.com/Linaro/amazon-freertos/pull/2/commits) along with
a [Readme](https://github.com/Linaro/amazon-freertos/pull/2/files#diff-2f722d7178d1065f926c803457657e2b).
The PSA Functional API Shim is available in FreeRTOS project under
the [psa folder](https://github.com/aws/amazon-freertos/tree/master/libraries/abstractions/pkcs11)
allowing TF-M enabled platforms to make use of this shim layer.

![](/media/2020/Figure-3.png)
*Figure 3: Armv8-M based Cortex-M processor with FreeRTOS, PSA Functional API shim and TF-M*

Table 1 shows the mapping of the PKCS #11 APIs that is used in FreeRTOS and the PSA Functional API that
gets invoked during provisioning of key and certificate and TLS client authentication.

| PKCS11 API | PSA Functional APIs |
| --- | --- |
| C\_CreateObject | psa\_ps\_setpsa\_import\_key psa\_close\_key  |
| C\_GenerateKeyPair  | psa\_generate\_key psa\_export\_public\_key psa\_import\_key  |
| C\_DestroyObject  | psa\_ps\_remove psa\_destroy\_key  |
| C\_VerifyInitC\_Verify  | psa\_verify\_hash  |
| C\_SignInitC\_Sign | psa\_sign\_hash |
| C\_FindObjectsInitC\_FindObjects  | psa\_open\_key  |
| C\_GetAttributeValue  | psa\_ps\_getpsa\_export\_key |
| C\_DigestInitC\_DigestUpdate C\_DigestFinal  | psa\_hash\_setup,psa\_hash\_update,psa\_hash\_finish  |
| C\_GenerateRandom  | psa\_generate\_random  |

*Table 1: PKCS#11 and PSA Functional APIs Mapping*


## What’s Next

The next step is to expand the integration of FreeRTOS security components with TF-M beyond the PKCS#11
interfaces. FreeRTOS OTA agent allows applications to receive, validate and deploy new images on the
platforms. Integrating OTA agent with TF-M’s secure boot allows FreeRTOS to authenticate new images
within the SPE leveraging all the security capabilities provided by the platform mitigating against
any image update vulnerabilities. As the Mbed TLS project starts using the PSA Functional Crypto API
for cryptographic operations, all TLS operations initiated by FreeRTOS will invoke TF-M Crypto Service
via the PSA Functional Crypto APIs. The current integration and these enhancements will be available
on a variety of Cortex-M devices enabled with TF-M simplifying security for developers of FreeRTOS based
applications.

Visit [Trusted Firmware](https://www.trustedfirmware.org/) project to learn more about TF-M
and [Github](https://github.com/Linaro/amazon-freertos/pulls) to access the FreeRTOS integration
on [Musca-B1](https://developer.arm.com/tools-and-software/development-boards/iot-test-chips-and-boards/musca-b-test-chip-board).
The PSA Functional API shim in [psa folder](https://github.com/aws/amazon-freertos/tree/master/libraries/abstractions/pkcs11)
can be leveraged by FreeRTOS and TF-M enabled platforms

![](/media/2020/Figure-4.png)
*Figure 4: Armv8-M based Cortex-M processor with complete FreeRTOS and TF-M integration*


## About the author

![](https://secure.gravatar.com/avatar/db732371ff8ea1e00013619782acc940?s=200&d=mm&r=g)
Shebu Varghese Kuriakose is Director, Software Technology Management with Arm’s Open Source Software
Group and Chairman of the Trusted Firmware Project Board. Shebu drives the Trusted Firmware-M development
roadmap and collaboration with Silicon vendors, RTOS and Tools ecosystem.
[View articles by this author](../author/arm-author)

FreeRTOS forums: Get industry-leading support from experts and collaborate with peers around the
globe. [View Forums](https://forums.freertos.org/)
