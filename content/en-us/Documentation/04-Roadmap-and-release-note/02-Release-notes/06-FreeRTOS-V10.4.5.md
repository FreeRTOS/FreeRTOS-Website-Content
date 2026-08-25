---
title: "Upgrading From FreeRTOS V10.4.4 to V10.4.5"
created: 2018-09-20
categories:
  - roadmap and release notes
description: Information on Upgrading From FreeRTOS V10.4.4 to V10.4.5
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: Beginner's guide to FreeRTOS
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: Download FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: FAQs
    link: /Why-FreeRTOS/FAQs
---


FreeRTOS V10.4.5 is a drop in replacement for FreeRTOS V10.4.4 for all ports other than the ARMv8-M ports with secure side support.


### ARMv8-M secure-side port

Tasks that call secure functions from the non-secure side of an ARMv8-M MCU (ARM Cortex-M23 and Cortex-M33) 
have two contexts – one on the non-secure side and one on the secure-side. Previous versions of the FreeRTOS 
ARMv8-M secure-side ports allocated the structures that reference secure-side contexts at run time. Now the 
structures are allocated statically at compile time. This change necessitates the introduction of the 
secureconfigMAX\_SECURE\_CONTEXTS configuration constant, which sets the number of statically allocated secure 
contexts. secureconfigMAX\_SECURE\_CONTEXTS defaults to 8 if left undefined. Applications that only use FreeRTOS 
code on the non-secure side, such as those running third-party code on the secure-side, are not affected by 
this change.
