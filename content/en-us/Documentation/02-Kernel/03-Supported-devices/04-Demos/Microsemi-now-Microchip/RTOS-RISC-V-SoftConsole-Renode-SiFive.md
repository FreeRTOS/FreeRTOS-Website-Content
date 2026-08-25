---
title: "RTOS Demo for RISC-V MiFive M2GL025 / Renode"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![RISC-V MiFive SiFive M2GL025](/media/2019/M2GL025_Creative_Board.png)

This page documents a pre-configured
[SoftConsole](https://www.microsemi.com/product-directory/design-tools/4879-softconsole)/GCC FreeRTOS project that originally
targeted the MiFive RISC-V core on the Microchip (previously MicroSemi)
[M2GL025 Creative Board](https://www.microsemi.com/existing-parts/parts/143948)
from Future Electronics. The target was switched to the [Renode](https://renode.io/) software emulation
of the same board when the project became too large to run out of target RAM (which necessitated
using the FPGA tools to program the application onto the target hardware).
Renode is installed with SoftConole.

---

#### IMPORTANT! Notes on using the MiFive RISC-V port

*Please read all the following points before using this RTOS port.*

1. [Instructions on using FreeRTOS on RISC-V cores](#important-notes-on-using-the-mifive-risc-v-port)
2. [Source code organisation](#source-code-organization)
3. [The demo application functionality](#the-microchip-mifive-risc-v-demo-application)
4. [Building the RTOS demo application](#building-the-rtos-demo-application)
5. [Running/debugging the RTOS demo in the Renode emulator](#running-the-rtos-demo-application-in-the-renode-emulator)
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
to use the FreeRTOS Microchip (previously Microsemi) MiFive RISC-V demo.

See the
[Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) page for information on the
zip file's directory structure. The MiFive RISV-C SoftConsole project is located
in the /Demo/RISC-V\_Renode\_Emulator\_SoftConsole directory. More information
is provided in the [build instructions](#building-the-rtos-demo-application)
section below.

On RISC-V architectures the additional [freertos\_risc\_v\_chip\_specific\_extensions.h header file](/Using-FreeRTOS-on-RISC-V#RISC_V_SOURCE_FILES)
is used to extend the base RISC-V RTOS port to any chip specific extensions the target RISC-V
chip may implement. The RISC-V core used on the M2GL025 board does not implement any
registers over and above those defined by the base RISC-V architecture, and includes
a CLINT. Therefore this project uses the freertos\_risc\_v\_chip\_specific\_extensions.h
header file from the /FreeRTOS/Source/portable/GCC/RISC-V/chip\_specific\_extensions/RV32I\_CLINT\_no\_extensions
directory.

---

### The Microchip MiFive RISC-V Demo Application

#### Functionality

The constant mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY, which is defined at the
top of main.c, is used to switch between a simple 'blinky' style getting started project
and a more comprehensive test and demo application.

##### When mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 1

When mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 1 main() calls main\_blinky().
main\_blinky() creates a basic example that uses two tasks and one queue.
* The Queue Send Task:

 The queue send task is implemented by the prvQueueSendTask() function.
 The task sits in a loop sending the value 100 to the queue
 every 1000 milliseconds (1 emulated second when running in
 the Renode emulator).
* The Queue Receive Task:

 The queue receive task is implemented by the prvQueueReceiveTask()
 function. The task sits in a loop that blocks on attempts to
 read from the queue (no CPU cycles are consumed while the task is blocked),
 writing 'blink' to the Renode console each time the value 100 is
 received from the queue send task.
 As the queue send task writes to the queue every 1000 emulated
 milliseconds the queue receive task unblocks and writes to the Renode console
 every 1000 emulated milliseconds (which may be different to real milliseconds).

##### When mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 0

When mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 0 main() calls main\_full().
main\_full() implements a comprehensive test and demo application that demonstrates and/or
tests (among other things):
* [Message buffers](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers)
* [Stream buffers](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers)
* [Task notifications](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)
* [Event groups](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups)
* [Software timers](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)
* [Queues](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)
* [Semaphores](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)
* [Mutexes](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/)

The created tasks are from the set of [standard demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
tasks. Standard demo tasks are used by all FreeRTOS port demo applications.
They have no specific functionality, and are created just to demonstrate how to use the FreeRTOS API,
and test the RTOS port.

A 'check' task is created that periodically inspects the standard
demo tasks (which contain self monitoring code) to ensure all the tasks are functioning
as expected. The check task outputs a '.' character or error message to the
Renode console each time it executes.
This gives visual feedback of the
system health. **If the '.' appears on the console every 3 emulated seconds (which
will differ from actual seconds), then the
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

To open and build the M2GL025 MiFive RISC-V project:

1. [Download and install](https://www.microsemi.com/product-directory/design-tools/4879-softconsole#downloads) the SoftConsole Eclipse based development tools.
2. Start SoftConsole and either select an existing or create a new workspace
 when prompted.
3. Select "Import..." from the SoftConsole 'File' menu. The Import dialog box
 will open.
4. In the Import dialog box, select "General->Existing Project into Workspace".
 The Import Projects dialog box will open.

![](/media/2019/Importing-an-existing-project-into-Eclipse-TriCore.jpg)

 Importing an existing project into the workspace
5. In the Import Projects dialog box, navigate to and select the
 FreeRTOS/Demo/RISC-V\_Renode\_Emulator\_SoftConsole
 directory, and ensure the 'copy projects into workspace'
 check box is not checked.

[![](/media/2019/opening_risc-v_project_in_softconsole.png)](/media/2019/opening_risc-v_project_in_softconsole.png)

 Selecting the directory and project in the Import Project
 dialog box. Click to enlarge.
6. In the 'Projects' window of the Import Projects dialog box, select the RTOSDemo project, and click finish.
7. Select "Build all" from the SoftConsole 'Project' menu. The project should build
 without any errors or warnings, outputting a file called RTOSDemo.elf.

#### Running the RTOS demo application in the Renode emulator

The instructions below demonstrate how to first start Renode, and then start a debug
session that connects to Renode, all from within the SoftConsole IDE.
The Renode emulator has shipped with SoftConsole since SoftConsole version 6.0:
1. Select "External Tools->External Tools Configuration..." from the
 SoftConsole 'Run' menu. The "Create, manage and run configurations" dialog will
 open.
2. This step creates a menu item in the SoftConsole IDE that,
 when clicked, starts the Renode emulator.

 In the "Create, manage and run configurations" dialog, double click "Program" to add a
 new configuration, then complete the configuration exactly as shown in the
 image below (click the image for a larger view). The tabs not shown in the image can be left at their
 default values.

[![](/media/2019/softconsole_renode_menu_main.png)](/media/2019/softconsole_renode_menu_main.png)

 Creating a configuration that starts the Renode emulator. Click
 to enlarge.
3. Click 'Run' to check the configuration starts Renode. Close the dialog once
 the configuration is able to
 start Renode successfully. **Note:** It is always necessary to stop Renode
 manually once it has been started, but for now, leave it running as it
 is needed in the next step.
4. This step creates a debug launch configuration.

 Right click the "RTOSDemo\_Debug\_Renode.launch"
 file in the Eclipse project explorer, then select "Debug As->RTOSDemo\_Debug\_Renode"
 from the pop up menu. The debugger should start and connect to Renode
 (assuming the previous step left Renode running).

[![](/media/2019/softconsole_creating_renode_debug_configuration.png)](/media/2019/softconsole_creating_renode_debug_configuration.png)

 Creating a debug launch configuration. Click
 to enlarge.
5. Once the launch configuration is able to successfully start a debug
 session, stop the debug session again by selecting it in the Eclipse Debug view
 then clicking the terminate speed button (which has a red square on it), then
 shut down Renode by likewise selecting it in the Eclipse Debug view and
 clicking the terminate speed button again.

**Note:** Stopping the debug
 session does not automatically stop Renode, and Renode must be manually
 stopped after each debug session. Failing to do this will result in high
 CPU load and the inability to start any new debug sessions.

[![](/media/2019/terminate_renode_debug_session.png)](/media/2019/terminate_renode_debug_session.png)

 Terminating the debug session and Renode.
6. Now the configuration to start Renode, and the configuration to
 start a debug session that connects to Renode, have both been created
 and tested, this step links both configurations together.

 Right click the "RTOSDemo-start-renode-emulator-and-attach.launch"
 file in the Eclipse project explorer, then select "Debug As->RTOSDemo-start-renode-emulator-and-attach"
 from the pop up menu. Renode should start, followed by the debug
 session that connects to Renode.

[![](/media/2019/softconsole_start_renode_and_attach.png)](/media/2019/softconsole_start_renode_and_attach.png)

 Starting the Renode emulator and attaching the debugger

### Configuration and Usage Details

#### RTOS port specific configuration

This section relates to the information provided on the [Running FreeRTOS on RISC-V Cores](/Using-FreeRTOS-on-RISC-V)
documentation page:
* Configuration items specific to this demo are contained in FreeRTOS/Demo/RISC-V\_Renode\_Emulator\_SoftConsole/FreeRTOSConfig.h. The
 [constants defined in that file](/Documentation/02-Kernel/03-Supported-devices/02-Customization) can be edited to suit your application. In particular, as the MiFive core includes a machine timer (MTIMER) configMTIME\_BASE\_ADDRESS and configMTIMECMP\_BASE\_ADDRESS are defined to 0xBFF8 and 0x4000 respectively, where PRCI\_BASE is the base address of the clint as defined in the Microchip (previously Microsemi) SDK.
* The MiFive core does not include any registers over and above those defined
 by the base RISC-V architecture. The project therefore uses the
 freertos\_risc\_v\_chip\_specific\_extensions.h
 header file located in the /FreeRTOS/Source/portable/GCC/RISC-V/chip\_specific\_extensions/RV32I\_CLINT\_no\_extensions directory,
 so that directory is in the assembler's include path.
* The interrupt handler provided in the MiFive software development kit (SDK)
 is called handle\_m\_ext\_interrupt, so the assembler's command line options include
 -DportasmHANDLE\_INTERRUPT=handle\_m\_ext\_interrupt.
* The file microsemi-riscv-renode.ld is a version of the linker
 script provided with the board, edited to add the \_\_freertos\_irq\_stack\_top
 linker variable necessary to ensure the stack that was used by main before
 the scheduler starts is reused as the interrupt stack after the scheduler starts.

Other notes:

* vPortEndScheduler() has not been implemented.
* Source/Portable/MemMang/heap\_4.c is included in the RISC-V project to provide the memory
 allocation required by the RTOS kernel.
 Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
 full information.
* At the time of writing, the demo does not support interrupt nesting.
