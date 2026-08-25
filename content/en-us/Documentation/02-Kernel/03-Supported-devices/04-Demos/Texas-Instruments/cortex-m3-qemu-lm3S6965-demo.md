---
title: "FreeRTOS demo for the QEMU LM3S6965 model port"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![QEMU [paused]](/media/2020/FreeRTOS_Cortex-M_QEMU.jpg)

This page describes a pre-configured Eclipse project that builds and runs the FreeRTOS ARM Cortex-M3 GCC port on the LM3S6965
QEMU model.

---

#### IMPORTANT! Notes on using the ARM Cortex-M3 port

_Please read all the following points before using this RTOS port._

1. [Instructions on using FreeRTOS on ARM Cortex-M3 cores](#configuration-and-usage-details)
2. [Source code organisation](#source-code-organization)
3. [The demo application functionality](#the-lm3s6965-qemu-demo-application)
4. [Building and running the RTOS demo application using LM3S6965 in the QEMU emulator](#building-the-rtos-demo-application)
5. [RTOS configuration and usage details](#configuration-and-usage-details)

Also see the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting).

---

### Using FreeRTOS on ARM Cortex-M3 cores

If you want to go beyond just running the demo described on this page, or if you want to create your own ARM Cortex-M
FreeRTOS project, then also read the [generic information on running the FreeRTOS kernel on ARM Cortex-M cores](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4).

### Source Code Organization

The code of the FreeRTOS kernel and demos is available to download from the [main download page](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS) on FreeRTOS.org.
The FreeRTOS zip file download contains the source code for all the FreeRTOS ports and demo applications – it therefore contains many more files than are needed for this project. See the [Source
Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) page for information on the directory structure.

The LM3S6965 QEMU project is located in the `/Demo/CORTEX_LM3S6965_GCC_QEMU` directory. The
[build instructions](#building-the-rtos-demo-application) section provides more information.

---

### The LM3S6965 QEMU Demo Application

#### Functionality

Because QEMU is mainly used as a development target, the demo does not [yet] contain a simple "blinky" project, like those
found in other projects. Instead, `main()` creates a comprehensive test and demo application directly. The demo
tests (among other things):

- [Stream buffers](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers)
- [Message buffers](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers)
- [Task notifications](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)
- [Event groups](/Documentation/02-Kernel/04-API-references/12-Event-groups-or-flags/00-Event-groups)
- [Semaphores](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)
- [Mutexes](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/)
- [Software timers](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers/)
- [Queues](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)

The tasks created are from the set of [standard demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview/) tasks. Standard demo
tasks are used by all FreeRTOS port demo applications. They have no specific functionality, and are only provided to demonstrate
how to use the FreeRTOS API, and to test the RTOS port.

The [tick hook](/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions) function periodically inspects the standard demo tasks (which contain self-monitoring
code) to ensure all the tasks are functioning as expected. It then sends a status message to a task, which prints the status
message on the emulated OLED display, and prints the status message to the emulated UART. If the status message is 'PASS',
then all the tasks are performing as expected. Otherwise, the status message indicates which task reported an error.

**NOTE:** If you execute the demo on a Windows host (and possibly on Linux) for several hours, an error may be
reported. This appears to be a false positive that is apparently caused by writing to the emulated IO. The demo runs for weeks
without reporting an error if it is built with the writes to the emulated OLED display and UART removed.

![](/media/2020/Screen-Shot-2020-08-19-at-5.34.52-PM.png)
QEMU Console Output.

#### Building the RTOS demo application

The project works with the base Eclipse version with Eclipse Embedded CDT plug-ins. To open and build the demo project:

1. Download and install the [Eclipse Embedded CDT (C/C++ Development Tools)](https://projects.eclipse.org/projects/iot.embed-cdt/downloads), which pack together the Eclipse IDE
   for C/C++ Developers standard distribution with the Eclipse Embedded CDT plug-ins.

2. Download and install the
   [GNU Arm Embedded Toolchain](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads)

3. Follow the "Prerequisite" section on the [Import and Build a Demo Project in Eclipse](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Device-independent-demo/building-demos-in-eclipse) page to ensure you have your environment set up correctly. The GCC compiler
   specific to this demo is part of the
   [GNU Arm Embedded Toolchain](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads) that you installed in a previous step.

4. Follow the "Import and Build a Demo Project" section on the [Import and Build a Demo Project in Eclipse](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Device-independent-demo/building-demos-in-eclipse) page. Import the project located in the
   `/Demo/CORTEX_LM3S6965_GCC_QEMU` directory of the FreeRTOS Git repo or FreeRTOS release zip-file.

#### Running the RTOS demo application in the QEMU emulator

**On a Windows Environment:**

1. [Download and install the pre-built QEMU Windows binaries.](https://www.qemu.org/download/#windows)

2. Make sure the directory that contains the QEMU executable is included in the PATH environment variable before you start
   Eclipse.

3. Import and build the project as described above.

4. Right-click the "`start_quem_and_debug.launch`" file in the Eclipse project explorer and select
   "Debug As->start_quem_and_debug" from the pop-up menu. QEMU will start, then the GDB debugger will start and connect
   to QEMU.

![](/media/2020/Screen-Shot-2020-08-19-at-5.00.48-PM.png)
Running a debug session (Windows).

**All Other Environments (also applies to Windows):**

1. Follow the instructions on the [Install and Start the QEMU Emulator](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/QEMU/Install-and-start-QEMU-emulator) page,
   and enter the following command from the CORTEX_LM3S6965_GCC_QEMU demo project directory to start QEMU:

   ```c
   qemu-system-arm -kernel ./Debug/RTOSDemo.elf -S -s -machine lm3s6965evb
   ```

2. Right-click the "RTOSDemo Debug.launch" file in the Eclipse project explorer, then select "Debug As->RTOSDemo Debug"
   from the pop-up menu. The debugger will start and connect to QEMU (assuming the previous step left QEMU running).

   ![](/media/2020/Screen-Shot-2020-08-19-at-4.37.15-PM.png)
   Running a debug session.

### Configuration and Usage Details

#### RTOS port specific configuration

This section relates to the information provided on the [Running the RTOS on a ARM Cortex-M Core](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4) documentation page. Configuration items specific to this demo are contained in `FreeRTOS/Demo/CORTEX_LM3S6965_GCC_QEMU/FreeRTOSConfig.h`.
The [constants defined in that file](/Documentation/02-Kernel/03-Supported-devices/02-Customization) can be edited to suit your application. In particular:

- **configKERNEL_INTERRUPT_PRIORITY**

  `configKERNEL_INTERRUPT_PRIORITY` should be set to the lowest priority. Remember that ARM Cortex-M cores
  use numerically low priority numbers to represent logically HIGH priority interrupts. The lowest priority on an ARM
  Cortex-M core is in fact 255 and different ARM Cortex-M microcontroller manufacturers implement a different number of
  priority bits. However, QEMU doesn't model the priority bits, so while the real LM3S6965 microcontroller has only three
  priority bits, the QEMU model has eight, and therefore `configKERNEL_INTERRUPT_PRIORITY` is set to 255.

- **configMAX_SYSCALL_INTERRUPT_PRIORITY**

  `configMAX_SYSCALL_INTERRUPT_PRIORITY` must not be set to zero. See
  [Running the RTOS on an ARM Cortex-M Core](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4).

Other notes:

- `vPortEndScheduler()` has not been implemented.

- The QEMU LM3S6965 Demo project builds `Source/Portable/MemMang/heap_4.c` to provide the memory allocation
  required by the RTOS kernel. Refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation
  for complete information.
