---
title: "FreeRTOS Support for Armv8-R AArch64 on Arm Cortex-R82"
date: 07 Apr 2026
feature: blog
authors:
  - aismail
---

by [Ahmed Ismail](../author/aismail) on 07 Apr 2026

Why 64-bit real-time, SMP scheduling, and MPU-backed isolation belong in the same design

## 1. Overview

This blog introduces a FreeRTOS symmetric multiprocessing (SMP) port for Arm Cortex-R82 running Armv8-R Arm Architecture 64-bit (AArch64), along with a small set of reference applications that demonstrate how to bring up the released porting layer on Arm's FVP_BaseR_AEMv8R Fixed Virtual Platform. The accompanying examples include an intentionally minimal SMP "ping/pong" demo, as well as two Memory Protection Unit (MPU) focused applications that illustrate privilege separation.

## 2. Real-time systems are scaling

Real-time software used to mean "one core, one control loop, one deadline." Today's real-time designs often look more like small servers combining tight control loops with storage or networking stacks, telemetry/logging, safety supervision, and larger software components that need isolation boundaries.

- **More concurrency:** multiple subsystems want to run at once, without turning the whole system into a background thread.
- **More address space pressure:** firmware images are bigger, buffers are bigger, and shared memory use is growing.
- **More isolation expectations:** It is increasingly common to separate critical functions from less-trusted code.

We want throughput (parallel work) while preserving determinism (bounded latency and repeatable behavior). And we want isolation without paying the full cost and complexity of a full Memory Management Unit (MMU) + virtual memory stack.

## 3. Why Arm Cortex-R82

Arm Cortex-R82 targets the "high-performance real-time" space where users want multicore scaling and a modern interrupt controller without losing the predictable response and tight control over the software environment.

- **Armv8-R AArch64 execution state:** a 64-bit programming model for R-profile systems.
- **SMP across multiple identical cores** sharing memory (the provided FVP configuration used by the reference applications models up to 4 cores).
- **Generic Interrupt Controller (GIC) v3.2 model** (with system-register interface enabled in the reference platform configuration).
- **R-profile MPU** implements Protected Memory System Architecture (PMSA) v8-64 to support privilege separation and bounded memory sharing.

## 4. Why FreeRTOS SMP

FreeRTOS SMP extends the FreeRTOS scheduler model to multiple cores. It allows predictable scheduling behaviors, portability, and parallel execution with the small footprint that is expected from FreeRTOS.

- A single FreeRTOS kernel instance schedules tasks across multiple Central Processing Unit (CPU) cores.
- Tasks can be pinned to specific cores (core affinity) or allowed to run on any core with available capacity.
- The port uses inter-core interrupts to request a reschedule on another core when a scheduling decision requires it.

For some workloads, we can achieve separation of concerns using core affinity: keep the tightest control loops on one core, and move background processing (logging, protocol parsing, maintenance tasks) to others.

## 5. Who is this for

This port targets designs that need multicore throughput but still treat determinism as a first-class requirement.

- **Storage controllers and flash translation layers:** parallelize background maintenance and Input/Output (I/O) while keeping strict latency budgets.
- **Automotive and industrial real-time systems:** split safety supervision, control, and communications across cores with clear isolation boundaries.
- **Modems and infrastructure control planes:** mix protocol processing and real-time control on a shared, deterministic platform.

## 6. What's next

To evaluate the port, we recommend starting with the minimal SMP demo to validate startup, timer configurations, and interrupt routing. Next, try the MPU reference applications to explore privilege separation.

### 6.1 Arm Cortex-R82 FreeRTOS reference applications

Arm has introduced the following Arm Cortex-R82 reference applications hosted on FreeRTOS-Partner-Supported-Demos repository:

- [Arm Cortex-R82 Non-MPU SMP application](https://github.com/FreeRTOS/FreeRTOS-Partner-Supported-Demos/blob/main/CORTEX_R82_SMP_FVP_GCC_ARMCLANG/README.md)
- [Arm Cortex-R82 SMP MPU application](https://github.com/FreeRTOS/FreeRTOS-Partner-Supported-Demos/blob/main/CORTEX_R82_SMP_MPU_FVP_GCC_ARMCLANG/README.md)
- [Arm Cortex-R82 SMP Extended MPU application](https://github.com/FreeRTOS/FreeRTOS-Partner-Supported-Demos/blob/main/CORTEX_R82_SMP_EXTENDED_MPU_FVP_GCC_ARMCLANG/README.md)

## 7. Further reading

- [FreeRTOS SMP port for Armv8-R AArch64 on Cortex-R82 Technical Page](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Arm/FreeRTOS-SMP-port-for-Armv8-R-AArch64-on-Cortex-R82)
- [Arm Cortex-R82 Technical Reference Manual](https://developer.arm.com/documentation/102670/0300)
- [Arm Architecture Reference Manual for R-profile AArch64 architecture](https://developer.arm.com/documentation/ddi0628/latest)
- [Arm Generic Interrupt Controller (GIC) Architecture Specification, v3 and v4](https://developer.arm.com/documentation/ihi0069/latest/)
- [Arm Cortex-R82 FreeRTOS-Kernel port](https://github.com/FreeRTOS/FreeRTOS-Kernel/tree/main/portable/GCC/ARM_CR82)

## 8. References

- [Arm Cortex-R82 Technical Reference Manual](https://developer.arm.com/documentation/102670/0300)
- [Arm Architecture Reference Manual for R-profile AArch64 architecture](https://developer.arm.com/documentation/ddi0628/latest)
- [Arm Generic Interrupt Controller (GIC) Architecture Specification, v3 and v4](https://developer.arm.com/documentation/ihi0069/latest/)
- [Arm Cortex-R82 FreeRTOS-Kernel port](https://github.com/FreeRTOS/FreeRTOS-Kernel/tree/main/portable/GCC/ARM_CR82)
