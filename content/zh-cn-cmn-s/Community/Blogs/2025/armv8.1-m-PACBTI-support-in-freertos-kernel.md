---
title: "FreeRTOS-Kernel 引入 Armv8.1-M 指针认证和分支目标识别 (PACBTI) 支持"
date: 2025 年 2 月 20 日
feature: blog
authors:
  - aismail
---

由 [Ahmed Ismail](../author/aismail) 撰写于 2025 年 2 月 20 日

还有什么比安全可靠的系统更好吗？Armv8.1-M 架构正引入**指针认证**和**分支目标识别**扩展，也称为 **PACBTI**，将其加入现有的 Armv8-M 安全功能，这些功能包括 Armv8-M 的 TrustZone、内存保护单元 (MPU) 和特权模式下永不执行 (PXN)。这些功能可有效隔离关键安全固件和私有数据，强制执行特权规则，分离进程并应用访问控制。**PACBTI** 引入新技术来捕获可利用的常见软件错误并缓解返回导向编程 (ROP) 和跳转导向编程 (JOP) 等漏洞，从而增强了这些功能。

## 指针认证

返回导向编程 (ROP) 属于软件攻击，攻击者会破坏存储在堆栈中的指针（通常为返回地址），使其指向库中包含一段有效机器指令序列的某个位置。这些序列被称为 gadget，在大多数代码都很常见。通过将多个 gadget 串连在一起，攻击者可以误导程序，使其执行最终导致出现安全漏洞的操作，例如启动了交互式 shell。

[![图 1：Gadget 攻击代码](/media/2025/Armv8.1-M_PACBTI_Support_Gadget_Attack_Code.png)](/media/2025/Armv8.1-M_PACBTI_Support_Gadget_Attack_Code.png)

*图 1：Gadget 攻击代码 [1]*

指针认证是 Armv8.1-M Arm 架构可以使用的一项功能，可在面对此类攻击时提供一定的保护。指针认证代码 (PAC) 由给定指针的值、修饰符和密钥生成，用于在使用指针之前验证指针。
如果攻击者试图修改内存中的此类指针，他们还需要计算指针的正确 PAC 签名。以 ROP 为例，如果存储在堆栈中的返回地址在返回之前已经签名并验证，则攻击者将无法控制程序流程，从而引发异常。

## 分支目标识别

用于创建和识别有效分支着陆区的机制称为分支目标识别（BTI）。配置处理器时可以确保在启用 BTI 时，所有间接分支都必须以跳转目标地址最开头处标有 **BTI** 指令的着陆区作为目标。如果分支指令的目标地址没有着陆区，则处理器会触发异常。这样可以减少潜在目标地址的数量，从而减少可以通过 JOP 创建的潜在 gadget 的数量。

[![图 2：启用 BTI 后，间接分支必须以着陆区指令为目标](/media/2025/Armv8.1-M_PACBTI_Support.png_BTI_Enabled.png)](/media/2025/Armv8.1-M_PACBTI_Support.png_BTI_Enabled.png)

*图 2：启用 BTI 后，间接分支必须以着陆区指令为目标 [2]*

请参阅 [Stack-smashing-and-execution-permissions 文档](https://developer.arm.com/documentation/102433/0200/Stack-smashing-and-execution-permissions)，了解栈溢出、返回导向编程和跳转导向编程的更多信息。[博客](https://community.arm.com/arm-community-blogs/b/architectures-and-processors-blog/posts/armv8-1-m-pointer-authentication-and-branch-target-identification-extension)深入讨论了 Armv8.1-M PACBTI。

## FreeRTOS-Kernel 中的实现

FreeRTOS-Kernel 的 ARMv8.1-M 移植现已支持**指针认证和分支目标识别**安全功能。为了增强安全性，Arm 引入了任务专用 PAC 密钥的概念，即在任务初始化期间和调度过程中为每个任务分配一个 PAC 密钥。当任务被取消运行调度/受到调度开始运行时，任务的 PAC 密钥会存入任务上下文/从任务上下文恢复。这样，攻击者需要猜出每个任务的 PAC 密钥，才能通过返回导向编程来利用系统。如需了解实现细节相关的更多信息，请参阅 [ARMv8.1-M PACBTI 扩展](https://developer.arm.com/documentation/109576/0100/Pointer-Authentication-Code/Instructions)。

## PACBTI 演示的 FreeRTOS 示例

Arm 引入了托管在 [FreeRTOS-Partner-Supported-Demos 存储库](https://github.com/FreeRTOS/FreeRTOS-Partner-Supported-Demos)的下列示例，以演示 PACBTI 安全功能： 
* MPU 示例 [**CORTEX_M85_MPU_PXN_PACBTI_FVP_ARMCLANG_IAR**](https://github.com/FreeRTOS/FreeRTOS-Partner-Supported-Demos/tree/main/CORTEX_M85_MPU_PXN_PACBTI_FVP_ARMCLANG_IAR)
* 非 MPU 示例 [**CORTEX_M85_PACBTI_FVP_ARMCLANG_IAR**](https://github.com/FreeRTOS/FreeRTOS-Partner-Supported-Demos/tree/main/CORTEX_M85_PACBTI_FVP_ARMCLANG_IAR)
* 任务专用 PAC 密钥示例 [**CORTEX_M85_TASK_DEDICATED_PAC_KEY_FVP_ARMCLANG**](https://github.com/FreeRTOS/FreeRTOS-Partner-Supported-Demos/tree/main/CORTEX_M85_TASK_DEDICATED_PAC_KEY_FVP_ARMCLANG) 

这些示例基于 Corstone-315 生态系统固定虚拟平台（Arm Cortex-M85 CPU 和 Ethos-U65 NPU），可以免费下载和使用。

## 参考资料

1. Arm Ltd.*返回导向编程。*获取地址：[https://developer.arm.com/documentation/102433/0200/Return-oriented-programming](https://developer.arm.com/documentation/102433/0200/Return-oriented-programming)
2. Arm Ltd.*着陆区。*获取地址：[https://developer.arm.com/documentation/109576/0100/Branch-Target-Identification/Landing-pad](https://developer.arm.com/documentation/109576/0100/Branch-Target-Identification/Landing-pad)