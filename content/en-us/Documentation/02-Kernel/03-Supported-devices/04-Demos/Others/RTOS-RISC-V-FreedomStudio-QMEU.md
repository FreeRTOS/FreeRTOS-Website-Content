---
title: "RTOS Demo for RISC-V QEMU sifive\_e Model"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![RISC-V HiFive SiFive QMEU](/media/2019/freedom_studio_risc-v.png)

This page documents a pre-configured SiFive Freedom Studio project that builds
and runs a FreeRTOS RISC-V demo in the sifive\_e QEMU model using GCC and GDB.

---

#### IMPORTANT! Notes on using the SiFive RISC-V port

*Please read all the following points before using this RTOS port.*

1. [Instructions on using FreeRTOS on RISC-V cores](#important-notes-on-using-the-sifive-risc-v-port)
2. [Source code organisation](#source-code-organization)
3. [The demo application functionality](#the-sifive_e-qemu-risc-v-demo-application)
4. [Building the RTOS demo application](#building-the-rtos-demo-application)
5. [Running/debugging the RTOS demo in the QEMU emulator](#running-the-rtos-demo-application-in-the-qemu-emulator)
6. [RTOS configuration and usage details](#configuration-and-usage-details)

Also see the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting).

---

### Instructions on using FreeRTOS on RISC-V cores

If you want to go beyond just running the demo described on this page, or if you
want to create your own RISC-V FreeRTOS project, then please also read the documentation
page that provides [generic information
on running the FreeRTOS kernel on RISC-V cores](Using-FreeRTOS-on-RISC-V).

### Source Code Organization

The FreeRTOS zip file download contains the source code for all the FreeRTOS ports, and
every demo application. That means it contains many more files than are required
to use the FreeRTOS sifive\_e QEMU RISC-V demo.

See the
[Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) page for information on the
zip file's directory structure. The sifive\_e RISC-V QEMU Freedom Studio project is located
in the /Demo/RISC-V-Qemu-sifive\_e-FreedomStudio directory. More information
is provided in the [build instructions](#building-the-rtos-demo-application)
section below.

On RISC-V architectures the additional [freertos\_risc\_v\_chip\_specific\_extensions.h header file](/Using-FreeRTOS-on-RISC-V#RISC_V_SOURCE_FILES)
is used to extend the base RISC-V RTOS port to any chip specific extensions the target RISC-V
chip may implement. The QEMU sive5\_e model does not implement any registers over
and above those defined by the base RISC-V architecture, and does emulate a CLINT.
Therefore this project uses the freertos\_risc\_v\_chip\_specific\_extensions.h
header file from the /FreeRTOS/Source/portable/GCC/RISC-V/chip\_specific\_extensions/RV32I\_CLINT\_no\_extensions
directory.

---

### The sifive\_e QEMU RISC-V Demo Application

#### Functionality

The constant mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY, which is defined at the
top of main.c, is used to switch between a simple 'blinky' style getting started project
and a more comprehensive test and demo application.

##### When mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 1

When mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 1 main() calls main\_blinky().
main\_blinky() creates a basic example that uses two tasks and one queue.
* The Queue Send Task:

 The queue send task is implemented by the prvQueueSendTask() function.
 It sits in a loop, sending the value 100 to the queue
 every 1000 emulated milliseconds (1 emulated second).
* The Queue Receive Task:

 The queue receive task is implemented by the prvQueueReceiveTask()
 function. It sits in a loop that blocks on attempts to
 read from the queue (no CPU cycles are consumed while the task is blocked),
 writing 'blink' to the QEMU console each time the value 100 is
 received from the queue send task.

 As the queue send task writes to the queue every 1000 emulated
 milliseconds the queue receive task unblocks and writes to the QEMU console
 every 1000 emulated milliseconds.

##### When mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 0

When mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 0 main() calls main\_full().
main\_full() implements a comprehensive test and demo application that demonstrates and/or
tests (among other things):
* [Stream buffers](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers)
* [Message buffers](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers)
* [Task notifications](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)
* [Event groups](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups)
* [Semaphores](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores)
* [Mutexes](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes)
* [Software timers](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)
* [Queues](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues)

The created tasks are from the set of [standard demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
tasks. Standard demo tasks are used by all FreeRTOS port demo applications.
They have no specific functionality, and are created just to demonstrate how to use the FreeRTOS API,
and test the RTOS port.

A 'check' task is created that periodically inspects the standard
demo tasks (which contain self monitoring code) to ensure all the tasks are functioning
as expected. The check task outputs a '.' character or error message to the
QEMU console each time it executes.
This gives visual feedback of the
system health. **If the '.' appears on the console every 3 emulated seconds (which may be
different to real seconds), then the
check task has not discovered any problems. If the console displays an error
message then the check task has
discovered a problem in one or more tasks.**

#### Building the RTOS demo application

**Important note:**
The project will not build if the directory structure is different to
the directory structure used in official FreeRTOS zip file releases.
Ensure the 'copy projects into workspace' check box is
not checked when importing the project into
the Eclipse workspace.

To open and build the Freedom Studio RISC-V project:

1. [Download and install the Freedom Studio development tools](https://www.sifive.com/boards) (scroll down to see software downloads).
2. Start Freedom Studio and either select an existing or create a new workspace
 when prompted.
3. Select "Import..." from the Freedom Studio 'File' menu. The Import dialog box
 will open.
4. In the Import dialog box, select "General->Existing Project into Workspace".
 The Import Projects dialog box will open.

![](/media/2019/Importing-an-existing-project-into-Eclipse-TriCore.jpg)

 Importing an existing project into the workspace
5. In the Import Projects dialog box, navigate to and select the
 FreeRTOS/Demo/RISC-V-Qemu-siFive\_e-FreedomStudio
 directory, and ensure the 'copy projects into workspace'
 check box is not checked.

[![](/media/2019/opening_risc-v_project_Freedom_Studio.png)](/media/2019/opening_risc-v_project_Freedom_Studio.png)

 Selecting the directory and project in the Import Project
 dialog box. Click to enlarge.
6. In the 'Projects' window of the Import Projects dialog box, select the RTOSDemo project, and click finish.
7. Select "Build all" from the Freedom Studio 'Project' menu. The project should build
 without any errors or warnings, and create a file called RTOSDemo.elf.

#### Running the RTOS demo application in the QEMU emulator

1. [Download QEMU](https://www.qemu.org/download/).
 The project was created and tested using the
 [pre-built Windows binaries](https://qemu.weilnetz.de/w64/).
2. Use the command line below to start QEMU, replacing "path/to"
 with the real path to the RTOSDemo.elf output by the following the build
 instructions above:

```c
qemu-system-riscv32 -kernel path/to/RTOSDemo.elf -S -s -machine sifive_e
```
3. Finally, right click the "Hardware\_QEMU.launch"
 file in the Eclipse project explorer, then select "Debug As->Hardware\_QEMU"
 from the pop up menu. The debugger should start and connect to QEMU
 (assuming the previous step left QEMU running).

[![](/media/2019/starting_debugger_freedom_studio_qemu.png)](/media/2019/starting_debugger_freedom_studio_qemu.png)

 Creating a debug launch configuration. Click
 to enlarge.

### Configuration and Usage Details

#### RTOS port specific configuration

This section relates to the information provided on the [Running FreeRTOS on RISC-V Cores](/Using-FreeRTOS-on-RISC-V)
documentation page:
* Configuration items specific to this demo are contained in FreeRTOS/Demo/RISC-V-Qemu-sifive\_e-FreedomStudio/FreeRTOSConfig.h. The
 [constants defined in that file](/Documentation/02-Kernel/03-Supported-devices/02-Customization)
 can be edited to suit your application. In particular, as the emulated SiFive core includes a machine timer (MTIMER)configMTIME\_BASE\_ADDRESS and configMTIMECMP\_BASE\_ADDRESS are defined to ( CLINT\_CTRL\_ADDR ) + 0xBFF8 and ( CLINT\_CTRL\_ADDR ) + 0x4000 respectively.
* The emulated SiFive core does not include any registers over and above those defined
 by the base RISC-V architecture. The project therefore uses the
 freertos\_risc\_v\_chip\_specific\_extensions.h
 header file located in the /FreeRTOS/Source/portable/GCC/RISC-V/chip\_specific\_extensions/RV32I\_CLINT\_no\_extensions directory,
 so that directory is in the assembler's include path.
* The interrupt handler provided in the SiFive software development kit (SDK)
 is called trap\_handler, so the assembler's command line options include
 -DportasmHANDLE\_INTERRUPT=handle\_trap.
* The file flash.lds is a version of the linker
 script provided with the development tools, edited to add the \_\_freertos\_irq\_stack\_top
 linker variable necessary to ensure the stack that was used by main before
 the scheduler starts is reused as the interrupt stack after the scheduler starts.

Other notes:

* vPortEndScheduler() has not been implemented.
* Source/Portable/MemMang/heap\_4.c is included in the RISC-V project to provide the memory
 allocation required by the RTOS kernel.
 Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
 full information.
* At the time of writing, the demo does not support interrupt nesting.
