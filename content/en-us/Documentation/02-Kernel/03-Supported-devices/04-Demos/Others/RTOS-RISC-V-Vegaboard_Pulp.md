---
title: "RISC-V RV32M1 VEGAboard Demo (RI5CY Core)"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![RISC-V RV32M1-Vega Pulp RI5CY Core](/media/2019/RISC-V-RV31M1-VEGA-board.png)

This page documents a pre-configured FreeRTOS Eclipse/GCC project that targets a RISC-V core on
the [RV32M1 VEGAboard](https://open-isa.org/order/).
The RV32M1 incorporates a PULP RI5CY RISC-V
core, a PULP Zero RISCY RISC-V core, an Arm Cortex-M4 core, and an
Arm Cortex-M0+ core. At the time of writing this demo only targets the RI5CY RISC-V core.

---

#### IMPORTANT! Notes on using the FreeRTOS Pulp RI5CY RISC-V port

*Please read all the following points before using this RTOS port.*

1. [Instructions on using FreeRTOS on RISC-V cores](#important-notes-on-using-the-freertos-pulp-ri5cy-risc-v-port)
2. [Source code organisation](#source-code-organization)
3. [The RTOS demo application functionality](#the-vegaboard-ri5cy-risc-v-demo-application)
4. [Building and running the RTOS demo application](#building-and-debugging-the-demo-application)
5. [RTOS configuration and usage details](#configuration-and-usage-details)

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
to use the FreeRTOS VEGAboard RI5CY RISC-V port.

See the
[Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) page for information on the
zip file's directory structure. The Eclipse project is located
in the /Demo/RISC-V\_RV32M1\_Vega\_GCC\_Eclipse directory. More information
is provided in the [build instructions](#building-and-debugging-the-demo-application)
section below.

On RISC-V architectures the additional [freertos\_risc\_v\_chip\_specific\_extensions.h header file](/Using-FreeRTOS-on-RISC-V#RISC_V_SOURCE_FILES)
is used to extend the base RISC-V RTOS port to any chip specific extensions the target RISC-V
chip may implement. The RI5CY RISC-V core used on the RV32M1 VEGAboard includes six additional
registers over and above those defined by the base RISC-V architecture, and does not include
a CLINT. Therefore this project uses the freertos\_risc\_v\_chip\_specific\_extensions.h
header file from the /FreeRTOS/Source/portable/GCC/RISC-V/chip\_specific\_extensions/Pulpino\_Vega\_RV32M1RM
directory.

---

### The VEGAboard RI5CY RISC-V Demo Application

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
 every 1000 milliseconds (1 second).
* The Queue Receive Task:

 The queue receive task is implemented by the prvQueueReceiveTask()
 function. The task sits in a loop that blocks on attempts to
 read from the queue (no CPU cycles are consumed while the task is blocked),
 writing 'blink' to the VEGAboard's UART and toggling an LED each time the value 100 is
 received from the queue send task. As the queue send task writes to the queue every 1000
 milliseconds the queue receive task unblocks and both writes to the UART
 and toggles the LED every 1000 milliseconds.

##### When mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 0

When mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 0 main() calls main\_full().
main\_full() implements a comprehensive test and demo application that demonstrates and/or
tests (among other things):
* [Message buffers](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers)
* [Stream buffers](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers)
* [Task notifications](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)
* [Queues](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues)
* [Semaphores](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores)
* [Mutexes](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes)
* [Event groups](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups)
* [Software timers](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)

The created tasks are from the set of [standard demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
tasks. Standard demo tasks are used by all FreeRTOS port demo applications.
They have no specific functionality, and are created just to demonstrate how to use the FreeRTOS API,
and test the RTOS port.

A 'check' task is created that periodically inspects the standard
demo tasks (which contain self monitoring code) to ensure all the tasks are functioning
as expected. The check task toggles the LED and outputs either a '.' character or error messagto the
UART each time it executes.
This gives visual feedback of the
system health. **If the LED is toggling every 3 seconds, then the
check task has not discovered any problems. If the LED is
toggling every 500 milliseconds, then the check task has
discovered a problem in one or more tasks, and the UART will output an error message
instead of '.'.**

#### Building and debugging the demo application

**Important note:**
The project will not build if the directory structure is different to
the directory structure used in official FreeRTOS zip file releases.
Ensure the 'copy projects into workspace' check box is
not checked when importing the project into
the Eclipse workspace.

To open and build the RI5CY project:

1. [Follow the instructions](https://open-isa.org/get-started/)
 on the open-isa.org web site to install the necessary
 GCC, OpenOCD and Eclipse development tools, and connect the host computer
 (the computer running the development tools) to the target hardware (the VEGAboard).
 More detailed instructions on configuring the Eclipse environment with the relevant tools can
 be found in [this open-isa guide](https://github.com/open-isa-org/open-isa.org/blob/master/RV32M1_Vega_Develop_Environment_Setup.pdf).
2. Start Eclipse and either select an existing or create a new workspace
 when prompted.
3. Select "Import..." from the Eclipse 'File' menu. The Import dialog box
 will open.
4. In the Import dialog box, select "General->Existing Project into Workspace".
 The Import Projects dialog box will open.

![](/media/2019/Importing-an-existing-project-into-Eclipse-TriCore.jpg)

 Importing an existing project into the workspace
5. In the Import Projects dialog box, navigate to and select the
 FreeRTOS/Demo/RISC-V\_RV32M1\_Vega\_GCC\_Eclipse/projects/RTOSDemo\_ri5cy
 directory, and ensure the 'copy projects into workspace'
 check box is not checked.

[![](/media/2019/opening_risc-v-vega_project_in_eclipse.png)](/media/2019/opening_risc-v-vega_project_in_eclipse.png)

 Selecting the directory and project in the Import Project
 dialog box. Click to enlarge.
6. In the 'Projects' window of the Import Projects dialog box, select the RTOSDemo\_ri5cy project, and click finish.
7. Select "Build all" from the Eclipse 'Project' menu. The project should build
 without any errors or warnings, and output a file called RTOSDemo\_ri5cy.elf.
8. Finally, to start a debug session, right click the "RTOSDemo\_ri5cy.launch"
 file in the Eclipse project explorer, then select "Debug As->RTOSDemo\_ri5cy"
 from the pop up menu.

[![](/media/2019/starting_debugger_vega_board_risc-v.png)](/media/2019/starting_debugger_vega_board_risc-v.png)

 Selecting "Debug As->RTOSDemo\_ri5cy"
 from the pop up windows after right clicking "RTOSDemo\_ri5cy.launch". Click to enlarge.

### Configuration and Usage Details

#### RTOS port specific configuration

This section relates to the information provided on the [Running FreeRTOS on RISC-V Cores](/Using-FreeRTOS-on-RISC-V)
documentation page:
* Configuration items specific to this demo are contained in FreeRTOS/Demo/RISC-V\_RV32M1\_Vega\_GCC\_Eclipse/projects/RTOSDemo\_ri5cy/FreeRTOSConfig.h. The
 [constants defined in that file](/Documentation/02-Kernel/03-Supported-devices/02-Customization) can be edited to suit your application. In particular configCLINT\_BASE\_ADDRESS and configMTIMECMP\_BASE\_ADDRESS
 are set to 0 because the RI5CY core on the VEGAboard does not include a machine timer (MTIMER).
* The RI5CY core has six additional registers over and above the registers
 defined by the base RISC-V architecture. These registers are saved and
 restored by the macros contained in the freertos\_risc\_v\_chip\_specific\_extensions.h
 header file located in the /FreeRTOS/Source/portable/GCC/RISC-V/chip\_specific\_extensions/Pulpino\_Vega\_RV32M1RM directory,
 so that directory is in the assembler's include path.
* The interrupt handler provided in the VEGAboard's software development kit (SDK)
 is called SystemIrqHandler(), so the assembler's command line options include
 -DportasmHANDLE\_INTERRUPT=SystemIrqHandler.
* The VEGAboard includes a vectored interrupt controller. The file FreeRTOS\_startup\_RV32M1\_ri5cy.S
 is an edited version of startup\_RV32M1\_ri5cy.S that sets the FreeRTOS trap handler as the interrupt
 handler for each vector. The FreeRTOS trap handler is called freertos\_risc\_v\_trap\_handler().

 The file RV32M1\_ri5cy\_flash.ld is a version of the linker
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
