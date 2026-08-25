---
title: Memory Protection Unit (MPU) Support
date: Jan.2022
---

[**See the Upgrading section for information on updating FreeRTOS-MPU projects to FreeRTOS V10.6.2**](#upgrade-information)

<span id="introduction"></span>
## Introduction

FreeRTOS provides official Memory Protection Unit (MPU) support on
ARMv7-M (Cortex-M3, Cortex-M4 and Cortex-M7 microcontrollers) and
ARMv8-M (Cortex-M23 and Cortex-M33 microcontroller) cores:

- There are two FreeRTOS ports for ARMv7-M cores, one that includes
  MPU support and one that doesn't.
- There is only one FreeRTOS port for ARMv8-M cores
  as [MPU support is a compile time option](/Community/Blogs/2020/using-freertos-on-armv8-m-microcontrollers).

Third parties maintain MPU ports to other microcontroller cores.


<span id="mpu_benefits"></span>
#### MPU costs and benefits

FreeRTOS MPU ports enable microcontroller applications to be more robust
and more secure by: first, enabling tasks to run in either privileged or
unprivileged mode; and second by restricting access to resources such as
RAM, executable code, peripherals, and memory beyond the limit of a
task's stack. Huge benefit is gained from, for example, preventing code
from ever executing from RAM. Doing so will protect against many attack
vectors such as buffer overflow exploits or the execution of malicious
code loaded into RAM.

Use of an MPU necessarily makes application design more complex because:
first the MPU's memory region restrictions must be determined and
described to the RTOS; and second the MPU restricts what application
tasks can and cannot do.


<span id="mpu_strategies"></span>
#### MPU strategies

Creating an application that constrains every task to its own memory
region may be the most secure, but it is also the most complex to design
and implement. Often it is best to use an MPU to create a pseudo process
and thread model - where groups of threads are allowed to share a memory
space. For example, create one memory space accessible to trusted first
party code, and another that is only accessible to untrusted third party
code.


<span id="mpu_examples"></span>
#### Additional examples

The LPC17xx edition of the FreeRTOS eBook [contains a chapter on using FreeRTOS-MPU](/media/MPU_Chapter.pdf),
although the information it contains is
a little out of date.

The [Using FreeRTOS on ARMv8-M Microcontrollers](/Community/Blogs/2020/using-freertos-on-armv8-m-microcontrollers)
blog mentions how to use MPU on ARMv8-M microcontrollers.

The demo project in the `FreeRTOS/Demo/CORTEX_MPU_Simulator_Keil_GCC`
directory, which uses Keil uVision to build and simulate a GCC project,
provides a worked example that does not require any particular hardware.
Additional FreeRTOS-MPU examples projects include the [Nuvoton NuMaker-PFM-M2351 demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Nuvoton/RTOS-Cortex-M23-NuMaker-PFM-M2351-Keil)
and the [NXP LPCXpresso55S69 demo](/Documentation/02-Kernel/03-Supported-devices/04-Demos/NXP/RTOS-Cortex-M33-LPC55S69-MCUXpresso-GCC), among others.

\[The FreeRTOS-MPU demo projects located in the FreeRTOS/Demo/CORTEX\_MPU\_LPC1768\_GCC\_RedSuite and
FreeRTOS/Demo/CORTEX\_MPU\_LM3Sxxxx\_Rowley directories were retired
prior to the release of FreeRTOS V9.0.0\]


<span id="upgrade-information"></span>
#### Upgrade Information

FreeRTOS MPU ports have been updated in response to end-user feedback.
This section describes the changes necessary to upgrade to FreeRTOS
V10.6.2 or newer, and prior to that, to upgrade to FreeRTOS V10.6.1,
V10.6.0, V10.5.0, V10.4.6, V10.4.0, and V10.3.0 or newer.

**Changes in FreeRTOS version 10.6.2:**

FreeRTOS V10.6.2 makes the following improvements to the new MPU wrapper
(mpu\_wrappers\_v2.c) introduced in version 10.6.0:

- Introduce an Access Control List (ACL) feature to allow the
  application writer to control an unprivileged task’s access to
  kernel objects.
- Update the system call entry mechanism to only require one
  Supervisor Call (SVC) instruction.
- Wrap parameters for system calls with more than four parameters in a
  struct to avoid special handling during system call entry.
- Fix 2 possible integer overflows.
- Convert some asserts to run time checks.


**Changes in FreeRTOS version 10.6.1:**

FreeRTOS V10.6.1 introduces runtime parameter checks to functions in the
mpu\_wrappers\_v2.c file. The same checks are already performed in API
implementations using asserts.

We thank the following people for their inputs in these changes:

1.  Lan Luo, Zixia Liu of School of Computer Science and Technology,
    Anhui University of Technology, China.
2.  Xinwen Fu of Department of Computer Science, University of
    Massachusetts Lowell, USA.
3.  Xinhui Shao, Yumeng Wei, Huaiyu Yan, Zhen Ling of School of Computer
    Science and Engineering, Southeast University, China.


**Changes in FreeRTOS version 10.6.0:**

FreeRTOS V10.6.0 introduces a new MPU wrapper that places additional
restrictions on unprivileged tasks. The following is the list of changes
introduced with the new MPU wrapper:

- Opaque and indirectly verifiable integers for kernel object handles:
  All the kernel object handles (for example, queue handles) are now
  opaque integers. Previously object handles were raw pointers.

- The task context is saved in the Task Control Block (TCB): When a
  task is swapped out by the scheduler, the task's context is now
  saved in its TCB. Previously the task’s context was saved on its
  stack.

- System calls execute on a separate, privileged only stack: FreeRTOS
  system calls, which execute with elevated privilege, now use a
  separate, privileged only stack. Previously system calls used the
  calling task's stack.

- Memory bounds checks: FreeRTOS system calls which accept a pointer
  and de-reference it, now verify that the calling task has required
  permissions to access the memory location referenced by the pointer.

- System calls restrictions: The following system calls are no longer
  available to unprivileged tasks:

  - vQueueDelete
  - xQueueCreateMutex
  - xQueueCreateMutexStatic
  - xQueueCreateCountingSemaphore
  - xQueueCreateCountingSemaphoreStatic
  - xQueueGenericCreate
  - xQueueGenericCreateStatic
  - xQueueCreateSet
  - xQueueRemoveFromSet
  - xQueueGenericReset
  - xTaskCreate
  - xTaskCreateStatic
  - vTaskDelete
  - vTaskPrioritySet
  - vTaskSuspendAll
  - xTaskResumeAll
  - xTaskGetHandle
  - xTaskCallApplicationTaskHook
  - vTaskList
  - vTaskGetRunTimeStats
  - xTaskCatchUpTicks
  - xEventGroupCreate
  - xEventGroupCreateStatic
  - vEventGroupDelete
  - xStreamBufferGenericCreate
  - xStreamBufferGenericCreateStatic
  - vStreamBufferDelete
  - xStreamBufferReset

  Also, an unprivileged task can no longer use vTaskSuspend to suspend
  any task other than itself.

We thank the following people for their inputs in these enhancements:

- David Reiss of Meta Platforms, Inc.
- Lan Luo, Xinhui Shao, Yumeng Wei, Zixia Liu, Huaiyu Yan, and Zhen
  Ling of the School of Computer Science and Engineering, Southeast
  University, China.
- Xinwen Fu of the Department of Computer Science, University of
  Massachusetts Lowell, USA.
- Yueqi Chen, Zicheng Wang, Minghao Lin, and Jiahe Wang of the
  University of Colorado Boulder, USA.


**Changes in FreeRTOS version 10.5.0:**

- The FreeRTOS ARMv7-M (ARM Cortex-M3/4/7) and ARMv8-M (ARM
  Cortex-M23/33/55) ports with memory protection unit (MPU) support
  can no longer create privileged tasks from unprivileged tasks using
  xTaskCreate or xTaskCreateStatic APIs. Also, unprivileged tasks can
  no longer call the following APIs:

  - xTimerCreate
  - xTimerCreateStatic
  - xTimerPendFunctionCall

  The application writer needs to perform these operations either
  before starting the scheduler or from a privileged task.


**Changes in FreeRTOS version 10.4.6:**

- FreeRTOS-MPU ports for ARMv7-M MCUs (ARM Cortex-M3/4/7) now include
  a new configuration option
  `configALLOW_UNPRIVILEGED_CRITICAL_SECTIONS`. Setting the constant
  to 0 in FreeRTOSConfig.h prevents unprivileged application tasks
  from using the `taskENTER_CRITICAL()` macro to create a critical
  section. Set the constant to 1, or leave it undefined, to maintain
  compatibility with previous FreeRTOS kernel versions, which allow
  both privileged and unprivileged tasks to create critical sections.
  Note: it is recommended to define the constant to 0 for maximum
  security; because of this, a compiler warning is output if the
  constant is left undefined.


**Changes in FreeRTOS version 10.4.0:**

- FreeRTOS V10.4.0 introduced a new variable `__privileged_functions_start__`
  to indicate the starting location
  of the privileged code. It needs to be exported from linker script
  in the same way as the pre-existing linker variables such
  as [`__privileged_functions_end__`](/media/MPU_Chapter.pdf).

  If you get a linker error in an earlier created project for
  unresolved symbol `__privileged_functions_start__`, you need to
  export a variable `__privileged_functions_start__` with the value
  equal to `__FLASH_segment_start__`.

- Heap memory is now placed in the privileged section, and as a
  result, unprivileged tasks cannot
  call [`pvPortMalloc()`](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) or
  [`vPortFree()`](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management).

- [`xTaskCreate()`](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate) can no longer be used to create an
  unprivileged task. Use [`xTaskCreateRestricted()`](/Documentation/02-Kernel/04-API-references/13-FreeRTOS-MPU-specific/01-xTaskCreateRestricted/) instead.

- FreeRTOS-MPU ports for ARM Cortex-M4 microcontrollers now support
  microcontrollers with 16 MPU regions. To use 16 regions set
  `configTOTAL_MPU_REGIONS` to 16 in [`FreeRTOSConfig.h`](/Documentation/02-Kernel/03-Supported-devices/02-Customization/).

- Application writers can now override the default values for the for
  TEX, Shareable (S), Cacheable (C) and Bufferable (B) bits for MPU
  regions covering Flash and RAM by defining `configTEX_S_C_B_FLASH`
  and `configTEX_S_C_B_SRAM` respectively in [`FreeRTOSConfig.h`](/Documentation/02-Kernel/03-Supported-devices/02-Customization/).


**Changes in FreeRTOS version 10.3.0:**

- It is now possible to prevent any privilege escalations originating
  from outside of the kernel code (other than escalations performed by
  the hardware itself when an interrupt is entered). To do so
  set `configENFORCE_SYSTEM_CALLS_FROM_KERNEL_ONLY` to 1
  in [`FreeRTOSConfig.h`](/Documentation/02-Kernel/03-Supported-devices/02-Customization/), and define the linker
  variables [`__syscalls_flash_start__`](https://github.com/FreeRTOS/FreeRTOS/blob/V10.3.1/FreeRTOS/Demo/CORTEX_MPU_STM32L4_Discovery_GCC_IAR_Keil/Projects/GCC/STM32L475VGTX_FLASH.ld#L113)
  and [`__syscalls_flash_end__`](https://github.com/FreeRTOS/FreeRTOS/blob/V10.3.1/FreeRTOS/Demo/CORTEX_MPU_STM32L4_Discovery_GCC_IAR_Keil/Projects/GCC/STM32L475VGTX_FLASH.ld#L115)
  to be the start and end addresses of the system calls memory respectively.


<span id="mpu-specifics"></span>
## FreeRTOS-MPU Specifics

<span id="mpu_features"></span>
#### FreeRTOS-MPU features

- Compatible with the standard ARM Cortex-M3 and Cortex-M4F ports.

- Tasks can be created to run in either Privileged mode or
  Unprivileged mode. Unprivileged tasks can only access their own
  stack and up to three user definable memory regions (three per
  task). User definable memory regions are assigned to tasks when the
  task is created, and can be reconfigured at run time if required.

- User definable memory regions can be parameterised individually. For
  example, some regions may be set to read only, while others may be
  set to not executable (execute never, or simply XN, in ARM
  terminology), etc.

- No data memory is shared between Unprivileged tasks, but
  Unprivileged tasks can pass messages to each other using the
  standard queue and semaphore mechanisms. Shared memory regions can
  be explicitly created by using a user definable memory region but
  this is discouraged.

- A Privileged mode task can set itself into Unprivileged mode, but
  once in Unprivileged mode it cannot set itself back to Privileged
  mode.

- The FreeRTOS API is located in a region of Flash that can only be
  accessed while the microcontroller is in Privileged mode (calling an
  API function causes a temporary switch to Privilege mode).

- The data maintained by the RTOS kernel (all non stack data that is
  private to the FreeRTOS source files) is located in a region of RAM
  that can only be accessed while the microcontroller is in Privileged
  mode.

- System peripherals can only be accessed while the microcontroller is
  in Privileged mode. Standard peripherals (UARTs, etc.) are
  accessible by any code but can be explicitly protected using a user
  definable memory region.


<span id="creating_tasks"></span>
#### Creating Tasks

FreeRTOS-MPU port can have two type of tasks:

1. **<span class="underline">Privileged Tasks:</span>** A privileged
   task has access to the entire memory map. Privileged tasks can be
   created using either the [xTaskCreate()](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate)
   or [xTaskCreateRestricted()](/Documentation/02-Kernel/04-API-references/13-FreeRTOS-MPU-specific/01-xTaskCreateRestricted/) API function.

2. **<span class="underline">Unprivileged Tasks:</span>** An
   unprivileged task only has access to its stack. In addition, it can
   be granted access up to three user definable memory regions (three
   per task). Unprivilged tasks can only be created using
   the [xTaskCreateRestricted()](/Documentation/02-Kernel/04-API-references/13-FreeRTOS-MPU-specific/01-xTaskCreateRestricted/) API.
   **Note that xTaskCreate() API must not be used to create an unprivileged task.**

If a task wants to use the MPU then the following additional information
has to be provided:

- The address of the task stack.
- The start, size and access parameters for up to three user definable
  memory regions.

The total number of parameters required to create a task is therefore
quite large. To make creating MPU aware tasks easier FreeRTOS-MPU uses
an API function called [xTaskCreateRestricted()](/Documentation/02-Kernel/04-API-references/13-FreeRTOS-MPU-specific/01-xTaskCreateRestricted/).
This allows all but one of the parameters to be defined in a const struct, with the
struct being passed (by reference) into xTaskCreateRestricted() as a
single parameter.

A Privileged mode task can call [portSWITCH\_TO\_USER\_MODE()](/Documentation/02-Kernel/04-API-references/13-FreeRTOS-MPU-specific/04-portSWITCH_TO_USER_MODE)
to set itself into Unprivileged mode. A task that is running in Unprivileged
mode cannot set itself into Privileged mode.

The memory regions allocated to a task can be changed
using [vTaskAllocateMPURegions()](/Documentation/02-Kernel/04-API-references/13-FreeRTOS-MPU-specific/03-vTaskAllocateMPURegions). See the
xTaskCreateRestricted() and vTaskAllocateMPURegions() API documentation
for more information.


<span id="acl_object_lifecycle"></span>
#### Kernel object lifecycle with Access Control Lists

When Access Control Lists are enabled (`configENABLE_ACCESS_CONTROL_LIST`
set to 1 with the MPU wrappers introduced in FreeRTOS V10.6.0), each
kernel object (task, queue, semaphore, timer, event group, stream buffer
or message buffer) occupies a slot in a protected kernel object pool.
Unprivileged tasks are granted access to individual objects using the
`vGrantAccessTo<Object>()` APIs (for example, `vGrantAccessToTimer()`),
and access is removed using the corresponding `vRevokeAccessTo<Object>()`
APIs.

Access grants are tied to the object's pool slot, not to the object
itself. This has an important consequence when objects are deleted.

**Always revoke access before deleting an object:** Privileged code
that deletes a kernel object shared with unprivileged tasks must first
revoke every unprivileged task's access to the object - for example,
using `vRevokeAccessToTimer()` - and only then delete the object - for
example, using [xTimerDelete()](/Documentation/02-Kernel/04-API-references/11-Software-timers/07-xTimerDelete).

```c
/* Correct sequence: revoke first, then delete. */
vRevokeAccessToTimer( xUnprivilegedTaskHandle, xTimerHandle );
xTimerDelete( xTimerHandle, portMAX_DELAY );
```

If an object is deleted while unprivileged tasks still hold access to
its pool slot, those access rights become stale but remain in effect for
the slot. If a new object is later created and reuses the same slot, the
old handle aliases the new object. Taking a timer as the example, an
unprivileged task holding a stale handle could then:

- Read or modify the new timer's state (its ID, period and active
  state) through the stale handle, and
- Cause the timer service (daemon) task, which runs with elevated
  privilege, to invoke an unexpected callback.

Deleting an object never implicitly revokes the access previously
granted to it. Revoking access before deletion ensures no task retains
rights to a pool slot that may be reused.
