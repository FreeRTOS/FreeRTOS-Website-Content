---
title: "SiFive HiFive1 RTOS demo (RISC-V)"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

 [[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![RISC-V HiFive1 SiFive Freedom Studio and IAR](/media/2020/RISC-V_HiFive-RevB.jpg)

This page documents pre-configured [Freedom Studio](https://www.sifive.com/boards)
(GCC) and [IAR Embedded Workbench for RISC-V](https://www.iar.com/iar-embedded-workbench/#!?architecture=RISC-V)
projects that build and runs a FreeRTOS RISC-V demo on the
[HiFive11 RevB](https://www.sifive.com/boards/hifive1-rev-b)
evaluation board.

---

### IMPORTANT! Notes on using the SiFive RISC-V port

*Please read all the following points before using this RTOS port.*

1. [Instructions on using FreeRTOS on RISC-V cores](#important-notes-on-using-the-sifive-risc-v-port)
2. [Source code organisation](#source-code-organization)
3. [The demo application functionality](#the-sifive-hifive1-revb-risc-v-demo-application)
4. [Building and running the RTOS demo application – Freedom Studio](#building-the-rtos-demo-application-using-freedom-studio)
5. [Building and running the RTOS demo application – IAR](#building-the-rtos-demo-application-use-iar-embedded-workbench)
6. [RTOS configuration and usage details](#configuration-and-usage-details)

Also see the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting).

---

## Instructions on using FreeRTOS on RISC-V cores

If you want to go beyond just running the demo described on this page, or if you
want to create your own RISC-V FreeRTOS project, then please also read the documentation
page that provides [generic information
on running the FreeRTOS kernel on RISC-V cores](Using-FreeRTOS-on-RISC-V).

## Source Code Organization

The FreeRTOS zip file download contains the source code for all the FreeRTOS ports and
demo applications – it therefore contains many more files than are required
to use the FreeRTOS HiFive1 RevB RISC-V demo.

See the
[Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) page for information on the
zip file’s directory structure.
The HiFive1 Freedom Studio and IAR projects are located in the /Demo/RISC-V\_RV32\_SiFive\_HiFive1-RevB\_FreedomStudio
and Demo/RISC-V\_RV32\_SiFive\_HiFive1-RevB\_IAR directories respectively. The [build instructions](#building-the-rtos-demo-application-using-freedom-studio) section provides more information.

On RISC-V architectures the additional [freertos\_risc\_v\_chip\_specific\_extensions.h header file](/Using-FreeRTOS-on-RISC-V#RISC_V_SOURCE_FILES)
is used to extend the base RISC-V RTOS port to any chip specific extensions the target RISC-V
chip may implement. The SiFive core on the HiFive1 provides a Core Local Interrupter (CLINT),
but does not implement any other registers over and above those defined by the base RISC-V
architecture. It therefore uses the freertos\_risc\_v\_chip\_specific\_extensions.h
header file from the /FreeRTOS/Source/portable/[compiler]/RISC-V/chip\_specific\_extensions/RV32I\_CLINT\_no\_extensions
directory.

---

## The SiFive HiFive1 RevB RISC-V Demo Application

### Functionality

The constant mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY, which is defined at the
top of main.c, is used to switch between a simple ‘blinky’ style getting started project
and a more comprehensive test and demo application.

####  When mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 1

When mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 1 main() calls main\_blinky().
main\_blinky() creates a basic example that uses two tasks and one queue, as follows:

* The Queue Send Task:

 The queue send task is implemented by the prvQueueSendTask() function.
 It sits in a loop, sending the value 100 to the queue
 every second.
* The Queue Receive Task:

 The queue receive task is implemented by the prvQueueReceiveTask()
 function. It sits in a loop that blocks on attempts to
 read from the queue (no CPU cycles are consumed while the task is blocked),
 toggling the blue LED each time the value 100 is
 received from the queue send task.

 As the queue send task writes to the queue every second
 the queue receive task unblocks and toggles the LED
 every second.

####  When mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 0

When mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY is set to 0 main() calls main\_full().
main\_full() creates a subset of the standard demo
tasks. Standard demo tasks are used by all FreeRTOS port demo applications.
They have no specific functionality, and are created just to demonstrate how to use the FreeRTOS API,
and test the RTOS port.

A ‘check’ task is created that periodically inspects the standard
demo tasks (which contain self monitoring code) to ensure all the tasks are functioning
as expected. The check task toggles the blue LED each time it executes.
This gives visual feedback of the
system health. **If the LED toggles every 3 seconds, then the
check task has not discovered any problems. If the LED toggles every 500ms, then the check task has
discovered a problem in one or more tasks.**

### Building the RTOS demo application using Freedom Studio

**Important note:**
The project will not build if the directory structure is different to
the directory structure used in official FreeRTOS zip file releases.
Ensure the ‘copy projects into workspace’ check box is
not checked when importing the project into
the Freedom Studio Eclipse workspace.

To open and build the Freedom Studio RISC-V project:

1. [Download and install the Freedom Studio development tools](https://www.sifive.com/boards) (scroll down to see software downloads).
2. Start Freedom Studio and either select an existing or create a new workspace
 when prompted.
3. Select “Import…” from the Freedom Studio ‘File’ menu. The Import dialog box
 will open.
4. In the Import dialog box, select “General->Existing Project into Workspace”.
 The Import Projects dialog box will open.

![](/media/2019/Importing-an-existing-project-into-Eclipse-TriCore.jpg)

 Importing an existing project into the workspace
5. In the Import Projects dialog box, navigate to and select the
 FreeRTOS/Demo/RISC-V\_RV32\_SiFive\_HiFive1-RevB\_FreedomStudio
 directory, and ensure the ‘copy projects into workspace’
 check box is not checked.

[![](/media/2020/copy_hifive1_project_into_workspace.jpg)](/media/2020/copy_hifive1_project_into_workspace.jpg)

 Selecting the directory and project in the Import Project
 dialog box. Click to enlarge.
6. In the ‘Projects’ window of the Import Projects dialog box, select the RTOSDemo project, and click finish.
 The project will be imported into your Eclipse workspace - the steps from here are just to check the path to the
 compiler is correct.
7. Select "Properties" from the IDE's "Project" menu.
8. In the "Properties" window, expand the "C/C++ Build" menu item then select its "Settings" item.
9. In the "Tool Settings" sub-window, select "Cross Settings".
10. In the window, **ensure the Path to the compiler is correct for your installation**. The
 image below shows the default path that will use the compiler installed
 when Freedom Studio was installed - although the GCC version number may
 change.

[![](/media/2020/navigating-to-toolchain-selector.jpg)](/media/2020/navigating-to-toolchain-selector.jpg)

 Configuring the path to the desired toolchain (click to enlarge).
11. When the path to the compiler is correct, in the "Properties" window, select "Apply and Close".
12. Select “Build all” from the Freedom Studio ‘Project’ menu. The FreeRTOS source and
 demo source files should build
 without any errors or warnings (although third party driver code may generate warnings),
 and create a file called RTOSDemo.elf.

To program the HiFive1 RevB board and debug the RTOS demo using Freedom Studio:

1. Connect the HiFive1 RevB board to your host computer using a USB cable.
2. Click the small arrow next to the debug speed button, and select
 “Debug Configurations…” from the pop up menu to bring up the
 debug configurations window.

![](/media/2018/TriCore-Eclipse-Debug-Speed-Button.jpg)

 The debug speed button
3. In the debug configurations window, double click “SiFive GDB SEGGER J-Link Debugging”
 to create a debug configuration.
 The J-Link is built onto the HiFive1 RevB board – you do not need a separate
 J-Link interface.

[![](/media/2020/CreateHiFiveDebugConfiguration.jpg)](/media/2020/CreateHiFiveDebugConfiguration.jpg)

 Creating a J-Link debug configuration
4. In the debug configuration, click the Debug button to program the HiFive1 RevB
 RISC-V evaluation board and start a debug session – after which the normal
 Eclipse debug menu items can be used to run and debug the RTOS application.

 It may be necessary to set the device name in the debug configuration
 before being able to start a debug session.

[![](/media/2020/HiFive1-setting-device-name.jpg)](/media/2020/HiFive1-setting-device-name.jpg)

 Setting the device name in the debug configuration

### Building the RTOS demo application use IAR Embedded Workbench

To open and build the IAR Embedded Workbench for RISC-V project:

1. Open /FreeRTOS/Demo/RISC-V\_RV32\_SiFive\_HiFive1-RevB\_IAR/RTOSDemo.eww
 from within the IAR Embedded Workbench for RISC-V IDE.
2. Select “Rebuild All” from the IDE’s “Project” menu (or just press F7) – the
 RTOS demo should build without any errors or warnings other than
 informative #warning messages.

To program the HiFive1 RevB board and debug the RTOS demo using IAR Embedded Workbench:

1. Connect an IAR I-Jet debug interface between the host computer and the 10-pin debug
 connector marked J1 on the HiFive1 Reb B development board.

[![](/media/2020/i-jet-hifive1.jpg)](/media/2020/i-jet-hifive1.jpg)

 IAR I-Jet connected to the HiFive1 evaluation board

- Select “Download and Debug” from the IDE’s “Project” menu (or press CTRL+D)
 to program the HiFive1 RevB RISC-V evaluation board and start a debug session
 – after which the normal IAR debug menu items can be used to run and debug
 the RTOS application.

## Configuration and Usage Details

### RTOS port specific configuration

This section relates to the information provided on the [Running FreeRTOS on RISC-V Cores](/Using-FreeRTOS-on-RISC-V)
documentation page:

	* Configuration items specific to the Freedom Studio project are contained in FreeRTOS/Demo/RISC-V\_RV32\_SiFive\_HiFive1-RevB\_FreedomStudio/FreeRTOSConfig.h.
	 Configuration items specific to the IAR project are contained in FreeRTOS/Demo/RISC-V\_RV32\_SiFive\_HiFive1-RevB\_IAR/FreeRTOSConfig.h.

	 The [constants defined in these files](/Documentation/02-Kernel/03-Supported-devices/02-Customization)
	 can be edited to suit your application. In particular, as the SiFive RISC-V core includes a
	 machine timer (MTIMER) configMTIME\_BASE\_ADDRESS and configMTIMECMP\_BASE\_ADDRESS
	 are defined to 0x20000BFF8 and 0x20004000 respectively.
	* The SiFive core includes a core local interrupter (CLINT), but does not
	 include any further registers over and above those defined
	 by the base RISC-V architecture. The project therefore uses the
	 freertos\_risc\_v\_chip\_specific\_extensions.h
	 header file located in the /FreeRTOS/Source/portable/[compiler]/RISC-V/chip\_specific\_extensions/RV32I\_CLINT\_no\_extensions directory,
	 so that directory is in the assembler’s include path.
	* The interrupt handler provided in the SiFive software development kit (SDK) and used
	 by the Freedom Studio project
	 is called trap\_handler, so the assembler’s command line options include
	 -DportasmHANDLE\_INTERRUPT=handle\_trap.

	 At the time of writing, the IAR project uses a skeleton trap handler called vApplicationHandleTrap(), which is defined in main.c.
	* The file flash.lds is a version of the linker
	 script provided with the Freedom Studio development tools, edited to add the \_\_freertos\_irq\_stack\_top
	 linker variable necessary to ensure the stack that was used by main before
	 the scheduler starts is reused as the interrupt stack after the scheduler starts.

	 The IAR project uses the configISR\_STACK\_SIZE\_WORDS constant to dimension a
	 statically allocated interrupt stack.

Other notes:

	* vPortEndScheduler() has not been implemented.
	* Source/Portable/MemMang/heap\_4.c is included in the RISC-V projects to provide the memory
	 allocation required by the RTOS kernel.
	 Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
	 full information.
	* At the time of writing, the demo does not support interrupt nesting.
