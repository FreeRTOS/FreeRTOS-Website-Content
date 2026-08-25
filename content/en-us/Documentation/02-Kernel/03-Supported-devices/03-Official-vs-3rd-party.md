---
title: "'Officially Supported' and 'Contributed' FreeRTOS Code"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

Each architecture **and** compiler combination is considered to be a separate FreeRTOS port.
The microcontroller architecture specific part of a FreeRTOS port is called the port layer.
There are several categories of FreeRTOS port, depending on who create the port and who supports the port:

1. Officially supported ports - these were created by and are supported directly by the FreeRTOS team.

2. Partner contributed ports that are supported by the FreeRTOS team.

3. Partner contributed ports that are supported by the contributing partner.

4. Community supported.

While different categories of port reside in different Git repos (described below), all are sub-moduled
into the main [FreeRTOS git repo](https://github.com/FreeRTOS/FreeRTOS) and all are included in
the [official zip file release](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS).


## Officially Supported Ports

Officially supported ports:

* Are included directly in the [FreeRTOS kernel Git repo](https://github.com/FreeRTOS/FreeRTOS-Kernel).

* Include at least one [demo application](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos) that is documented on the FreeRTOS.org site.

* Are of known origin, removing doubt as to their intellectual property ownership. This in turn allows commercial
  licenses and support contracts to be (optionally) supplied by our partner WITTENSTEIN high integrity systems under the
  OPENRTOS brand.

* Have been written and/or fully inspected and tested by Amazon Web Services Inc.

* Are, in general and where possible, maintained and updated as new versions of the core FreeRTOS source code or
  new versions of the relevant build tools are released.

* Can normally be supported on the freely accessible and monitored
  [support forum](https://forums.freertos.org/).

* Can be included in Long Term Support (LTS) releases.


## Third Party Contributed Ports

Contributed ports:

* Are created by FreeRTOS partners, rather than Amazon Web Services directly.

* Are made freely available from Github.

* Can only be provided under the standard open source FreeRTOS license. Commercial licenses are not offered for
  contributed code.

* Are documented by the contributors themselves. The amount and quality of documentation provided therefore varies
  between contributed packages.

Contributed ports are divided into the categories described by the next three subsections.

**1: FreeRTOS team supported contributed ports**

Location: [https://github.com/FreeRTOS/FreeRTOS-Kernel/tree/main/portable/ThirdParty](https://github.com/FreeRTOS/FreeRTOS-Kernel/tree/main/portable/ThirdParty)

These third party FreeRTOS ports are supported by the FreeRTOS team. For a
FreeRTOS team supported third party FreeRTOS port:

* The code has been reviewed by the FreeRTOS team.

* FreeRTOS team has access to the hardware and the test results have been
  verified by the FreeRTOS team.

* Customer queries as well as bugs are addressed by the FreeRTOS team.

* The code can be included in Long Term Support (LTS) releases.

A new FreeRTOS port cannot be directly contributed to this location. Instead,
the FreeRTOS team will decide to take ownership of a partner supported or a
community supported FreeRTOS port based on the community interest.


**2: Partner supported FreeRTOS ports**

Location: [https://github.com/FreeRTOS/FreeRTOS-Kernel-Partner-Supported-Ports/tree/main](https://github.com/FreeRTOS/FreeRTOS-Kernel-Partner-Supported-Ports/tree/main)

These FreeRTOS ports are supported by a FreeRTOS partner. For a partner
supported FreeRTOS port:

* The code has not been reviewed by the FreeRTOS team.

* FreeRTOS team has not verified the tests results but tests exist and are
  reported to be successful by the partner.

* Customer queries as well as bugs are addressed by the partner.

A new FreeRTOS port can be directly contributed by a partner. The process to contribute a FreeRTOS port
is [documented in Github](https://github.com/FreeRTOS/FreeRTOS-Kernel-Partner-Supported-Ports/blob/main/README.md).


**3: Community supported FreeRTOS ports**

Location: [https://github.com/FreeRTOS/FreeRTOS-Kernel-Community-Supported-Ports/tree/main](https://github.com/FreeRTOS/FreeRTOS-Kernel-Community-Supported-Ports/tree/main).

These FreeRTOS ports are supported by the FreeRTOS community members. For a
community supported FreeRTOS port:

* The code has not been reviewed by the FreeRTOS team.
* Tests may or may not exist for the FreeRTOS port.
* Customer queries as well as bugs are addressed by the community.

A new FreeRTOS port can be directly contributed by anyone. The process to contribute a FreeRTOS port
is [documented on Github](https://github.com/FreeRTOS/FreeRTOS-Kernel-Community-Supported-Ports/blob/main/README.md).
