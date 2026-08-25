---
title: What's new in the 202011.00 FreeRTOS release
created: 2020-11-10
feature: blog
categories:
  - Long term support
authors:
  - luciodj
relatedLinks:
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
---

by [Lucio Di Jasio](../author/luciodj) on 10 Nov 2020

We are happy to announce the 202011.00 FreeRTOS release is now available for immediate [download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS).

This release brings in a number of new features and capabilities by graduating libraries from the
published [LTS roadmap](/Documentation/03-Libraries/01-Library-overview/03-LTS-libraries/02-More-about-LTS) into the official FreeRTOS distribution - the LTS roadmap
page gives an insight into what will follow.

In recognition of this growing number of libraries we have made two other changes. First, and as mentioned
in our [previous post](/Documentation/04-Roadmap-and-release-note/02-Release-notes/05-FreeRTOS-V10.4.x), 
we have moved away from using the FreeRTOS kernel's version number to version the download in favor of 
instead using timestamp versioning.  Second, to make the libraries easier to consume, we have placed each 
library in its own GitHub repository.


## FreeRTOS libraries update

The new libraries comply with the code quality checklist [documented on the LTS roadmap page](/Documentation/03-Libraries/01-Library-overview/03-LTS-libraries/02-More-about-LTS#lts-code-quality-checklist),
including a growing number of memory safety proofs. For maximum design flexibility they are also designed to
be standalone, so they have no dependencies on anything other than the standard C library - so there is
no dependency on FreeRTOS or threading.

The first wave of newly added libraries are providing cloud agnostic support for security and connectivity
protocols commonly used in IoT applications. These now include:

* **[coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT)**: implements an [MQTT v.3.1.1](http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/mqtt-v3.1.1.html)
  client. This library has been designed to run on top of any TCP/IP stack. It can be used without multitasking,
  or, as our examples demonstrate, it can run as an agent in a multithreaded application.

* **[coreJSON](/Documentation/03-Libraries/03-FreeRTOS-core/07-coreJSON/01-coreJSON)**: implements a memory
  efficient ([ECMA-404 compliant](https://www.ecma-international.org/publications/standards/Ecma-404.htm)) [JSON](/Documentation/03-Libraries/03-FreeRTOS-core/07-coreJSON/02-coreJSON-terminology)
  parser ideal for small footprints for easy manipulation of objects serialized with this popular notation,
  a requirement for many IoT applications.

* **[corePKCS11](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/01-corePKCS11)**: implements a subset of
  the [OASIS PKCS #11 API standard](https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=pkcs11))
  for cryptographic tokens controlling authentication information. These APIs will help your IoT applications
  to handle secure authentication in a portable way.

Lastly:

* **[AWS IoT Device Shadow](/Documentation/03-Libraries/04-AWS-libraries/03-AWS-IoT-Device-Shadow/01-AWS-IoT-device-shadow)** is a client for
  the [AWS IoT Shadow service](https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-shadows.html)
  which is designed to make an IoT device’s state available to applications and cloud services whether
  the device is active and connected or not.


## FreeRTOS kernel update

The 202011.00 includes a new patch release of the FreeRTOS kernel - version 10.4.2. Note the FreeRTOS
kernel is now in [its own GitHub repo too](https://github.com/FreeRTOS/FreeRTOS-Kernel) for ease of
inclusion (sub-moduling) into a variety of projects. The v10.4.2 release contains patches to a number
of ports - see the kernel's [change history](/Documentation/04-Roadmap-and-release-note/02-Release-notes/00-Release-history)
for details.


## Additional updates

A complete FreeRTOS release always includes, in addition to the kernel, several folders containing demo
projects, FreeRTOS Plus libraries and third party libraries. Among those, this new release brings the
following changes:

* The WolfSSL TLS library has now been updated to v4.5.0 and a new FIPS ready demo has been added.
* Support for ESP IDF v4.2 has been added to include the latest Espressif toolchain release.

Additional updates include increased levels of [MISRA C](https://www.misra.org.uk/) compliance across
the entire project.


##  And One More Thing

Before closing, I am excited to announce our new video series "FreeRTOS On Demand Video" covering topics
related to FreeRTOS and common questions requested by members of the community. Here is
a  [sneak peek at a first interview with Richard Barry](https://forums.freertos.org/t/freertos-on-demand-video-the-new-core-libraries-and-what-to-expect-in-lts/).
Let us know (in the [forums](https://forums.freertos.org/)) what you think!


## About the author

![](https://secure.gravatar.com/avatar/9938f7b242eb47e5e8c3f41e0e927283?s=200&d=mm&r=g)
Lucio is a Product Manager at Amazon Web Services. He has held various technical and marketing roles
in the semiconductor industry for the past 20 years. As an opinionated and prolific author he has published
numerous articles and technical books on programming for embedded control applications. Following his
passion for flying, he has achieved both FAA and EASA private pilot licenses.
[View articles by this author](../author/luciodj)

FreeRTOS forums: Get industry-leading support from experts and collaborate with peers around the
globe. [View Forums](https://forums.freertos.org/)
