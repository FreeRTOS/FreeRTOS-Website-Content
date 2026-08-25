---
title: "低功耗 RTOS 演示 - NXP LPCXpresso51U68 包含适用于 MCUXpressoIDE 的移植，支持使用 GCC、IAR 和 Keil"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

 

![](/media/2019/OM40005-BD-300x184.png) 

 **NXP OM40005：面向 LPC51U68 MCU 的 LPCXpresso51U68**
 

### 简介

本页记录的应用程序演示了如何使用 FreeRTOS 的[滴答抑制](/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support)功能来最大限度地降低在 [NXP](https://www.nxp.com/) LPC51U68 ARM Cortex-M0+ 微控制器上运行的应用程序的功耗。LPC51U68 专为成本敏感且需要低功耗的应用而设计。

为以下开发工具提供了构建演示的预配置项目：

1. [MCUXpresso IDE](https://www.nxp.com/design/software/development-software/mcuxpresso-software-and-tools/mcuxpresso-integrated-development-environment-ide:MCUXpresso-IDE)
2. [IAR Embedded Workbench](https://www.iar.com/products/architectures/nxp)
3. [ARM Keil MDK](http://www2.keil.com/NXP/)

---

### *重要！*FreeRTOS LPCXpresso51U68 低功耗演示项目使用说明

*请查看“[OM40005：面向 LPC51U68 MCU 的 LPCXpresso51U68](https://www.nxp.com/products/processors-and-microcontrollers/arm-microcontrollers/general-purpose-mcus/lpcxpresso51u68-for-the-lpc51u68-mcus:OM40005)”以获取有关此开发板的一般信息，查看“*[LPCXpresso51U68 入门指南](https://www.nxp.com/document/guide/get-started-with-the-lpcxpresso51u68:GS-LPCXpresso51U68) *”以获取此开发板开箱即用的演示。*

*此演示假设用户能够设置 IDE 和工具链。使用此 RTOS 移植之前，请仔细阅读以下所有要点。*

1. [源代码组织](#源代码组织)
2. [NXP LPCXpresso51U68 演示应用程序](#nxp-lpcxpresso51u68-演示应用程序)
3. [RTOS 配置和使用详情](#lpcxpresso51u68-rtos-演示特定配置)

 

---

 

### 源代码组织

FreeRTOS 源代码可从[官方渠道](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/)下载。请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)部分，了解下载文件的整体描述以及有关创建新项目的信息。此演示的项目文件位于 FreeRTOS/Demo/CORTEX_M0+_LPC51U68_GCC_IAR_KEIL/ 目录中，包含以下文件：

```c
CORTEX_M0+_LPC51U68_GCC_IAR_KEIL
	|
	+- /app    Contains demo application code and FreeRTOSConfig.h.
	+- ...     Vendor code.
	+- .project, .cproject    MCUXpresso IDE project.
	+- CORTEX_M0+_LPC51U68_IAR.{ewd, ewp, ewt, ew}   IAR project.
	+- CORTEX_M0+_LPC51U68_Keil.{uvoptx, uvprojx}    Keil project.

```

---

 

### NXP LPCXpresso51U68 演示应用程序

#### 设置

本演示使用电路板上的三色 LED 和 UART ，因此不需要硬件设置。UART 已配置为使用 115200 波特率、8 个数据位、无奇偶校验位和 1 个停止位。

#### 功能

演示的行为由 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 和 mainNO_TASK_NO_CHECK 宏控制，这些宏可在 FreeRTOSConfig.h 中定义，如下所示：请注意，只有选项 3 演示无滴答模式：

1. 要创建一个简单的 Blinky 演示构建项目，请将 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1。blinky 项目创建了两个任务和一个队列。一个任务通过队列定期向另一个任务发送值。每次接收值时，接收任务都会切换一次 LED。
2. 若要创建运行标准演示任务子集的项目，请在构建项目时将 mainCREATE_SIMPLE_Blinky_DEMO_ONLY 和 mainNO_TASK_NO_CHECK 均设置为 0。标准演示任务是所有 RTOS 移植演示应用程序执行的任务，除了演示 RTOS API 和测试 RTOS 移植外，没有特别的用途。
3. 要尝试使用无滴答闲置模式，请将 mainCREATE_SIMPLE_Blinky_DEMO_ONLY 设置为 0，并将 mainNO_TASK_NO_CHECK 设置为 1。然后尝试在首次构建后运行演示应用程序，将 [configUSE_TICKLESS_IDLE](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configuse_tickless_idle) 设置为 1，然后将 configUSE_TICKELSS_IDLE 设置为 0，在两种情况下都监视 UART 的输出。 更多信息请参阅下一节。

以下部分仅介绍无滴答低功耗演示。

 

#### 低功耗演示

将 mainNO_TASK_NO_CHECK 设置为 1 可防止创建任何演示应用程序任务，而是将内核的[空闲](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/15-Idle-task)和[定时服务](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/02-Timer-service-daemon-task)任务作为唯一正在运行的任务。[滴答钩子](/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions)函数用于计数滴答中断次数，软件定时器用于切换 LED，并将计数的滴答中断次数输出到 UART。定时器的回调函数称为 prvCheckTimerCallback()，其周期由 main.c 中定义的 mainCHECK_TIMER_PERIOD_MS 常量设置。 

configUSE_TICKLESS_IDLE 设置为 1 时，只要除了空闲任务之外没有其他任务可以执行，内核就会进入无滴答空闲模式，停止 RTOS 滴答中断。退出无滴答模式时，无论内核处于无滴答模式时发生了多少个滴答周期，滴答计数都会向前推进。然而，尽管 RTOS 滴答计数调整到正确的时间，但滴答中断实际上从未发生，因此滴答钩子函数（从 RTOS 滴答中断调用）执行的次数的计数低于滴答计数，如下图所示。 有关详细信息，请参阅 [FreeRTOS 低功耗支持](/Documentation/02-Kernel/02-Kernel-features/07-Lower-power-support)。

 

MCU Xpresso IDE 提供了一个[功耗测量工具](https://community.nxp.com/t5/LPC-Microcontrollers-Knowledge/IDE-Tool-Energy-Measurement-in-MCUXpresso-IDE/ta-p/1444553)，用于量化由滴答空闲功能节省的功耗，但请注意，此演示并未尝试最大限度地节省功耗，为此，有必要使用低功耗时钟，关闭 UART 等外围设备，并断开调试器。

![](/media/2020/power_tickless_enabled.png) 

**功耗测量 — configUSE_TICKLESS_IDLE 设置为 1**
 

![](/media/2020/power_no_tickless.png) 

**功耗测量 — configUSE_TICKLESS_IDLE 设置为 0**
 

![](/media/2020/serial_tickless_enabled.png) 

**串行输出 — configUSE_TICKLESS_IDLE 设置为 1**
 

![](/media/2020/serial_no_tickless.png) 

**串行输出 — configUSE_TICKLESS_IDLE 设置为 0**
 

功耗测量显示，启用和禁用无滴答空闲模式之间，目标电流有 0.8mA 的差异。如前所述，此演示并不试图最大限度地节省功耗，因为未使用低功耗时钟，也不禁用外围设备或调试器，如果这样做，功耗会大幅降低。使用 LPC51U68 VDD vsense 4.12Ω 电阻器进行测量。在串行输出中，启用和禁用无滴答空闲模式时，触发 ISR 的次数差异非常明显。

---

 

### 构建和运行 FreeRTOS 演示应用程序

#### MCUXpresso IDE 设置

1. 启动 the MCUXpresso IDE。此页面上的屏幕截图显示的是 MCUXpresso IDE 版本 11.0.1。
2. 选择现有或新工作区目录，然后单击 "Launch"。

  [![MCUXpresso IDE Launcher。](/media/2020/step2-launch.png)](/media/2020/step2-launch.png)

MCUXpresso IDE Launcher。点击放大
3. 点击 "File -> Open Projects from File System..."，导入 MCUXpresso IDE 项目。在 "Import Source" 中，将目录更新为项目文件夹路径 FreeRTOS-root\FreeRTOS\Demo\CORTEX_M0+_LPC51U68_GCC_IAR_KEIL。

  [![MCUXpresso IDE 导入项目。](/media/2020/step3-open-project-redbox.png)](/media/2020/step3-open-project-redbox.png)

MCUXpresso IDE 导入项目。点击放大。
4. 点击 "Project -> Build All"，构建项目。项目在构建过程中不应报错或出现警告。

  [![MCUXpresso IDE 控制台构建结果。](/media/2020/step4-build-all.png)](/media/2020/step4-build-all.png)

MCUXpresso IDE 控制台构建结果。点击放大。

 要使用内置于评估板中的 CMSIS-DAP 调试接口对微控制器闪存进行编程并启动调试会话，请执行以下操作：
1. 确保评估板的 Link2 和 LPC51U68 目标侧均已通电，并且调试 USB 线缆已连接到主计算机上。（对于 Rev A 板，请将 micro USB 线缆连接到 J6，而不是 J5）。
2. 在 IDE 的项目资源管理器窗口中，右键单击项目名称，选择 "Debug As -> MCUXpresso IDE LinkServer (inc. CMSIS-DAP) probes"。如果成功检测到评估板，则 LPC-LINK2 CMSIS-DAP 显示为可用。单击 "OK" 进入 MCUXpresso 调试视图。

  [![MCUXpresso IDE 调试探头。](/media/2020/step5-debug.png)](/media/2020/step5-debug.png)

MCUXpresso IDE 调试探头。点击放大。
3. MCUXpresso IDE 包括用于测量平均功耗和在运行时观察 FreeRTOS 任务/队列/内存使用情况的便利工具。有关详细信息，请参阅 [MCUXpresso IDE 用户指南](https://community.nxp.com/pwmxy87654/attachments/pwmxy87654/mcuxpresso-ide/9289/1/MCUXpresso_IDE_User_Guide.pdf)。

#### 其他 IDE

IAR Embedded Workbench 和 ARM Keil MDK 项目可以直接在其各自的 IDE 中打开，或者只需在目录结构中双击项目文件即可。有关详细信息，请参阅 NXP 的 [LPCXpresso51U68 入门指南](https://www.nxp.com/document/guide/get-started-with-the-lpcxpresso51u68:GS-LPCXpresso51U68)。

---

### LPCXpresso51U68 RTOS 演示特定配置

 此演示的特定配置项目位于 FreeRTOSConfig.h中。可编辑此文件中定义的常量，以适应您的应用程序。有关详细信息，请参阅“自定义”。特别是关于内核移植和内存管理：
内核移植

 面向 GCC、IAR 和 Keil 的 ARM Cortex M0(+) 移植尚未实现 vPortEndScheduler() 函数。 

内存分配

 Source/Portable/MemMang/heap_5.c 用于 LPCXpresso51U68 演示应用程序项目，用于支持内存库之间的内存分配。请参阅内存管理。在 compiler_attributes.h 中定义了用于将第二个 FreeRTOS 堆内存区域放置在第二个内存库中的编译器特定属性。

 

 

 
