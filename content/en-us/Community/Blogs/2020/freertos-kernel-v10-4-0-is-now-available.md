---
title: FreeRTOS Kernel v10.4.0 is now available
created: 2020-09-09
feature: blog
categories:
  - Long term support
authors: 
  - luciodj
relatedLinks:
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
---


by [Lucio Di Jasio](../author/luciodj) on 09 Sep 2020

FreeRTOS kernel v10.4.0 is now available for [download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS). The new version brings numerous 
new features such as improved direct to task notifications functionality, enhancements to kernel ports 
that support memory protection units (MPUs), and a new Linux port. See 
the [change history](/Documentation/04-Roadmap-and-release-note/02-Release-notes/00-Release-history) for additional 
details.

  
## Direct to Task Notification Enhancements

Prior to FreeRTOS V10.4.0, each task had a single [direct to task notifications](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications). 
From FreeRTOS V10.4.0, each task now has access to 
a [user definable *array* of task notifications](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configtask_notification_array_entries) 
and the [task notification API](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/00-RTOS-task-notifications) has been extended with new functions 
postfixed with "Indexed" to allow them to operate on any task notification within the array.

A note for Tracealyzer users: The task notification feature in FreeRTOS V10.4.0 is backward compatible 
with that in FreeRTOS V10.3.x with the exception of trace recorder macros. Tracealyzer users will need 
to update their trace recorder code to that provided in the FreeRTOS V10.4.0 release, and 
set TRC\_CFG\_FREERTOS\_VERSION to TRC\_FREERTOS\_VERSION\_10\_4\_0 in their trcConfig.h files.


## Improved MPU support for AMRv7-M and ARMv8-M

FreeRTOS V10.4.0 includes improved [Memory Protection Unit](/Security/04-FreeRTOS-MPU-memory-protection-unit) (MPU) 
support for both the ARMv7-M (ARM Cortex-M3/4/7) and ARMv8-M (ARM Cortex-M23/33) RTOS ports. Additionally 
the ARMv7-M MPU port now supports devices that have 16 MPU regions, and tickless idling support has been 
extended to the ARMv8-M RTOS port. See 
the [MPU support documentation page](/Security/04-FreeRTOS-MPU-memory-protection-unit#upgrading-to-FreeRTOS-10.4.0) 
for important upgrade information.


## Contributed Linux port change

A new POSIX port layer allows FreeRTOS to run on Linux hosts in the same way the Windows port layer enables 
FreeRTOS to run on Windows hosts. 

The original Linux FreeRTOS port provided by William Davy has been replaced with an enhanced port provided 
by David Vrabel. Read  [the Linux simulator documentation page](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Linux/FreeRTOS-simulator-for-Linux) for 
more information.


## Backward Compatibility

FreeRTOS v10.4.0 is a drop in replacement for FreeRTOS V10.3.x for all 
ports [other than those supporting memory protection units (MPUs)](/Security/04-FreeRTOS-MPU-memory-protection-unit#upgrading-to-FreeRTOS-10.4.0). 

If updating a project from a previous FreeRTOS kernel version, refer to 
the [Upgrade to FreeRTOSv10.4.0](/Documentation/04-Roadmap-and-release-note/02-Release-notes/05-FreeRTOS-V10.4.x) page.


## About the author

![](https://secure.gravatar.com/avatar/9938f7b242eb47e5e8c3f41e0e927283?s=200&d=mm&r=g)   
Lucio is a Product Manager at Amazon Web Services. He has held various technical and marketing roles in 
the semiconductor industry for the past 20 years. As an opinionated and prolific author he has published 
numerous articles and technical books on programming for embedded control applications. Following his 
passion for flying, he has achieved both FAA and EASA private pilot licenses.    
[View articles by this author](../author/luciodj) 


FreeRTOS forums: Get industry-leading support from experts and collaborate with peers around the 
globe. [View Forums](https://forums.freertos.org/)
