---
title: "Download FreeRTOS"
created: 2018-09-20
categories:
  - kernel
description: How to download FreeRTOS
relatedLinks:
  - title: FreeRTOS release notes
    link: /Documentation/04-Roadmap-and-release-note/02-Release-notes/00-Release-history
  - title: FreeRTOS github repositories
    link: https://github.com/FreeRTOS
customStrings:
  - id: 0
    value: FreeRTOS 202604.01 LTS
  - id: 1
    value: "[Package](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/04-FreeRTOS-libraries-and-3rd-party-tools/#freertos-source-code-organisation) containing the FreeRTOS LTS libraries, which includes the FreeRTOS kernel and IoT libraries without example projects. See the [LTS Libraries page](/Documentation/03-Libraries/01-Library-overview/03-LTS-libraries/01-LTS-libraries) for additional details. Source code is also available on [GitHub](https://github.com/FreeRTOS/FreeRTOS-LTS)."
  - id: 4
    value: Getting started with the FreeRTOS kernel
  - id: 5
    value: "Learn how to select a FreeRTOS kernel port, select and build a pre-configured example that demonstrates kernel features, and find other useful kernel documentation. <br/>[Learn More](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/02-Quick-start-guide)"
  - id: 6
    value: Getting started with FreeRTOS-Plus Libraries
  - id: 7
    value: "FreeRTOS-Plus libraries implement addon functionality for the FreeRTOS kernel and are for use in resource-constrained devices. The FreeRTOS-Plus-TCP TCP/IP stack is optimized for use with the FreeRTOS kernel. Some libraries in this category can be used with or without multithreading. FreeRTOS-Plus libraries have a dependency on the FreeRTOS RTOS kernel. <br/>[Learn More](/Documentation/03-Libraries/02-FreeRTOS-plus/01-Introduction)"
  - id: 8
    value: Getting started with FreeRTOS Core Libraries
  - id: 9
    value: "FreeRTOS Core libraries implement open standards based connectivity, security, and related functionality. They are suitable for building smart microcontroller-based devices that connect to the cloud. Unlike the FreeRTOS-Plus libraries, FreeRTOS Core libraries have no dependencies other than on the standard C libraries, so they are not dependent on the FreeRTOS RTOS kernel. <br/>[Learn More](/Documentation/03-Libraries/03-FreeRTOS-core/01-Introduction)"
  - id: 10
    value: Getting started with AWS IoT Libraries
  - id: 11
    value: "The AWS IoT libraries provide clients for connecting to AWS IoT services, including secure over-the-air update functionality. All libraries in this category are suitable for building microcontroller-based IoT devices. Also see the [AWS IoT reference integrations](/Documentation/03-Libraries/04-AWS-libraries/09-AWS-reference-integrations). <br/>[Learn More](/Documentation/03-Libraries/04-AWS-libraries/01-Introduction)"
  - id: 12
    value: Getting started using a Quick Connect board
  - id: 13
    value: "Quick Connect boards are produced in collaboration with partner manufacturers allowing them to connect out of the box to the cloud in less than 5 minutes. All you need is a computer, board specific cables, and a wifi network. No cloud service account such as AWS is required. Once connected, you can view data from the microcontroller's sensors, and then follow the tutorials to add new sensors and actuator controls. <br/>[Learn More](/Why-FreeRTOS/Quick-connect)"
  - id: 14
    value: Getting started with an AWS Reference Integration
  - id: 15
    value: "AWS Reference Integrations are pre-integrated FreeRTOS projects ported to microcontroller-based evaluation boards that demonstrate end to end connectivity to the cloud. AWS Reference Integrations help save months of development effort and accelerate time to market. <br/>[Learn More](/Documentation/03-Libraries/04-AWS-libraries/09-AWS-reference-integrations)"
  - id: 16
    value: Getting started with FreeRTOS Labs
  - id: 17
    value: "FreeRTOS Labs includes libraries that are currently under development but not yet ready for release, as well as experimental projects and libraries that may graduate to become FreeRTOS products. <br/>[Learn More](/Documentation/03-Libraries/05-FreeRTOS-labs/01-Introduction)"
  - id: 18
    value: FreeRTOS Forums
  - id: 19
    value: "Interact with, and get support from, the FreeRTOS community and Amazon Web Services (AWS). <br/>[Learn More](https://forums.freertos.org/)"
  - id: 20
    value: FAQs
  - id: 21
    value: "Frequently Asked Questions <br/>[Learn More](/Why-FreeRTOS/FAQs)"
---

Download the latest FreeRTOS and Long Term Support (LTS) packages below.

The [FAQ](/Why-FreeRTOS/FAQs/Github-repository-structure-and-versioning/#how-are-freertos-git-repositories-structured) describes the difference between individual libraries and library packages, and
provides [links to individual library repositories](/Why-FreeRTOS/FAQs/Github-repository-structure-and-versioning/#how-do-i-obtain-and-use-individual-freertos-libraries).

```jsx
<InfoBlock
  title="0"
  content="1"
  variant="download-primary"
  version="202604.01"
/>
```

Find information on [known issues and security updates](#known-issues-with-the-current-release) at the end of this page.


## Security updates

See the [Security Updates](/Security/03-Vulnerabilities) page.


## Next Steps

The development activity for FreeRTOS has migrated from SVN to GitHub and can now be found directly on
our [GitHub organization](https://github.com/FreeRTOS). Download
a [previous release](https://github.com/FreeRTOS/FreeRTOS/releases) of FreeRTOS from GitHub as a standard
zip (.zip) or self-extracting zip file (.exe). Unzip the source code while making sure to maintain the
folder structure. Please read the documentation referenced below to understand the directory structure and get
started quickly!

```jsx
<InfoBlock
  title="4"
  content="5"
/>
<InfoBlock
  title="6"
  content="7"
/>
<InfoBlock
  title="8"
  content="9"
/>
<InfoBlock
  title="10"
  content="11"
/>
<InfoBlock
  title="12"
  content="13"
/>
<InfoBlock
  title="14"
  content="15"
/>
<InfoBlock
  title="16"
  content="17"
/>
<InfoBlock
  title="18"
  content="19"
/>
<InfoBlock
  title="20"
  content="21"
/>
```


## Security Updates

See the [Security Updates](/Security/03-Vulnerabilities) page.

## Upgrade Instructions

* [Upgrading from FreeRTOS V10.4.6 to V10.5.0](/Documentation/04-Roadmap-and-release-note/02-Release-notes/08-FreeRTOS-V10.5.0)
* [Upgrading from FreeRTOS V10.4.5 to V10.4.6](/Documentation/04-Roadmap-and-release-note/02-Release-notes/07-FreeRTOS-V10.4.6)
* [Upgrading from FreeRTOS V10.4.4 to V10.4.5](/Documentation/04-Roadmap-and-release-note/02-Release-notes/06-FreeRTOS-V10.4.5)
* [Upgrading From FreeRTOS V10.3.0 to V10.4.x](/Documentation/04-Roadmap-and-release-note/02-Release-notes/05-FreeRTOS-V10.4.x)
* [Upgrading From FreeRTOS V10.2.1 to V10.3.0](/Documentation/04-Roadmap-and-release-note/02-Release-notes/04-FreeRTOS-V10.3.0)
* [Upgrading to FreeRTOS Version 10](/Documentation/04-Roadmap-and-release-note/02-Release-notes/03-FreeRTOS-V10)
* [Upgrading to FreeRTOS Version 9](/Documentation/04-Roadmap-and-release-note/02-Release-notes/02-FreeRTOS-V9)
* [Upgrading to FreeRTOS V8.x.x From FreeRTOS V7.x.x](/Documentation/04-Roadmap-and-release-note/02-Release-notes/01-FreeRTOS-V8)


## Known Issues with the Current Release

### Legacy Issues

#### Coldfire V2 CodeWarrior port

The Coldfire V2 CodeWarrior code will not run with the latest (Eclipse) based CodeWarrior tools. A fix is
posted [on the support forum](https://forums.freertos.org/t/starting-a-simple-task/5743) (post 4), and will
be incorporated into the main release in due course.


#### Coldfire V1 CodeWarrior port

The Coldfire V1 CodeWarrior projects will not automatically update to later CodeWarrior versions unless all
unnecessary files are deleted from the FreeRTOS/Source directory first.
See [this support thread](https://forums.freertos.org/t/project-from-scrap-problems-mcf51cn/653) for more information.


#### MSP430 CrossWorks and GCC demos

The CrossWorks demo has not yet been updated to use CrossWorks V2.0 or later. The GCC demo has not yet been
updated to use the latest MSPGCC compiler version.


#### AVR32 demos

The IAR Embedded Workbench demos for the AVR32 will not currently build if you are using a later version of
the IAR tool chain. The issue is caused by changes to macro names within the compiler header files.


#### Silicon Labs SDCC ports

Unfortunately these will not work with the latest compiler versions. The compiler version used to generate the
port is now rather old, but is stated on the port documentation page.
