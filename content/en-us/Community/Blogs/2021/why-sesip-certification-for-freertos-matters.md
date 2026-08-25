---
title: Why SESIP™ Certification for FreeRTOS Matters
description:
date:
feature: blog
categories:
  - Long term support
authors:
  - elberger
relatedLinks:
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
---

by [Richard Elberger](../author/elberger) on 01 Mar 2021

FreeRTOS is now [certified](https://trustcb.com/iot/sesip/sesip-certificates/) for
the [Security Evaluation Standard for IoT Platforms](https://globalplatform.org/specs-library/security-evaluation-standard-for-iot-platforms-sesip-v1-0-gp_fst_070/)
(SESIP™) Assurance Level 2. [FreeRTOS](/) is software that, in most cases, runs on embedded
system processors. More than ever, developers are building FreeRTOS applications while participating
in a growing community that has been working together for more than 18 years. Although the primary
FreeRTOS software is a [real-time operating system kernel](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/01-FreeRTOS-kernel), FreeRTOS provides foundational
libraries such as [FreeRTOS-Plus-TCP](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP), which is a robust,
secure, and ever improving TCP library. FreeRTOS also provides IoT application protocol libraries,
like [coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT), that help developers confidently and securely connect to the cloud.
FreeRTOS is an open source project and is continuously improving with community involvement so it can
continue to be the best choice for developers building embedded systems and solutions.

Across all FreeRTOS projects, security is the top priority. FreeRTOS is already continuously improving
coverage [with memory safety proofs](/Community/Blogs/2020/ensuring-the-memory-safety-of-freertos-part-1).
Now FreeRTOS has demonstrated safety and security through
the [Security Evaluation Standard for IoT Platforms (SESIP™)](https://trustcb.com/iot/sesip/) certification.
SESIP™ derives its fundamental tenets from the industry
established [Common Criteria](https://en.wikipedia.org/wiki/Common_Criteria) framework.  Common Criteria
is an international standard (ISO/IEC 15408) for computer security certification. FreeRTOS has been
rigorously scrutinized by a strong and understandably demanding community. SESIP™ certification demonstrates
our commitment to security to all FreeRTOS application developers whether they actually need to demonstrate
cybersecurity compliance themselves or not, while especially helping products achieve cybersecurity
compliance more quickly for those that do need it. Customers can quickly identify SESIP™ certified applications
that meet a strict set of criteria.

The [SESIP™ Project for FreeRTOS](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-SESIP), configured
with the [FreeRTOS 202012.00 LTS libraries](https://github.com/FreeRTOS/FreeRTOS-LTS/tree/202012.00-LTS),
was used for the certification test and is maintained by FreeRTOS on GitHub. Some of the topics in this
blog assumes knowledge about specific FreeRTOS kernel features or libraries. Feel free to engage the
community through the [FreeRTOS forums](https://forums.freertos.org/) if there is any question about
these specific features.

This blog lists the key areas in the FreeRTOS kernel and related FreeRTOS libraries that were evaluated
by the certification process. The first section covers the certification test assumptions. The next three
sections cover the major areas that were put to the test. The fifth section explains benefits to product
developers looking to achieve SESIP™ certification.


## About SESIP™ certification for the FreeRTOS kernel and related libraries

SESIP™ certification has five assurance levels ranging from zero to five. As the assurance levels increase
so do the complexity and rigidity of the tests. [GlobalPlatform™](https://globalplatform.org/sesip/)
governs [the five SESIP™ Assurance Levels](https://trustcb.com/iot/sesip/), while test partners execute
tests. TrustCB™ provides certification for all five levels of SESIP™ certification. FreeRTOS tested
at SESIP™ level 2, which includes a two-week long black box penetration test
run. [Riscure](https://www.riscure.com/), a highly experienced security test lab, performed the independent
tests required at SESIP™ Level 2. Then, [TrustCB™](https://trustcb.com/) issued the certificate after
verifying the test results. The certification tested for verification of platform identity and instance
identity, firmware update over-the-air, secure communications, isolation capabilities, and cryptographic
operations against the Target of Evaluation (TOE), or body of software under test, which is the FreeRTOS
kernel and relevant IoT libraries.


## Environmental assumptions

Some environmental assumptions had to be made in order to narrow test parameters when testing FreeRTOS
for SESIP™ certification.

It is assumed that he platform shall only be deployed in environments where physical attacks are not
required. The TOE must have a Memory Protection Unit (MPU) as part of the underlying hardware. Next,
tests do not add any hostile code to the TOE. In practice, development teams need to be trusted and
must implement development team rules that constrain FreeRTOS source code modification. The last assumption
is that the Firmware Over-the-Air (FOTA) function
uses [AWS IoT OTA Update Manager](https://docs.aws.amazon.com/freertos/latest/userguide/ota-manager.html).
FOTA capabilities rely on centralized systems to deliver commands and firmware payloads. The centralized
system is not under test. The device connected to the centralized system is under test.

With these assumptions in mind, let's take a look at the top three areas under test.


### Identity verification

The specification states, "Users can only verify they have a secure product, if they can obtain the
identifications of the product parts (application and Connected Platform)." The common mechanism to
achieve identification is source code and configuration management. FreeRTOS maintains the FreeRTOS
kernel and associated libraries on [GitHub](https://github.com/FreeRTOS/FreeRTOS). Github an online
system that uses the [Git source control system](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control).
The source control system allows modification by authenticated and authorized users. The source control
system tracks every atomic [commit](https://git-scm.com/docs/git-commit) made to the system, resulting
in a detailed repository [commit history](https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History).
Developers usually organize software components to individual repositories for ease of management and
composability. Likewise, the FreeRTOS kernel and each library is a software component and has its own
repository.

Although every file contributing to the software component has a version, the configuration manager
applies a git source code repository [tag](https://git-scm.com/book/en/v2/Git-Basics-Tagging) to simplify
what the contiguous set of sources at a specific time represents. FreeRTOS maintains a manifest file
for every software component (represented by individual repositories) which describes the continuous
set of FreeRTOS kernel and libraries. FreeRTOS considers the manifest as the identity verification artifact
for both [Long Term Support (LTS)](https://github.com/FreeRTOS/FreeRTOS-LTS/blob/202012-LTS/manifest.yml)
and [non-LTS](https://github.com/FreeRTOS/FreeRTOS/blob/master/manifest.yml) releases. The FreeRTOS 202012.00
LTS release was used for the TOE.

The certification test evaluated the source code practice and found that implementers can verify software
versions included in their products by the LTS manifest file. The application development team must operate
under the environment condition that the implementer can be trusted and would not modify any SESIP™
certified FreeRTOS source code. Consider making the FreeRTOS source code immutable since modification
of the source code invalidates the certification.

Identity verification for the connected platform relates to the runtime identification under device
operation. Meaning, developers and operators can uniquely identify the runtime device through standard
APIs or structures. In this test, the library responsible for delivering runtime identity APIs was coreMQTT.
Specifically, the developer initializes
the [MQTTConnectInfo](https://github.com/FreeRTOS/coreMQTT/blob/v1.1.0/source/include/core_mqtt_serializer.h#L133)
structure according to application requirements. When an IoT device connects to an MQTT broker, the
client ID must be unique, which is a behavior defined by
the [MQTT v3.1.1 specification, section 3.1, third paragraph](http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.pdf).
The developer must implement a mechanism to uniquely initialize the structure
member [pClientIdentifier](https://github.com/FreeRTOS/coreMQTT/blob/v1.1.0/source/include/core_mqtt_serializer.h#L148)
on a per device basis but the CoreMQTT library presents a consistent API to determine runtime identification.


### System update

An Over-the-Air update makes it possible to update device firmware without an expensive recall or technician
visit. The OTA method enables quick response to security vulnerabilities and software bugs that are discovered
after the devices are deployed in field. Updates are verified to be sent from a trusted source, along with
other validations like version checking and compatibility. The FreeRTOS over-the-air (OTA) client library
enables the app developer to manage the notification of a newly available update, download the update,
and perform cryptographic verification of the firmware update. We talked about how to verify the OTA
model in a previous blog
named [Using Formal Methods to validate OTA Protocol](/Community/Blogs/2020/using-formal-methods-to-validate-ota-protocol).

A key aspect of OTA is a centralized service that provides the security and job management mechanisms
on the server-side that OTA processing demands. Each centralized service may implement the capability
differently. Earlier, this blog mentioned the environmental assumption that AWS, and more specifically
the OTA Update Manager service, would be used as the centralized service. We used
the [AWS IoT Over-the-air Update Library](https://github.com/aws/ota-for-aws-iot-embedded-sdk) when we
implemented the device-side application for OTA, which integrates seamlessly with the OTA Update Manager
service.


### Software isolation

Software isolation helps protect against attackers modifying memory that could have negative impacts
across all running Tasks at application runtime. Software isolation requires two parts: hardware and
software. Software isolation for hardware requires a Memory Management Unit (MMU) or a Memory Protection
Unit (MPU). For software, the FreeRTOS kernel must have a port for an architecture that has the hardware
features and then implements capabilities to work with the MMU and MPU.

When undergoing certification, the FreeRTOS team used
the [LPC54018 IoT Module](https://www.nxp.com/products/processors-and-microcontrollers/arm-microcontrollers/general-purpose-mcus/lpc54000-cortex-m4-/lpc54018-iot-module-for-the-lpc540xx-family-of-mcus:OM40007)
from [NXP™](https://www.nxp.com/) which meets the hardware requirement since it has an MPU. Meeting the
requirements for software isolation was straightforward since the capability has been part of the FreeRTOS
ports for Cortex™-M architectures for some time now. Isolation happens at the FreeRTOS task level so
the implementer must be aware of two different APIs. For more information on this topic,
see [Gaurav Aggarwal's blog section](/Community/Blogs/2020/using-freertos-on-armv8-m-microcontrollers#FREERTOS_WITH_MPU)
relating to ARMv8-M features.


## Additional benefits for those who desire SESIP™ certification

For application developers desiring certification for their own application, a powerful aspect of SESIP™
certification is the certification builds on the SESIP™ certifications already achieved by software and
hardware dependencies. This is known as composition and can be a powerful tool when building a secure
and trusted product. It can be especially important for IoT devices when applications become more complex
due to the software and hardware stacks used to communicate across networks securely. Figure 1 shows
the ideal case when an application goes under certification.

![](/media/2021/blog_sesip_ideal.png)   
*Figure 1. The ideal case where all underlying components of the application in green have SESIP™ certification
at the same or above level of the application's desired level.*

When the application undergoes SESIP™ certification, it is desirable that the developer's TOE focus
is the code or hardware directly under the developer's control. When the developer chooses hardware
and software that is not SESIP™ certified, then the test authority, for example Riscure, will need to
test the entire hardware and software stack. As an example, Figure 2 demonstrates a cause for re-certification
due to FreeRTOS kernel modification.

![](/media/2021/blog_sesip_mod.png)   
*Figure 2. The case where the application developer team modifies the FreeRTOS kernel which voids the certification.*


### What to do next

Well, that was a whirlwind tour of what we did to get SESIP™ Level 2 certified! As next steps, I would
encourage digging even deeper into the APIs that played a part in this certification. OTA offers fantastic
capabilities to anyone deploying IoT devices at scale. Ensuring protection of our runtime code across
memory is just as important. And don't forget, the manifest for both LTS and non-LTS describes the contiguous
set of software that represents the FreeRTOS and libraries software identity. When desiring SESIP™ certification
a new product to build on top of the SESIP™ for FreeRTOS, check out
the [requirements on the GlobalPlatform™ site](https://globalplatform.org/sesip/). Then, start using
FreeRTOS and its libraries based on the manifest file to rely on certification and its assurances throughout
future development efforts.

Have good times and happy coding!


## About the author

![](https://secure.gravatar.com/avatar/df55a46d5a2ea6b956a43b968ff57d3d?s=200&d=mm&r=g)
Richard Elberger is an IoT Principal Technologist at Amazon Web Services. As a prolific speaker, periodic
writer, and tireless embedded technology addict, he creates content and builds community for IoT and
Cloud practitioners globally. Richard maintains and contributes to multiple IoT-related open source
projects (FreeRTOS, meta-aws, ThingPress) which helps customers build and deliver amazing IoT solutions
on AWS.
[View articles by this author](../author/elberger)

FreeRTOS forums: Get industry-leading support from experts and collaborate with peers around the
globe. [View Forums](https://forums.freertos.org/)
