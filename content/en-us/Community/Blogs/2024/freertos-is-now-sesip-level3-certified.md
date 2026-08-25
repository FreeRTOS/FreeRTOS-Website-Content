---
title: "FreeRTOS is now SESIP Level 3 certified"
date: 09 Oct 2024
feature: blog
authors:
  - kanherea
---

by [Aniruddha Kanhere](../author/kanherea) on 09 Oct 2024

## What is SESIP?

See our previous blog post [Why SESIP™ Certification for FreeRTOS Matters](/Community/Blogs/2021/why-sesip-certification-for-freertos-matters) 
to learn more about SESIP certification and why it matters for embedded systems.

## SESIP level 3 certification

Security is the first priority for FreeRTOS and in support of this commitment FreeRTOS has achieved 
[certification](https://trustcb.com/iot/sesip/sesip-certificates) for the 
[Security Evaluation Standard for IoT Platforms](https://globalplatform.org/sesip) (SESIP™) Assurance Level 3. 
Primarily used in embedded system processors, [FreeRTOS](https://www.freertos.org/) remains one of the top 
choices among developers, supported by a community that has been collaborating for over 21 years. While its 
core is a [real-time operating system (RTOS) kernel](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/01-FreeRTOS-kernel), 
FreeRTOS also offers essential libraries like [FreeRTOS-Plus-TCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP), 
a secure and continually evolving TCP/IP library. Additionally, it includes IoT application protocol libraries 
such as [coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT), helping to enable 
developers to securely connect to the cloud. As an open-source project, FreeRTOS thrives on community 
contributions, ensuring it remains a top choice for embedded systems development.

The level 3 certificate can be found [here](https://www.trustcb.com/iot/sesip/sesip-certificates/) by 
searching for “FreeRTOS”.

## What is the difference between SESIP level 2 and SESIP level 3?

SESIP™ certification has five assurance levels ranging from one to five. As the assurance levels increase so do 
the complexity and rigidity of the tests. [GlobalPlatform™](https://globalplatform.org/sesip/) governs the 
[five SESIP™ Assurance Levels](https://trustcb.com/iot/sesip/), while test partners execute tests. TrustCB™ 
provides certification for all five levels of SESIP™ certification.

SESIP3 is a substantial level of assurance for (parts of) IoT platforms. It provides significantly more 
assurance than SESIP2 by requiring comprehensive source code analysis by an evaluator as input to the 
vulnerability analysis. SESIP3 is clear-box testing where the testers perform time-limited source code 
analysis combined with a time-limited penetration testing as opposed to SESIP2 which is a closed testing 
performed without the help of the developer.

Scope and Depth of Evaluation:

* SESIP2 involves a more limited security evaluation focused on the Target Of Evaluation (TOE) security functionality.
* SESIP3 requires a more comprehensive and in-depth security analysis, including the TOE's full functional specification, implementation details, and guidance documentation.

Attack Resistance:

* SESIP2 evaluates resistance against Basic attack potential.
* SESIP3 evaluates resistance against Enhanced-Basic attack potential, which is a higher level of sophistication.

Development Environment Controls:

* SESIP2 has minimal requirements for the TOE's development environment.
* SESIP3 mandates more robust controls and evidence for the secure development environment.

Configuration Management:

* SESIP2 has basic requirements for configuration management.
* SESIP3 requires more extensive configuration management practices, including automation, to ensure the integrity of the TOE.

In summary, SESIP3 provides a more rigorous, comprehensive, and higher level of security assurance compared 
to SESIP2, making it suitable for IoT and embedded products with higher security requirements.

Components certified with SESIP level 3 certificate:

| Component Name | Version | GIT hash identifier |
| -------------- | ------- | ------------------- |
| FreeRTOS Kernel | [V10.6.1](https://github.com/FreeRTOS/FreeRTOS-Kernel/tree/V10.6.1) | 0264280230aa6a828247b5f05bf57e33f1994581 |
| FreeRTOS+TCP | [V3.1.0](https://github.com/FreeRTOS/FreeRTOS-Plus-TCP/tree/V3.1.0) | 0bf460c935ca59cf0423ef0ac3505f13961c2e9e |
| corePKCS #11 | [V3.5.0](https://github.com/FreeRTOS/corePKCS11/tree/v3.5.0) | 781f5774948fa8e6427be544b1bf1ad512ae9e90 |
| OTA Updates | [V3.4.0](https://github.com/aws/ota-for-aws-iot-embedded-sdk/tree/v3.4.0) | f9760892ba152f2c9104d08192ea5ffbbf9fa8ea |
| Mbed TLS | [V2.28.7](https://github.com/Mbed-TLS/mbedtls/tree/mbedtls-2.28.7) | 555f84735aecdbd76a566cf087ec8425dfb0c8ab |

All the above libraries, along with other helper libraries such as coreMQTT and vendor drivers are added 
as a submodule to the [FreeRTOS/iot-reference-nxp-rt1060](https://github.com/FreeRTOS/iot-reference-nxp-rt1060/tree/v202403.00-SESIP) 
repository which was used for the SESIP Assessment. 

## Scope of SESIP certification

Ideally, everything bundled with FreeRTOS would be certified by SESIP. It can be especially important for IoT 
devices when applications become more complex due to the software and hardware stacks used to communicate across 
networks securely.

But, as we mentioned in the previous blog post, when the application undergoes SESIP™ certification, it is desirable that the developer's TOE focus is the code or hardware directly under the developer's control. When the developer chooses hardware and software that is not SESIP™ certified, then the test authority, for example Riscure, will need to test the entire hardware and software stack. Therefore, we chose the below components to get certified for SESIP level 3 as it allows the application developers to choose other libraries and/or other hardware stack without breaching the SESIP certification guarantee.

[![Figure 1. Components covered in the SESIP level 3 certification](/media/2024/SESIP_level3_scope.png)](/media/2024/SESIP_level3_scope.png)
*Figure 1. Components covered in the SESIP level 3 certification*


## Environmental assumptions

Some environmental assumptions had to be made in order to narrow test parameters when testing FreeRTOS for SESIP™ certification.
It is assumed that:

* The platform shall only be deployed in environments where protection from physical attacks is not required. The TOE must have a Memory Protection Unit (MPU) as part of the underlying hardware.
* Next, it is assumed that the application developer shall follow development best practices to avoid memory corruption attacks. In practice, development teams need to be trusted and must implement development team rules that constrain FreeRTOS source code modification. Only authorized and trustworthy personnel shall have access to the TOE development environment.
* Thirdly, when connecting to AWS IoT and other secure services, it is assumed that the hardware where the platform is deployed shall provide a cryptographically secure random number generator.
* The last assumption is that the Firmware Over-the-Air (FOTA) function uses [AWS IoT OTA Update Manager](https://docs.aws.amazon.com/freertos/latest/userguide/ota-manager.html). FOTA capabilities rely on centralized systems to deliver commands and firmware payloads. The centralized system is not under test. The device connected to the centralized system is under test. 

With these assumptions in mind, let's take a look at the top five areas under test.

### Verification of Platform Identity

The source code repository for all the components covered for SESIP3 tests contains a manifest.yml file. This file provides the unique identification of the TOE including the name, description, and specific version of the item. It also includes the same information for any source code dependencies. The version field found in the manifest.yml file is the git tag identifier which also corresponds to the git hash of the component.
The third-party Mbed-TLS library contains a ChangeLog file which uniquely identifies the version of the source code in the repository. The version number also corresponds to the git tag and git hash of Mbed-TLS.

### Verification of Platform Instance Identity

When a device connects to AWS IoT Core, the primary identifier is called the ThingName. This ThingName must be unique across all the devices in the system. AWS IoT Core also allows devices to have additional attributes, such as a serial number or software version. Device manufacturers can choose to either hardcode the ThingName during the manufacturing process, or include software that sets the ThingName at the time the device is provisioned. Regardless of the method, the ThingName is stored by the user in a secure location, like flash memory or a secure element, to ensure it cannot be changed. This unique ThingName is then used by the device to interact with the AWS IoT Core services.

### Secure Update of Platform

The OTA (Over-The-Air) update process starts with the device's OTA Agent checking for new updates by sending a message to the configured server. When a new update is available, the server sends the update metadata to the OTA Agent on the device. Depending on the configuration, the agent will either store the new firmware image in a file or write it directly to a reserved flash memory location. The OTA Agent then validates the integrity of the new image by checking its digital signature. Once validated, the OTA Agent notifies the application about the successful update. The device will then restart and begin running the new firmware. The application developer is responsible for providing the update infrastructure and implementing the mechanism to verify the digital signature of the new firmware image, which can be a custom solution or use platform-specific security features.

### Secure Update of Application

The over-the-air (OTA) Agent is designed to simplify the amount of code the app developer must write to add OTA update functionality to the product. That integration burden consists primarily of initialization of the OTA Agent and, optionally, creating a custom callback function for responding to the OTA completion event messages.
For a client to accept an OTA update, the version number of the update it’s receiving needs to be higher than the version of the firmware that it’s currently running.
The application version of the device software is set by the developer by assigning the build, minor, and major members of the appFirmwareVersion data structure.

### Secure Communication Support

To create embedded applications that communicate securely, developers often utilize TLS (Transport Layer Security) libraries. For SESIP3 certification, the application is required to specifically use TLS and select the cipher suite ECDHE_RSA_WITH_AES_128_GCM_SHA256. This particular cipher suite is mandated as it provides strong cryptographic algorithms and protocols to ensure the confidentiality and integrity of the communication. Additionally, the application must set the root of trust server certificate for the TLS socket connection. This ensures the device can authenticate the server it is communicating with, preventing man-in-the-middle attacks and other security vulnerabilities. By adhering to these specific TLS requirements, the embedded application can meet the rigorous security standards set forth by the SESIP3 certification, providing a higher level of assurance for secure communication in IoT and other embedded systems.

## What next?

I recommend checking out the libraries and the repository along with their documentation to start using SESIP level 3 certified FreeRTOS to help make your applications secure and robust.



