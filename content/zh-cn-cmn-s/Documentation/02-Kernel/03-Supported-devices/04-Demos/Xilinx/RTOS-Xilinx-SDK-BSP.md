---
title: "适用于 Xilinx SDK 的 FreeRTOS BSP"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

## 引言

Xilinx 软件开发工具包 [(SDK)](https://www.xilinx.com/products/design-tools/embedded-software/sdk.html)
可以从硬件定义文件自动生成板级支持包 (BSP)。BSP 
可提供全面的运行时、处理器和外设支持，也可以 
包含 FreeRTOS 实时操作系统。

在 BSP 中包含 FreeRTOS 可为应用程序编写者提供预配置的 FreeRTOS 环境， 
无需手动添加任何源文件，也无需应用程序代码提供任何回调函数，
并且可在 IDE 中编辑 FreeRTOSConfig.h 。

以下是创建 FreeRTOS BSP 的说明。FreeRTOS 下载包中还包括针对以下设备的 
独立和综合演示应用程序： 
[Xilinx Zynq](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Xilinx/RTOS-Xilinx-Zynq) 双核 
ARM Cortex-A9 处理器、 
[UltraScale+ MPSoC 上的 ARM Cortex-A53 核心](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Xilinx/RTOS-Xilinx-UltraScale_MPSoC_64-bit)（AArch64，64 位）、 
[UltraScale+ MPSoC 上的 ARM Cortex-R5 核心](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Xilinx/RTOS-ARM-Cortex-R5-Xilinx-UltraScale_MPSoC)（32 位） 
以及 [Xilinx Microblaze](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Xilinx/RTOS-Xilinx-Microblaze-KC705)
软核处理器。这些综合演示应用程序（在 FreeRTOS 下载包中提供） 
使用独立的 BSP。独立 BSP 本身不包含 FreeRTOS，因此 FreeRTOS 
作为应用程序的一部分构建。即使 
使用 FreeRTOS BSP，仍有必要阅读这些独立演示的文档页面，因为这些页面会介绍 FreeRTOS 
在这些 ARM 和 Xilinx 架构上的使用方法。

---

## 说明

### 创建使用 FreeRTOS BSP 的 Hello World 项目

随 Xilinx SDK 一起提供的板级支持包 (BSP) 存储库包含简单的 
FreeRTOS Hello World 应用程序。创建 Hello World 项目的步骤如下：

1. 从 SDK 的 "File" 菜单中依次选择 "New" 和 "Application Project"，
   打开 "New Project" 窗口，然后为项目命名。

   ![新建 RTOS BSP 项目](/media/2018/new_sdk_rtos_bsp_project.png)   
   *"New: Application Project" 菜单选项*

2. 在 "New Project" 窗口中，首先选择使用的硬件平台。 
   FreeRTOS 支持的所有处理器（Zynq ARM Cortex-A9、UltraScale+ ARM Cortex-A53 和 ARM Cortex-A9 核心以及 Microblaze）都提供了 
   预定义的硬件平台。下图显示了使用的预配置 ZC702 平台 
   。

3. 选择硬件平台后，选择处理器。下图显示了 
   选择的 ps7_cortexa9_0 处理器。

4. 选择处理器后，选择操作系统平台。下图显示了选择的 freertos822 
   。

   ![创建 RTOS 应用程序](/media/2018/creating_the_rtos_bsp_project.png)   
   *定义项目设置*

5. 点击 "Next" 按钮进入下一阶段。"Templates" 窗口随即出现，选择 
   "FreeRTOS Hello World" 模板，然后单击 "Finish" 按钮以生成 FreeRTOS 
   BSP 和 Hello World 项目。

   ![选择 RTOS Hello World 模板](/media/2018/RTOS_BSP_Hello_World.png)   
   *选择 FreeRTOS Hello World 模板*


### 编辑 FreeRTOS 配置

生成 FreeRTOS BSP 时，会自动创建 FreeRTOSConfig.h 文件。可以通过以下步骤 
查看并编辑该文件中的值：

1. 从 SDK 的 "Xilinx Tools" 菜单中选择 "Board Support Package Settings"。"Board Support Package Settings" 
   窗口随即出现。

2. 在 "Board Support Package Settings" 窗口的左侧窗格中选择 FreeRTOS。右侧窗格中的表格 
   将填充 FreeRTOSConfig.h 设置。

3. 根据需要编辑设置，然后单击 "Ok" 按钮，使用编辑后的值更新 FreeRTOSConfig.h ， 
   并重新构建 BSP。

   [![编辑 RTOS 设置](/media/2018/editing_the_rtos_settings.png)](/media/2018/editing_the_rtos_settings.png)   
   *"Board Support Package Settings" 窗口*


### 启动调试会话

必须确保用于启动调试会话的 SDK 启动配置可重置整个 CPU， 
并运行必要的初始化脚本。适用于运行 Zynq 演示的调试配置 
如下图所示。

![](/media/2018/Zynq_target_setup_tab.jpg)

