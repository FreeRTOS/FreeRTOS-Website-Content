---
title: FreeRTOS V10.3.1 Now Available and LTS Development Underway
created: 2020-02-18
feature: blog
categories:
  - Long term support
authors: 
  - ribarry
relatedLinks:
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
---

by [Richard Barry](../author/ribarry) on 18 Feb 2020

We are excited to share the following updates with you:

FreeRTOS V10.3.1 is now available for immediate download. V10.3.1, among other things, enhances our 
memory protection unit (MPU) ports for both ARM v7-M and ARM v8-M cores, and extends RISC-V support 
to include a new [IAR port](/Documentation/02-Kernel/03-Supported-devices/04-Demos/SiFive/RTOS-RISC-V-FreedomStudio-IAR-HiFive-RevB). With this release, we 
are also officially switching from our long serving SourceForge SVN repository, to Git repositories 
hosted at https://github.com/FreeRTOS. 

The SVN repository has been mirrored in that Git repository for some time now and development done in 
Git will now be mirrored the other way – back to SVN. We hope the Git workflows will ease your interaction 
with FreeRTOS.

We also made recent improvements to the FreeRTOS.org website, including a website refresh to improve 
navigation. We added downloads that contain the FreeRTOS kernel and additional libraries, [blogs](/Community/Blogs/Blog), 
and hosted the [FreeRTOS Community Forums](https://forums.freertos.org/) directly on the FreeRTOS.org 
website. The forums are esigned to help you quickly find support and take part in community-driven conversation. 
You will see additional website changes rolling out over the coming months.

Additionally we have released new libraries that are intended to help you tackle IoT use cases, from 
securely connecting devices to the cloud, to remotely updating devices already deployed in the field 
with over-the-air updates. The [Libraries Category page](/Documentation/03-Libraries/01-Library-overview/Library-categories) describes how the 
libraries are grouped and selecting a group takes you to information on individual libraries. To help 
you quickly get started, we have added links to IoT reference integrations, which are pre-integrated 
FreeRTOS projects ported to microcontroller-based evaluation boards that demonstrate end to end connectivity 
to the cloud. The [IoT Reference Integrations page](/Why-FreeRTOS/FAQs/AWS-IoT-reference-integrations) provides both the 
projects and their documentation.

Lastly, we have started working on a long-term support (LTS) release. An LTS release is separately maintained 
from the continuously evolving open baseline and maintained for years after launch. You can follow our progress 
on the [LTS page](/Documentation/03-Libraries/01-Library-overview/03-LTS-libraries/02-More-about-LTS).

Thanks to all of our users for your support as we continue to enhance FreeRTOS.


## About the author

![](https://secure.gravatar.com/avatar/2197982f95321bd156e6f3b3fa184b92?s=200&d=mm&r=g)   
Richard Barry founded the FreeRTOS project in 2003, spent more than a decade developing and promoting FreeRTOS 
through his company Real Time Engineers Ltd, and now continues his work on FreeRTOS within a larger team as a 
principal engineer at Amazon Web Services. Richard graduated with 1st Class Honors in Computing for Real Time 
Systems, and was awarded an Honorary Doctorate for his contributions to the development of embedded technology. 
Richard has also been directly involved in the startup of several companies, and authored several books.   
[View articles by this author](../author/ribarry) 


FreeRTOS forums: Get industry-leading support from experts and collaborate with peers around the 
globe. [View Forums](https://forums.freertos.org/)
