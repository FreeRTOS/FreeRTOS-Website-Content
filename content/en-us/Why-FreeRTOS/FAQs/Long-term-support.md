---
title: "FreeRTOS FAQ - What is a Long Term Support (LTS) release?"
created: 2018-09-20
categories:
  - kernel
description: Frequently asked questions about the FreeRTOS Long Term Support (LTS) release
---


## Which libraries are covered under FreeRTOS Long Term Support (LTS)?

See the [LTS libraries](/Documentation/03-Libraries/01-Library-overview/03-LTS-libraries/01-LTS-libraries) page for details.


## What is the support period for FreeRTOS LTS libraries?

The support period for FreeRTOS LTS libraries is two years. The latest LTS release, FreeRTOS 202604.00 
LTS will be supported with security and bug fixes that AWS determines as critical until April 30, 2028. 
Support for the previous LTS release, FreeRTOS 202406.05 LTS, will end on June 30, 2026.


## What are the benefits of using FreeRTOS LTS libraries?

FreeRTOS LTS libraries help reduce maintenance and testing costs associated with updating libraries 
on production devices. The FreeRTOS mainline libraries can introduce both new features and critical 
fixes, and it might be difficult for a project nearing production to include only critical fixes. 
FreeRTOS LTS libraries provide two years of predictability and feature stability, and receive security 
updates and critical bug fixes to help keep devices secure.


## Where do I obtain the FreeRTOS LTS libraries?

You can get the FreeRTOS LTS libraries by cloning 
the [FreeRTOS-LTS GitHub repository](https://github.com/FreeRTOS/FreeRTOS-LTS), cloning individual LTS 
libraries, or by downloading the latest FreeRTOS LTS zip file from 
the [downloads page](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS).


## How do I integrate FreeRTOS LTS libraries into my project?

You can include or sub-module individual LTS libraries into your project, or update individual libraries 
to LTS libraries by cloning them from their corresponding repositories. For example, you can update your 
project to the FreeRTOS LTS MQTT library by downloading code from the coreMQTT GitHub repository.


## How do I find information on and download the FreeRTOS LTS patches?

You can visit 
the '[FreeRTOS LTS Patches](/Documentation/03-Libraries/01-Library-overview/03-LTS-libraries/01-LTS-libraries.md#freertos-lts-patches)' 
section in the LTS Libraries page for the latest information, or subscribe to GitHub notifications for 
the FreeRTOS 202604.00 LTS repository. FreeRTOS LTS releases use a date-based versioning scheme (YYYYMM) 
followed by a patch sequential number (.XX). For example, FreeRTOS 202012.02 LTS means the second patch 
to the December-2020 FreeRTOS LTS release. You can get the latest patch from GitHub by using the associated 
download link.


## What is the software license for FreeRTOS LTS?
 
FreeRTOS LTS libraries are distributed free under the MIT open source license. 


## Do I have to pay to use FreeRTOS LTS libraries?

No. FreeRTOS LTS libraries are free for all users under the MIT open source license.


## Who is releasing and supporting FreeRTOS LTS?

AWS will release and provide ongoing maintenance of the FreeRTOS LTS libraries for the benefit of the 
FreeRTOS community. The FreeRTOS community is encouraged to provide feedback and contribute code in the 
form of GitHub pull requests. 


## What is the release cycle for FreeRTOS LTS?

We expect new FreeRTOS LTS releases to happen every 1.5 years.


## What is the SLA for security updates and critical bug fixes?

We aim to address security vulnerabilities and critical bugs on FreeRTOS LTS libraries within seven 
days from successfully implementing a mitigation to releasing an update. 


## Can I get support for more than two years?

Yes, see 
the [FreeRTOS Extended Maintenance Plan](https://aws.amazon.com/freertos/features/#FreeRTOS_Extended_Maintenance_Plan) 
for details.
