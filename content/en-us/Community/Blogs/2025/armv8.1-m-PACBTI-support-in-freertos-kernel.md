---
title: "Introducing Armv8.1-M Pointer Authentication and Branch Target Identification (PACBTI) support in FreeRTOS-Kernel"
date: 20 Feb 2025
feature: blog
authors:
  - aismail
---

by [Ahmed Ismail](../author/aismail) on 20 Feb 2025


What’s better than a secure and reliable system? The Armv8.1-M architecture is introducing **Pointer Authentication** and **Branch Target Identification** extension, also known as **PACBTI**, to add on top of existing Armv8-M's security features which includes TrustZone for Armv8-M, the Memory Protection Unit (MPU), and Privileged Execute-never (PXN). These features efficiently isolate critical security firmware and private data, enforce privilege rules, separate processes, and apply access controls. The **PACBTI** enhances these capabilities by introducing new techniques to catch common exploitable software errors and mitigate Return-Oriented Programming (ROP) and Jump-Oriented Programming (JOP) vulnerabilities.

## Pointer Authentication

Return Oriented Programming (ROP) is a software attack where the attacker corrupts a pointer (typically return address) stored on the stack to point it to somewhere in the library with a useful sequence of machine instructions. These sequences are known as gadgets and are prevalent in most code. By chaining multiple gadgets, the attacker can mislead the program to perform actions that end up in a security compromise. An example of such a security compromise is spawning an interactive shell.

[ ![Figure1. Gadget attack code](/media/2025/Armv8.1-M_PACBTI_Support_Gadget_Attack_Code.png)](/media/2025/Armv8.1-M_PACBTI_Support_Gadget_Attack_Code.png)

*Figure1. Gadget attack code [1]*

Pointer Authentication is a feature, available for Armv8.1-M Arm architecture, to provide some protection against such attacks. A Pointer Authentication Code (PAC) is generated from the value of a given pointer, a modifier and a secret key and is used to verify the pointer before using it.
If attackers attempt to modify such a pointer in memory, they will also need to compute the right PAC signature for it. Using the ROP example, if the return address stored in the stack is signed and verified before returning to it, the attacker will not be able to control the program flow, and an exception is raised.

## Branch Target Identification

The mechanism used to create and identify valid branch landing pads is called Branch Target Identification (BTI). The processor can be configured in such a way that when BTI is enabled, all indirect branches must target landing pads marked by a **BTI** instruction at the very beginning of the address jumped to. If the target address of the branch instruction does not have a landing pad, then the processor triggers an exception. This reduces the number of possible targets addresses and therefore reduces the number of possible gadgets that can be created using JOP.

[ ![Figure2. When BTI is enabled, indirect branches must target a landing pad instruction](/media/2025/Armv8.1-M_PACBTI_Support.png_BTI_Enabled.png)](/media/2025/Armv8.1-M_PACBTI_Support.png_BTI_Enabled.png)

*Figure2. When BTI is enabled, indirect branches must target a landing pad instruction [2]*

Please refer to the [Stack-smashing-and-execution-permissions document](https://developer.arm.com/documentation/102433/0200/Stack-smashing-and-execution-permissions) to find out more about stack smashing, return-oriented programming, and jump-oriented programming. [The blog](https://community.arm.com/arm-community-blogs/b/architectures-and-processors-blog/posts/armv8-1-m-pointer-authentication-and-branch-target-identification-extension) talks in depth about Armv8.1-M PACBTI.

## Implementation in FreeRTOS-Kernel

The **Pointer Authentication and Branch Target Identification** security feature is now supported on ARMv8.1-M ports in FreeRTOS-Kernel. To harden the security, Arm introduced the concept of task dedicated PAC key, where each task is assigned a PAC key during the task initialization process and as part of scheduling, the task's PAC key is stored/restored to/from the task's context when a task is unscheduled/scheduled from/to run. So that attackers need to guess all the tasks' PAC keys to exploit the system using Return Oriented Programming. For more information on the implementation details refer to [ARMv8.1-M PACBTI Extensions](https://developer.arm.com/documentation/109576/0100/Pointer-Authentication-Code/Instructions).

## FreeRTOS examples demonstrating PACBTI

Arm has introduced the following examples hosted on [FreeRTOS-Partner-Supported-Demos repository](https://github.com/FreeRTOS/FreeRTOS-Partner-Supported-Demos) to demonstrate the PACBTI security feature: 
* The MPU example [**CORTEX_M85_MPU_PXN_PACBTI_FVP_ARMCLANG_IAR**](https://github.com/FreeRTOS/FreeRTOS-Partner-Supported-Demos/tree/main/CORTEX_M85_MPU_PXN_PACBTI_FVP_ARMCLANG_IAR)
* The non-MPU example [**CORTEX_M85_PACBTI_FVP_ARMCLANG_IAR**](https://github.com/FreeRTOS/FreeRTOS-Partner-Supported-Demos/tree/main/CORTEX_M85_PACBTI_FVP_ARMCLANG_IAR)
* The task dedicated PAC key example [**CORTEX_M85_TASK_DEDICATED_PAC_KEY_FVP_ARMCLANG**](https://github.com/FreeRTOS/FreeRTOS-Partner-Supported-Demos/tree/main/CORTEX_M85_TASK_DEDICATED_PAC_KEY_FVP_ARMCLANG) 

These are based on Corstone-315 Ecosystem Fixed Virtual Platform (Arm Cortex-M85 CPU and Ethos-U65 NPU) which can be freely downloaded and used.

## References

1. Arm Ltd. *Return-oriented programming.* Available at: [https://developer.arm.com/documentation/102433/0200/Return-oriented-programming](https://developer.arm.com/documentation/102433/0200/Return-oriented-programming)
2. Arm Ltd. *Landing pads.* Available at: [https://developer.arm.com/documentation/109576/0100/Branch-Target-Identification/Landing-pad](https://developer.arm.com/documentation/109576/0100/Branch-Target-Identification/Landing-pad)
