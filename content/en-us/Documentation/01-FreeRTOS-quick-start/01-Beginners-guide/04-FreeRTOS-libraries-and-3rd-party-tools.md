---
title: "FreeRTOS Libraries"
created: 2018-09-20
categories:
  - kernel
description: A brief introduction to FreeRTOS kernel
relatedLinks:
  - title: FreeRTOS libraries overview
    link: /Documentation/03-Libraries/01-Library-overview/01-All-libraries/
  - title: LTS libraries
    link: /Documentation/03-Libraries/01-Library-overview/03-LTS-libraries/01-LTS-libraries/

previous:
  title: Build your first project
  link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project/
next:
  title: FreeRTOS plus AWS solutions
  link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/05-FreeRTOS-plus-AWS-solutions/
---

The FreeRTOS distribution includes more than just the kernel. It also provides [a set of libraries](/Documentation/03-Libraries/01-Library-overview/01-All-libraries) that offer distinct functionality, most of which can be used across various platforms, including Linux and other real-time operating systems (RTOSes).

The libraries are available with examples of their use
[in the main FreeRTOS download package](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS).
They are also available individually directly [from GitHub](/Why-FreeRTOS/FAQs/Github-repository-structure-and-versioning#how-do-i-obtain-and-use-individual-freertos-libraries).

These libraries are categorized based on their status and any dependencies they might have as follows:

1. **[FreeRTOS-Plus libraries](/Documentation/03-Libraries/02-FreeRTOS-plus/01-Introduction)** implement addon functionality for the FreeRTOS kernel, and are specifically for use with FreeRTOS.
	- [**FreeRTOS-Plus-TCP**](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP)
	- [**FreeRTOS-Plus-CLI**](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/01-FreeRTOS-plus-CLI)
1. **[FreeRTOS core libraries](/Documentation/03-Libraries/03-FreeRTOS-core/01-Introduction)** have no dependencies on anything other than the C library - not even on multithreading.  They implement open standards based connectivity, security and related functionality.
	- [**coreMQTT**](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT)
	- [**coreMQTT Agent**](/Documentation/03-Libraries/03-FreeRTOS-core/03-coreMQTT-agent/01-coreMQTT-agent)
	- [**coreHTTP**](/Documentation/03-Libraries/03-FreeRTOS-core/04-coreHTTP/01-coreHTTP)
	- [**coreSNTP**](/Documentation/03-Libraries/03-FreeRTOS-core/05-coreSNTP/01-coreSNTP)
	- [**Transport Interface**](/Documentation/03-Libraries/03-FreeRTOS-core/06-Transport-Interface/01-Transport-interface)
	- [**coreJSON**](/Documentation/03-Libraries/03-FreeRTOS-core/07-coreJSON/01-coreJSON)
	- [**corePKCS \#11**](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/01-corePKCS11)
	- [PKCS \#11](https://en.wikipedia.org/wiki/PKCS_11) an open standard cryptographic API layer (OASIS standard)
	- [**FreeRTOS Cellular Interface Library**](/Documentation/03-Libraries/03-FreeRTOS-core/09-Cellular-interface/01-Cellular-interface)
	- [**Modular Over the Air Updates**](/Documentation/03-Libraries/07-Modular-over-the-air-updates/01-Over-the-air-updates)

1. **[FreeRTOS for AWS IoT](/Documentation/03-Libraries/04-AWS-libraries/01-Introduction)** implement clients for AWS IoT specific value add cloud services.
	- [**AWS IoT Device Shadow**](/Documentation/03-Libraries/04-AWS-libraries/03-AWS-IoT-Device-Shadow/01-AWS-IoT-device-shadow)
	- [**AWS IoT Jobs**](/Documentation/03-Libraries/04-AWS-libraries/04-AWS-IoT-Jobs/01-AWS-IoT-jobs)
	- [**AWS IoT Device Defender**](/Documentation/03-Libraries/04-AWS-libraries/05-AWS-IoT-Device-Defender/01-AWS-IoT-device-defender)
	- [**AWS IoT Fleet Provisioning**](/Documentation/03-Libraries/04-AWS-libraries/06-AWS-IoT-Fleet-Provisioning/01-AWS-IoT-fleet-provisioning)
	- [**AWS Signature Version 4**](/Documentation/03-Libraries/04-AWS-libraries/07-AWS-Signature-Version-4/01-AWS-signature-version-4)
1. **[FreeRTOS labs](/Documentation/03-Libraries/05-FreeRTOS-labs/01-Introduction)** libraries are functional but either incomplete, experimental, or simply provided for open source community interest. The banner on the documentation page of each Labs library describes which criteria applies to that library.
	- [**LoRaWAN**](/Documentation/03-Libraries/05-FreeRTOS-labs/02-LoRaWAN/01-LoRaWAN-library)
	- [**FreeRTOS-Plus-POSIX**](/Documentation/03-Libraries/05-FreeRTOS-labs/03-FreeRTOS-plus-POSIX/00-FreeRTOS-Plus-POSIX)
	- [**FreeRTOS-Plus-FAT**](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/01-FreeRTOS-plus-FAT)
	- [**FreeRTOS MCUBoot**](/Documentation/03-Libraries/05-FreeRTOS-labs/05-FreeRTOS-MCUBoot)
	- [**Delta Over-the-Air Updates**](/Community/Blogs/2022/delta-over-the-air-updates)

The libraries are available with examples of their use in the main FreeRTOS download package, and individually directly from GitHub.


