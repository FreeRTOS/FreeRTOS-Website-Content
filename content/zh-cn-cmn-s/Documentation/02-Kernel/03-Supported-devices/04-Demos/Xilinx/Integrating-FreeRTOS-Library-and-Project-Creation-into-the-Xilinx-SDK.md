---
title: "FreeRTOS/Xilinx SDK 集成 将 FreeRTOS 库和项目创建集成到 Xilinx SDK 中"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![Xilinx Spartan 6 SP605 开发板](/media/2018/Xilinx-Spartan-6-SP605-development-board.jpg)

有关在 MicroBlaze 上使用 FreeRTOS 的重要信息，请参阅
[MicroBlaze 演示应用程序文档主页的
“配置和使用”部分](Free-RTOS-for-Xilinx-MicroBlaze-on-Spartan-6-FPGA.md#ConfigAndUsage)。
使用 FreeRTOS 之前，请参阅此 MicroBlaze 特定信息。

在 Xilinx SDK 环境中，可通过两种方式使用 FreeRTOS：

1. 使用独立的 BSP

 独立的板级支持包 (BSP) 是由 SDK生成的库，
 特定于硬件设计（FPGA 配置）。该库
 包含用于 MicroBlaze 软核处理器本身和设计中所有外设的软件驱动程序，
 但无法支持 FreeRTOS。
 要将 FreeRTOS 与独立的 BSP 一起使用，可以将 FreeRTOS 源文件
 构建为引用 BSP 库的应用程序的一部分。这个
 方法由
 [主要的 FreeRTOS MicroBlaze 演示应用程序](Free-RTOS-for-Xilinx-MicroBlaze-on-Spartan-6-FPGA)采用。
2. 使用 FreeRTOS BSP

 FreeRTOS BSP 扩展了上述独立的 BSP，纳入了
 FreeRTOS 源文件。FreeRTOS 可以与 FreeRTOS BSP 一起使用，
 而无需将 FreeRTOS 源文件作为引用 BSP 库的
 应用程序的一部分。本页描述了如何生成和使用 FreeRTOS BSP，
 以及 SDK 如何自动生成
 使用 FreeRTOS BSP 库的完整（但简单）的 FreeRTOS 示例应用程序。

1. [将 FreeRTOS 集成到 SDK 环境中](#将-freertos-集成到-sdk-环境中)
2. [使用 SDK 创建完整（但简单）的 FreeRTOS 应用程序](#使用-sdk-创建完整但简单的-freertos-应用程序)
3. [在 SDK 中创建 FreeRTOS BSP](#在-sdk-中创建-freertos-bsp)

---

### 将 FreeRTOS 集成到 SDK 环境中

将 FreeRTOS 集成到 SDK 环境中所需的文件（针对未与
FreeRTOS 预集成的 SDK 版本）位于
FreeRTOS/Demo/MicroBlaze_Spartan-6_EthernetLite/KernelAwareBSPRepository
目录中。为确保 SDK 环境支持 FreeRTOS，必须将 KernelAwareBSPRepository 目录
注册为存储库目录。但是，执行此操作前，
必须将最新的 FreeRTOS 源文件复制到 KernelAwareBSPRepository
目录中。为此，请执行
位于 FreeRTOS/Demo/MicroBlaze_Spartan-6_EthernetLite/SDKProjects/RTOSDemoSource
目录中的 CreateProjectDirectoryStructure.bat 批处理文件。  **[注意：当演示项目在
单独的 zip 文件中提供时，无需运行此批处理文件；仅当演示项目包含在 FreeRTOS.org 的主下载中时才需要运行此批处理文件。]**

**必须先执行 CreateProjectDirectoryStructure.bat，
方可执行下述步骤。**

要将 KernelAwareBSPRepository 注册为存储库目录：

1. 确保 CreateProjectDirectoryStructure.bat 已成功执行。
2. 在 SDK 中，依次单击 "Xilinx Tools" 和 "Repositories"，以打开 "Preferences" 对话框中的 "Software Repositories" 选项卡。
3. 要添加本地或全局存储库，请单击 "New"。浏览并选择
 FreeRTOS/Demo/MicroBlaze_Spartan-6_EthernetLite/KernelAwareBSPRepository 目录。

![将 FreeRTOS 源存储库添加到引用的存储库列表中](/media/2018/Adding-the-FreeRTOS-source-repository-to-the-list-of-referenced-repositories.jpg)

 将 FreeRTOS BSP 存储库目录

 添加到 SDK 中的引用存储库列表

---

### 使用 SDK 创建完整（但简单）的 FreeRTOS 应用程序
如上所述安装存储库后，SDK 菜单即可用于
创建一个完整但非常简单的 FreeRTOS 应用程序。请按以下步骤操作：
1. 在 SDK 中，依次单击 "File > New > Xilinx C Project" 打开 "New Project" 对话框。
 如果尚未定义硬件项目，系统将提示您
 在打开 "New Project" 对话框之前进行选择。
2. 选择 "FreeRTOS Hello World" 作为项目模板，然后单击 "Next"

![在 "New Project" 对话框中选择 "FreeRTOS Hello World" 作为项目模板](/media/2018/Selecting-FreeRTOS-Hello-World-as-the-project-template-in-the-Xilinx-SDK.jpg)

 在 "New Project" 对话框中选择 "FreeRTOS Hello World" 作为项目模板
3. 在打开的下一个对话框中，可以对项目进行命名。
4. 创建应用程序后， 可以使用 "Board Support Package Settings" 对话框修改 FreeRTOS 配置
 。要在 SDK 中
 访问 "Board Support Package Settings" 对话框，在 SDK 中
 单击 "Xilinx Tools > Board Support Package Settings"。
 打开的对话框与下文
 [在 SDK 中创建 FreeRTOS BSP](#在-sdk-中创建-freertos-bsp) 部分
 所描述的对话框相同。

由 SDK 创建的简单应用程序
并不依赖于其所执行的硬件（MicroBlaze
软核本身除外）。因此，运行时，
没有可见的状态指示。但是，可以使用调试器
检查其执行和行为。

应用程序行为的描述包含在
名为 FreeRTOS-main.c 的单个源文件的顶部，为方便起见，将其复制到此处：

```c

/*
 * FreeRTOS-main.c (this file) defines a very simple demo that creates two tasks,
 * one queue, and one timer.
 *
 * The main() Function:
 * main() creates one software timer, one queue, and two tasks. It then starts
 * the RTOS scheduler.
 *
 * The Queue Send Task:
 * The queue send task is implemented by the prvQueueSendTask() function in
 * this file. prvQueueSendTask() sits in a loop that causes it to repeatedly
 * block for 200 milliseconds, before sending the value 100 to the queue that
 * was created within main(). Once the value is sent, the task loops back
 * around to block for another 200 milliseconds.
 *
 * The Queue Receive Task:
 * The queue receive task is implemented by the prvQueueReceiveTask() function
 * in this file. prvQueueReceiveTask() sits in a loop that causes it to
 * repeatedly attempt to read data from the queue that was created within
 * main(). When data is received, the task checks the value of the data, and
 * if the value equals the expected 100, increments the ulRecieved variable.
 * The 'block time' parameter passed to the queue receive function specifies
 * that the task should be held in the Blocked state indefinitely to wait for
 * data to be available on the queue. The queue receive task will only leave
 * the Blocked state when the queue send task writes to the queue. As the queue
 * send task writes to the queue every 200 milliseconds, the queue receive task
 * leaves the Blocked state every 200 milliseconds, and therefore toggles the LED
 * every 200 milliseconds.
 *
 * The Software Timer:
 * The software timer is configured to be an "auto reset" timer. Its callback
 * function simply increments the ulCallback variable each time it executes.
 */

```

---

### 在 SDK 中创建 FreeRTOS BSP
上述简单应用程序使用 FreeRTOS BSP 库。FreeRTOS BSP 库
也可以自行创建，而无需简单的应用程序。请按以下步骤操作：
1. 确保已将 KernelAwareBSPRepository 安装为存储库目录
 （如前所述）。
2. 在 SDK 中，依次单击 "File > New > Xilinx Board Support Package" 打开 "New Board Support Package Project" 对话框。
 如果尚未定义硬件项目，系统将提示您
 在打开 "New Board Support Package Project" 对话框之前进行选择。
3. 单击 "Finish" 之前，选择“freertos”作为板级支持包操作系统。

![选择 freertos 作为板级支持包操作系统](/media/2018/Selecting-FreeRTOS-as-the-board-support-package-OS.jpg)

 选择 freertos 作为板级支持包操作系统
4. 系统将打开 "Board Support Package Settings" 对话框，可在其中根据需要调整 FreeRTOS 参数。

!["Board Support Package Settings" 对话框](/media/2018/FreeRTOS-board-support-package-BSP-settings-dialog.jpg)

 使用 "Board Support Package Settings" 对话框配置 FreeRTOS

FreeRTOS BSP 创建后，即可由其他 SDK 项目引用，
以快速简单地为任何应用程序添加 FreeRTOS 控制的多任务处理功能。
