---
title: Introducing the FreeRTOS Symmetric Multiprocessing (SMP) Github Branch
created: 2021-06-30
feature: blog
categories:
  - Long term support
authors: 
  - luciodj
relatedLinks:
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
---

by [Lucio Di Jasio](../author/luciodj) on 30 Jun 2021

With processes shrinking and approaching the limits of physics, in the last decade we have all got used 
to multicore chips of increasing complexity and performance extending Moore’s law in our desktops and 
laptops. In embedded control, where cost, size and robustness demands often take precedence over performance, 
it seems the time for multicore has finally come with the introduction of a number of innovative multicore 
microcontrollers for IoT, communication, digital signal processing, and Artificial Intelligence. The FreeRTOS 
community has recognized this rising tide with many contributions aiming at extending the FreeRTOS kernel 
to support symmetric multiprocessing (SMP) applications. To make a space for these contributions to consolidate, 
we have created a new [FreeRTOS kernel SMP branch](https://github.com/FreeRTOS/FreeRTOS-Kernel/tree/smp). 

Among the most influential contributions thus far, we must recognize [Espressif](https://www.espressif.com/en) 
with Tensilica Xtensa and RISC-V multi core SoCs for wireless connectivity and IoT (previously a fork of 
the FreeRTOS kernel) and [XMOS](https://www.xmos.ai/) with its original xcore platform allowing extreme 
flexibility in architecting IoT solutions combining different forms of computing (DSP, AI, etc) in a 
homogeneous environment making development, testing and maintenance simpler and more cost effective. 
For more information on the XMOS SMP port, see the 
related [press release](https://www.xmos.ai/xmos-announces-the-launch-of-smp-freertos-for-multicore-processors-in-collaboration-with-amazon-web-services/). 
Ports for more architectures, vendors and SoCs will be added in the coming months. While still much 
work is in progress, we invite all FreeRTOS users to give SMP a try, and we welcome all ideas and contributions 
to this exciting new chapter of the evolution of FreeRTOS. 

Get involved by cloning the FreeRTOS SMP [Github](https://github.com/FreeRTOS/FreeRTOS-Kernel/tree/smp) 
repository branch, or choose to be notified by GitHub of updates and activity on this branch.


## About the author

![](https://secure.gravatar.com/avatar/9938f7b242eb47e5e8c3f41e0e927283?s=200&d=mm&r=g)   
Lucio is a Product Manager at Amazon Web Services. He has held various technical and marketing roles 
in the semiconductor industry for the past 20 years. As an opinionated and prolific author he has published 
numerous articles and technical books on programming for embedded control applications. Following his 
passion for flying, he has achieved both FAA and EASA private pilot licenses.   
[View articles by this author](../author/luciodj) 

FreeRTOS forums: Get industry-leading support from experts and collaborate with peers around the 
globe. [View Forums](https://forums.freertos.org/)
