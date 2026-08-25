---
title: "FreeRTOS Kernel Quick Start Guide"
created: 2018-09-20
categories:
  - kernel
description: Quick Start Guide
---


This page starts by describing how to get the RTOS running on your target as quickly
as possible. Below that, the "[Next steps - further reading](#further-reading)" section provides a set of
links to enable you to further your knowledge, answer common questions, and
become an expert FreeRTOS user.

Also see
the [Getting Started With Simple FreeRTOS Projects](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project#getting-started-with-simple-freertos-demo-projects) documentation,
and for the best possible start, the [FreeRTOS books](/Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book). There are even FreeRTOS
[Windows](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW) and [Linux](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Linux/FreeRTOS-simulator-for-Linux)
ports and [QEMU projects](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/QEMU/freertos-on-qemu-mps2-an385-model) to allow experimentation with FreeRTOS using free tools, and
without any special hardware requirements.


### Preliminary tips


Whether you are new to FreeRTOS or an experienced developer, it is always advised to start new developments with [configASSERT()](/Documentation/02-Kernel/03-Supported-devices/02-Customization#configassert) defined,
a [malloc failed hook](/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions#malloc-failed-hook-function) implemented, and [configCHECK\_FOR\_STACK\_OVERFLOW](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/02-Stack-usage-and-stack-overflow-checking) set to 2.


### RTOS quick start instructions


FreeRTOS has been ported to many different architectures and compilers. Each RTOS port is accompanied by
a pre-configured [demo application](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos) to get you up and running quickly. Better still, each demo application is
accompanied by a documentation page providing full information on locating the RTOS demo project source code, building the demo project, and configuring the target
hardware.

The demo application documentation page also provides **essential RTOS port specific information**, including **how to write FreeRTOS compatible
interrupt service routines**, which is necessarily slightly different on different microcontroller architectures.


Follow these easy instructions to get up an running in minutes:


1. **Download the RTOS source code**:

The RTOS libraries [are available individually from Git](/Why-FreeRTOS/FAQs/Github-repository-structure-and-versioning), but the easiest way to get started is to [download the FreeRTOS .zip file](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) as that also contains demo projects for every official port. Don't be overwhelmed by the amount of files, [only a tiny subset are required for one demo](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)! Unzip the files into a convenient directory.

2. **Locate the relevant documentation page**:

View the "[Supported Devices](/Documentation/02-Kernel/03-Supported-devices/00-Supported-devices)" page to see a list of microcontroller vendors that are officially supported by FreeRTOS. Clicking a microcontroller vendor name will take you to a list of documentation pages specific to that vendor.


Refer to the [Modifying a demo application to run on different hardware](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos) page if a pre-configured port is not available for your development board.

3. **Building the project**:

Follow the instructions on the RTOS port documentation page to locate the required project within the [FreeRTOS directory structure](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization), then open and build the demo project.

4. **Running the demo application**:

Follow the instructions on the RTOS port documentation page to set up the target hardware, download, and execute the demo application. The same documentation page will provide information on the functionality of the demo application, so you know if it is executing correctly or not.

5. **Create your own project:**

The simplest way to [create your own FreeRTOS project](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project) is to base it on the demo application that is provided for your chosen port. Once you have the demo application running, incrementally remove the demo functions and source files and replace them with your own application code.  Troubleshooting help is available under the FAQ "[My Application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting)".


### Further Reading


The simplest way to create your own FreeRTOS application is to base it on the demo application that is provided for your chosen port. Once you have the demo application
running, incrementally remove the demo functions and source files and replace them with your own application code.


The following are some shortcuts to valuable information for the serious developer:


* [Download the FreeRTOS books and manuals](/Documentation/02-Kernel/07-Books-and-manual/01-RTOS_book).
* [Understanding the FreeRTOS directory structure](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization).
* [An introduction to the RTOS demo application projects](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview).
* [Modifying an RTOS demo application to run on different hardware](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos).
* [Understanding the FreeRTOS license](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/04-Licensing).
* [FAQ: My application does not run, what could be wrong](/Why-FreeRTOS/FAQs/Troubleshooting)?
* [Using configASSERT() to trap user errors](/Documentation/02-Kernel/03-Supported-devices/02-Customization#configassert)
* [Obtaining free support](https://forums.freertos.org/).
* [Obtaining commercial licenses and development services](https://www.highintegritysystems.com/).
