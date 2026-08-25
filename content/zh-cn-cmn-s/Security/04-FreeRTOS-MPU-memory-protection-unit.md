---
title: 内存保护单元 (MPU) 支持
date: 2022 年 1 月
---

[**有关将 FreeRTOS-MPU 项目更新到 FreeRTOS V10.5.0 的信息，请参阅升级部分**](#升级信息)

<span id="introduction"></span>
## 简介

FreeRTOS 为以下微控制器内核提供官方内存保护单元（MPU）支持：
ARMv7-M（Cortex-M3、Cortex-M4 和 Cortex-M7 微控制器）和
ARMv8-M（Cortex-M23 和 Cortex-M33 微控制器）内核：

- 有两个针对 ARMv7-M 内核的 FreeRTOS 移植，
  一个包括 MPU 支持，一个不包括。
- 只有一个 FreeRTOS 移植用于 ARMv8-M 内核，因为 
  [MPU 支持是一个编译时间选项](/2020/04/using-freertos-on-armv8-m-microcontrollers.html)。

第三方维护 MPU 到其他微控制器内核的移植。


<span id="mpu_benefits"></span>
#### MPU 成本和收益

FreeRTOS MPU 移植通过以下方式使微控制器应用程序更稳健、更安全：
首先，使任务能够在特权或非特权模式下运行；
其次，
限制对 RAM、可执行代码、外设和内存等资源的访问，
使其超出任务堆栈的限制。例如，
防止代码从 RAM 执行就能获得巨大好处。这样做可以防止许多攻击载体，
如缓冲区溢出漏洞
或加载到 RAM 中的恶意代码的执行。

使用 MPU 必然会使应用程序设计变得更加复杂，因为：
首先，必须确定 MPU 的内存区域限制，
并向 RTOS 说明；其次，MPU 限制应用任务能做什么、
不能做什么。


<span id="mpu_strategies"></span>
#### MPU 策略

创建一个应用程序，将每个任务都限制在自己的内存区域内，
可能是最安全的做法，
但也是设计和实施起来最复杂的做法。通常情况下，最好使用 MPU 来创建一个伪进程
和线程模型——允许一组线程共享一个内存
空间。例如，创建一个可供受信任的第一方代码访问的内存空间，
以及另一个仅供不受信任的第三方代码访问的内存空间
。


<span id="mpu_examples"></span>
#### 其他示例

LPC17xx 版 FreeRTOS 电子书中[有一章介绍如何使用 FreeRTOS-MPU](/MPU_Chapter.pdf)， 
尽管其中包含的信息
有些过时。

[在 ARMv8-M 微控制器上使用 FreeRTOS](/2020/04/using-freertos-on-armv8-m-microcontrollers.html)
的博客文章提到了在 ARMv8-M 微控制器上使用 MPU 的方法。

`FreeRTOS/Demo/CORTEX_MPU_Simulator_Keil_GCC` 目录中的演示项目
使用 Keil uVision 来构建和模拟 GCC 项目，
提供了一个不需要任何特殊硬件的工作实例。
其他 FreeRTOS-MPU 示例项目包括 [Nuvoton NuMaker-PFM-M2351 演示](/RTOS-Cortex-M23-NuMaker-PFM-M2351-Keil.html)
和 [NXP LPCXpresso55S69 演示](/RTOS-Cortex-M33-LPC55S69-MCUXpresso-GCC.html) 等。

\[FreeRTOS-MPU 演示项目——位于 FreeRTOS/Demo/CORTEX_MPU_LPC1768_GCC_RedSuite 和
FreeRTOS/Demo/CORTEX_MPU_LM3Sxxxx_Rowley 目录中，
在 FreeRTOS V9.0.0 发布前已停止使用\]


<span id="upgrade-information"></span>
#### 升级信息

已根据终端用户的反馈对 FreeRTOS MPU 移植进行了升级。
本节介绍升级到 FreeRTOS V10.6.2 或更高版本所需的更改，
以及在此之前，升级到 FreeRTOS V10.6.1、
V10.6.0、V10.5.0、V10.4.6、V10.4.0 和 V10.3.0 或更高版本所需的更改。

**FreeRTOS V10.6.2 中的更改：**   

FreeRTOS V10.6.2 对 V10.6.0 中引入的新 MPU 包装函数
(mpu_wrappers_v2.c) 做了以下改进：

- 引入访问控制列表（ACL）功能，
  允许应用程序写入器控制非特权任务
  对内核对象的访问。
- 更新系统调用输入机制，
  使其只需要一条监督员调用 (SVC) 指令。
- 将参数超过四个的系统调用的参数包在一个结构体中，
  以避免在系统调用输入时进行特殊处理。
- 修复了 2 个可能的整数溢出。
- 将一些断言转换为运行时检查。


** FreeRTOS 版本 10.6.1 中的更改：**

FreeRTOS V10.6.1 将运行时参数检查引入
mpu_wrappers_v2.c 文件中的函数。API 实现中已使用断言
执行了相同的检查。

我们感谢以下人士为这些更改提供的贡献：

1.  中国安徽工业大学计算机科学与技术学院的
    Lan Luo、Zixia Liu。
2.  美国马萨诸塞大学洛厄尔分校计算机科学系的
    Xinwen Fu。
3.  中国东南大学计算机科学与工程学院的
    Xinhui Shao、Yumeng Wei、Huaiyu Yan、Zhen Ling。


** FreeRTOS 版本 10.6.0 中的更改：**

FreeRTOS V10.6.0 引入了一个全新 MPU 包装函数，
对非特权任务施加了额外限制。以下是
随新 MPU 包装函数引入的更改列表：

- 内核对象句柄的不透明和间接可验证整数：
  所有内核对象句柄（例如队列句柄）现在都是
  不透明整数。以前，对象句柄是原始指针。

- 任务上下文保存在任务控制块（TCB）中： 
  当任务被调度器交换出去时，
  任务的上下文会保存在其 TCB 中。以前，任务的上下文保存在其
  堆栈中。

- 系统调用在单独的、仅限特权的堆栈上执行：FreeRTOS
  系统调用以更高的权限执行，现在使用单独的
  仅限特权的堆栈。以前，
  系统调用使用调用任务的堆栈。

- 内存边界检查：接受指针并取消引用的 FreeRTOS 系统调用，
  现在要验证调用任务是否拥有所需的权限，
  以访问指针引用的内存位置。

- 系统调用限制：以下系统调用不再
  可用于非特权任务：

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

  此外，非特权任务不能再使用 vTaskSuspend 挂起
  除自身以外的任何任务。

我们感谢以下人员对这些增强功能的贡献：

- Meta Platforms, Inc. 的 David Reiss。
- 中国东南大学计算机科学与工程学院的
  Lan Luo、Xinhui Shao、Yumeng Wei、Zixia Liu、Huaiyu Yan 和 Zhen Ling
  。
- 美国马萨诸塞大学洛厄尔分校计算机科学系的
  Xinwen Fu。
- 美国科罗拉多大学博尔德分校的
  Yueqi Chen、Zicheng Wang、Minghao Lin 和 Jiahe Wang。


**FreeRTOS 10.5.0 版中的更改：**

- FreeRTOS ARMv7-M (ARM Cortex-M3/4/7) 和 ARMv8-M (ARM
  Cortex-M23/33/55）移植，支持内存保护单元（MPU），
  不再能够使用 xTaskCreate 或 xTaskCreateStatic API
  从非特权任务创建特权任务。另外，非特权任务
  无法再调用以下 API：

  - xTimerCreate
  - xTimerCreateStatic
  - xTimerPendFunctionCall

  应用程序写入器需要在
  启动调度器之前或从特权任务中执行这些操作。


**FreeRTOS 10.4.6 版中的更改：**

- 用于 ARMv7-M MCU (ARM Cortex-M3/4/7) 的 FreeRTOS-MPU 移植现在包含
  新的配置选项
  `configALLOW_UNPRIVILEGED_CRITICAL_SECTIONS`。在
  FreeRTOSConfig.h 中将该常量设置为 0 可防止非特权应用程序任务使用
  `taskENTER_CRITICAL()` 宏创建临界区
  。将该常量设置为 1，
  或不对其进行定义则可维持与先前 FreeRTOS 内核版本的兼容性，后者同时允许
  特权任务和非特权任务创建临界区。
  注意：建议将此常量定义为 0，以获得最高的安全性。
  因此，如果未定义该常量，
  将输出编译器警告。


**FreeRTOS 10.4.0 版中的更改：**

- FreeRTOS V10.4.0 引入了一个新变量 `__privileged_functions_start__` 
  来指示特权代码的起始位置
  。它需要从链接器脚本中导出，
  导出方式与 
  [`__privileged_functions_end__`](/MPU_Chapter.pdf)  等已有链接器变量相同。
    
  如果在早期创建的项目中
  因未解决的符号 `__privileged_functions_start__` 而出现链接器错误，
  则需要导出一个变量 `__privileged_functions_start__`，其值
  等于 `__FLASH_segment_start__`。

- 堆内存现在被放在特权区，因此，
  非特权任务无法 
  调用 [`pvPortMalloc()`](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) 或 
  [`vPortFree()`](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)。

- [`xTaskCreate()`](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate) 不能再用于创建
  非特权任务。请使用 [`xTaskCreateRestricted()`](/Documentation/02-Kernel/04-API-references/13-FreeRTOS-MPU-specific/01-xTaskCreateRestricted/) 代替。

- 适用于 ARM Cortex-M4 微控制器的 FreeRTOS-MPU 移植
  现在支持带有 16 个 MPU 区域的微控制器。要使用这 16 个区域，
  需在 [`FreeRTOSConfig.h`](/Documentation/02-Kernel/03-Supported-devices/02-Customization/) 中将 `configTOTAL_MPU_REGIONS` 设置为 16。

- 应用程序写入器现在可以
  覆盖 TEX、可共享 (S)、可缓存 (C) 和可缓冲 (B) 位的默认值（属于 MPU 区域，
  该区域涵盖闪存和 RAM），具体做法是通过分别定义 `configTEX_S_C_B_FLASH`
  和 `configTEX_S_C_B_SRAM`（在 [`FreeRTOSConfig.h`](/Documentation/02-Kernel/03-Supported-devices/02-Customization/) 中定义）。


**FreeRTOS 10.3.0 版中的更改：**

- 现在可以防止来自内核代码之外的任何权限升级
  （硬件本身在进入中断时执行的升级除外）
  。要实现这一点， 
  需将 `configENFORCE_SYSTEM_CALLS_FROM_KERNEL_ONLY` 设置为 1 
  （在 [`FreeRTOSConfig.h`](/Documentation/02-Kernel/03-Supported-devices/02-Customization/) 中设置），并将链接器 
  变量 [`__syscalls_flash_start__`](https://github.com/FreeRTOS/FreeRTOS/blob/V10.3.1/FreeRTOS/Demo/CORTEX_MPU_STM32L4_Discovery_GCC_IAR_Keil/Projects/GCC/STM32L475VGTX_FLASH.ld#L113)
  和 [`__syscalls_flash_end__`](https://github.com/FreeRTOS/FreeRTOS/blob/V10.3.1/FreeRTOS/Demo/CORTEX_MPU_STM32L4_Discovery_GCC_IAR_Keil/Projects/GCC/STM32L475VGTX_FLASH.ld#L115)
  分别定义为系统调用内存的起始和终止地址。


<span id="mpu-specifics"></span>
## FreeRTOS-MPU 特定

<span id="mpu_features"></span>
#### FreeRTOS-MPU 功能

- 与标准 ARM Cortex-M3 和 Cortex-M4F 移植相兼容。

- 可以创建任务在特权模式或非特权模式下运行
  。非特权
  任务只能访问自己的堆栈和最多三个用户可定义的内存区域（每个任务三个）
  。创建任务时，将用户可定义的内存区域分配给任务，
  如果需要，可以在运行时重新配置。

- 用户可定义内存区域可以单独参数化。例如，
  某些区域可设置为只读，而其他区域可设置为不可执行
  （永不执行，或在 ARM 术语简称为 XN）
  等。

- 非特权任务之间没有共享数据内存，
  但非特权任务可以
  使用标准队列和信号量机制将消息传递给彼此。可通过使用用户可定义的内存区域明确创建共享内存区域，
  但不推荐这样做
  。

- 特权模式任务可以将自己设置为非特权模式，
  但一旦进入非特权模式，就无法将自己设置回特权模式
  。

- FreeRTOS 的 API 位于闪存中的一个区域，
  只有在微控制器处于特权模式时才能访问
  （调用 API 函数会暂时切换到特权模式）。

- 由 RTOS 内核维护的数据
  （所有 FreeRTOS 源文件专有的非堆栈数据）位于 RAM
  中的一个区域，只有在微控制器处于特权模式时才能访问
  。

- 只有在微控制器处于特权模式时
  方可访问系统外围设备。标准
  外围设备（UART 等）可被任何代码访问，
  但可以使用用户可定义的内存区域进行明确保护。

  
<span id="creating_tasks"></span>
#### 创建任务

FreeRTOS-MPU 移植可以有两种类型的任务：

1. **<span class="underline">特权任务：</span>**
   特权任务可以访问整个内存映射。可以
   使用 [xTaskCreate()](/Documentation/02-Kernel/04-API-references/01-Task-creation/01-xTaskCreate) 
   或 [xTaskCreateRestricted()](/Documentation/02-Kernel/04-API-references/13-FreeRTOS-MPU-specific/01-xTaskCreateRestricted/) API 函数创建特权任务。

2. **<span class="underline">非特权任务：</span>**
   非特权任务只能访问自己的堆栈。此外，
   还可以授予它最多三个用户可定义内存区域的访问权限（每个任务三个）
   。只能使用 
   [xTaskCreateRestricted()](/Documentation/02-Kernel/04-API-references/13-FreeRTOS-MPU-specific/01-xTaskCreateRestricted/) API 创建非特权任务。
   **请注意，请勿使用 xTaskCreate() API 创建非特权任务。**

如果任务想要使用 MPU，
则必须提供以下附加信息：

- 任务堆栈的地址。
- 最多三个用户可定义内存区域的起始参数、大小参数和访问参数
  。

因此，创建任务所需的参数总数相当大
。为了更轻松创建 MPU 感知任务，FreeRTOS-MPU
会使用名为 [xTaskCreateRestricted()](/Documentation/02-Kernel/04-API-references/13-FreeRTOS-MPU-specific/01-xTaskCreateRestricted/) 的 API 函数。 
这使得除一个参数外的所有参数都被定义在一个常量结构体中，
并将该结构体作为单个参数（通过引用）传入 xTaskCreateRestricted()
。

特权模式任务可以通过调用 [portSWITCH_TO_USER_MODE()](/portSWITCH_TO_USER_MODE.html) 
将自身设置为非特权模式。以非特权模式运行的任务
无法将自己设置为特权模式。

可使用 
[vTaskAllocateMPURegions()](/vTaskAllocateMPURegions.html) 更改分配给任务的内存区域。请参阅
xTaskCreateRestricted() and vTaskAllocateMPURegions() API 文档
了解更多信息。

