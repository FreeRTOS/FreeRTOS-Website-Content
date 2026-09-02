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
Look at /FreeRTOS/FreeRTOS-Kernel/portable FreeRTOS source code folder. There are a plenty of templates are provided for most toolchains and architectures. But not all of them are fully and tested or even completed.
To make FreeRTOS port for newer hardware, the software engineer should deeply know an architecture of new system, it's assemble language and CPU features.
Most important for pre-emptive OS implementation is exception and/or interruption mechanism. Some notes about porting the OS are collected here.

### An importance of serialized interrupt calling and interrupt masking sequence
