---
title: "FreeRTOS Xilinx Zynq-7000 QEMU Demo (Arm Cortex-A9) Using Xilinx Vitis Eclipse based tools"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

This page documents a FreeRTOS kernel demo that targets the Arm Cortex-A9
 [xilinx-zynq-a9 QEMU](https://www.qemu.org/) model - although the demo also runs on Zynq-7000 hardware too. The
 demo builds and runs using the provided pre-configured [Xilinx Vitis](https://www.xilinx.com/products/design-tools/vitis/vitis-platform.html) project. The Vitis Unified Software Platform provides several integrated tools - this demo only requires the Eclipse based C development IDE.

 There is also [an older Xilinx Zynq-7000 demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Xilinx/RTOS-Xilinx-Zynq) that includes additional libraries and
 is preconfigured to build with the legacy XSDK tools.

---

#### *IMPORTANT! Notes on using the QEMU Cortex-A9 RTOS demo*

*Please read all the following points before using this RTOS port.*

1. [Source Code Organisation](#source-code-organisation)
2. [The Demo Application](#the-xilinx-zynq-a9-arm-cortex-a9-qemu-demo-application)
3. [RTOS Configuration and Usage Details](#rtos-configuration-and-usage-details)

See also the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting),
noting in particular the recommendation to develop with
[configASSERT()](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert) defined
in FreeRTOSConfig.h and [configCHECK\_FOR\_STACK\_OVERFLOW](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/02-Stack-usage-and-stack-overflow-checking)
set to 2.

---

### Source Code Organisation

The FreeRTOS [package](/Why-FreeRTOS/FAQs/Github-repository-structure-and-versioning#how-are-freertos-git-repositories-structured) distribution contains source code for all the FreeRTOS kernel
ports, and projects for all the FreeRTOS demo applications - so contains many
more files than required by this Arm Cortex-A9 QEMU demo.
See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)
section for a description of the directory structure and information on creating a
new FreeRTOS project.

The Vitis project for the Zynq-7000 xilinx-zynq-a9 QEMU demo application is in the
FreeRTOS/Demo/CORTEX\_A9\_Zynq\_ZC702\_Vitis\_QEMU/RTOSDemo directory. That
is the directory to select when importing the project into the Vitis Eclipse
IDE.

---

### The xilinx-zynq-a9 Arm Cortex-A9 QEMU Demo Application

#### Functionality

The demo project provide both the simple blinky and comprehensive test/demo
configurations described on the [FreeRTOS Demos Applications](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
documentation page. Specific to the demo documented on this page, the "check"
task both toggles an LED in case you are running on real hardware, and periodically
prints a message in case you are running in QEMU. The message has the following format:

```c

AAAA - StatusMessageString:BBBB - CCCC
```

Where AAAA is the current RTOS tick count, StatusMessageString is a descriptive text string, BBBB is a hexadecimal
bitmap value where each bit represents one of the self checking tests (if a bit is set then
the test reported an error - see
[prvCheckTask()](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS/Demo/CORTEX_A9_Zynq_ZC702_Vitis_QEMU/RTOSDemo/src/full_demo/main_full.c#L262)),
and CCCC is the number of times the application detected interrupts becoming
nested.

#### Building and executing the demo application

The Vitis demo project references the [ZC702 platform](https://www.xilinx.com/products/boards-and-kits/ek-z7-zc702-g.html),
which is the platform modelled in QEMU. The project will actually run on different hardware platforms as well as in QEMU.
If you are using real hardware other than the ZC702 it might be necessary to
[update
the source code to toggle a different GPIO](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS/Demo/CORTEX_A9_Zynq_ZC702_Vitis_QEMU/RTOSDemo/src/ParTest.c#L51) to see an LED change state.

To add the
ZC702 platform to the Vitis project:

1. Start the Xilinx Vitis IDE (**not** the Vitis HLS IDE) with a new (clean) workspace.
2. From the **File** menu, select **new**, then
 **Platform project...**.
3. Enter "zc702" as the platform project name and click the Next button.

[![](/media/2021/zynq-qemu-platform-project-name.jpg)](/media/2021/zynq-qemu-platform-project-name.jpg)
4. Select "zc702" from the list of hardware specifications. Leave the operating system as
 Standalone as the project already contains FreeRTOS so we don't want
 Vitis to bring FreeRTOS into the project for us. Also leave Processor
 as ps7\_cortexa9\_0.

[![](/media/2021/selecting-zc702.jpg)](/media/2021/selecting-zc702.jpg)
5. Click the Finish button.

Now the Vitis Eclipse project contains the platform, which is a dependency of the demo project. Next import the FreeRTOS demo
project itself:

1. From the **File** menu, select **Import**.
2. In the next window, select the **Eclipse workspace or zip file** radio button, then click the Next button.

[![](/media/2021/importing-eclipse-workspace.jpg)](/media/2021/importing-eclipse-workspace.jpg)
3. In the next Window, select FreeRTOS/FreeRTOS/Demo/CORTEX\_A9\_Zynq\_ZC702\_Vitis\_QEMU
 as the root directory, check both the RTOSDemo and RTOSDemo\_system projects, and
 crucially **uncheck** the "Copy projects into workspace" check box.

[![](/media/2021/importing-zynq-qemu.jpg)](/media/2021/importing-zynq-qemu.jpg)
4. Click the Finish button to import the projects into Vitis.

Everything needed is now in the Vitis workspace and the project can be built
and executed. These instructions assume a QEMU target.

1. Open main.c, and set mainCREATE\_SIMPLE\_BLINKY\_DEMO\_ONLY to generate either
 the [simply blinky demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview/#simple-blinky-demo-configuration), or the [comprehensive test and demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview/#comprehensive-testdemo-configuration) application, as
 required.
2. From the **Project** menu, select **Build project**.
 The zc702 platform project is a dependency of the RTOSDemo project so
 will build before the RTOSdemo project itself. A successful build
 creates the elf file FreeRTOS/Demo/CORTEX\_A9\_Zynq\_ZC702\_Vitis\_QEMU/Debug/RTOSDemo.elf
3. Ensure QEMU is installed on your host computer.
4. Start QEMU with the following command line, replacing [path-to] with
 the correct path to the RTOSDemo.elf file generated by the Vitis GCC build.

```c

qemu-system-arm -M xilinx-zynq-a9 -smp 1 -nographic -kernel [path_to]/RTOSDemo.elf -nographic -serial stdio -semihosting -semihosting-config enable=on,target=native -s -S
```

QEMU command line

 Omit the "-s -S" if you just
 want to run the FreeRTOS application in QEMU without attaching the
 debugger.
5. Click the little arrow next to the green bug speed button, then select "Debug Configurations..." from the resultant menu.

[![](/media/2021/zynq-qemu-debug-config.jpg)](/media/2021/zynq-qemu-debug-config.jpg)
6. In the debug configurations window, select "zc702 Configuration QEMU" from under "GDB Hardware Debugging", then
 click the Debug button. The Eclipse debugger should create a GDB connection to QEMU, start a debug
 session, and break on entry to the main() function.

[![](/media/2021/zynq-qemu-debug-configuration.jpg)](/media/2021/zynq-qemu-debug-configuration.jpg)

---

### RTOS Configuration and Usage Details

#### FreeRTOS ARM Cortex-A port specific configuration

Attention please!: Refer to the page that provides
[instruction on using FreeRTOS on ARM Cortex-A embedded processors](/Using-FreeRTOS-on-Cortex-A-Embedded-Processors),
paying particular attention to the value and meaning of the
configMAX\_API\_CALL\_INTERRUPT\_PRIORITY setting, **and**
the special notes regarding using the floating point unit with GCC.

Configuration items specific to this demo are contained in /FreeRTOS/Demo/CORTEX\_A9\_Zynq\_ZC702\_Vitis\_QEMU/RTOSDemo/src/FreeRTOSConfig.h.
[The constants defined in this file can be edited to suit your application](/Documentation/02-Kernel/03-Supported-devices/02-Customization).

#### Interrupt vector table

By default, SDK projects define the interrupt vector table as part of the BSP. This
makes it difficult to install the FreeRTOS handlers using the methods described
on the [page about
running FreeRTOS on ARM Cortex-A embedded processors](Using-FreeRTOS-on-Cortex-A-Embedded-Processors). Therefore this demo
defines its own interrupt vector table in FreeRTOS\_asm\_vectors.S.
The vector table defined by the BSP is replaced by the vector table defined in
FreeRTOS\_asm\_vectors.S at run time by calling vPortInstallFreeRTOSVectorTable(),
which in the demo, is done in the prvSetupHardware() function.

The vector table defined in FreeRTOS\_asm\_vectors.S is placed in a linker
segment called .freertos\_vectors, and the linker script lscript.ld places
the .freertos\_vectors segment at the beginning of the .text region.

#### [Application Defined] Interrupt service routines

This demo uses drivers provided by Xilinx to configure the interrupt controller,
and install application defined interrupts. Examples can be found in
FreeRTOS/Demo/CORTEX\_A9\_Zynq\_ZC702/RTOSDemo/src/Full\_Demo/serial.c and
FreeRTOS/Demo/CORTEX\_A9\_Zynq\_ZC702/RTOSDemo/src/Full\_Demo/IntQueueTimer.c.

The Xilinx drivers require interrupt
service routines (ISRs) to accept a void * parameter, although the parameter
is not always used. The required ISR prototype is therefore:

```c

    void Interrupt_Handler( void *pvUnusedParameter );
```

The interrupt handler called prvUART\_Handler() in serial.c
provides an example of an interrupt handler that does not use its parameter. The
interrupt handler called prvTimerHandler() in IntQueueTimer.c
provides an example of an interrupt that uses its parameter to determine which
peripheral generated the interrupt, as in that case the same interrupt handler
implementation is installed as the handler for more than one timer.

If an ISR causes a task of equal or higher priority than the currently executing
task to leave the Blocked state then the ISR must request a context switch before
the ISR exits. When this is done the interrupt will interrupt one RTOS task,
but return to a different RTOS task.

The macros portYIELD\_FROM\_ISR() (or portEND\_SWITCHING\_ISR()) can be used to
request a context switch from within an ISR.
The following source code snippet is provided as an example. The example ISR
uses a semaphore to synchronise with a task (not shown), and calls portYIELD\_FROM\_ISR()
to ensure the interrupt returns directly to the task. The prvUART\_Handler() and
prvTimerhandler() functions already referenced provide further examples.

```c

void Dummy_IRQHandler( void *pvUnusedInThisExample )
{
long lHigherPriorityTaskWoken = pdFALSE;

    /* The parameter is not used in this case. */
    ( void ) pvUnusedInThisExample;

    /* Clear the interrupt if necessary. */
    Dummy_ClearITPendingBit();

    /* This interrupt does nothing more than demonstrate how to synchronise a
 task with an interrupt. A semaphore is used for this purpose. Note
 lHigherPriorityTaskWoken is initialised to pdFALSE. */
    [xSemaphoreGiveFromISR](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/17-xSemaphoreGiveFromISR)( xTestSemaphore, &lHigherPriorityTaskWoken );

    /* If there was a task that was blocked on the semaphore, and giving the
 semaphore caused the task to unblock, and the unblocked task has a priority
 higher than or equal to the currently Running task (the task that this
 interrupt interrupted), then lHigherPriorityTaskWoken will have been set to
 pdTRUE internally within xSemaphoreGiveFromISR(). Passing pdTRUE into the
 portYIELD\_FROM\_ISR() macro will result in a context switch being pended to
 ensure this interrupt returns directly to the unblocked, higher priority,
 task. Passing pdFALSE into portYIELD\_FROM\_ISR() has no effect. */
    portYIELD_FROM_ISR( lHigherPriorityTaskWoken );
}
```

Only FreeRTOS API functions that end in "FromISR" can be called from an
interrupt service routine - and then only if the priority of the interrupt
is less than or equal to that set by the configMAX\_API\_CALL\_INTERRUPT\_PRIORITY
configuration constant (meaning a numerically higher value).

#### Resources used by FreeRTOS

Information is provided on the [Using FreeRTOS on ARM Cortex-A Embedded Processors](/Using-FreeRTOS-on-Cortex-A-Embedded-Processors) page.
This demo is configured to generate the tick interrupt from the SCU timer.

#### Memory allocation

Source/Portable/MemMang/heap\_4.c is included in the ARM Cortex-A demo application project to provide the memory
allocation required by the RTOS kernel.
Please refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of the API documentation for
full information.

#### Miscellaneous

Note that vPortEndScheduler() has not been implemented.
