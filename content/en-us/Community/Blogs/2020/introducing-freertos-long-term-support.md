---
title: Introducing FreeRTOS Long Term Support
created: 2020-12-14
feature: blog
categories:
  - Long term support
authors: 
  - stanmoy
relatedLinks:
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
---

by [Tanmoy Sen](../author/stanmoy) on 14 Dec 2020

Over the last few years, we have been working with our embedded developer partners and customers on 
increasing the pace at which we deliver feature updates for FreeRTOS kernel and libraries. Even as we 
do this, we recognize that there is tension between iterating quickly to add new capabilities, and embedded 
developers’ needs for feature stability, and not having to worry about changes that do not affect existing 
projects or devices. For existing projects and devices, developers need only critical bug fixes and security 
patches, and want the easiest way to identify and incorporate them into their code. 

Today, we are excited to launch the first Long Term Support (LTS) release of FreeRTOS - 202012.00 LTS. 
With this release, developers can rely on a FreeRTOS version that provides feature stability, and security 
patches and critical bug fixes for two years from release date. This makes it easier to identify and 
include the changes, without the risk of introducing updates that could break an existing application. 
The figure below shows the operating model for FreeRTOS LTS releases and how it compares with development 
in the mainline branch. You will notice that bug fixes and security patches are released at a regular 
cadence. These changes will not introduce any new features or changes to existing features that are not 
required for bug fixes or address a newly discovered security vulnerability.


## Highlights

Here are some highlights of FreeRTOS LTS releases going forward:

* FreeRTOS LTS libraries will have feature stability and will not add new features or changes. Only 
  security patches and critical bug fixes will be available with the release for two years.

* FreeRTOS LTS releases use date-based versioning (YYYYMM) followed by a patch sequential number (.XX). 
  Date-based versioning will help identify a specific FreeRTOS LTS release and patch. For 
  example, you can identify the December 2020 LTS release containing a second patch as FreeRTOS 202012.02 
  LTS. Individual libraries continue to use [semantic versioning](https://semver.org/).

* New FreeRTOS LTS releases are expected to be available once every 18 months. We will balance expectations 
  for new feature updates and feature stability from the FreeRTOS community and speed up or slow down 
  release cadence based on feedback.

* FreeRTOS mainline libraries will continue to have rolling releases, with the latest features and updates.

* There are no charges for using FreeRTOS LTS libraries and patches.

* FreeRTOS LTS libraries and patches will continue to be available under the MIT open-source license.


![FreeRTOS LTS Operating Model (Patch releases are examples)](/media/2020/LTS-Operating-Model.png)   
*FreeRTOS LTS Operating Model (Patch releases are examples)*

The first FreeRTOS [LTS release](/Community/Blogs/2021/freertos-aws-reference-integrations-now-include-freertos-202012-01-lts-libraries) is FreeRTOS 202012.00 It includes the FreeRTOS 
kernel and IoT libraries - FreeRTOS-Plus-TCP, coreMQTT, coreHTTP, corePKCS11, coreJSON, and AWS IoT 
Device Shadow. These libraries will be maintained at least until December 31, 2022. 


## FreeRTOS security and memory usage improvements

Security is our #1 priority at AWS, and this applies to our FreeRTOS development as well. To further improve 
security of FreeRTOS and its libraries, we have been working with 
the [Automated Reasoning Group](https://aws.amazon.com/security/provable-security/) at AWS to apply mathematically 
driven provable security techniques to FreeRTOS. The FreeRTOS libraries in the LTS release have been 
validated for memory safety with the C Bounded Model Checker ([CBMC](https://www.cprover.org/cbmc/)) 
automated reasoning tool to mitigate code security issues such as buffer overflow. See the blog Ensuring 
the Memory Safety of FreeRTOS ([Part 1](/Community/Blogs/2020/ensuring-the-memory-safety-of-freertos-part-1), [Part 2](/Community/Blogs/2020/ensuring-the-memory-safety-of-freertos-part-2)) 
to learn more.

The FreeRTOS libraries in the LTS release have been optimized for memory usage and provide more modularity. 
These libraries have no dependencies on any additional libraries other than the standard C library –improving 
design flexibility. They have also undergone a number of code quality checks 
including [MISRA-C](https://misra.org.uk/misra-c/) compliance 
and [Coverity](https://scan.coverity.com/) static analysis to ensure code safety, portability, and reliability 
in embedded systems (see the list in the [LTS Code Quality Checklist](/Community/Blogs/2021/freertos-aws-reference-integrations-now-include-freertos-202012-01-lts-libraries#checklist)). 

These security, memory usage, and code quality attributes are common across FreeRTOS libraries, in mainline 
or an LTS branch, making them easier for use in resource-constrained devices.


## New GitHub repo structure

Each LTS library now comes in its [own GitHub repository](https://github.com/FreeRTOS/FreeRTOS). This 
makes it easier for developers to integrate and update libraries in their FreeRTOS projects. Developers 
can now integrate individual libraries from the FreeRTOS repo 
as [Git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules) (“Git repo inside another”), 
without having to include the rest of the libraries. Developers can also update libraries in their project 
by updating a submodule pointer, without having to copy or move libraries.


## Getting Started

To get started, [download FreeRTOS 202012.00](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) LTS source code from FreeRTOS.org. Alternatively, 
integrate the LTS libraries into your project by submoduling either individual LTS libraries or the entire 
FreeRTOS 202012.00 LTS repository. If you want to connect your devices to AWS IoT and use features such as 
AWS IoT Device Shadow, visit the AWS IoT Reference Integrations [page](/Documentation/03-Libraries/04-AWS-libraries/09-AWS-reference-integrations), 
then select and download an IoT reference integration marked as using the LTS libraries. 


## FreeRTOS LTS Response

We are excited about the response to the new LTS release, which we built with feedback from the FreeRTOS 
community of partners, customers, and embedded developers. We have some early feedback from the FreeRTOS 
community that might help you decide to adopt the LTS release. Here is what we have heard so far… 

* "With the LTS release, developers now can rely on stable interfaces, and using the CMSIS-Pack management 
  system simplifies product lifecycle management." - *Reinhard Keil, Senior Director Embedded Tools, Arm*

* "We are delighted at the introduction of FreeRTOS Long Term Support, because our customers will benefit 
  both from the stability and security updates that long term support releases offer." - *Teo Swee Ann, 
  Founder and CEO, Espressif*.

* "We are glad to see AWS launching FreeRTOS LTS to further strengthen FreeRTOS in the commercial market 
  and address the needs of our mutual customers." - *Anders Holmsberg, GM Embedded Tools, IAR Systems*

* "FreeRTOS LTS libraries coupled with long-term semiconductor support give our customers the stability 
  and longevity assurance they need when choosing a solution for their IoT product." - *Rob Conant, VP 
  of Software and Ecosystem, IoT Compute and Wireless Business Unit – Infineon*

* "Integrating the FreeRTOS LTS libraries further extends our commitment to our MCU customers who develop 
  secure edge devices that are connected to AWS Cloud services and need to be able to depend on critical 
  software updates." - *Joe Yu, VP and GM of IoT Product Line, NXP Semiconductors*

* "With the FreeRTOS LTS release, we believe our customers can benefit from even higher quality and 
  reliability, address security vulnerabilities quickly, and be able to focus more on adding value to 
  their development than before." - *Daryl Khoo, VP of IoT Platform Business Division, Renesas*

* "The FreeRTOS LTS release and its integration in our STM32Cube software package ensures long-term 
  stability and guaranteed maintenance, enabling our customers to focus on quality and added value in building 
  their AWS connectivity solutions." - *Laurent Desseignes, Microcontroller Ecosystem Marketing Manager, 
  STMicroelectronics.*

We are eager to see how the FreeRTOS LTS release improves development and maintenance of the next generation 
of embedded applications. We are looking forward to your feedback. Reach out to us on 
the [FreeRTOS forums](https://forums.freertos.org/) if you have comments or requests!


## About the author

![](https://secure.gravatar.com/avatar/4b004f93afe063d6b8444f0fafc89d00?s=200&d=mm&r=g)   
Tanmoy Sen is a Senior Product Manager at Amazon Web Services where he focuses on helping customers and 
embedded developers connect microcontroller-based devices to the cloud.   
[View articles by this author](../author/stanmoy) 


FreeRTOS forums: Get industry-leading support from experts and collaborate with peers around the 
globe. [View Forums](https://forums.freertos.org/)
