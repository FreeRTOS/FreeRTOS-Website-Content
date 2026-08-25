---
title: Using FreeRTOS on ARMv8-M Microcontrollers
created: 2020-04-06
feature: blog
categories:
  - Long term support
authors:
  - aggarg
relatedLinks:
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
---

by [Gaurav Aggarwal](../author/aggarg) on 06 Apr 2020

[Also see the page that describes [how to set ARM Cortex-M interrupt priorities when using FreeRTOS](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4).]

ARM introduced TrustZone to the Cortex-M series of microcontrollers with the ARMv8-M architecture. TrustZone
is an optional security extension that enables two security domains within a single processor. Cortex-M
cores (including the Cortex-M33 and Cortex-M23) that include TrustZone use it to divide the execution
space into secure ('s') and non-secure ('ns') partitions (or 'sides'). This enhances security by enabling
complete isolation between trusted software executing on the secure side and untrusted software executing
on the non-secure side. Both the secure and non-secure sides have separate Memory Protection Units (MPUs)
that enable additional isolation within both security domains.

The software running on the secure side can export functions it wants to make available to the software
running on the non-secure side. These functions must be placed in a memory region explicitly marked as
Non-Secure Callable (NSC). The non-secure software can only access secure software through these exported
functions in the NSC memory.

The ARMv8-M architecture also introduced stack limit registers that enable the application software
to catch a stack overflow as soon as it happens.

The following subsections describe the run-time and configuration options available when
running FreeRTOS on ARMv8-M cores:
* [The Anatomy of an ARMv8-M Application](#the-anatomy-of-an-armv8-m-application)
* [Features of the FreeRTOS ARMv8-M Ports](#features-of-the-freertos-armv8-m-ports)
* [Quick Start](#quick-start)
* [FreeRTOS ARMv8-M Ports Usage Instructions](#freertos-armv8-m-ports-usage-instructions)
	+ [Using FreeRTOS with TrustZone Support](#using-freertos-with-trustzone-support)
	+ [Using FreeRTOS without TrustZone Support](#using-freertos-without-trustzone-support)
	+ [Using FreeRTOS with Memory Protection Unit (MPU) Support](#using-freertos-with-memory-protection-unit-mpu-support)
	+ [Using FreeRTOS with Floating Point Unit (FPU) support](#using-freertos-with-floating-point-unit-fpu-support)
* [Contributing to FreeRTOS ARMv8-M ports](#contributing-to-freertos-armv8-m-ports)

---

<span id="APPLICATION_STRUCTURE"/>

## The Anatomy of an ARMv8-M Application

Applications that make use of TrustZone consist of two separate projects:

1. A secure application that runs on the secure side.
2. A non-secure application that runs on the non-secure side.

ARMv8-M cores always boot up to the secure side. It is then the responsibility of the secure software
to program the Security Attribution Unit (SAU) and the Implementation Defined Attribution Unit (IDAU)
to divide the memory space into secure and non-secure areas before branching to the non-secure software.
The software on the secure side can access both secure and non-secure memories while the software on
the non-secure side can only access non-secure memories.

Typically the software executing on the secure side needs to be robust and trusted, so it is kept as
small as possible - often limited to providing the system's root of trust (secure boot, identity, cryptographic
functions, etc.). The Memory Protection Unit (MPU) on the non-secure side is then used to run non-secure
tasks at lower privilege  level, and provide fine grained access controls to memory and peripherals on
a thread (RTOS task) by thread basis.


<span id="FREERTOS_V8M_FEATURES" />

## Features of the FreeRTOS ARMv8-M Ports

The FreeRTOS ARMv8-M (ARM Cortex-M33 and ARM Cortex-M23) ports:
* Can run on either the secure or non-secure side.
* Allow non-secure tasks (or threads) to call secure-side trusted functions (via the designated entry
  points in the NSC memory) that, in turn, can call back to non-secure functions, all without breaching
  the kernel's prioritized scheduling policy.
* Have optional support for TrustZone (when the FreeRTOS kernel runs on the non-secure side).
* Have optional support for the Memory Protection Unit (MPU).
* Have optional support for the Floating Point Unit (FPU).
* Only allow privilege escalations that originate from within the FreeRTOS kernel code.

In the most common scenario, the FreeRTOS scheduler runs on the non-secure side, and each non-secure
FreeRTOS task can call functions exported by the secure side software. This enables application developers
to put critical software on the secure side, and ensures that a bug in the non-secure software does
not affect critical secure software.

Using the MPU allows tasks on the non-secure side to have lower privilege level, to be isolated from
each other, and to be isolated from the kernel.


<span id="QUICK_START"/>

## Quick Start

The main body of this page provides detailed information on building FreeRTOS for ARMv8-M microcontrollers,
but the simplest way to get started is to use one of the following pre-configured example projects:

* [Keil Simulator using Keil uVision IDE](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Arm-Virtual-Hardware/RTOS-Cortex-M33-Keil-Simulator)
* [NXP LPCXpresso55S69 Development Board using MCUXpresso IDE](/Documentation/02-Kernel/03-Supported-devices/04-Demos/NXP/RTOS-Cortex-M33-LPC55S69-MCUXpresso-GCC)
* [Nuvoton NuMaker-PFM-M2351 Board using Keil uVision and IAR IDEs](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Nuvoton/RTOS-Cortex-M23-NuMaker-PFM-M2351-Keil)

The example ARMv8-M projects are located in sub-directories of FreeRTOS/Demo in the
main [FreeRTOS zip file download](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS). These projects can be used directly, or simply as a
worked example and reference for the source files, configuration options, and compiler settings detailed
below.

---

<span id="FREERTOS_ARMv8M_PORTS" />

## FreeRTOS ARMv8-M Ports Usage Instructions

FreeRTOS ARMv8-M ports use the following compile time macros to enable or disable TrustZone, Memory
Protection Unit (MPU) and Floating Point Unit (FPU) support. The following sections of this page elaborate
on their use.

```c
    /* Set to 1 when running FreeRTOS on the non-secure side to enable the
     * ability to call the (non-secure callable) functions exported from secure side. */
    #define configENABLE_TRUSTZONE 1

    /* Set to 1 when running FreeRTOS on the secure side. Note that in this case TrustZone is
     * not supported as secure tasks cannot call non-secure code i.e. configENABLE_TRUSTZONE
     * must be set to 0 when setting configRUN_FREERTOS_SECURE_ONLY to 1. */
    #define configRUN_FREERTOS_SECURE_ONLY 1

    /* Set to 1 to enable the Memory Protection Unit (MPU), or 0 to leave the Memory
     * Protection Unit disabled. */
    #define configENABLE_MPU 1

    /* Set to 1 to enable the Floating Point Unit (FPU), or 0 to leave the Floating
     * Point Unit disabled. */
    #define configENABLE_FPU 1

    /* Set to 1 to enable the M-Profile Vector Extension (MVE) support, or 0 to
     * leave the MVE support disabled. This option is only applicable to Cortex-M55
     * and Cortex-M85 ports as M-Profile Vector Extension (MVE) is available only on
     * these architectures. configENABLE_MVE must be left undefined, or defined to 0
     * for the Cortex-M23 Cortex-M33 and Cortex-M35P ports. */
    #define configENABLE_MVE 1
```
*Enabling Support for Various Features in FreeRTOS ARMv8-M Ports*

---

<span id="FREERTOS_WITH_TRUSTZONE" />

## Using FreeRTOS with TrustZone Support

### Description

When FreeRTOS is running on the non-secure side, the TrustZone support in FreeRTOS ARMv8-M ports enable
the non-secure FreeRTOS tasks to call the secure functions that have been marked as non-secure callable (NSC).
Secure functions are functions implemented on the secure side.


### FreeRTOSConfig.h settings

To enable TrustZone support build FreeRTOS with `configENABLE_TRUSTZONE` set to one
in [FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization):

```c
#define configENABLE_TRUSTZONE 1
```
*Enabling TrustZone support in FreeRTOS*

Tasks that call secure functions from the non-secure side of an ARMv8-M MCU (ARM Cortex-M23 and Cortex-M33)
have two contexts – one on the non-secure side and one on the secure-side. Before FreeRTOS v10.4.5,
ARMv8-M secure-side ports allocated the structures that reference secure-side contexts at run time.
From FreeRTOS V10.4.5 the structures are allocated statically at compile time. `secureconfigMAX_SECURE_CONTEXTS`
sets the number of statically allocated secure contexts. `secureconfigMAX_SECURE_CONTEXTS` defaults
to 8 if left undefined. Applications that only use FreeRTOS code on the non-secure side of ARMv8-M
microcontrollers, such as those running third-party code on the secure-side, do not require this constant.

```c
#define secureconfigMAX_SECURE_CONTEXTS 8
```
*Defining Maximum Number of Secure Contexts*


### Building the port

The [FreeRTOS kernel source code organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) page contains information on adding the
FreeRTOS kernel to your project. **In addition to the information on that page**, the FreeRTOS ARMv8-M
ports with TrustZone support require additional port files to be compiled in the secure project and
the non-secure project.

* *Source files to be compiled in the secure project*: FreeRTOS/Source/portable/[compiler]/[architecture]/secure
* *Source files to be compiled in the non-secure project*: FreeRTOS/Source/portable/[compiler]/[architecture]/non\_secure

Where [architecture] is either ARM\_CM23 or ARM\_CM33, depending on whether the target hardware is an
ARM Cortex-M23 or an ARM Cortex-M33.

**Note 1:**The GCC port can also be used with the ARM compiler version 6 and above (ARM Clang).

**Note 2:**The above two directories must also be included in the include path of the respective compiler projects.


### Defining secure functions as non-secure callable (NSC)

Use the `secureportNON_SECURE_CALLABLE` macro to make a secure function callable from the non-secure side.

```c
secureportNON_SECURE_CALLABLE void NSCFunction( void );
```
*Example use of the secureportNON\_SECURE\_CALLABLE macro to make the secure side function NSCFunction()
callable from a non-secure task*

The linker script for the secure project then needs to make sure that the non-secure callable functions
are placed in a memory region that is explicitly marked as Non-Secure Callable. The following is the
GCC syntax for placing non-secure callable functions in the NSC memory:

```c
MEMORY
{
    /* Define each memory region. */
    PROGRAM_FLASH (rx)  : ORIGIN = 0x10000000, LENGTH = 0xfe00
    veneer_table (rx)   : ORIGIN = 0x1000fe00, LENGTH = 0x200
    Ram0 (rwx)          : ORIGIN = 0x30000000, LENGTH = 0x8000
}

/* Veneer Table Section (Non-Secure Callable). */

.text_Flash2 : ALIGN(4)

{
    FILL(0xff)
    *(.text_veneer_table*)
    *(.text.$veneer_table*)
    *(.rodata.$veneer_table*)
} > veneer_table
```
*GCC syntax for placing Non-Secure Callable functions in the NSC memory*

The pre-configured examples projects in the main FreeRTOS distribution contain examples for various
other compilers.


### Allocating a secure context for a non-secure task

Any non-secure FreeRTOS task that wants to call a secure side function must first allocate a secure
context by calling the `portALLOCATE_SECURE_CONTEXT` macro:

```c
/* This task calls secure side functions. So allocate a secure
 * context for it. */
portALLOCATE_SECURE_CONTEXT( configMINIMAL_SECURE_STACK_SIZE );
```
*Allocating a Secure context for a Non-Secure task*

It is recommended for non-secure tasks that make secure calls to allocate a
secure context as their first action.

---

<span id="FREERTOS_WITHOUT_TRUSTZONE" />

### Using FreeRTOS without TrustZone Support

#### Description

The application writer can choose to disable TrustZone in hardware. When that is done the microcontroller
boots as non-secure, and the entire memory space is non-secure.


#### FreeRTOSConfig.h setting to run FreeRTOS on the non-secure side without TrustZone support

To disable TrustZone support build FreeRTOS with configENABLE\_TRUSTZONE set to zero
in [FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization) file:

```c
#define configENABLE_TRUSTZONE 0
```
*Disabling TrustZone support in FreeRTOS*


### FreeRTOSConfig.h setting to run FreeRTOS on the secure side without TrustZone support

If the application writer does not want to use TrustZone but the hardware does not support disabling
TrustZone then the entire application (including the FreeRTOS scheduler) can run on the secure side
without ever branching to the non-secure side. To do that, in addition to setting configENABLE\_TRUSTZONE
to 0, also set `configRUN_FREERTOS_SECURE_ONLY` to 1.

```c
#define configENABLE_TRUSTZONE 0

#define configRUN_FREERTOS_SECURE_ONLY 1
```
*Running FreeRTOS on the Secure side only*


### Building the port

The [FreeRTOS kernel source code organization](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization) page contains information on adding the
FreeRTOS kernel to your project. The port files for the FreeRTOS ARMv8-M ports without TrustZone support
are in the following directory: FreeRTOS/Source/portable/[compiler]/[architecture]/non\_secure

Where [architecture] is either ARM\_CM23\_NTZ or ARM\_CM33\_NTZ depending on whether the target hardware
is an ARM Cortex-M23 or an ARM Cortex-M33.

**Note 1:**The GCC port can also be used with the ARM compiler version 6 and above (ARM Clang).

**Note 2:**The above directory must also be included in the include path of the respective compiler project.

---

<span id="FREERTOS_WITH_MPU"></span>

## Using FreeRTOS with Memory Protection Unit (MPU) Support

### Description

Memory Protection Unit (MPU) support in FreeRTOS ARMv8-M ports enables application tasks to execute
in a privileged or unprivileged (user) mode, and provides fine grained memory and peripheral access
control on a task by task basis.

Unprivileged tasks:

1. Are created using the [xTaskCreateRestricted()](/Documentation/02-Kernel/04-API-references/13-FreeRTOS-MPU-specific/01-xTaskCreateRestricted) API.
2. Default to having no RAM access other than to their own stacks.
3. Cannot execute code marked by the MPU as privileged access only.
4. Can optionally be assigned access up to three additional memory regions, which can be changed at
   run-time.

A memory fault is triggered any time an unprivileged task tries to access any memory region for which
it has not been granted access. The fault handler gives the application writer a chance to take an
appropriate action, which may be terminating the offending task.

Do not confuse the privilege level of a task with the security domain it executes in. The secure and
non-secure sides of an ARMv8-M core each have their own MPU - so it is possible to have both privileged
and unprivileged execution on both the secure and non-secure sides.

To reduce security risks, and to reduce the impact of software bugs, it is recommended for application
code to be unprivileged whenever possible. A change from unprivileged execution to privileged execution
is called a privilege escalation. Software initiated privilege  escalations can only occur from within
the FreeRTOS kernel's API functions, but privilege escalations also occur each time the hardware accepts
an interrupt. If you do not want application provided interrupt service routines (ISRs) to run as privileged
then install subs for each interrupt routine that either reduce the privilege level before calling an
application provided handler function, or
otherwise [defer the execution of an application provided handler function to a task](/Documentation/02-Kernel/02-Kernel-features/11-Deferred-interrupt-handling)
 (such functionality must be provided by the application writer).


### MPU Hardware Restrictions

The ARMv8-M MPU is much more flexible than the ARMv7-M MPU, with only the following restrictions on
the definition of memory regions:

* The smallest size that can be programmed for an MPU region is 32 bytes.
* The maximum size of any MPU region is 4GB.
* The size of an MPU region must be a multiple of 32 bytes.
* All MPU regions must begin on a 32 byte aligned address.


### FreeRTOSConfig.h settings

To enable MPU support, build FreeRTOS with configENABLE\_MPU set
to one in [FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization) file:

```c
#define configENABLE_MPU 1
```
*Enabling Memory Protection Unit (MPU) support in FreeRTOS*


### Building the port

If the application uses TrustZone support, build FreeRTOS source files as mentioned in
the [Using FreeRTOS with TrustZone Support](#using-freertos-with-trustzone-support) section. If the application does
not use TrustZone support, build FreeRTOS source files as mentioned in
the [Using FreeRTOS without TrustZone Support](#using-freertos-without-trustzone-support) section. **In addition,**
build the following file in the non-secure project: FreeRTOS/Source/portable/Common/mpu\_wrappers.c.


### Allocating stack for an unprivileged task

The MPU support in ARMv8-M ports uses an MPU region to grant an unprivileged task access to its stack.
Therefore, the application writer must ensure that the stack buffer supplied to
the [xTaskCreateRestricted()](/Documentation/02-Kernel/04-API-references/13-FreeRTOS-MPU-specific/01-xTaskCreateRestricted) API, satisfies
the [MPU hardware restrictions](#mpu-hardware-restrictions). The following is the GCC syntax for placing
the stack buffer on a 32 byte boundary:

```c
StackType_t xTaskStackBuffer[ configMINIMAL_STACK_SIZE ] __attribute__( ( aligned( 32 ) ) );
```
*GCC syntax for placing a buffer on 32 byte boundary*


### Granting access to additional memory regions to an unprivileged task

An unprivileged task can be granted access to up to three additional memory regions at the time of the
task creation. Three MPU regions are used to grant access to these memory regions and therefore, these
memory regions must satisfy the [MPU hardware restrictions](#mpu-hardware-restrictions). The following
is an example of creating an unprivileged task which is granted Read Only access to the ucSharedMemory:

```c
static uint8_t ucSharedMemory[ SHARED_MEMORY_SIZE ] __attribute__( ( aligned( 32 ) ) );

void vStartMPUDemo( void )
{
    static StackType_t xROAccessTaskStack[ configMINIMAL_STACK_SIZE ] __attribute__( ( aligned( 32 ) ) );
    TaskParameters_t xROAccessTaskParameters =
    {
        .pvTaskCode     = prvROAccessTask,
        .pcName         = "ROAccess",
        .usStackDepth   = configMINIMAL_STACK_SIZE,
        .pvParameters   = NULL,
        .uxPriority     = tskIDLE_PRIORITY,
        .puxStackBuffer = xROAccessTaskStack,
        .xRegions       =   {
                            { ucSharedMemory, 32, tskMPU_REGION_READ_ONLY | tskMPU_REGION_EXECUTE_NEVER },
                            { 0,              0,  0                                                     },
                            { 0,              0,  0                                                     },
                        }
    };

    /* Create an unprivileged task with RO access to ucSharedMemory. */
    xTaskCreateRestricted( &( xROAccessTaskParameters ), NULL );
}
```
*Creating an unprivileged task*

Note that the code ensures that both `ucSharedMemory` and `xROAccessTaskStack`
satisfy [MPU hardware restrictions](#mpu-hardware-restrictions).


### Memory layout

The memory layout of an application with MPU support looks like the following:

![](/media/2021/MemoryLayout.jpg)
*Memory layout of an Application with MPU Support*

**Kernel Code** - The kernel code section contains the FreeRTOS kernel executable code, and is only
accessible to privileged software. Unprivileged software needs to go through a kernel system
call (see below) to access functionalities provided by the FreeRTOS kernel. All FreeRTOS kernel functions
are placed in a named linker section  privileged\_functions, and the linker script needs to place them
in a separate flash section.

An MPU region is used to ensure only privileged software can access the FreeRTOS kernel code and therefore,
the linker script must ensure the flash section containing the FreeRTOS kernel code satisfies
the [MPU hardware restrictions](#mpu-hardware-restrictions). In addition, the linker script needs to
export two variables, namely \_\_privileged\_functions\_start\_\_ and \_\_privileged\_functions\_end\_\_,
indicating the start and end of the FreeRTOS kernel code which are used by the FreeRTOS kernel to program
the MPU.

The following is the GCC syntax for placing FreeRTOS kernel code in a separate section:

```c
/* Privileged functions - Section needs to be 32 byte aligned to satisfy
 * MPU requirements. */
.privileged_functions : ALIGN(32)
{
    . = ALIGN(32);
    __privileged_functions_start__ = .;
    *(privileged_functions)
    . = ALIGN(32);
    /* End address must be the last address in the region, therefore, -1. */
    __privileged_functions_end__ = . - 1;
} > PROGRAM_FLASH
```
*GCC syntax for placing FreeRTOS kernel code in a separate section*

The pre-configured examples projects in the main FreeRTOS distribution contain examples for various
other compilers.

**System Calls** - The system calls section contains all the FreeRTOS system calls. A system call is
a way for an unprivileged task to access FreeRTOS APIs which otherwise are only available to the privileged
software. When an unprivileged task calls a FreeRTOS API, it goes through a system call which temporarily
raises the privilege of the calling task, then executes the requested API and resets the privilege back
before returning to the caller. All the FreeRTOS system calls are placed in a named linker section
freertos\_system\_calls and the linker script needs to place them in a separate flash section.

An MPU region is used to ensure that both privileged and unprivileged software can access system calls.
Therefore the linker script must ensure that the flash section containing the system calls satisfies
the [MPU hardware restrictions](#mpu-hardware-restrictions). In addition, the linker script needs to
export two variables, namely \_\_syscalls\_flash\_start\_\_ and \_\_syscalls\_flash\_end\_\_, indicating
the start and end of the FreeRTOS system calls which are used by the FreeRTOS kernel to program the
MPU. These variables are also used to ensure that the unprivileged software cannot escalate its privilege
arbitrarily and that privilege escalations are limited to within the FreeRTOS kernel only.

The following is the GCC syntax for placing FreeRTOS system calls in a separate section:

```c
/* FreeRTOS System calls - Section needs to be 32 byte aligned to satisfy
 * MPU requirements. */
.freertos_system_calls : ALIGN(32)
{
    . = ALIGN(32);
    __syscalls_flash_start__ = .;
    *(freertos_system_calls)
    . = ALIGN(32);
    /* End address must be the last address in the region, therefore, -1. */
    __syscalls_flash_end__ = . - 1;
} > PROGRAM_FLASH
```
*GCC syntax for placing FreeRTOS system calls in a separate section*

The pre-configured examples projects in the main FreeRTOS distribution contain examples for various
other compilers.

**Kernel Data** - The kernel data (RAM) section contains all the FreeRTOS kernel data and is only accessible
to privileged software. All the FreeRTOS kernel data is placed in a named linker section privileged\_data
and the linker script needs to place them in a separate RAM section.

An MPU region is used to ensure that only privileged software can access the FreeRTOS kernel data and
therefore the linker script must ensure that the RAM section containing the FreeRTOS kernel data satisfies
the [MPU hardware restrictions](#mpu-hardware-restrictions). In addition, the linker script needs to
export two variables, namely \_\_privileged\_sram\_start\_\_ and \_\_privileged\_sram\_end\_\_, indicating
the start and end of the FreeRTOS kernel data which are used by the FreeRTOS kernel to program the MPU.

The following is the GCC syntax for placing FreeRTOS kernel data in a separate section:

```c
/* Main Data section (Ram0). */
.data : ALIGN(4)
{
    /* Privileged data - It needs to be 32 byte aligned to satisfy
     * MPU requirements. */
    . = ALIGN(32);
    __privileged_sram_start__ = .;
    *(privileged_data);
    . = ALIGN(32);
    /* End address must be the last address in the region, therefore, -1. */
    __privileged_sram_end__ = . - 1;
} > Ram0 AT>PROGRAM_FLASH
```
*GCC syntax for placing FreeRTOS kernel data in a separate section*

The pre-configured examples projects in the main FreeRTOS distribution contain examples for various other compilers.

---

<span id="FREERTOS_WITH_FPU"></span>

## Using FreeRTOS with Floating Point Unit (FPU) Support

### Description

If the target microcontroller includes a floating point unit (FPU), and you pass options to your compiler
telling it to generate floating point instructions (as opposed to using emulated floating point operations),
then the FPU support must be enabled.


### FreeRTOSConfig.h settings

To enable FPU support build FreeRTOS with `configENABLE_FPU` set to one
in [FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization) file:

```c
#define configENABLE_FPU 1
```
*Enabling Floating Point Unit (FPU) support in FreeRTOS*


### Building the port

If the application uses TrustZone support, build FreeRTOS source files as mentioned in
the [Using FreeRTOS with TrustZone Support](#using-freertos-with-trustzone-support) section. If the application does
not use TrustZone support, build FreeRTOS source files as mentioned in
the [Using FreeRTOS without TrustZone Support](#using-freertos-without-trustzone-support) section.

---

<span id="CONTRIBUTION"></span>

## Contributing to FreeRTOS ARMv8-M ports

The FreeRTOS ARMv8-M ports are organized as follows:

* **Master Copy** - Maintained at FreeRTOS/Source/portable/ARMv8M.
* **Replicas** - The master copy is replicated in several [compiler]/[architecture] directories to ensure
  that the users can easily find the port files required for their compiler and architecture combination.

If you want to contribute to FreeRTOS ARMv8-M ports, please make your changes to the master copy and
replicate them using the script FreeRTOS/Source/portable/ARMv8M/copy\_files.py.

## About the author

![](https://secure.gravatar.com/avatar/ec2b9cace8c52148e35991ba7595c481?s=200&d=mm&r=g)
Gaurav Aggarwal is a FreeRTOS kernel and embedded connectivity specialist within the IoT edge devices
team at Amazon Web Services. He was instrumental in bringing both the ARM Cortex-M33 and Cortex-M23
FreeRTOS kernel ports to market, and now supports their use while also maintaining an active role in
the development and enhancement of the FreeRTOS library portfolio.
[View articles by this author](../author/aggarg)


FreeRTOS forums: Get industry-leading support from experts and collaborate with peers around the
globe. [View Forums](https://forums.freertos.org/)
