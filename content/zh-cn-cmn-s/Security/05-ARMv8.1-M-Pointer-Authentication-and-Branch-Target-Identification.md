---
title: ARMv8.1-M 指针认证和分支目标识别 (PACBTI) 支持
date: 2025 年 2 月
---

<span id="introduction"></span>
## 引言

Armv8-M 包含强大的安全和内存保护功能，例如适 Armv8-M 的 TrustZone、内存保护单元 (MPU) 和特权模式下永不执行 (PXN)。这些功能可有效隔离关键安全固件和私有数据，强制执行特权规则，分离进程并应用访问控制。 
Armv8.1-M 架构引入了**指针认证**和**分支目标识别**扩展（也称为 **PACBTI**）。该扩展引入新技术来检测返回导向编程 (ROP) 和跳转导向编程 (JOP) 漏洞，从而增强了这些功能。在返回导向编程中，函数返回前的指令用于在可执行代码区域内构建 [gadget](https://developer.arm.com/documentation/102433/0200/Return-oriented-programming)。同样，在跳转导向编程中，函数调用或 switch-case 语句（间接跳转）之前的指令用于在可执行代码区域中构建 gadget。

[![图 1：Gadget 攻击代码](/media/2025/Armv8.1-M_PACBTI_Support_Gadget_Attack_Code.png)](/media/2025/Armv8.1-M_PACBTI_Support_Gadget_Attack_Code.png)

*图 1：Gadget 攻击代码 [1]*

请参阅 [Stack-smashing-and-execution-permissions 文档](https://developer.arm.com/documentation/102433/0200/Stack-smashing-and-execution-permissions)，了解栈溢出、返回导向编程和跳转导向编程的更多信息。[博客](https://community.arm.com/arm-community-blogs/b/architectures-and-processors-blog/posts/armv8-1-m-pointer-authentication-and-branch-target-identification-extension)深入讨论了 Armv8.1-M PACBTI。
PACBTI 旨在捕获可利用的常见软件错误，但它并不是所有 ROP 和 JOP 攻击的终极解决方案。PACBTI 依赖于强大的软件模型。在此类模型中与良好的软件开发实践相结合时，它可以成为强大的工具。PACBTI 扩展的合理编译器实现应确保所有 PAC 和 BTI 功能都正确插入已编译的代码。


<span id="pointer authentication"></span>
## 指针认证

<span id="pointer authentication code creation"></span>
#### 指针认证代码创建

PAC 功能的一项主要用途是检测函数调用中返回地址的损坏情况。由于返回地址通常存储在堆栈中，因此存在堆栈损坏可能更改返回地址的风险，导致攻击有机可乘。创建指针认证代码 (PAC) 的过程可以称为对指针进行签名。如需创建 PAC，要将相关指针、修饰符和密钥输入加密机制，然后此机制生成 32 位固定长度的代码，称为指针认证代码。PAC 指令使用固定寄存器（即链接寄存器 (LR) 作为指针、栈指针 (SP) 作为修饰符）和 R12 存储生成的 PAC。此操作如下图所示，其中：

- **PAC**：32 位认证代码。
- **修饰符 (MOD)**：来自输入寄存器的 32 位值。
- **指针 (PTR)**：需要保护的地址。
- **密钥**：128 位密钥。
- **加密机制**：示例：[QARMA](https://eprint.iacr.org/2016/444.pdf)。

[![图 2：创建 PAC](/media/2025/Armv8.1-M_PACBTI_Support_Creating_PAC.png)](/media/2025/Armv8.1-M_PACBTI_Support_Creating_PAC.png)

*图 2：创建 PAC [2]*

修饰符必须是未更改的值，在函数的开始和结束必须具有相同的值。因此栈指针 (SP) 可以用作修饰符，在函数执行期间其值可以更改，但是函数结束的值将与刚开始的值相同。

<span id="pointer authentication code validation"></span>
#### 指针认证代码验证

编译器在函数结束时插入认证指令 (**aut**)，将函数刚开始时创建的 PAC 与函数执行后创建的 PAC 加以比较 (**PACreturn**) ，这两个值必须完全相同，表示以下任何一项均未损坏：

* 指针。
* 修饰符。
* 密钥。
* 原始 PAC。

如果原始 PAC 与 **PACreturn** 不匹配，则认证指令会生成 **INVSTATE** UsageFault 异常。任何推测执行的指令都应终止，确保不会因指针、修饰符、密钥或 PAC 损坏而产生明显的不良后果。

[![图 3：验证 PAC](/media/2025/Armv8.1-M_PACBTI_Support_Validating_PAC.png)](/media/2025/Armv8.1-M_PACBTI_Support_Validating_PAC.png)

*图 3：验证 PAC [2]*

<span id="branch target identification"></span>
## 分支目标识别

用于创建和识别有效分支着陆区的机制称为分支目标识别（BTI）。配置处理器时可以确保在启用 BTI 时，所有间接分支都必须以着陆区作为目标。如果分支指令的目标地址没有着陆区，则处理器会触发异常。这样可以减少潜在目标地址的数量，从而减少可以通过 JOP 创建的潜在 gadget 的数量。
这些跳转指令被称为 **BTI 设置**指令，在执行时会将特定位 (**EPSR.B**) 设置为 1。**BTI 清除**或**着陆区**指令会将 **EPSR.B** 清除为零。BTI 设置指令后面必须始终跟着 BTI 清除指令，否则将触发 **INVSTATE** UsageFault 异常。下图描述了通用的 Armv8.1-M BTI 行为模型：

[![图 4：BTI 行为](/media/2025/Armv8.1-M_PACBTI_Support_BTI_Behavior.png)](/media/2025/Armv8.1-M_PACBTI_Support_BTI_Behavior.png)

*图 4：BTI 行为 [2]*

生成异常时，**EPSR** 会被正常压入堆栈，因此 **EPSR.B** 的状态会被保存。进入处理程序之前，由于可能无法在处理程序中启动 BTI，**EPSR.B** 会被清除为零。处理程序将终止线程，因为任何授权失败都清晰表明存在篡改。

<span id="implementation in FreeRTOS-Kernel"></span>
## FreeRTOS-Kernel 中的实现

<span id="configurability"></span>
#### 可配置性

PACBTI 是 Armv8.1-M 中引入的可选扩展。虽然只是可选，但 Arm 强烈建议使用 PACBTI 安全功能。如果是在硬件中实现，那么 PACBTI 必须一起实现。不过，可以使用控制寄存器单独启用/禁用此扩展。此外，可以使用编译器选项单独启用/禁用 PACBTI。因此，我们引入了内核配置选项来支持可能的不同 PACBTI 配置。

<span id="for cmake projects"></span>
#### 对于 CMake 项目

当用户选择以下任意一项配置时，将自动设置适当的工具链选项：

| **配置选项** | **值** | **描述** |
|--------------------------|-----------|---------------|
| **FREERTOS_ARM_V_8_1_M_PACBTI_CONFIG** | **ARM_V_8_1_M_PACBTI_CONFIG_STANDARD** | PACBTI 安全功能标准配置（无叶函数支持的情况下启用 PAC，同时启用 BTI）。 |
| | **ARM_V_8_1_M_PACBTI_CONFIG_PACRET_LEAF_BTI** | PACBTI 安全功能标准 + Leaf 配置（PAC 具有叶函数支持，同时启用 BTI）。 |
| | **ARM_V_8_1_M_PACBTI_CONFIG_PACRET** | 仅启用 PAC 的 PACBTI 安全功能。 |
| | **ARM_V_8_1_M_PACBTI_CONFIG_PACRET_LEAF** | PAC 和用于叶函数支持的 PAC 都已启用的 PACBTI 安全功能。 |
| | **ARM_V_8_1_M_PACBTI_CONFIG_BTI** | 仅启用 BTI 的 PACBTI 安全功能。 |
| | **ARM_V_8_1_M_PACBTI_CONFIG_NONE** | PACBTI 安全功能已禁用。 |

**请注意：**
**对于 CMake 项目**，如果用户选择启用 PAC 和/或 BTI，则应为内核代码之外的所有已编译代码（即应用程序、库等等）设置适当的工具链选项。

<span id="for non-cmake projects"></span>
#### 对于非 CMake 项目

用户可以通过以下 C 配置宏选择是否启用/禁用 PAC 和/或 BTI：

| **C 配置宏** | **值** | **描述** |
|--------------------------|-----------|---------------|
| **configENABLE_PAC** | **1** | PAC 安全功能已启用。 |
| | **0** | PAC 安全功能已禁用。 |
| **configENABLE_BTI** | **1** | BTI 安全功能已启用。 |
| | **0** | BTI 安全功能已禁用。 |

**请注意：**
**对于非 CMake 项目**，如果用户选择启用 PAC 和/或 BTI，则应为所有已编译代码（即应用程序、内核代码、库等等）设置适当的工具链选项。
**同时启用 PAC 和 BTI 的情况下设置适当 ARMClang 工具链选项的示例**
```sh
armclang —target=arm-arm-none-eabi -march=armv8.1-m.main+pacbti -mbranch-protection=bti+pac-ret source.c -c -o source.o
armlink source.o —library_security=pacbti-m -o output.elf
```

**prvConfigurePACBTI** 函数在调度器启动过程中（即在第一个任务启动之前）调用，以根据用户配置来配置特殊用途控制寄存器 PAC 和 BTI 位。

<span id="dedicated pac key for each task"></span>
#### 每项任务都有专用 PAC 密钥

为了增强安全性，在任务初始化过程中，每项任务都被分配了一个专用 PAC 密钥。这样，攻击者需要猜出每个任务的 PAC 密钥，才能通过返回导向编程来利用系统。
内核现支持以下各项：

* 创建任务时，会使用生成的随机数设置 PAC 密钥并将其保存到任务的上下文中。
* 调度过程中，当任务被取消运行调度/受到调度开始运行时，任务的 PAC 密钥会存入任务的上下文/从任务的上下文恢复。

**随机数生成**

内核通过实现 **vApplicationGenerateTaskRandomPacKey** API，即启用 PAC 时内核在 ARMv8.1-M 移植代码中需要的 API， 
让用户能够实现自己的随机数生成器函数。预计此函数将接受指向 4 字（128 位）数组的指针，该数组由代表任务 PAC 密钥的 128 位随机数填充。

<span id="FreeRTOS examples demonstrating PACBTI"></span>
## PACBTI 演示的 FreeRTOS 示例

Arm 引入了托管在 [FreeRTOS-Partner-Supported-Demos 存储库](https://github.com/FreeRTOS/FreeRTOS-Partner-Supported-Demos)的下列示例，以演示 PACBTI 安全功能： 
* MPU 示例 [**CORTEX_M85_MPU_PXN_PACBTI_FVP_ARMCLANG_IAR**](https://github.com/FreeRTOS/FreeRTOS-Partner-Supported-Demos/tree/main/CORTEX_M85_MPU_PXN_PACBTI_FVP_ARMCLANG_IAR)
* 非 MPU 示例 [**CORTEX_M85_PACBTI_FVP_ARMCLANG_IAR**](https://github.com/FreeRTOS/FreeRTOS-Partner-Supported-Demos/tree/main/CORTEX_M85_PACBTI_FVP_ARMCLANG_IAR)
* 任务专用 PAC 密钥示例 [**CORTEX_M85_TASK_DEDICATED_PAC_KEY_FVP_ARMCLANG**](https://github.com/FreeRTOS/FreeRTOS-Partner-Supported-Demos/tree/main/CORTEX_M85_TASK_DEDICATED_PAC_KEY_FVP_ARMCLANG) 

这些示例演示了如何在 Cortex-M85 处理器上使用 Armv8.1-M 架构扩展中引入的指针认证和分支目标识别 (PACBTI) 这一全新安全功能。为了增强安全性，MPU 和非 MPU 示例包括了在 Armv8.1-M 处理器安全端运行的 [TrustedFirmware-M](https://www.trustedfirmware.org/projects/tf-m/)、FreeRTOS-Kernel 以及在 Armv8.1-M 处理器的非安全端运行的应用程序任务。这三个示例基于 Corstone-315 生态系统固定虚拟平台（Arm Cortex-M85 CPU 和 Ethos-U65 NPU）。
MPU 和非 MPU 示例包含两个测试（即指针认证测试和分支目标识别测试）。在指针认证测试中，FreeRTOS 任务将调用会篡改堆栈中保存的链接寄存器 (LR) 值的一个应用程序函数，然后在调用的函数结束时验证指针认证代码。这将导致 aut（认证指令）失败，从而触发 UsageFault 异常。
在分支目标识别测试期间，FreeRTOS 任务将尝试跳转到某个应用程序函数中间，这样由于跳转到的地址并非 BTI 清除指令，因此将导致触发 UsageFault 异常。UsageFault 异常处理程序旨在通过检查异常是否为故意触发来正常恢复。
而任务专用 PAC 密钥示例则包含两个主要任务。这些任务用于确保任务中随机生成的 PAC 密钥在未被修改的情况下得到可靠地存储/恢复。
这些任务执行以下序列：
1. 每项任务开始运行后，获取随机生成的专用 PAC 密钥。
2. 通过调用 vTaskDelay() 函数将任务移至阻塞状态。
3. 作为上下文切换处理程序的一部分，任务的 PAC 密钥将在任务解除阻塞后恢复，其中阻塞前后的 PAC 密钥值应相同，以证明任务专用 PAC 密钥存储/恢复程序安全可靠。
4. 如果阻塞前后任务的 PAC 密钥不相同，则会触发 configASSERT() 语句。


<span id="references"></span>
## 参考资料

1. Arm Ltd.*返回导向编程。*获取地址：[https://developer.arm.com/documentation/102433/0200/Return-oriented-programming](https://developer.arm.com/documentation/102433/0200/Return-oriented-programming)
2. Mujumdar, A. *Armv8.1-M 指针认证和分支目标识别扩展。*获取地址：[https://community.arm.com/arm-community-blogs/b/architectures-and-processors-blog/posts/armv8-1-m-pointer-authentication-and-branch-target-identification-extension](https://community.arm.com/arm-community-blogs/b/architectures-and-processors-blog/posts/armv8-1-m-pointer-authentication-and-branch-target-identification-extension)
