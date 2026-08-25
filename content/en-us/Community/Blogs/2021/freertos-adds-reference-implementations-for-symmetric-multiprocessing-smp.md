---
title: FreeRTOS adds reference implementations for symmetric multiprocessing (SMP)
created: 2021-10-14
feature: blog
categories:
  - Long term support
authors: 
  - stanmoy
relatedLinks:
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
---

by [Tanmoy Sen](../author/stanmoy) on 14 Oct 2021

Earlier this year, we [introduced](/Community/Blogs/2021/introducing-the-freertos-symmetric-multiprocessing-smp-github-branch) 
the FreeRTOS Symmetric Multiprocessing GitHub branch for multi-core microcontrollers. We are excited to 
share that we now have reference implementations on two platforms - xcore from [XMOS](https://www.xmos.ai/) 
and [Raspberry Pi Pico](https://www.raspberrypi.com/products/raspberry-pi-pico/). With FreeRTOS SMP, 
developers can use the SMP capabilities of multi-core microcontrollers to design applications.

Multi-core microcontrollers, in which two or more identical processor cores share the same memory, allow 
the operating system to distribute tasks between cores to balance processor load as desired by the application. 
This allows the application to optimize the resource utilization of multi-core microcontrollers. The FreeRTOS 
SMP kernel has a consistent set of configuration options, APIs and behaviors for systems with multiple compute 
cores. With the SMP kernel, you will be able to transition between multi-core and single-core systems with 
minimal effort. 

For more details on the FreeRTOS SMP kernel, 
see [Symmetric Multiprocessing (SMP) with FreeRTOS](/Documentation/02-Kernel/02-Kernel-features/13-Symmetric-multiprocessing-introduction/) on 
FreeRTOS.org 
and [Porting to FreeRTOS SMP Kernel](https://github.com/FreeRTOS/FreeRTOS-SMP-Demos/blob/main/Porting-to-FreeRTOS-SMP-Kernel.md). 
Get started by downloading FreeRTOS SMP kernel source code from [GitHub](https://github.com/FreeRTOS/FreeRTOS-Kernel/tree/smp).


## About the author

![](https://secure.gravatar.com/avatar/4b004f93afe063d6b8444f0fafc89d00?s=200&d=mm&r=g)   
Tanmoy Sen is a Senior Product Manager at Amazon Web Services where he focuses on helping customers and 
embedded developers connect microcontroller-based devices to the cloud.   
[View articles by this author](../author/stanmoy) 

FreeRTOS forums: Get industry-leading support from experts and collaborate with peers around the 
globe. [View Forums](https://forums.freertos.org/)
