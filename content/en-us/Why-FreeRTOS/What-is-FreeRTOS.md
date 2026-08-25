---
title: What is FreeRTOS?
created: 2023-05-16
categories:
  - get started
description: An introduction to the history and current features of FreeRTOS.
featuredImage: /media/2023/what_is_freertos.png
feature: blog
relatedLinks: 
  - title: Why use FreeRTOS?
    link: /Why-FreeRTOS/Why-FreeRTOS
  - title: FAQs
    link: /Why-FreeRTOS/FAQs
next: 
  title: RTOS fundamentals
  link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/01-RTOS-fundamentals
---

<blockquote>
  <span class="content">
    "Provide a free product that surpasses the quality and service demanded by users of commercial alternatives"
  </span>
</blockquote>

Dedicated FreeRTOS developers have been working in close partnership with the world's leading chip companies for more 
than 15 years to provide 
you [market leading](https://www.embedded.com/embedded-survey-2023-more-ip-reuse-as-workloads-surge/), 
commercial grade, and completely free [high quality](/Documentation/02-Kernel/06-Coding-guidelines/02-FreeRTOS-Coding-Standard-and-Style-Guide) **RTOS** and tools ...but 
what is an RTOS?

This page starts by defining an operating system, then refines this to define a 
[real time operating system](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/01-FreeRTOS-kernel), then 
refines this once more to define a real timer kernel (or real time executive).
 
See also the FAQ item "[why use an RTOS](/Why-FreeRTOS/FAQs/What-is-this-all-about#why-use-an-rtos)" for information on when and why it can be useful to use an
RTOS in your embedded systems software design.


## What is a General Purpose Operating System?

An operating system is a computer program that supports a computer's basic functions, and provides services to other 
programs (or *applications*) that run on the computer. The applications provide the functionality that the user of the 
computer wants or needs. The services provided by the operating system make writing the applications faster, simpler, 
and more maintainable. If you are reading this web page, then you are using a web browser (the application program 
that provides the functionality you are interested in), which will itself be running in an environment provided by 
an operating system.


## What is an RTOS?

Most operating systems appear to allow multiple programs to execute at the same time. This is called multi-tasking. In 
reality, each processor core can only be running a single thread of execution at any given point in time. A part of the 
operating system called the scheduler is responsible for deciding which program to run when, and provides the illusion 
of simultaneous execution by rapidly switching between each program.
 
The type of an operating system is defined by how the scheduler decides which program to run when. For example, the 
scheduler used in a multi user operating system (such as Unix) will ensure each user gets a fair amount of the processing 
time. As another example, the scheduler in a desk top operating system (such as Windows) will try and ensure the computer 
remains responsive to its user. (**Note: FreeRTOS is not a big operating system, nor is it designed to run on a desktop 
computer class processor, I use these examples purely because they are systems readers will be familiar with.**)

The scheduler in a Real Time Operating System is
designed to provide a predictable (normally described 
as *deterministic*) execution pattern. This is particularly of interest to embedded systems as embedded systems 
often have real time requirements. A real time requirement is one that specifies that the embedded system must 
respond to a certain event within a strictly defined time (the *deadline*). A guarantee to meet real time 
requirements can only be made if the behaviour of the operating system's scheduler can be predicted (and is 
therefore deterministic).
 
Traditional small real time schedulers, such as the [scheduler used in FreeRTOS](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/04-Task-scheduling), achieve determinism by allowing the user
to assign a priority to each thread of execution. The scheduler then uses the priority to know which thread of 
execution to run next. In FreeRTOS, a thread of execution is called a *task*.


## What is FreeRTOS?

(See also "[more about FreeRTOS](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/01-FreeRTOS-kernel)")

FreeRTOS is a class of RTOS that is designed to be small enough to run on a microcontroller - although its use 
is not limited to microcontroller applications.

A microcontroller is a small and resource constrained processor that incorporates, on a single chip, the processor 
itself, read only  memory (ROM or Flash) to hold the program to be executed, and the random access  memory (RAM) 
needed by the programs it executes. Typically the program is  executed directly from the read only memory.

Microcontrollers are used in deeply embedded applications (those applications where you never actually see the 
processors themselves, or the software they are running) that normally have a very specific and dedicated job to 
do. The size constraints, and dedicated end application nature, rarely warrant the use of a full RTOS implementation - 
or indeed make the use of a full RTOS implementation possible. FreeRTOS therefore provides the core real time 
scheduling functionality, inter-task communication, timing and synchronisation primitives only. This means it is 
more accurately described as a real time kernel, or real time executive. Additional functionality, such as a 
command console interface, or networking stacks, can then be included with add-on components.
