---
title: "FreeRTOS Version 10"
created: 2018-09-20
categories:
  - roadmap and release notes
description: Information on FreeRTOS Version 10
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


### Backward Compatibility

FreeRTOS V10 contains a new source file, stream\_buffers.c, and for
consistency has renamed the StackMacros.h header file stack\_macros.h.
However, **V10 is a drop-in compatible replacement for FreeRTOS V9.x.x**, as
the new source file is only required to enable new features, and two copies of
the changed header file are provided - one with the old name and one with the new.
stack\_macros.h is only used internally within the FreeRTOS kernel code.


### Introducing Stream Buffers and Message Buffers

FreeRTOS 10 contains two significant new features: [Stream Buffers and Message Buffers](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers).

Stream Buffers are an inter process communication (IPC) primitive optimized for
use in scenarios where there is only one reader and only one writer, such as
sending a stream of data from an interrupt service routine (ISR) to an RTOS task,
or from one processor core to another.

Message Buffers build on top of Stream Buffers. Whereas Stream Buffers send
a continuous stream of bytes, Message Buffers send discrete messages that can be
of varying length.


### Other Changes

See the [change history](/Documentation/04-Roadmap-and-release-note/02-Release-notes/00-Release-history) for more details of new ports
and other enhancements.
  
