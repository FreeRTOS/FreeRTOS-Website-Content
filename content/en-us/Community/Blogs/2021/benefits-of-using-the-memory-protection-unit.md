---
title: Benefits of Using the Memory Protection Unit
created: 2021-02-16
feature: blog
categories:
  - Long term support
authors: 
  - adamlewis
relatedLinks:
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
---

by [Adam Lewis](../author/adamlewis) on 16 Feb 2021

The device you are reading this on relies on your processor’s Memory Management Unit (MMU) to sandbox 
each running application. Without its ability to prevent erroneous or even malicious accesses to the 
wrong memory – be it the operating system’s data or another task’s – consumer devices would be a minefield 
of bugs and security exploits

When it comes to your embedded project, the Memory Protection Unit (MPU) that you’re using can offer 
you many of the same advantages. MPUs typically allow you to run in either privileged or unprivileged 
mode and use a set of ‘regions’ to determine whether the currently executing code has permission to 
access both the code and data. Each region is a continuous block of memory with a set of permissions 
for that memory; both privileged and unprivileged access. Privileged code tends to be given access to 
most, if not all of the device’s memory, compared to a much smaller subset given to unprivileged code.

These regions do not have to be the same for the whole runtime of your application. MPU regions can 
be modified on a per-task basis; each task can have its own unique set of regions that are configured 
when the task is moved to the running state. This allows you to grant access to code and data only to 
the tasks that require it. An embedded operating system utilising the MPU will manage the regions and 
privilege level of each task during every context switch.

[![An example of both global and task MPU regions](/media/2021/MPU_regions-300x238.png)   
*Figure 1: An example of both global and task MPU regions. Click to enlarge.*

Figure 1 shows how two different tasks may view the system memory when using an MPU. There are two global 
MPU regions; one at the start of flash memory and one at the start of RAM. Task 1 is given execute access 
for some code in flash which Task 2 does not have access to. Task 2 is instead given execute access for a 
different set of code within flash. If Task 1 attempted to execute any of Task 2’s code here, then an MPU 
fault will be generated, and vice versa.

Both Task 1 and Task 2 have MPU regions covering the same range of memory in RAM but they are not given 
the same permissions. Task 1 can only read data within the region whereas Task 2 can read and write. This 
could be useful in a scenario where Task 2 is the producer of some data and Task 1 is the consumer who 
should never modify the data.

FreeRTOS offers MPU support in several of its ARM Cortex ports - the M3, M4, M23 and M33 - as well as 
in its Aurix Tricore and Xtensa ESP32 ports. The safety critical relative of 
FreeRTOS, [SAFE**RTOS**](https://www.highintegritysystems.com/safertos/rtos-features/), supports the 
MPU on all platforms where one is available.


## Why use an MPU?

Using the MPU in your embedded project can save you a lot of frustration, time and, by extension, money. 
The biggest single benefit of the MPU for a developer is the ability for it to catch bugs early in development. 
Catching bugs early on significantly reduces development time. Fixing bugs in your code late in the project 
can reduce the rework required on documentation and test code. On the other hand, fixing bugs early will 
reduce the number of bugs present in your code in the later stages of your project. This will simplify the 
process of identifying and fixing the remaining bugs as it is less likely that there will be multiple 
bugs present at once. This helps you keep to a more predictable schedule and prevent unexpected delays.

How does an MPU achieve this? The most evident way is by protecting all of the data that is not associated 
with the currently executing code. A simple example can be constructed with just two RTOS tasks, A and B. 
Tasks A and B should not interact with each other, but there is a bug where task A can accidentally write 
to some data used occasionally by task B. Overwriting this data does not affect the correct operation of 
task A. However when task B attempts to use the corrupt data, task B may malfunction unexpectedly. Without 
an MPU configured to prevent task A from writing to task B’s data, this bug may take a long time for a 
developer to track down. This problem would be especially difficult to solve if the bug was subtle or if 
Task B very rarely used that data. With an MPU, however, the erroneous write operation would immediately 
cause an exception allowing you to pin down which line of code caused the fault.

An MPU can even, on some architectures, help you detect NULL pointer dereferences as you can set up the 
MPU regions to prevent unprivileged code from accessing memory at 0x0.

A well designed set of MPU regions in your application can explicitly protect important areas of memory 
to prevent specific problems. A great example of this is preventing buffer overflows by situating buffers 
at the end of your MPU regions. You can also place your task stacks in areas inaccessible to any unprivileged 
code. If this is done, then each task must use one of their own MPU regions to explicitly grant themselves 
access to their own stack. Using an MPU forces you to really think about the structure of your application 
in order for you to cleanly separate out data between tasks resulting in a more robust and maintainable code base.


## When wouldn’t you use an MPU?

There are two primary scenarios where you *wouldn’t* use the MPU on your processor; a simple project and 
a performance-critical project. The first is straightforward; a very simple application may not benefit 
from the added complexity of using the MPU. Your blinky demo can probably get by without you setting up 
MPU regions covering your flash, RAM, and peripherals.

If you need every last drop of performance out of your processor, then the overhead of using an MPU might 
be a deal breaker for you. The task context switch routines are longer in FreeRTOS ports using the MPU as 
each task has several MPU regions that need to be programmed. When a new task is being context switched in, 
the RTOS must program each task MPU region as well as performing its usual duties such as stacking used 
registers. Additionally, as the kernel code and data is protected by the MPU, all kernel function calls must 
be protected by a wrapper function. This wrapper function simply raises the privilege level of the processor 
before calling the kernel function, then restores the privilege and returning. This will not only increase 
the time required to run your code but also potentially increase the required stack size for your tasks. 
The task’s control block will also have to store information on its MPU regions and in the case of some 
safety critical RTOS’s like SAFE**RTOS**, mirrors of this data will also be stored.

You should also be wary that working with an MPU can be difficult and, at times, frustrating. It will 
take more time to design your application as you must consider MPU regions for each of your tasks. Mistakes 
in these regions, such as incorrect region lengths, permissions or not linking the data of your application 
correctly can be confusing to debug.


## Learn More about MPU usage

While using an MPU may be difficult to learn in the short term, and adds a small amount of overhead to 
your code, the advantages are significant. FreeRTOS provides official MPU support on ARMv7-M (Cortex-M3, 
Cortex-M4 and Cortex-M7 microcontrollers) and ARMv8-M (Cortex-M23 and Cortex-M33 microcontroller) cores. 
Read more about [FreeRTOS memory protection support](/Security/04-FreeRTOS-MPU-memory-protection-unit).

If you’re looking to learn more on the MPU, WITTENSTEIN high integrity systems offer a 
helpful [“Memory Protection” app note](https://www.highintegritysystems.com/rtos/rtos-tutorials/) as 
well as a variety of [useful videos on their YouTube channel](https://www.youtube.com/user/HighIntegritySystems/videos).

This blog has been contributed by one of the engineers working on the SAFE**RTOS** project from WITTENSTEIN 
high integrity systems. SAFE**RTOS** is a safety critical, pre-certified real-time operating system that 
shares a functional model with FreeRTOS. A variety of [white papers](https://www.highintegritysystems.com/white-papers/) 
are available on SAFE**RTOS**, including a detailed example of how to upgrade from FreeRTOS to SAFE**RTOS**. 
 

## Tags

[memory protection unit](/Community/Blogs/2021/benefits-of-using-the-memory-protection-unit), [SAFERTOS](/Partners/Software/SafeRTOS)


## About the author

![](https://secure.gravatar.com/avatar/9c02430671eb1d27752892beeb52070b?s=200&d=mm&r=g)   
Adam Lewis is an embedded engineer on the SAFE**RTOS**® development team at WITTENSTEIN high integrity 
systems.   
[View articles by this author](/Community/Blogs/author/adamlewis) 

FreeRTOS forums: Get industry-leading support from experts and collaborate with peers around the 
globe. [View Forums](https://forums.freertos.org/)
