---
title: "适用于 Nuvoton NuMaker-PFM-M2351 板的 ARM Cortex-M23 (ARMv8-M) 演示"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

使用 Keil uVision 和 IAR IDE

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

[\![](/media/2019/Nuvoton_Numaker_PFM_M2351.png)](/media/2019/Nuvoton_Numaker_PFM_M2351.png)

本页面记录预配置的 FreeRTOS 项目，该项目面向
[ARM Cortex-M23](https://developer.arm.com/products/processors/cortex-m/cortex-m23) 核心
[Nuvoton NuMaker-PFM-M2351](https://www.nuvoton.com/products/iot-solution/iot-platform/numaker-pfm-m2351/)
板上）。

提供了如下两个项目：

1. [IAR Embedded Workbench](https://www.iar.com/iar-embedded-workbench/) 项目，
   该项目使用 IAR 编译器。
2. 一个 [Keil uVision](http://www2.keil.com/mdk5/uvision/) 项目，
   该项目使用 [armclang](https://developer.arm.com/docs/100067/0611)
   编译器。

这些项目演示如何使用 ARM Cortex-M23 TrustZone 和 ARM
Cortex-M23 内存保护单元 (MPU)。

---

#### 重要提示！FreeRTOS ARM Cortex-M23 移植使用说明

_使用此 RTOS 移植前,请阅读下述所有要点。_

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [构建并运行 RTOS 演示应用程序](#构建和运行-rtos-演示应用程序)
4. [RTOS 配置和使用详情](#rtos-配置和使用详情)

另请参阅常见问题中的[“我的应用程序无法运行，问题可能出在哪里？”](/Why-FreeRTOS/FAQs/Troubleshooting)、
[介绍在 ARMv8-M 核心上运行
FreeRTOS](/Community/Blogs/2020/using-freertos-on-armv8-m-microcontrollers) 的页面，以及介绍[设置 
ARM Cortex-M 中断优先级以与 FreeRTOS 配合使用](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4)的页面。

---

### 源代码组织

FreeRTOS zip 文件下载内容中包含所有 FreeRTOS 移植的源代码及
所有演示应用程序。这意味着它包含的文件数量比
使用 FreeRTOS ARMv8-M Cortex-M23 移植所需的多得多。有关此 zip 文件目录结构的信息，请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)页面。
此演示的项目文件组织如下：

- IAR Embedded Workbench 项目文件位于
  FreeRTOS/Demo/CORTEX_MPU_M23_Nuvoton_NuMaker_PFM_M2351_IAR_GCC/Projects/IAR
  目录并命名为 FreeRTOSDemo.eww。此 IAR工作区包含两个项目——
  一个用于 ARM Cortex-M23 核心安全端，
  另一个用于非安全端。这两个项目中编译的 FreeRTOS ARMv8-M Cortex-M23 移植文件
  组织如下：

  - 在安全端项目中编译的移植文件位于 FreeRTOS/Source/portable/IAR/ARM_CM23/secure 目录下
  - 在非安全端项目中编译的移植文件位于 FreeRTOS/Source/portable/IAR/ARM_CM23/non_secure 目录下。

- Keil uVision 项目文件位于
  FreeRTOS/Demo/CORTEX_MPU_M23_Nuvoton_NuMaker_PFM_M2351_IAR_GCC/Projects/Keil
  目录中，名为 FreeRTOSDemo.uvmpw。这个 Keil 多项目
  工作区包含两个项目，一个是 ARM Cortex-M23 核心安全端项目，
  另一个用于非核心安全端。在这两个项目中编译的 FreeRTOS ARMv8-M Cortex-M23
  移植文件组织如下：

  - 在安全端项目中编译的移植文件位于 FreeRTOS/Source/portable/GCC/ARM_CM23/secure 目录下。
  - 在非安全端项目中编译的移植文件位于 FreeRTOS/Source/portable/GCC/ARM_CM23/non_secure 目录下。

---

### 演示应用程序

这些项目包括两个演示：

1. TrustZone 演示
2. 内存保护单元 (MPU) 演示

#### TrustZone 演示

TrustZone 演示展示了如何从
ARM Cortex-M23 核心安全端导出函数，以及如何从非安全端的 RTOS 任务中
调用这些函数。

- 非安全可调用函数：

以下函数从安全端导出，并标记为
非安全可调用：

secureportNON_SECURE_CALLABLE uint32_t NSCFunction( Callback_t pxCallback )

**注意使用 secureportNON_SECURE_CALLABLE 宏
将函数标记为非安全可调用**。此函数接受回调
作为实参。它首先调用作为实参提供的回调函数，
然后递增安全端计数器。安全端计数器的增量值
将返回给调用者。

- 非安全回调：

以下函数在非安全端实现，
并作为实参传递给上述非安全可调用函数：

void prvCallback( void )

此函数可递增非安全计数器。

- 安全调用任务：

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
授予各个内存区域的任务特定访问许可。MPU 演示包含以下两个任务：

- RW 任务：

RW 任务对共享内存区域
（即 ucSharedMemory）具有读写访问权限。

- RO 任务：

RO 任务对同一共享内存区域
（即 ucSharedMemory）具有只读访问权限。此任务会尝试写入
且由于它拥有对共享内存的只读权限，
因此会导致硬故障。故障处理程序检查它是否
RO 任务引发的预期故障。如果是，
则会将程序计数器递增到下一条语句，以不引人注意的方式恢复正常。

---

### 构建和运行 RTOS 演示应用程序

#### 使用 IAR Embedded Workbench IDE

1. 下载并安装 Nu-Link USB 驱动程序：

   - 前往以下页面：
     [Nuvoton NuMaker-PFM-M2351](https://www.nuvoton.com/products/iot-solution/iot-platform/numaker-pfm-m2351/?group=Software&tab=2)
   - 单击 “Resources” 选项卡。
   - 向下滚动到 “Software” 部分，然后下载名为 Nu-Link_IAR_Driver_Vx.xx.xxxx 的文件。
   - 解压缩并安装。

2. 双击 FreeRTOS/Demo/CORTEX_MPU_M23_Nuvoton_NuMaker_PFM_M2351_IAR_GCC/Projects/IAR/FreeRTOSDemo.eww
   在 IAR Embedded Workbench IDE 中打开它。IAR 工作区
   FreeRTOSDemo.eww 包含一个安全项目 (FreeRTOSDemo_s)
   以及一个非安全项目 (FreeRTOSDemo_ns)。
3. 通过右键单击 “FreeRTOSDemo_s - Release”，然后单击 “Make” 来构建安全项目。

[![IAR Embedded Workbench IDE - 构建安全项目](/media/2019/Nuvoton_Numaker_PFM_M2351_IAR_Sec_Proj_Build.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_IAR_Sec_Proj_Build.png)

IAR Embedded Workbench IDE - 构建安全项目点击放大。4. 通过右键单击 “FreeRTOSDemo_ns - Release”，然后单击 “Make” 来构建非安全项目。

[![IAR Embedded Workbench IDE - 构建非安全项目](/media/2019/Nuvoton_Numaker_PFM_M2351_IAR_NonSec_Proj_Build.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_IAR_NonSec_Proj_Build.png)

IAR Embedded Workbench IDE - 构建非安全项目。点击放大。5. 右键单击 "FreeRTOSDemo_ns - Release"，
然后单击 “Set as Active”，将非安全项目设置为活动项目。

[![IAR Embedded Workbench IDE - 设置非安全项目为活动项目](/media/2019/Nuvoton_Numaker_PFM_M2351_IAR_NonSec_Proj_Active.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_IAR_NonSec_Proj_Active.png)

IAR Embedded Workbench IDE - 设置非安全项目为活动项目。点击放大。6. 单击 “Project -- Download -- Download active application” 来闪烁非安全二进制文件。

[![IAR Embedded Workbench IDE - 闪烁非安全二进制文件](/media/2019/Nuvoton_Numaker_PFM_M2351_IAR_NonSec_Proj_Download.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_IAR_NonSec_Proj_Download.png)

IAR Embedded Workbench IDE - 闪烁非安全二进制文件。点击放大。7. 右键单击 "FreeRTOSDemo_s - Release"，
然后单击 “Set as Active”，将安全项目设置为活动项目。

[![IAR Embedded Workbench IDE - 设置安全项目为活动项目](/media/2019/Nuvoton_Numaker_PFM_M2351_IAR_Sec_Proj_Active.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_IAR_Sec_Proj_Active.png)

IAR Embedded Workbench IDE - 设置安全项目为活动项目。点击放大。8. 单击 “Project -- Download -- Download active application” 来闪烁安全二进制文件。

[![IAR Embedded Workbench IDE - 闪烁安全二进制文件](/media/2019/Nuvoton_Numaker_PFM_M2351_IAR_Sec_Proj_Download.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_IAR_Sec_Proj_Download.png)

IAR Embedded Workbench IDE - 闪烁安全二进制文件。点击放大。9. 单击 “Project -- Download and Debug” 启动调试会话。

[![IAR Embedded Workbench IDE - 启动调试会话](/media/2019/Nuvoton_Numaker_PFM_M2351_IAR_Debug_Session.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_IAR_Debug_Session.png)

IAR Embedded Workbench IDE - 启动调试会话。点击放大。

#### 使用 Keil uVision IDE

1. 下载并安装 Nu-Link Keil 驱动器：

   - 转到以下页面：[Nuvoton NuMaker-PFM-M2351](https://www.nuvoton.com/hq/products/iot-solution/iot-platform/numaker-maker-platform/numaker-pfm-m2351/?__locale=en)
   - 单击 “Resources” 选项卡。
   - 向下滚动到 “Software” 部分，然后下载名为 Nu-Link_Keil_Driver_Vx.xx.xxxx 的文件。
   - 解压缩并安装。

2. 双击 FreeRTOS/Demo/CORTEX_MPU_M23_Nuvoton_NuMaker_PFM_M2351_IAR_GCC/Projects/Keil/FreeRTOSDemo.uvmpw
   文件，在 Keil uVision IDE 中打开。Keil 多项目工作区
   FreeRTOSDemo.uvmpw 包含一个安全项目 (FreeRTOSDemo_s)
   和一个非安全项目 (FreeRTOSDemo_ns)。
3. 要将安全项目设置为活动项目，请右键单击 "Project: FreeRTOSDemo_s"，
   然后选择 "Set as Active Project"。

[![Keil uVision IDE - 将安全项目设置为活动项目](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_Sec_Proj_Active.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_Sec_Proj_Active.png)

Keil uVision IDE - 将安全项目设置为活动项目。点击放大。4. 单击 "Project --> Build 'FreeRTOSDemo_s (FreeRTOSDemo_s)'" 构建安全项目。

[![Keil uVision IDE - 构建安全项目](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_Sec_Proj_Build.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_Sec_Proj_Build.png)

Keil uVision IDE - 构建安全项目。点击放大。5. 单击 "Project --> Options for FreeRTOSDemo_s - Target 'FreeRTOSDemo_s'..."，打开安全项目的选项窗口。

[![Keil uVision IDE - 打开安全项目选项](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_Sec_Proj_Options.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_Sec_Proj_Options.png)

Keil uVision IDE - 打开安全项目选项。点击放大。6. 通过单击 Debug 选项卡中 "Nuvoton Nu-Link Debugger" 旁边的 “Settings” 按钮，打开 Nu-Link 驱动器设置窗口。

[![Keil uVision IDE - 打开 Nu-Link 驱动器设置](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_Sec_Proj_Debugger_1.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_Sec_Proj_Debugger_1.png)

Keil uVision IDE -打开 Nu-Link 驱动器设置。点击放大。7. 在 “Chip Type” 下拉菜单中选择 “M2351”。

[![Keil uVision IDE - 选择 M2351](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_Sec_Proj_Debugger_2.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_Sec_Proj_Debugger_2.png)

Keil uVision IDE - 选择 M2351。点击放大。8. 单击窗口上的 “OK”，关闭 “Nu-Link Driver Setup” 和 “Options” 窗口。9. 要将非安全项目设置为活动项目，请右键单击 "Project: FreeRTOSDemo_ns"，
然后选择 "Set as Active Project"。

[![Keil uVision IDE - 将非安全项目设置为活动状态](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_NonSec_Proj_Active.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_NonSec_Proj_Active.png)

Keil uVision IDE - 将非安全项目设置为活动状态。点击放大。10. 单击 “Project -- Build 'FreeRTOSDemo_ns (FreeRTOSDemo_ns)” 构建非安全项目。

[![Keil uVision IDE - 构建非安全项目](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_NonSec_Proj_Build.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_NonSec_Proj_Build.png)

Keil uVision IDE - 构建非安全项目。点击放大。11. 单击 “Project -- Options for FreeRTOSDemo_ns - Target 'FreeRTOSDemo_ns'...”，打开非安全项目的选项窗口。

[![Keil uVision IDE - 打开非安全项目选项](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_NonSec_Proj_Options.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_NonSec_Proj_Options.png)

Keil uVision IDE - 打开非安全项目选项。点击放大。12. 通过单击 Debug 选项卡中 "Nuvoton Nu-Link Debugger" 旁边的 “Settings” 按钮，打开 Nu-Link 驱动器设置窗口。

[![Keil uVision IDE - 打开 Nu-Link 驱动器设置](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_NonSec_Proj_Debugger_1.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_NonSec_Proj_Debugger_1.png)

Keil uVision IDE -打开 Nu-Link 驱动器设置。点击放大。13. 在 “Chip Type” 下拉菜单中选择 “M2351”。

[![Keil uVision IDE - 选择 M2351](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_NonSec_Proj_Debugger_2.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_NonSec_Proj_Debugger_2.png)

Keil uVision IDE - 选择 M2351。点击放大。14. 单击窗口上的 “OK”，关闭 “Nu-Link Driver Setup” 和 “Options” 窗口。15. 单击 "Flash --> Download" 闪烁非安全二进制文件。

[![Keil uVision IDE - 闪烁非安全二进制文件](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_NonSec_Proj_Download.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_NonSec_Proj_Download.png)

Keil uVision IDE - 闪烁非安全二进制文件。点击放大。16. 要将安全项目设置为活动项目，请右键单击 "Project: FreeRTOSDemo_s"，
然后选择 "Set as Active Project"。

[![Keil uVision IDE - 将安全项目设置为活动项目](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_Sec_Proj_Active.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_Sec_Proj_Active.png)

Keil uVision IDE - 将安全项目设置为活动项目。点击放大。17. 单击 "Flash --> Download" 闪烁安全二进制文件。

[![Keil uVision IDE - 闪烁安全二进制文件](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_Sec_Proj_Download.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_Sec_Proj_Download.png)

Keil uVision IDE - 闪烁安全二进制文件。点击放大。18. 单击 "Debug --> Start/Stop Debug Session" 启动调试会话。

[![Keil uVision IDE - 启动调试会话](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_Debug_Session.png)](/media/2019/Nuvoton_Numaker_PFM_M2351_Keil_uVision_Debug_Session.png)

Keil uVision IDE - 启动调试会话。点击放大。

---

### RTOS 配置和使用详情

另请参阅[介绍在 ARMv8-M 核心上运行
FreeRTOS](/Community/Blogs/2020/using-freertos-on-armv8-m-microcontrollers) 的页面以及介绍[设置 
ARM Cortex-M 中断优先级以与 FreeRTOS 配合使用](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4)的页面。

- 此演示的相关配置项目位于
  FreeRTOS/Demo/CORTEX_MPU_M23_Nuvoton_NuMaker_PFM_M2351_IAR_GCC/Projects/Keil/ConfigFreeRTOSConfig.h
  （Keil uVision IDE 项目中的）目录和
  FreeRTOS/Demo/CORTEX_MPU_M23_Nuvoton_NuMaker_PFM_M2351_IAR_GCC/Projects/IAR/ConfigFreeRTOSConfig.h
  （IAR Embedded Workbench IDE 项目中的）目录。该文件中定义的[常量](/Documentation/02-Kernel/03-Supported-devices/02-Customization)
  可进行编辑以适配您的应用程序。以下配置
  选项适配于 ARM Cortex-M23 移植：

  - configENABLE_MPU - 启用/禁用内存保护单元 (MPU)。
  - configENABLE_TRUSTZONE - 启用/禁用 TrustZone。

- 如果要在禁用 TrustZone 的情况下运行 FreeRTOS，
  （在您的 FreeRTOSConfig.h 中设置），并使用 FreeRTOS 移植文件
  （位于 FreeRTOS/Source/portable/GCC/ARM_CM23_NTZ 目录下，适用于 GCC；
  和 FreeRTOS/Source/portable/IAR/ARM_CM23_NTZ 目录下，
  适用于 IAR）。
- 如果要在安全端运行 FreeRTOS，
  请在 FreeRTOSConfig.h 中将 configENABLE_TRUSTZONE 设置为 0，将 configRUN_FREERTOS_SECURE_ONLY 设置为 1，
  并使用 FreeRTOS 移植文件（位于 FreeRTOS/Source/portable/GCC/ARM_CM23_NTZ 目录下，
  适用于 GCC；和位于 FreeRTOS/Source/portable/IAR/ARM_CM23_NTZ 目录下，
  适用于 IAR）。
- Source/Portable/MemMang/heap_4.c 包含在项目中
  可提供 RTOS 内核所需的内存分配。请
  参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
  以获取完整信息。
- vPortEndScheduler() 尚未实现。
