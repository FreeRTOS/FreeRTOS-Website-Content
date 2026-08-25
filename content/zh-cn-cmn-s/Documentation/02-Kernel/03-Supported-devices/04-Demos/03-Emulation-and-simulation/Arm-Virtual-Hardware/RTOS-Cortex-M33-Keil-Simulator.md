---
title: "ARM Cortex-M33 (ARMv8-M) Keil 模拟器演示 使用 Keil uVision IDE"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

[![ARM Cortex-M33 核心](/media/2019/Keil_uVision_IDE.png)](/media/2019/Keil_uVision_IDE.png)

本页记录了一个预配置的 FreeRTOS 项目，该项目针对
[Keil uVision](http://www2.keil.com/mdk5/uvision/) ARM
[Cortex-M33](https://developer.arm.com/products/processors/cortex-m/cortex-m33)
模拟器，并使用 [armclang](https://developer.arm.com/docs/100067/0611)
编译器来构建 FreeRTOS ARMv8-M GCC 移植。该项目演示了如何使用
ARM Cortex-M33 TrustZone 和 ARM Cortex-M33 内存保护单元 (MPU)。

---

#### 重要！FreeRTOS ARM Cortex-M33 移植使用说明

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [构建并运行 RTOS 演示应用程序](#构建并运行-rtos-演示应用程序)
4. [RTOS 配置和使用详情](#rtos-配置和使用详情)

另请参阅常见问题中的[“我的应用程序无法运行，问题可能出在哪里？”](/Why-FreeRTOS/FAQs/Troubleshooting)、 
[介绍在 ARMv8-M 核心上运行 
FreeRTOS](/Community/Blogs/2020/using-freertos-on-armv8-m-microcontrollers.md) 的页面，以及介绍[设置 
ARM Cortex-M 中断优先级以与 FreeRTOS 配合使用](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4)的页面。 

---

### 源代码组织

FreeRTOS zip 文件下载内容中包含所有 FreeRTOS 移植的源代码及
所有演示应用程序。这意味着它包含的文件数量远多于
使用 FreeRTOS ARMv8-M Cortex-M33 移植所需的数量。有关此 zip 文件目录结构的信息，请参阅[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)页面。

此演示的项目文件位于 FreeRTOS/Demo/CORTEX_MPU_M33F_Simulator_Keil_GCC
目录中，名为 FreeRTOSDemo.uvmpw。此 Keil 多项目
工作区包含两个项目，一个项目适用于 ARM Cortex-M33 核心安全端，
另一个项目适用于非安全端。在这两个项目中编译的 FreeRTOS ARMv8-M Cortex-M33
移植文件组织如下：

* 在安全项目中编译的移植文件位于 FreeRTOS/Source/portable/GCC/ARM_CM33/secure 目录中。
* 在非安全项目中编译的移植文件位于 FreeRTOS/Source/portable/GCC/ARM_CM33/non_secure 目录中。

---

### 演示应用程序

该项目包括两个演示：
1. TrustZone 演示
2. 内存保护单元 (MPU) 演示

#### TrustZone 演示

TrustZone 演示展示了如何从
ARM Cortex-M33 核心的安全端导出函数，以及如何从非安全端的 RTOS 任务中调用
这些函数。
* 非安全可调用函数：

 以下函数从安全端导出，并标记为
 非安全可调用：

secureportNON_SECURE_CALLABLE uint32_t NSCFunction( Callback_t pxCallback )

**注意使用 secureportNON_SECURE_CALLABLE 宏
 将函数标记为非安全可调用**。此函数接受回调
 作为实参。它首先调用作为实参提供的回调函数，
 然后递增安全端计数器。安全端计数器的增量值
 将返回给调用者。
* 非安全回调：

 以下函数在非安全端实现，
 并作为实参传递给上述非安全可调用函数：

void prvCallback( void )

 此函数可递增非安全计数器。
* 安全调用任务：

 无特权的非安全任务
 [xTaskCreateRestricted()](/Documentation/02-Kernel/04-API-references/13-FreeRTOS-MPU-specific/01-xTaskCreateRestricted)
 是使用 API 创建的。此任务首先调用 portALLOCATE_SECURE_CONTEXT
 为自己分配安全上下文。**所有想要调用
 从安全端导出的函数的非安全任务都必须通过调用 portALLOCATE_SECURE_CONTEXT 为自己分配
 安全上下文**。

 然后，该任务调用安全端函数，并将非安全
 回调作为实参传递。非安全计数器在回调中递增，
 安全计数器在安全函数中递增。因此，
 在安全函数调用完成后，两个计数器都必须递增。
 要确保这一点，可使用 [configASSERT()](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert)。任务
 会休眠一秒钟，然后重复相同操作。

![TrustZone 演示调用序列](/media/2019/TZ_Demo.png)

**TrustZone 演示调用序列**

#### 内存保护单元 (MPU) 演示

MPU 演示展示了如何使用 MPU
向任务授予对不同内存区域的不同权限。MPU 演示包含以下两项任务：
* RW 任务：

 RW 任务对共享内存区域
 （即 ucSharedMemory）具有读写访问权限。
* RO 任务：

 RO 任务对同一共享内存区域
 （即 ucSharedMemory）具有只读访问权限。此任务会尝试写入
 共享内存，但由于对共享内存具有只读权限，
 因此会导致内存故障。故障处理程序可检查是否为
 RO 任务引发的预期故障。如果是，
 则会将程序计数器递增到下一条语句，以不引人注意的方式恢复正常。

---

### 构建并运行 RTOS 演示应用程序

1. 双击 FreeRTOS/Demo/CORTEX_MPU_M33F_Simulator_Keil_GCC/FreeRTOSDemo.uvmpw
 文件，在 Keil uVision IDE 中打开。Keil 多项目工作区
 FreeRTOSDemo.uvmpw 包含一个安全项目 (FreeRTOSDemo_s)
 和一个非安全项目 (FreeRTOSDemo_ns)。
2. 要将安全项目设置为活动项目，请右键单击 "Project: FreeRTOSDemo_s"，
 然后选择 "Set as Active Project"。

[![Keil uVision IDE - 将安全项目设置为活动项目](/media/2019/Keil_uVision_Sec_Proj_Active.png)](/media/2019/Keil_uVision_Sec_Proj_Active.png)

 Keil uVision IDE - 将安全项目设置为活动项目。点击放大。
3. 要构建安全项目，请依次单击 "Project" 和 "Build 'FreeRTOSDemo_s (FVP Simulation Model)'"。

[![Keil uVision IDE - 构建安全项目](/media/2019/Keil_uVision_Sec_Proj_Build.png)](/media/2019/Keil_uVision_Sec_Proj_Build.png)

 Keil uVision IDE - 构建安全项目。点击放大。
4. 要将非安全项目设置为活动项目，请右键单击 "Project: FreeRTOSDemo_ns"，
 然后选择 "Set as Active Project"。

[![Keil uVision IDE - 将非安全项目设置为活动状态](/media/2019/Keil_uVision_NonSec_Proj_Active.png)](/media/2019/Keil_uVision_NonSec_Proj_Active.png)

 Keil uVision IDE - 将非安全项目设置为活动状态。点击放大。
5. 要构建非安全项目，请依次单击 "Project" 和 "Build 'FreeRTOSDemo_ns (FVP Simulation Model)'"。

[![Keil uVision IDE - 构建非安全项目](/media/2019/Keil_uVision_NonSec_Proj_Build.png)](/media/2019/Keil_uVision_NonSec_Proj_Build.png)

 Keil uVision IDE - 构建非安全项目。点击放大。
6. 要启动调试会话，请依次单击 "Debug" 和 "Start/Stop Debug Session"。

[![Keil uVision IDE - 启动调试会话](/media/2019/Keil_uVision_Start_Debug_Session.png)](/media/2019/Keil_uVision_Start_Debug_Session.png)

 Keil uVision IDE - 启动调试会话。点击放大。

---

### RTOS 配置和使用详情

另请参阅[介绍在 ARMv8-M 核心上运行 
FreeRTOS](/Community/Blogs/2020/using-freertos-on-armv8-m-microcontrollers.md) 的页面以及介绍[设置 
ARM Cortex-M 中断优先级以与 FreeRTOS 配合使用](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4)的页面。 

* 此演示特定的配置项位于 FreeRTOS/Demo/CORTEX_MPU_M33F_Simulator_Keil_GCC/Config/FreeRTOSConfig.h 中。
 您可以编辑[该文件中定义的常量](/Documentation/02-Kernel/03-Supported-devices/02-Customization)，
 确保适配您的应用程序。以下配置选项
 特定于 ARM Cortex-M33 移植：

	+ configENABLE_MPU - 启用/禁用内存保护单元 (MPU)。
	+ configENABLE_FPU - 启用/禁用浮点单元 (FPU)。
	+ configENABLE_TRUSTZONE - 启用/禁用 TrustZone。
* 如果要在禁用 TrustZone 的情况下运行 FreeRTOS，
 请在 FreeRTOSConfig.h 中将 configENABLE_TRUSTZONE 设置为 0，并使用 FreeRTOS 移植文件
 （位于 FreeRTOS/Source/portable/GCC/ARM_CM33_NTZ 目录中）。
* 如果要在安全端运行 FreeRTOS，
 请在 FreeRTOSConfig.h 中将 configENABLE_TRUSTZONE 设置为 0，将 configRUN_FREERTOS_SECURE_ONLY 设置为 1，
 并使用 FreeRTOS/Source/portable/GCC/ARM_CM33_NTZ 目录中的 FreeRTOS 移植文件
 。
* 项目中包含的 Source/Portable/MemMang/heap_4.c
 可提供 RTOS 内核所需的内存分配。请
 参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
 以获取完整信息。
* vPortEndScheduler() 尚未实现。

