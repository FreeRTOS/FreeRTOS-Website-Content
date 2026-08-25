---
title: "ARM Cortex-M33 (ARMv8-M) Keil Simulator Demo Using Keil uVision IDE"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

[![ARM Cortex-M33 Core](/media/2019/Keil_uVision_IDE.png)](/media/2019/Keil_uVision_IDE.png)

This page documents a pre-configured FreeRTOS project that targets the
[Keil uVision](http://www2.keil.com/mdk5/uvision/) ARM
[Cortex-M33](https://developer.arm.com/products/processors/cortex-m/cortex-m33)
Simulator and uses the [armclang](https://developer.arm.com/docs/100067/0611)
compiler to build the FreeRTOS ARMv8-M GCC port. The project demonstrates using
the ARM Cortex-M33 TrustZone and the ARM Cortex-M33 Memory Protection Unit (MPU).

---

#### IMPORTANT! Notes on using the FreeRTOS ARM Cortex-M33 port

*Please read all the following points before using this RTOS port.*

1. [Source Code Organization](#source-code-organization)
2. [The Demo Application](#the-demo-application)
3. [Building and Running the RTOS Demo Application](#building-and-running-the-rtos-demo-application)
4. [RTOS Configuration and Usage Details](#rtos-configuration-and-usage-details)

Also see the FAQ [My application does not run, what could be wrong?](/Why-FreeRTOS/FAQs/Troubleshooting),
the page that [describes running
FreeRTOS on ARMv8-M cores](/Community/Blogs/2020/using-freertos-on-armv8-m-microcontrollers), and the page that describes [setting
ARM Cortex-M interrupt priorities for use with FreeRTOS](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4).

---

### Source Code Organization

The FreeRTOS zip file download contains the source code for all the FreeRTOS ports, and
every demo application. That means it contains many more files than are required
to use the FreeRTOS ARMv8-M Cortex-M33 port. See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) page for information on the zip file's directory structure.

The project file for this demo is located in the FreeRTOS/Demo/CORTEX\_MPU\_M33F\_Simulator\_Keil\_GCC
directory and is named FreeRTOSDemo.uvmpw. This Keil multi-project
workspace contains two projects - one for the secure side of the ARM Cortex-M33
core, and one for the non-secure side. The FreeRTOS ARMv8-M Cortex-M33 port files
compiled in these two projects are organized as follows:

* Port files compiled in the secure project are in the FreeRTOS/Source/portable/GCC/ARM\_CM33/secure directory.
* Port files compiled in the non-secure project are in the FreeRTOS/Source/portable/GCC/ARM\_CM33/non\_secure directory.

---

### The Demo Application

The project includes two demos:
1. TrustZone Demo
2. Memory Protection Unit (MPU) Demo

#### TrustZone Demo

The TrustZone demo demonstrates how to export functions from the secure side
of the ARM Cortex-M33 core, and how to call them from RTOS tasks on the
non-secure side.
* NonSecure Callable Function:

 The following function is exported from the secure side and is marked
 as non-secure callable:

secureportNON\_SECURE\_CALLABLE uint32\_t NSCFunction( Callback\_t pxCallback )

**Note the use of secureportNON\_SECURE\_CALLABLE macro to mark
 the function as non-secure callable**. This function accepts a callback
 as argument. It first invokes the callback function supplied as argument
 and then increments a secure side counter. The incremented value of the
 secure side counter is returned to the caller.
* NonSecure Callback:

 The following function is implemented on the non-secure side and is
 passed to the above mentioned non-secure callable function as argument:

void prvCallback( void )

 This function increments a non-secure counter.
* Secure Calling Task:

 An un-privileged non-secure task is created using the
 [xTaskCreateRestricted()](/Documentation/02-Kernel/04-API-references/13-FreeRTOS-MPU-specific/01-xTaskCreateRestricted)
 API. This task first calls portALLOCATE\_SECURE\_CONTEXT to allocate
 itself a secure context - **any non-secure task which wants to call a
 function exported from the secure side must allocate itself a secure
 context by calling portALLOCATE\_SECURE\_CONTEXT**.

 The task then calls the secure side function and passes the non-secure
 callback as the argument. The non-secure counter is incremented in the callback
 and the secure counter is incremented in the secure function. Therefore,
 both the counters must be incremented after the call to the secure function
 is complete - this is ensured using [configASSERT()](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert). The task
 sleeps for one second and then repeats the same.

![TrustZone Demo Call Sequence](/media/2019/TZ_Demo.png)

**The TrustZone Demo Call Sequence**

#### Memory Protection Unit (MPU) Demo

The MPU demo demonstrates how to use MPU to grant a task different permissions
to various memory regions. The MPU demo consists of the following two tasks:
* RW Task:

 The RW task has Read-Write access to a shared region of memory (namely
 ucSharedMemory).
* RO Task:

 The RO task has Read-Only access to the same shared region of memory
 (namely ucSharedMemory). This task tries to write to the
 shared memory and since it has read only permission to the shared memory,
 it results in a memory fault. The fault handler checks if it is the
 expected fault from the RO task and if so, it recovers gracefully by
 incrementing the Program Counter to the next statement.

---

### Building and Running the RTOS Demo Application

1. Double click the FreeRTOS/Demo/CORTEX\_MPU\_M33F\_Simulator\_Keil\_GCC/FreeRTOSDemo.uvmpw
 file to open it in the Keil uVision IDE. The Keil multi-project workspace
 FreeRTOSDemo.uvmpw contains a secure project (FreeRTOSDemo\_s)
 and a non-secure project (FreeRTOSDemo\_ns).
2. Set the secure project as active by right clicking on "Project: FreeRTOSDemo\_s"
 and selecting "Set as Active Project".

[![Keil uVision IDE - Set Secure Project Active](/media/2019/Keil_uVision_Sec_Proj_Active.png)](/media/2019/Keil_uVision_Sec_Proj_Active.png)

 Keil uVision IDE - Set Secure Project Active. Click to enlarge.
3. Build the secure project by clicking "Project --> Build 'FreeRTOSDemo\_s (FVP Simulation Model)'".

[![Keil uVision IDE - Build Secure Project](/media/2019/Keil_uVision_Sec_Proj_Build.png)](/media/2019/Keil_uVision_Sec_Proj_Build.png)

 Keil uVision IDE - Build Secure Project. Click to enlarge.
4. Set the non-secure project as active by right clicking on "Project: FreeRTOSDemo\_ns"
 and selecting "Set as Active Project".

[![Keil uVision IDE - Set Non-Secure Project Active](/media/2019/Keil_uVision_NonSec_Proj_Active.png)](/media/2019/Keil_uVision_NonSec_Proj_Active.png)

 Keil uVision IDE - Set Non-Secure Project Active. Click to enlarge.
5. Build the non-secure project by clicking "Project --> Build 'FreeRTOSDemo\_ns (FVP Simulation Model)'".

[![Keil uVision IDE - Build Non-Secure Project](/media/2019/Keil_uVision_NonSec_Proj_Build.png)](/media/2019/Keil_uVision_NonSec_Proj_Build.png)

 Keil uVision IDE - Build Non-Secure Project. Click to enlarge.
6. Start the Debug Session by clicking "Debug -> Start/Stop Debug Session".

[![Keil uVision IDE - Start Debug Session](/media/2019/Keil_uVision_Start_Debug_Session.png)](/media/2019/Keil_uVision_Start_Debug_Session.png)

 Keil uVision IDE - Start Debug Session. Click to enlarge.

---

### RTOS Configuration and Usage Details

Also see the page that [describes running
FreeRTOS on ARMv8-M cores](/Community/Blogs/2020/using-freertos-on-armv8-m-microcontrollers), and the page that describes [setting
ARM Cortex-M interrupt priorities for use with FreeRTOS](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4).

* Configuration items specific to this demo are contained in FreeRTOS/Demo/CORTEX\_MPU\_M33F\_Simulator\_Keil\_GCC/Config/FreeRTOSConfig.h.
 The [constants defined in that file](/Documentation/02-Kernel/03-Supported-devices/02-Customization) can be edited
 to suit your application. The following configuration options are
 specific to the ARM Cortex-M33 port:

	+ configENABLE\_MPU - Enable/Disable Memory Protection Unit (MPU).
	+ configENABLE\_FPU - Enable/Disable Floating Point Unit (FPU).
	+ configENABLE\_TRUSTZONE - Enable/Disable TrustZone.
* If you want to run FreeRTOS with TrustZone disabled, set configENABLE\_TRUSTZONE
 to 0 in your FreeRTOSConfig.h and use the FreeRTOS port files
 in the FreeRTOS/Source/portable/GCC/ARM\_CM33\_NTZ directory.
* If you want to run FreeRTOS on the secure side, set configENABLE\_TRUSTZONE
 to 0 and configRUN\_FREERTOS\_SECURE\_ONLY to 1 in your FreeRTOSConfig.h
 and use the FreeRTOS port files in the FreeRTOS/Source/portable/GCC/ARM\_CM33\_NTZ
 directory.
* Source/Portable/MemMang/heap\_4.c is included in the project
 to provide the memory allocation required by the RTOS kernel. Please
 refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of
 the API documentation for full information.
* vPortEndScheduler() has not been implemented.
