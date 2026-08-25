---
title: "FreeRTOS SMP port for Armv8-R AArch64 on Cortex-R82"
created: 2026-04-07
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: FreeRTOS SMP overview
    link: /Documentation/02-Kernel/02-Kernel-features/13-Symmetric-multiprocessing-introduction
  - title: FreeRTOS MPU
    link: /Security/04-FreeRTOS-MPU-memory-protection-unit
---

[[RTOS Ports](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

Technical reference: architecture, build, and extension guide

See also the accompanying blog post: [FreeRTOS Support for Armv8-R AArch64 on Arm Cortex-R82](/Community/Blogs/2026/freertos-support-for-armv8-r-aarch64-on-arm-cortex-r82)

## 1. Overview

This page describes the FreeRTOS Symmetric Multiprocessing (SMP) port targeting Arm Cortex-R82 (Armv8-R) in Arm Architecture 64-bit (AArch64) state, and the accompanying reference applications. This page is intended for users and developers who want to evaluate, build, and extend the port on Arm Fixed Virtual Platforms (FVP) or on their own Arm Cortex-R82-based hardware.

### 1.1 Scope

Supported in this release:

- FreeRTOS SMP porting layer for Arm Cortex-R82 (Armv8-R AArch64).
- Scheduler integration for multi-core operation with per-core critical nesting state.
- Inter-core yield mechanism using a Generic Interrupt Controller (GIC) Software Generated Interrupt (SGI).
- Application-owned tick interrupt setup via configSETUP_TICK_INTERRUPT.
- Optional Memory Protection Unit (MPU) support with privilege separation (kernel and privileged tasks run at Exception Level 1 (EL1) and unprivileged tasks run at Exception Level (EL0)) and per-task MPU regions.
- Reference Board Support Package (BSP) and three example applications targeting Arm Cortex-R82 running on FVP_BaseR_AEMv8R (CMake-based build system, Arm GNU and ArmClang toolchains supported).

Not supported in this release:

- No Memory Management Unit (MMU) / virtual memory support (the reference platform config disables Virtual Memory System Architecture (VMSA)).
- No cache maintenance operations in the port. Fully coherent shared memory is assumed for SMP communication.
- No EL2 / hypervisor mode support in the reference configuration (Privilege Level 2 (PL2) disabled).
- No multi-security-state configuration in the reference platform (single security state modeled).
- No production-ready device drivers beyond the minimal BSP required to boot, program the timer, and drive the GIC.

## 2. Architecture overview

### 2.1 Reference platform model

The example applications target Arm Cortex-R82 platform running on Arm's FVP_BaseR_AEMv8R model with a simple configuration file. Key modeled properties used by the applications include:

- AArch64 enabled (cluster0.has_aarch64=1).
- VMSA/MMU disabled (cluster0.VMSA_supported=0).
- 4 cores modeled (cluster0.NUM_CORES=4).
- EL2 disabled (cluster0.has_pl2=0).
- Single security state modeled (gic_distributor.has-two-security-states=0).

### 2.2 Execution levels and privilege model

The port expects the kernel to run at EL1. When MPU support is enabled, tasks may run either:

- Privileged tasks at EL1 (for logging, system services, etc.).
- Unprivileged tasks at EL0 (for isolation of application logic).

A task's initial Processor State (PSTATE) is selected during stack initialization: privileged tasks use an EL1 PSTATE value, while unprivileged tasks use an EL0 PSTATE value. Context save/restore preserves the Saved Program Status Register (SPSR_EL1) value.

## 3. FreeRTOS SMP design in this port

### 3.1 Scheduler model and core affinity

This port can be used with the FreeRTOS SMP kernel. A single kernel instance manages ready lists and schedules tasks onto available cores. The reference SMP Non-MPU application explicitly pins two tasks to different cores to demonstrate parallel execution and coherent sharing.

### 3.2 Core bring-up and synchronization

In the reference BSP and reference applications, all cores start from the same reset entry. Core 0 performs C runtime initialization and runs main(). Secondary cores wait in a low-power loop until the primary core indicates that platform and kernel initializations are complete.

**Core 0 bring-up sequence:**

- Zeros all GP registers
- Sets Vector Base Address Register (VBAR_EL1) to reset-vector-table base
- Enables Floating-Point/Single-Instruction-Multiple-Data (FP/SIMD) access at EL0 and EL1
- Sets EL1 exception level stack pointer (SP_EL1)
- Invalidates instruction and data caches
- Configures System Control Register (SCTLR_EL1)
- Copies .data from ROM to RAM and zeros the .bss section
- Initializes C Standard Library (LibC)
- Sets VBAR_EL1 to FreeRTOS-vector-table base
- Starts scheduler and setup MPU
- Starts the timer that generates the Tick ISR
- Sets "primary-init-done" flag
- Waits for all the secondary cores to be ready
- Enables MPU
- Start the first task on the primary core

**Core 1..N-1 bring-up sequence:**

- Zeros all GP registers
- Sets VBAR_EL1 to reset-vector-table base
- Enables FP/SIMD access at EL0 and EL1
- Sets EL1 exception level stack pointer (SP_EL1)
- Invalidates instruction and data caches
- Configures System Control Register (SCTLR_EL1)
- Issues a Wait for Event (WFE) instruction to sleep until primary core init is done
- Sets VBAR_EL1 to FreeRTOS-vector-table base
- Enables yield Software Generated interrupt (SGI) on this core through GIC
- Setup MPU
- Marks the core as ready
- Enables MPU
- Issues a Supervisor/System Call (SVC) with value equal to `portSVC_START_FIRST_TASK` (106) to start the first task on that core

This model keeps the porting layer concise: the port coordinates the scheduler and per-core context, while the BSP provides the reset flow and any platform-specific gating needed for secondary cores.

### 3.3 Critical sections and spinlocks

For SMP, the port uses a combination of per-core interrupt masking and a global spinlock. The port uses exclusive-load/store (LDXR/STXR) loops to acquire a lock, paired with full-system barriers (Data Memory Barrier (DMB) System (SY)). Unlocking writes 0 to the lock and uses Send Event (SEV) instruction to wake up waiters.

Implementation note: the lock operations are inside the porting layer and are used to protect scheduler and kernel data structures.

## 4. Interrupt model

### 4.1 GICv3.2 integration approach

The port is designed for a GICv3.2-style interrupt controller and uses the system register interface for key operations. The reference BSP enables delivery of Group-1 interrupts at EL1 via the Interrupt Controller Interrupt Group 1 Enable register (ICC_IGRPEN1_EL1). The reference BSP also configures the distributor and per-core redistributor.

The port itself delegates the Interrupt Request (IRQ) dispatch to the application by calling an application-provided IRQ handler. This keeps the port portable across platforms with different interrupt wiring or interrupt ID assignments.

### 4.2 Per-core vs shared interrupts in the demos

In the reference demos, two interrupts are central to the system behavior:

- The FreeRTOS tick interrupt (configured via configSETUP_TICK_INTERRUPT, the application configures the AArch64 physical timer).
- An inter-core yield SGI used to request rescheduling on another core.

Interrupt path:

IRQ entry → FreeRTOS IRQ handler → application IRQ dispatcher

- if timer interrupt: clear timer, call FreeRTOS tick handler
- if yield SGI: call FreeRTOS SGI handler which set the per-core variable indicating request for a context switch (i.e., ullPortYieldRequired)

### 4.3 SVC usage

The port uses Supervisor/System calls (SVC) for yield, interrupt mask management, and per-core scheduler entry. Key SVC numbers (from the porting layer) include:

- SVC 104: System call exit
- SVC 105: Yield
- SVC 106: Start scheduler on a core (used for secondary core entry in the reference design)
- SVC 107/108: Disable/Enable interrupts
- SVC 109: Fetch core ID
- SVC 110/111/112: Mask/Unmask interrupts
- SVC 113: Check task's privilege level
- SVC 114/115: Save/Restore task context
- SVC 116: Delete current executing task
- SVC 117: Send an inter-core interrupt (writes to the Interrupt Controller Software Generated Interrupt Group 1 Register (ICC_SGI1R_EL1))

These are implementation choices of this porting layer (not architectural requirements).

### 4.4 Tick timer: explicit, application-owned setup

The port requires the application to provide configSETUP_TICK_INTERRUPT(). In the reference applications, this config hook configures the AArch64 physical timer (CNTP) and enables its interrupt in the GIC.

This makes it easy to reuse the port across different platforms (FVP, FPGA prototypes, or silicon) where the timer and interrupt wiring may differ.

## 5. Memory system

### 5.1 Cache coherency assumptions

The port assumes that shared data used for SMP communication are fully cache coherent by the platform. The port does not perform cache clean/invalidate operations for shared objects.

The user should place inter-core shared objects (queues, semaphores, locks, shared flags, etc.) in coherent, cacheable memory, or in memory that is otherwise guaranteed coherent by the SoC design. Users must avoid mixing non-coherent regions with SMP sharing unless they add explicit cache maintenance.

### 5.2 MPU support

When enabled (configENABLE_MPU=1), the port programs a set of fixed MPU regions at startup and then applies per-task regions during context switches. Fixed regions configured by the reference MPU-aware linker scripts and porting layer include:

- Privileged flash/code region.
- Unprivileged flash/code region.
- System call wrappers region (read-only to both privileged and unprivileged tasks).
- Privileged RAM region.

The port reserves MPU regions 0-3 for these fixed regions, uses a dedicated stack region, and allows additional user regions starting at a configurable region index. The default total region count is 16 but can also be set to 32 (configTOTAL_MPU_REGIONS).

The MPU requires a minimum region size, granularity, and alignment of 64 bytes. Therefore, any user-defined region base address and size must be 64-byte aligned.

The port enforces 64-byte alignment for both the start and end addresses. It verifies that the configured region size is not smaller than the minimum supported region size and checks for overlaps with kernel-defined regions (for example, the stack region) as well as with previously defined user MPU regions.

### 5.3 Barriers and ordering

The port uses explicit ordering primitives where required for correctness on a multi-core system e.g., barriers around lock acquisition/release and around system register programming (Data Synchronization Barrier (DSB)/Instruction Synchronization Barrier (ISB) when enabling interrupts or MPU state).

## 6. Build and toolchain

The port is compatible with both Arm GNU and ArmClang toolchains. The reference applications are CMake-based and provide two toolchain files:

- gnu_toolchain.cmake (aarch64-none-elf-gcc)
- armclang_toolchain.cmake (armclang targeting aarch64-arm-none-eabi)

Example build commands:

```
rm -rf build && cmake -B build --toolchain=<armclang/gnu>_toolchain.cmake .
cmake --build build
```

Running on FVP_BaseR_AEMv8R FVP (all reference applications):

```
./run.sh
```

The run script launches FVP_BaseR_AEMv8R with the built Arm Executable File (AXF) image and the included FVP configuration (fvp_config.txt).

## 7. Example applications

Three reference applications are included:

| Application | Primary purpose | Highlights |
| --- | --- | --- |
| CORTEX_R82_SMP_FVP_GCC_ARMCLANG | Minimal SMP bring-up and inter-core behavior | Two tasks pinned to different cores, shared flag protected by a mutex. Validates tick + yield SGI + coherency assumptions. |
| CORTEX_R82_SMP_MPU_FVP_GCC_ARMCLANG | MPU-backed privilege separation patterns | Unprivileged tasks communicate via queue; privileged logger task demonstrates a common "privileged services" pattern. |
| CORTEX_R82_SMP_EXTENDED_MPU_FVP_GCC_ARMCLANG | MPU fault behavior and robustness patterns | Extends the MPU demo with explicit fault injection and handling. |

### 7.1 How to choose a starting point

- Start with the SMP Non-MPU demo to validate your reset flow, interrupt routing, and tick timer wiring on your platform.
- Move to the MPU demo to validate linker script region layout, unprivileged task execution, and system call-based privilege transitions.
- Use the extended MPU demo when you want to validate fault handling and debug hooks early in the bring-up sequence.

### 7.2 Arm Cortex-R82 FreeRTOS reference applications

Arm has introduced the following Arm Cortex-R82 reference applications hosted on FreeRTOS-Partner-Supported-Demos repository:

- [Arm Cortex-R82 Non-MPU SMP application](https://github.com/FreeRTOS/FreeRTOS-Partner-Supported-Demos/blob/main/CORTEX_R82_SMP_FVP_GCC_ARMCLANG/README.md)
- [Arm Cortex-R82 SMP MPU application](https://github.com/FreeRTOS/FreeRTOS-Partner-Supported-Demos/blob/main/CORTEX_R82_SMP_MPU_FVP_GCC_ARMCLANG/README.md)
- [Arm Cortex-R82 SMP Extended MPU application](https://github.com/FreeRTOS/FreeRTOS-Partner-Supported-Demos/blob/main/CORTEX_R82_SMP_EXTENDED_MPU_FVP_GCC_ARMCLANG/README.md)

## 8. Limitations and assumptions

These constraints are explicit in the released code and reference platform setup:

- SMP sharing assumes coherent memory; no cache maintenance is performed by the port.
- Reference platform uses a single security state and does not enable EL2 in the supplied configuration.
- Only minimal BSP functionality is provided for the reference FVP. Production systems will need their own drivers and integration work.

## 9. Further reading

- [FreeRTOS SMP overview](/Documentation/02-Kernel/02-Kernel-features/13-Symmetric-multiprocessing-introduction)
- [FreeRTOS MPU](/Security/04-FreeRTOS-MPU-memory-protection-unit)
- [Arm Cortex-R82 Technical Reference Manual](https://developer.arm.com/documentation/102670/0300)
- [Arm Architecture Reference Manual for R-profile AArch64 architecture](https://developer.arm.com/documentation/ddi0628/latest)
- [Arm Generic Interrupt Controller (GIC) Architecture Specification, v3 and v4](https://developer.arm.com/documentation/ihi0069/latest/)
