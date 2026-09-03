---
title: "FreeRTOS Porting Notes"
created: 2026-09-02
categories:
  - kernel
description: Some important nuances of Implementing the Stubs
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: Beginner's guide to FreeRTOS
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: Download FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: Supported devices
    link: /Documentation/02-Kernel/03-Supported-devices/00-Supported-devices/
---

### Intro

Every new architecture of computing platform will require their own kernel stubs - a number of definitions, assemble inserts or small functions to control the code flow and memory.
Some of them could be written from scratch, some of them could be adapted.
Look at /FreeRTOS/FreeRTOS-Kernel/portable FreeRTOS source code folder. There are a plenty of templates provided for most toolchains and architectures. But not all of them are fully and tested or even completed.
To make FreeRTOS port for newer hardware, the software engineer should deeply know an architecture of new system, it's assemble language and CPU features.
Most important for pre-emptive OS implementation is exception and/or interruption mechanism. Some notes about porting the OS are collected here.

### An importance of robust interrupt calling and interrupt masking sequence serialization

Hard to notice, hard to debug could be the race condition between context switch interrupt request and interrupt masking in code after. In several places of FreeRTOS sources, particularly in blocking sections there are combinations like these, for correct task blocking and resuming, the yielding functions should ensure that the interrupt or exception used for context switching will be not blocked by entering critical section even being placed back-to-back in the code:

        {
            ...
            {
                taskYIELD_WITHIN_API();
            }
            ...
        }
        taskENTER_CRITICAL();

This arrangement is usually placed at the boundary between task blocking (yielding) and running which starts from entering critical part. Actually, taskYIELD command is the point where the task is blocked. And next instructions after it are executed when the task is switched-in by the scheduler back to run.
In task yield macro, an interrupt or exception is triggered to switch an execution from task being blocking to the scheduler function. Triggering an interrupt is normal way to execute the scheduler in any case: when an API function like taskYIELD_WITHIN_API() is called or when system tick interval is ended.
From another side, the entering into critical section should block scheduler interrupt to prevent scheduler interrupt during the time the task control block is updated.
In short:

  - taskYIELD calls an interrupt to block the task. Until an interrupt is executed (the scheduler is executed) the task is not blocked and will continue.
  - taskENTER_CRITICAL, in contrast, blocks an interrupt calling to prevent scheduler execution during processing critical part of task control on switching-in running state.

So these control functions should be executed in the order they are arranged. The scheduler should be executed first, the critical section should be executed only when the task should be unblocked (switched-in). Exact behavior depends on hardware a lot.

  - In case of an exception usage for calling the scheduler, the exception is synchronous interrupt for a CPU. Being triggered by an instruction it acts immediately.
  - In case of hardware interrupt usage, an interrupt is asynchronous for the CPU and has a latency.

An exception mechanism is usually intrinsic for a CPU. In that case the order of an execution of yield and enter critical parts is ensured by immediate propagation of an exception signal.
In contrast, an interrupt controller is external block for a CPU even being placed on the same silicon. After an instruction to trigger scheduler interrupt is executed, an interrupt signal takes several CPU cycles to propagate through an interrupt controller to the CPU back. This latency between yield command and actual scheduler interrupt start opens a window for the race: the code after yield instruction continues it's execution for several CPU cycles before being interrupted by the scheduler.
In some cases, particularly at higher compiler optimization levels, an instruction which masks an interrupts globally is executed before scheduler interrupt signal reaching internal CPU interrupt line! We have a BUG! The scheduler interrupt is missed. This way the task skips the blocking state and, after critical section interrupt masking, continues to run like it is already unblocked. In critical part the state of the task is switched to running completely and upon critical part exiting and unmasking scheduler interrupt, the scheduler interrupt takes it's place. But it is too late - the task is already unblocked and blocking state is completely missed.

Conclusion for this note: When porting the FreeRTOS, while implementing or reviewing the YIELD stub, do know which way the scheduler execution is called and how much CPU cycles it could take? Knowing that, ensure the interrupt masking for critical section (typically, global interrupt disable assemble instruction) will not be executed before entering the scheduler interrupt. This sequence should be ensured in any cases for every possible compiler optimizations.
