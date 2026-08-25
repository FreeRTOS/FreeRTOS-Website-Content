---
title: Kernel threat model
date: Jan.2022
---

## Introduction

This is the threat model for FreeRTOS ports that support hardware memory protection, such as the ARM 
Cortex-M Memory Protection Unit (MPU). It is applicable to applications using the MPU wrapper C file 
introduced in FreeRTOS V10.6.0. Application writers that use FreeRTOS in their devices assume responsibility 
for securing both the device and the software running on it. Note that co-routines, being deprecated and
lacking MPU support, fall outside the scope of the threat model.


## Assets

1. FreeRTOS Kernel C Code.
1. Application Code - defined as all the code other than the kernel C code.
1. FreeRTOS Kernel internal data.
1. Application Data - defined as all the data other than the kernel internal data.
1. Saved Task Context - the context of a task that is not in the Running state.
1. Task Stack – each task has its own stack.
1. [Task] System Call Stack - each task has a separate system call stack to execute system calls.
1. System Stack - the stack used by Interrupt Service Routines (ISRs).
1. Special CPU Registers such as –
   + MPU control registers.
   + CPU operational registers (e.g. execution mode).
1. General purpose CPU registers.


## Actors

1. Unprivileged tasks – FreeRTOS tasks with limited privileges.
1. Privileged tasks – FreeRTOS tasks with full privileges.
1. Interrupt Service Routines (ISRs).
1. Peripherals with access to memory, for example Direct Memory Access DMA controllers and communication ports.


## Authorizations

The following table describes each actor's authorizations for each asset, unless explicitly granted 
additional authorization at run-time (for example, an unprivileged task that is granted read only access 
to application data):

| &nbsp; | Unprivileged task | Privileged task | ISR code | Peripherals | 
|---|---|---|---|---| 
| Kernel code | - | RW | RX | RW |
| Application code | RX | RX | RX | RW |
| Kernel data | - | RW | RW | RW |
| Application data | - | RW | RW | RW |
| Task context | - | RW | RW | RW |
| Special registers | - | RW | RW | RW* |
| General purpose registers | RW | RW | RW | - |

*R - Read, W - Write, X - Execute, NA - Not Applicable. A dash without any letters means "no access".*

*\* Peripherals have access to their own special registers.*

Summarizing the table above.
1. Unprivileged tasks have
    + Read and Execute access to application code.
    + Read and Write access to their own stack.
    + Read and Write access to general purpose registers.

2. Privileged tasks have
    + Read and Execute access to all the code.
    + Read and Write access to all the data.
    + Read and Write access to all the registers.

3. Interrupt Service Routines have
    + Read and Execute access to all the code.
    + Read and Write access to all the data.
    + Read and Write access to all the registers.

4. Peripherals have
    + Read and Write access to all the memory and their own registers.


## Entry points

System Calls – FreeRTOS system calls make the kernel services available to unprivileged tasks by wrapping 
kernel Application Programming Interface (API) functions with code that temporarily grants any unprivileged 
task which calls a kernel API the privilege necessary to execute kernel code.


## Trust boundaries

The only time the trust boundary is crossed is when an unprivileged task makes a system call to execute 
a kernel API function.

![Trust boundaries diagram](/media/2023/trust_boundary.png)


## Invariant

After the FreeRTOS scheduler has started, an actor cannot access any asset it is not authorized to access.


## Threats mitigated by the Kernel
The following threats are mitigated by the FreeRTOS Kernel. 
In all the threats below, the attacker is assumed to be running unprivileged.

1. Access Privilege Violation

    An Access Privilege violation occurs if an actor successfully accesses (to read, write or execute) an 
    asset it is not authorized to access.

    Mitigation- The FreeRTOS kernel programs the MPU when the scheduler starts, and on each task context 
    switch, so that the MPU enforces the authorizations described by the table in the Authorizations section.

2. Stack Overflow

    A stack overflow occurs when the stack pointer grows beyond the stack memory, leading to memory corruption.

    Mitigation– The FreeRTOS kernel uses an MPU region to grant unprivileged tasks access to their own 
    stack. The size and start address of the MPU region match the size and start address of the stack, 
    so writing outside the stack results in a memory protection fault.

    The application writer must ensure the stack size and alignment are compatible with any limitations 
    imposed by the MPU hardware. The application writer must also ensure memory adjacent to the stack is 
    not accessible to the same task.

3. Stack Manipulation Attacks

    An unprivileged task has write-access to its own stack. An attacker can use this ability to exploit 
    a kernel function that fails to initialize stack memory before using it.

    Mitigation– Execute system calls on a separate stack accessible to privileged code only.

4. Exploiting system calls that take pointers as parameters to achieve arbitrary reads or writes

    An attacker can pass the address of the location they want to read from or write to as a parameter 
    to a system call that dereferences the address - effectively allowing the attacker read from or write 
    to any memory.

    Mitigation– System calls that accept pointers must reject addresses to which the calling task does 
    not have the necessary access permissions.

5. Exploiting system calls which take a function pointer as a parameter to achieve arbitrary code execution

    An attacker can elevate their privilege by passing the address of a function to a system call, the 
    implementation of which executes the supplied function from a privileged context.

    Mitigation– Review all the system calls to ensure those that accept a function pointer as a parameter 
    only execute the function in the calling task's context.

6. Fake kernel object handles

    An attacker can trick the kernel into an arbitrary memory read or write by passing the address of a 
    specially crafted memory block instead of a kernel object handle as a parameter to a system call.

    Mitigation– Kernel object handles are opaque and indirectly verifiable integers, not addresses.

7. Using attacker controlled memory for creating kernel objects

    Statically allocated kernel objects use memory provided by the application writer. Using memory provided 
    by an attacker can enable the attacker to manipulate the kernel.

    Mitigation– Unprivileged tasks cannot access system calls used to create kernel objects in statically 
    allocated memory. Objects can be created using statically allocated memory from privileged tasks or 
    before starting the scheduler.

8. Overriding kernel MPU protections

    An attacker can circumvent kernel memory protections by overlapping MPU regions (where supported by 
    the MPU hardware).

    Mitigation– The ARMv7-M MPU is the only supported MPU that allows overlapping MPU regions. On that 
    architecture, higher MPU region numbers take precedence over lower MPU region numbers, so the kernel 
    uses the highest region numbers (which can't be overridden) to protect its own code and data.

9. Manipulating task context after it is swapped out

    A task's context includes both general and special purpose registers. The kernel stores the context 
    of each task that is not running, so that it can run the task again in the future. An attacker can 
    hijack control flow, or escalate a task's privilege, by manipulating a saved context.

    Mitigation- Task context is stored in the Task Control Block (TCB), which is a kernel internal data 
    structure, and so not accessible to unprivileged code.

10. Privilege escalation attempts

    An attacker could execute assembly instructions used by system calls to escalate privilege.

    Mitigation- Privilege escalations are only granted when originating from a system call.

11. Leaking information through a stack

    Confidential data stored on the stack by a system call could remain on the stack and accessible to 
    the unprivileged task after the system call returns.

    Mitigation– Execute system calls on a separate stack accessible to privileged code only.


## Threats not mitigated by the Kernel

1. Leaking information through registers

    Confidential data stored in a general purpose register by a system call could remain in the register 
    accessible to the unprivileged task after the system call returns.

    Mitigation– This threat is considered low risk and not mitigated because kernel system calls don't 
    use data which would be problematic if read by an unprivileged task. System calls added by application 
    writers that do use confidential data must take appropriate measures to remove the data from the registers 
    before returning.


## Threats to be mitigated by the application
The following threats should be mitigated by the application:

1. Untrusted code execution before starting the scheduler

    The microcontroller (MCU) boots into privileged mode and remains privileged until the scheduler starts. 
    The kernel doesn’t provide any protections against untrusted code execution before the scheduler starts.
    This includes the initialization code injected using `configINCLUDE_FREERTOS_TASK_C_ADDITIONS_H`.

    Mitigation- The application writer must ensure no untrusted code executes before the scheduler starts. 
    It is strongly recommended to use a secure boot sequence that only boots verified signed images, and to 
    only execute untrusted code in unprivileged tasks.

2. Untrusted code execution in ISRs

    The MCU enters privileged mode before executing ISRs. The kernel doesn't provide any protections against 
    untrusted code execution between entering an ISR and the ISR either returning or lowering its privilege.

    Mitigation- The application writer must ensure no untrusted code executes in any ISR. It is strongly 
    recommended to use a secure boot sequence that only boots verified signed images, to keep ISRs as short 
    as possible, and defer the majority of interrupt processing to unprivileged tasks. Installing a single 
    entry point for all ISRs can help manage privilege levels.

3. Incorrect configuration

    The application may fail to correctly export the following linker variables:

    - Start and end of the memory containing all code:
      ```
      __FLASH_segment_start__
      __FLASH_segment_end__
      ```

    - Start and end of the memory containing kernel code placed in the
      privileged\_functions section.
      ```
      __privileged_functions_start__
      __privileged_functions_end__
      ```

    - Start and end of the memory containing FreeRTOS system calls placed in the
      freertos\_system\_calls section.
       ```
       __syscalls_flash_start__
       __syscalls_flash_end__
       ```

    - Start and end of the memory containing kernel data placed in the
      privileged\_data section.
      ```
      __privileged_data_start__
      __privileged_data_end__
      ```

    The application writer must ensure the size and alignment of the above memory regions are compliant 
    with any limitations imposed by the MPU hardware. The application writer must define configENABLE_MPU 
    to 1 for ARMv8-M ports.

    Mitigation- The application writer must ensure that FreeRTOS is configured correctly.

4. Physical attacks

    The end product may be subjected to physical attacks such as glitching or side channel attacks.

    Mitigation- MPU protections do not protect against all physical attacks. The application writer must 
    develop protections against physical attacks, or deploy the device running FreeRTOS in environments 
    with physical access restrictions, if required.

5. Source Code Integrity

    FreeRTOS source code can be modified by the application writer which may introduce vulnerabilities.

    Mitigation- The application writer must not modify the FreeRTOS source code.

6. Application Binary Integrity

    The binary running in the end product may be modified to introduce vulnerabilities.

    Mitigation- The application writer must use mechanisms like hardware root of trust, secure boot, and 
    cryptographic signature verification to ensure application binary integrity.

7. Unprivileged task accessing valid kernel objects using legitimate system calls

    An unprivileged task may access a valid kernel object using legitimate system calls which it is not 
    supposed to access.

    Mitigation- The application writer must ensure that an unprivileged task does not access any kernel 
    object that it is not supposed to access.

8. Untrusted code execution in callbacks

    The following callbacks run in the privileged context:
    - [Idle Hook Function](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions#idle-hook-function)
    - [Tick Hook Function](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions#tick-hook-function)
    - [Malloc Failed Hook Function](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions#malloc-failed-hook-function)
    - [Stack Overflow Hook Function](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions#stack-overflow-hook-function)
    - [Daemon Task Startup Hook](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions#daemon-task-startup-hook)
    - [Software Timer Callback](https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)

    The kernel does not provide any protection against untrusted code execution
    in the above mentioned callbacks.

    Mitigation - The application writer must ensure no untrusted code executes
    in the above mentioned callbacks. One option is to disable hooks using
    configuration constants.
