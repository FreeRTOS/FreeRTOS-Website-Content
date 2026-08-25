---
title: "ARM Cortex-M23 (ARMv8-M) Demo for Nuvoton NuMaker-PFM-M2351 Board"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

Using Keil uVision and IAR IDEs

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

[![](/media/2019/Nuvoton_Numaker_PFM_M2351.png)](/media/2019/Nuvoton_Numaker_PFM_M2351.png)

This page documents pre-configured FreeRTOS projects that target the
[ARM Cortex-M23](https://developer.arm.com/products/processors/cortex-m/cortex-m23) core on the
[Nuvoton NuMaker-PFM-M2351](https://www.nuvoton.com/products/iot-solution/iot-platform/numaker-pfm-m2351/)
board.

Two projects are provided:

1. An [IAR Embedded Workbench](https://www.iar.com/iar-embedded-workbench/)
   project that uses the IAR compiler.
2. A [Keil uVision](http://www2.keil.com/mdk5/uvision/)
   project that uses the [armclang](https://developer.arm.com/docs/100067/0611)
   compiler.

The projects demonstrate using the ARM Cortex-M23 TrustZone and the ARM
Cortex-M23 Memory Protection Unit (MPU).

---

#### IMPORTANT! Notes on using the FreeRTOS ARM Cortex-M23 port

_Please read all the following points before using this RTOS port._

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
to use the FreeRTOS ARMv8-M Cortex-M23 port. See the [Source Code Organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) page for information on the zip file's directory structure.
The project files for this demo are organized as follows:

- The IAR Embedded Workbench project file is located in
  FreeRTOS/Demo/CORTEX_MPU_M23_Nuvoton_NuMaker_PFM_M2351_IAR_GCC/Projects/IAR
  directory and is named FreeRTOSDemo.eww. This IAR workspace contains
  two projects - one for the secure side of the ARM Cortex-M23 core, and
  one for the non-secure side. The FreeRTOS ARMv8-M Cortex-M23 port files
  compiled in these two projects are organized as follows:

  - Port files compiled in the secure project are in the FreeRTOS/Source/portable/IAR/ARM_CM23/secure directory.
  - Port files compiled in the non-secure project are in the FreeRTOS/Source/portable/IAR/ARM_CM23/non_secure directory.

- The Keil uVision project file is located in
  FreeRTOS/Demo/CORTEX_MPU_M23_Nuvoton_NuMaker_PFM_M2351_IAR_GCC/Projects/Keil
  directory and is named FreeRTOSDemo.uvmpw. This Keil multi-project
  workspace contains two projects - one for the secure side of the ARM Cortex-M23
  core, and one for the non-secure side. The FreeRTOS ARMv8-M Cortex-M23
  port files compiled in these two projects are organized as follows:

  - Port files compiled in the secure project are in the FreeRTOS/Source/portable/GCC/ARM_CM23/secure directory.
  - Port files compiled in the non-secure project are in the FreeRTOS/Source/portable/GCC/ARM_CM23/non_secure directory.

---

### The Demo Application

The projects include two demos:

1. TrustZone Demo
2. Memory Protection Unit (MPU) Demo

#### TrustZone Demo

The TrustZone demo demonstrates how to export functions from the secure side
of the ARM Cortex-M23 core, and how to call them from RTOS tasks on the
non-secure side.

- NonSecure Callable Function:

The following function is exported from the secure side and is marked
as non-secure callable:

secureportNON_SECURE_CALLABLE uint32_t NSCFunction( Callback_t pxCallback )

**Note the use of secureportNON_SECURE_CALLABLE macro to mark
the function as non-secure callable**. This function accepts a callback
as argument. It first invokes the callback function supplied as argument
and then increments a secure side counter. The incremented value of the
secure side counter is returned to the caller.

- NonSecure Callback:

The following function is implemented on the non-secure side and is
passed to the above mentioned non-secure callable function as argument:

void prvCallback( void )

This function increments a non-secure counter.

- Secure Calling Task:

An un-privileged non-secure task is created using the
[xTaskCreateRestricted()](/Documentation/02-Kernel/04-API-references/13-FreeRTOS-MPU-specific/01-xTaskCreateRestricted)
API. This task first calls portALLOCATE_SECURE_CONTEXT to allocate
itself a secure context - **any non-secure task which wants to call a
function exported from the secure side must allocate itself a secure
context by calling portALLOCATE_SECURE_CONTEXT**.

The task then calls the secure side function and passes the non-secure
callback as the argument. The non-secure counter is incremented in the callback
and the secure counter is incremented in the secure function. Therefore,
both the counters must be incremented after the call to the secure function
is complete - this is ensured using [configASSERT()](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert). The task
sleeps for one second and then repeats the same.

![TrustZone Demo Call Sequence](/media/2019/TZ_Demo.png)

**The TrustZone Demo Call Sequence**

#### Memory Protection Unit (MPU) Demo

The MPU demo demonstrates how to use the MPU to grant a task different access permissions
for various memory regions. The MPU demo consists of the following two tasks:

- RW Task:

The RW task has Read-Write access to a shared region of memory (namely
ucSharedMemory).

- RO Task:

The RO task has Read-Only access to the same shared region of memory
(namely ucSharedMemory). This task tries to write to the
shared memory and since it has read only permission to the shared memory,
it results in a hard fault. The fault handler checks if it is the
expected fault from the RO task and if so, it recovers gracefully by
incrementing the Program Counter to the next statement.

---

### Building and Running the RTOS Demo Application

#### Using IAR Embedded Workbench IDE

1. Download and install the Nu-Link USB Driver:

   - Go to the following page:
     [Nuvoton NuMaker-PFM-M2351](https://www.nuvoton.com/products/iot-solution/iot-platform/numaker-pfm-m2351/?group=Software&tab=2)
   - Click on the Resources tab.
   - Scroll down to the Software section and download the file named Nu-Link_IAR_Driver_Vx.xx.xxxx.
   - Unzip and install.

2. Double click the FreeRTOS/Demo/CORTEX_MPU_M23_Nuvoton_NuMaker_PFM_M2351_IAR_GCC/Projects/IAR/FreeRTOSDemo.eww
   file to open it in the IAR Embedded Workbench IDE. The IAR workspace
   FreeRTOSDemo.eww contains a secure project (FreeRTOSDemo_s)
   and a non-secure project (FreeRTOSDemo_ns).
3. Build the secure project by right clicking "FreeRTOSDemo_s - Release" and then clicking "Make".

[![IAR Embedded Workbench IDE - Build Secure Project](/media/2019/Nuvoton_Numaker_PFM_M2351_IAR_Sec_Proj_Build.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_IAR_Sec_Proj_Build.png)

IAR Embedded Workbench IDE - Build Secure Project. Click to enlarge. 4. Build the non-secure project by right clicking "FreeRTOSDemo_ns - Release" and then clicking "Make".

[![IAR Embedded Workbench IDE - Build Non-Secure Project](/media/2019/Nuvoton_Numaker_PFM_M2351_IAR_NonSec_Proj_Build.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_IAR_NonSec_Proj_Build.png)

IAR Embedded Workbench IDE - Build Non-Secure Project. Click to enlarge. 5. Set the non-secure project as active by right clicking on "FreeRTOSDemo_ns - Release"
and then clicking "Set as Active".

[![IAR Embedded Workbench IDE - Set Non-Secure Project Active](/media/2019/Nuvoton_Numaker_PFM_M2351_IAR_NonSec_Proj_Active.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_IAR_NonSec_Proj_Active.png)

IAR Embedded Workbench IDE - Set Non-Secure Project Active. Click to enlarge. 6. Flash the non-secure binary by clicking "Project --> Download --> Download active application".

[![IAR Embedded Workbench IDE - Flash the Non-Secure Binary](/media/2019/Nuvoton_Numaker_PFM_M2351_IAR_NonSec_Proj_Download.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_IAR_NonSec_Proj_Download.png)

IAR Embedded Workbench IDE - Flash the Non-Secure Binary. Click to enlarge. 7. Set the secure project as active by right clicking on "FreeRTOSDemo_s - Release"
and then clicking "Set as Active".

[![IAR Embedded Workbench IDE - Set Secure Project Active](/media/2019/Nuvoton_Numaker_PFM_M2351_IAR_Sec_Proj_Active.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_IAR_Sec_Proj_Active.png)

IAR Embedded Workbench IDE - Set Secure Project Active. Click to enlarge. 8. Flash the secure binary by clicking "Project --> Download --> Download active application".

[![IAR Embedded Workbench IDE - Flash the Secure Binary](/media/2019/Nuvoton_Numaker_PFM_M2351_IAR_Sec_Proj_Download.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_IAR_Sec_Proj_Download.png)

IAR Embedded Workbench IDE - Flash the Secure Binary. Click to enlarge. 9. Start the Debug Session by clicking "Project --> Download and Debug".

[![IAR Embedded Workbench IDE - Start Debug Session](/media/2019/Nuvoton_Numaker_PFM_M2351_IAR_Debug_Session.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_IAR_Debug_Session.png)

IAR Embedded Workbench IDE - Start Debug Session. Click to enlarge.

#### Using Keil uVision IDE

1. Download and install the Nu-Link Keil Driver:

   - Go to the following page: [Nuvoton NuMaker-PFM-M2351](https://www.nuvoton.com/hq/products/iot-solution/iot-platform/numaker-maker-platform/numaker-pfm-m2351/?__locale=en)
   - Click on the Resources tab.
   - Scroll down to the Software section and download the file named Nu-Link_Keil_Driver_Vx.xx.xxxx.
   - Unzip and install.

2. Double click the FreeRTOS/Demo/CORTEX_MPU_M23_Nuvoton_NuMaker_PFM_M2351_IAR_GCC/Projects/Keil/FreeRTOSDemo.uvmpw
   file to open it in the Keil uVision IDE. The Keil multi-project workspace
   FreeRTOSDemo.uvmpw contains a secure project (FreeRTOSDemo_s)
   and a non-secure project (FreeRTOSDemo_ns).
3. Set the secure project as active by right clicking on "Project: FreeRTOSDemo_s"
   and selecting "Set as Active Project".

[![Keil uVision IDE - Set Secure Project Active](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_Sec_Proj_Active.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_Sec_Proj_Active.png)

Keil uVision IDE - Set Secure Project Active. Click to enlarge. 4. Build the secure project by clicking "Project --> Build 'FreeRTOSDemo_s (FreeRTOSDemo_s)'".

[![Keil uVision IDE - Build Secure Project](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_Sec_Proj_Build.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_Sec_Proj_Build.png)

Keil uVision IDE - Build Secure Project. Click to enlarge. 5. Open the Options Window for the secure project by clicking "Project --> Options for FreeRTOSDemo_s - Target 'FreeRTOSDemo_s'...".

[![Keil uVision IDE - Open Secure Project Options](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_Sec_Proj_Options.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_Sec_Proj_Options.png)

Keil uVision IDE - Open Secure Project Options. Click to enlarge. 6. Open the Nu-Link Driver Setup Window by clicking "Settings" button next to the "Nuvoton Nu-Link Debugger" in the Debug tab.

[![Keil uVision IDE - Open Nu-Link Driver Setup](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_Sec_Proj_Debugger_1.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_Sec_Proj_Debugger_1.png)

Keil uVision IDE - Open Nu-Link Driver Setup. Click to enlarge. 7. Select "M2351" in the "Chip Type" dropdown.

[![Keil uVision IDE - Select M2351](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_Sec_Proj_Debugger_2.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_Sec_Proj_Debugger_2.png)

Keil uVision IDE - Select M2351. Click to enlarge. 8. Dismiss "Nu-Link Driver Setup" and "Options" Windows by clicking "OK" on both the windows. 9. Set the non-secure project as active by right clicking on "Project: FreeRTOSDemo_ns"
and selecting "Set as Active Project".

[![Keil uVision IDE - Set Non-Secure Project Active](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_NonSec_Proj_Active.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_NonSec_Proj_Active.png)

Keil uVision IDE - Set Non-Secure Project Active. Click to enlarge. 10. Build the non-secure project by clicking "Project --> Build 'FreeRTOSDemo_ns (FreeRTOSDemo_ns)'".

[![Keil uVision IDE - Build Non-Secure Project](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_NonSec_Proj_Build.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_NonSec_Proj_Build.png)

Keil uVision IDE - Build Non-Secure Project. Click to enlarge. 11. Open the Options Window for the non-secure project by clicking "Project --> Options for FreeRTOSDemo_ns - Target 'FreeRTOSDemo_ns'...".

[![Keil uVision IDE - Open Non-Secure Project Options](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_NonSec_Proj_Options.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_NonSec_Proj_Options.png)

Keil uVision IDE - Open Non-Secure Project Options. Click to enlarge. 12. Open the Nu-Link Driver Setup Window by clicking "Settings" button next to the "Nuvoton Nu-Link Debugger" in the Debug tab.

[![Keil uVision IDE - Open Nu-Link Driver Setup](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_NonSec_Proj_Debugger_1.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_NonSec_Proj_Debugger_1.png)

Keil uVision IDE - Open Nu-Link Driver Setup. Click to enlarge. 13. Select "M2351" in the "Chip Type" dropdown.

[![Keil uVision IDE - Select M2351](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_NonSec_Proj_Debugger_2.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_NonSec_Proj_Debugger_2.png)

Keil uVision IDE - Select M2351. Click to enlarge. 14. Dismiss "Nu-Link Driver Setup" and "Options" Windows by clicking "OK" on both the windows. 15. Flash the non-secure binary by clicking "Flash --> Download".

[![Keil uVision IDE - Flash the Non-Secure Binary](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_NonSec_Proj_Download.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_NonSec_Proj_Download.png)

Keil uVision IDE - Flash the Non-Secure Binary. Click to enlarge. 16. Set the secure project as active by right clicking on "Project: FreeRTOSDemo_s"
and selecting "Set as Active Project".

[![Keil uVision IDE - Set Secure Project Active](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_Sec_Proj_Active.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_Sec_Proj_Active.png)

Keil uVision IDE - Set Secure Project Active. Click to enlarge. 17. Flash the secure binary by clicking "Flash --> Download".

[![Keil uVision IDE - Flash the Secure Binary](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_Sec_Proj_Download.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_Sec_Proj_Download.png)

Keil uVision IDE - Flash the Secure Binary. Click to enlarge. 18. Start the Debug Session by clicking "Debug --> Start/Stop Debug Session".

[![Keil uVision IDE - Start Debug Session](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_Debug_Session.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_Debug_Session.png)

Keil uVision IDE - Start Debug Session. Click to enlarge.

---

### RTOS Configuration and Usage Details

Also see the page that [describes running
FreeRTOS on ARMv8-M cores](/Community/Blogs/2020/using-freertos-on-armv8-m-microcontrollers), and the page that describes [setting
ARM Cortex-M interrupt priorities for use with FreeRTOS](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4).

- Configuration items specific to this demo are contained in
  FreeRTOS/Demo/CORTEX_MPU_M23_Nuvoton_NuMaker_PFM_M2351_IAR_GCC/Projects/Keil/ConfigFreeRTOSConfig.h
  for the Keil uVision IDE project and in
  FreeRTOS/Demo/CORTEX_MPU_M23_Nuvoton_NuMaker_PFM_M2351_IAR_GCC/Projects/IAR/ConfigFreeRTOSConfig.h
  for the IAR Embedded Workbench IDE project. The [constants defined in that file](/Documentation/02-Kernel/03-Supported-devices/02-Customization)
  can be edited to suit your application. The following configuration
  options are specific to the ARM Cortex-M23 port:

  - configENABLE_MPU - Enable/Disable Memory Protection Unit (MPU).
  - configENABLE_TRUSTZONE - Enable/Disable TrustZone.

- If you want to run FreeRTOS with TrustZone disabled, set configENABLE_TRUSTZONE
  to 0 in your FreeRTOSConfig.h and use the FreeRTOS port files
  in the FreeRTOS/Source/portable/GCC/ARM_CM23_NTZ directory
  for GCC and in the FreeRTOS/Source/portable/IAR/ARM_CM23_NTZ
  directory for IAR.
- If you want to run FreeRTOS on the secure side, set configENABLE_TRUSTZONE
  to 0 and configRUN_FREERTOS_SECURE_ONLY to 1 in your FreeRTOSConfig.h
  and use the FreeRTOS port files in the FreeRTOS/Source/portable/GCC/ARM_CM23_NTZ
  directory for GCC and in the FreeRTOS/Source/portable/IAR/ARM_CM23_NTZ
  directory for IAR.
- Source/Portable/MemMang/heap_4.c is included in the project
  to provide the memory allocation required by the RTOS kernel. Please
  refer to the [Memory Management](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) section of
  the API documentation for full information.
- vPortEndScheduler() has not been implemented.
