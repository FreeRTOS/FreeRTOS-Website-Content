---
title: "SiFive HiFive1 RTOS 演示 (RISC-V)"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

 [[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![RISC-V HiFive1 SiFive Freedom Studio 和 IAR](/media/2020/RISC-V_HiFive-RevB.jpg)

本页面记载了预配置的 [Freedom Studio](https://www.sifive.com/boards)
(GCC) 和 [IAR Embedded Workbench for RISC-V](https://www.iar.com/iar-embedded-workbench/#!?architecture=RISC-V) 项目，
这些项目构建并运行 FreeRTOS RISC-V 演示
（在 [HiFive11 RevB](https://www.sifive.com/boards/hifive1-rev-b)
评估板上）。

---

### 重要！使用 SiFive RISC-V 移植的注意事项

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [在 RISC-V 核心上使用 FreeRTOS 的说明](#重要使用-sifive-risc-v-移植的注意事项)
2. [源代码组织](#源代码组织)
3. [演示应用程序功能](#sifive-hifive1-revb-risc-v-演示应用程序)
4. [构建和运行 RTOS 演示应用程序 – Freedom Studio](#使用-freedom-studio-构建-rtos-演示应用程序)
5. [构建和运行 RTOS 演示应用程序 – IAR](#使用-iar-embedded-workbench-构建-rtos-演示应用程序)
6. [RTOS 配置和使用详情](#配置和使用详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？](/Why-FreeRTOS/FAQs/Troubleshooting)”。

---

### 在 RISC-V 核心上使用 FreeRTOS 的说明

如果您不满足于仅仅运行本页所描述的演示，或者
如果想要创建自己的 RISC-V FreeRTOS 项目，请阅读相关文档页面。
这些页面会介绍[在 RISC-V 核心上运行 FreeRTOS 内核的基本信息](Using-FreeRTOS-on-RISC-V)。


### 源代码组织

FreeRTOS zip 文件下载包含所有 FreeRTOS 移植和
演示应用程序的源代码，因此包含的文件数量远远超过
使用 FreeRTOS HiFive1 RevB RISC-V 演示所需的文件。

请参阅
[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)页面，
了解 zip 文件的目录结构信息。
HiFive1 Freedom Studio 和 IAR 项目分别位于 /Demo/RISC-V_RV32_SiFive_HiFive1-RevB_FreedomStudio
和 Demo/RISC-V_RV32_SiFive_HiFive1-RevB_IAR 目录下。[构建说明部分](#使用-freedom-studio-构建-rtos-演示应用程序)提供了更多信息。

在 RISC-V 架构中，额外的 [freertos_risc_v_chip_specific_extensions.h 头文件](/Using-FreeRTOS-on-RISC-V#RISC_V_SOURCE_FILES)
用于将基础 RISC-V RTOS 移植扩展到目标 RISC-V 芯片
可能实现的任意芯片特定扩展。HiFive1 上的 SiFive 核心提供了一个核心本地中断器 (CLINT)，
但除了基础 RISC-V 架构定义的寄存器外，它不实现其它任何寄存器
。因此，它使用 freertos_risc_v_chip_specific_extensions.h 头文件，
该头文件位于 /FreeRTOS/Source/portable/[compiler]/RISC-V/chip_specific_extensions/RV32I_CLINT_no_extensions
目录下。

---

### SiFive HiFive1 RevB RISC-V 演示应用程序

#### 功能

常量 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY（定义于
main.c 顶部）用于在简单 "blinky" 风格的入门项目
和更全面的测试和演示应用程序之间进行切换。

#### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 时

当将 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 时，main() 会调用 main_blinky()。
main_blinky() 会创建使用两个任务和一个队列的基本示例，如下所示：

* 队列发送任务：

 队列发送任务由 prvQueueSendTask() 函数实现。
 它位于一个循环中，每秒都会向队列发送值 100
 。
* 队列接收任务：

 队列接收任务由 prvQueueReceiveTask()
 函数实现。它位于一个循环中，
 该循环会阻塞读取队列的尝试（任务被阻塞时不会消耗 CPU 周期），
 每次从队列发送任务收到值 100 时，便会切换成蓝色 LED
 。

 由于队列发送任务每秒向队列写入一次，
 因此队列接收任务也会每秒解除阻塞并切换 LED
 。

#### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时

当将 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时，main() 会调用 main_full()。
main_full() 会创建标准演示任务的子集
。所有 FreeRTOS 移植演示应用程序都使用标准演示任务。
这些任务没有特定的功能，创建它们仅为演示如何使用 FreeRTOS API，
以及测试 RTOS 移植。

创建“检查”任务，定期检查标准
演示任务（包含自我监控代码），以确保所有任务
都按预期运行。检查任务每次执行时都会切换为蓝色 LED 。
这提供了有关系统健康状况的
直观反馈。**如果 LED 每 3 秒切换一次，则表示
检查任务未发现任何问题。如果 LED 每 500 毫秒切换一次，则表示检查任务
已在一个或多个任务中发现了问题。**

#### 使用 Freedom Studio 构建 RTOS 演示应用程序

**重要提示：**
如果目录结构与
在官方 FreeRTOS zip 文件版本中使用的目录结构不同，则不会构建项目。
确保在将项目导入 Freedom Studio Eclipse 工作区时，
不要勾选 "copy projects into workspace"
复选框。

想要打开并构建 Freedom Studio RISC-V 项目，则需：

1. [下载并安装 Freedom Studio 开发工具](https://www.sifive.com/boards)（下滑查看软件下载）。
2. 启动 Freedom Studio，根据提示选择现有工作区，
 或创建新的工作区。
3. 在 Freedom Studio 的 "File" 菜单中选择 "Import..."。"Import" 对话框
 随即打开。
4. 在 "Import" 对话框中，选择 "General -> Existing Project into Workspace"，
 "Import Projects" 对话框随即打开。

![](/media/2019/Importing-an-existing-project-into-Eclipse-TriCore.jpg)

 将现有项目导入工作区
5. 在 "Import Projects" 对话框中，导航到
 FreeRTOS/Demo/RISC-V_RV32_SiFive_HiFive1-RevB_FreedomStudio 目录并选中此目录，
 并确保没有选中 "copy projects into workspace"
 复选框。

[\![](/media/2020/copy_hifive1_project_into_workspace.jpg)](/media/2020/copy_hifive1_project_into_workspace.jpg)

 在 "Import Project" 对话框中选择
 目录和项目。点击放大。
6. 在 "Import Projects" 对话框的 "Projects" 窗口中，选择 RTOS 演示项目，然后点击 "Finish"。
 项目会被导入至您的 Eclipse 工作区。以下几个步骤仅为检查
 编译器路径是否正确。
7. 在 IDE 的 "Project" 菜单中选择 "Properties"。
8. 在 "Properties" 窗口中，展开 "C/C++ Build" 菜单项，然后选择其中的 "Settings" 选项。
9. 在 "Tool Settings" 子窗口中，选择 "Cross Settings"。
10. 在此窗口中，**确保编译器的路径是适合安装的路径**。下图
 显示了安装 Freedom Studio 时使用已安装编译器的默认路径
 \- 尽管 GCC 版本号可能会
 改变。

[\![](/media/2020/navigating-to-toolchain-selector.jpg)](/media/2020/navigating-to-toolchain-selector.jpg)

 配置所需工具链的路径（点击放大）。
11. 编译器路径正确时，在 "Properties" 窗口中，选择 "Apply and Close"。
12. 在 Freedom Studio 的 "Project" 菜单中选择 “Build all”。FreeRTOS 源码和
 演示源文件构建时不应产生任何错误和警告
 （尽管第三方驱动程序代码可能会生成警告），
 并创建一个名为 RTOSDemo.elf 的文件。

要使用 Freedom Studio 对 HiFive1 RevB 板进行编程并调试 RTOS 演示，则需：

1. 使用 USB 数据线将 HiFive1 RevB 板连接至您的主机。
2. 单击调试速度按钮旁边的小箭头，
 然后在弹出菜单中选择 "Debug Configurations..." 以调出
 调试配置窗口。

![](/media/2018/TriCore-Eclipse-Debug-Speed-Button.jpg)

 调试速度按钮
3. 在调试配置窗口中，双击 "SiFive GDB SEGGER J-Link Debugging"
 以创建调试配置。
 HiFive1 RevB 板内置 J-Link，您无需单独的
 J-Link 接口。

[\![](/media/2020/CreateHiFiveDebugConfiguration.jpg)](/media/2020/CreateHiFiveDebugConfiguration.jpg)

 创建 J-Link 调试配置
4. 在调试配置中，单击 "Debug" 按钮对 HiFive1 RevB
 RISC-V 评估板进行编程，并启动调试会话。此后
 可使用普通的 Eclipse 调试菜单项运行和调试 RTOS 应用程序。

 启动调试会话前，可能需要在调试配置中设置设备名称
 。

[\![](/media/2020/HiFive1-setting-device-name.jpg)](/media/2020/HiFive1-setting-device-name.jpg)

 在调试配置中设置设备名称

#### 使用 IAR Embedded Workbench 构建 RTOS 演示应用程序

要打开并构建 IAR Embedded Workbench for RISC-V 项目，则需：

1. 打开 /FreeRTOS/Demo/RISC-V_RV32_SiFive_HiFive1-RevB_IAR/RTOSDemo.eww
 （在 IAR Embedded Workbench for RISC-V IDE 中）。
2. 在 IDE 的 "Project" 菜单中选择 "Rebuild All"（或只需按 F7）,
 RTOS 演示应当构建，没有产生任何错误或警告，
 但消息性的 #warning 信息除外。

要使用 IAR Embedded Workbench 对 HiFive1 RevB 板进行编程并调试 RTOS 演示，则需：

1. 连接 IAR I-Jet 调试接口，该接口位于主机和
 hiFive1 Reb B 开发板上标有 J1 的 10 针调试连接器之间。

[\![](/media/2020/i-jet-hifive1.jpg)](/media/2020/i-jet-hifive1.jpg)

 连接至 HiFive1 评估板的 IAR I-Jet

- 在 IDE 的 "Project" 菜单中选择 "Download and Debug"（或按 CTRL+D）
 对 HiFive1 RevB RISC-V 评估板进行编程并启动调试会话，
 之后可使用正常的 IAR 调试菜单项运行和调试
 RTOS 应用程序。

### 配置和使用详情

#### RTOS 移植的特定配置

本部分相关信息，详见“[在 RISC-V 核心上运行 FreeRTOS](/Using-FreeRTOS-on-RISC-V)”
文档页面：

	* FreeRTOS/Demo/RISC-V_RV32_SiFive_HiFive1-RevB_FreedomStudio/FreeRTOSConfig.h 包含了 Freedom Studio 项目的特定配置项。
	 FreeRTOS/Demo/RISC-V_RV32_SiFive_HiFive1-RevB_IAR/FreeRTOSConfig.h 包含了 IAR 项目的特定配置项。

	 您可以编辑[这些文件中定义的常量](/Documentation/02-Kernel/03-Supported-devices/02-Customization)，
	 使其适用于您的应用程序。具体而言，由于 SiFive RISC-V 核心包括
	 硬件定时器 (MTIMER)，configMTIME_BASE_ADDRESS 和 configMTIMECMP_BASE_ADDRESS
	 分别被定义为 0x20000BFF8 和 0x20004000。
	* SiFive 核心包括一个核心本地中断器 (CLINT)，
	 但除了
	 基础 RISC-V 架构定义的寄存器，它不包括其他寄存器。因此该项目使用
	 freertos_risc_v_chip_specific_extensions.h 头文件
	 （位于 /FreeRTOS/Source/portable/[compiler]/RISC-V/chip_specific_extensions/RV32I_CLINT_no_extensions 目录），
	 因此该目录在汇编的包含路径中。
	* 由 SiFive 软件开发套件 (SDK) 提供
	 并用于 Freedom Studio 项目的中断处理程序
	 名为 trap_handler，因此汇编程序的命令行选项包括
	 -DportasmHANDLE_INTERRUPT=handle_trap。


	 编写时，IAR 项目会使用一个名为 vApplicationHandleTrap() 的框架陷阱处理程序，该处理程序在 main.c 中定义。
	* 文件 flash.lds 是随 Freedom Studio 开发工具一起提供的链接器脚本的一个版本，
	 经过编辑，添加了必要的 __freertos_irq_stack_top
	 链接器变量，以确保在调度器启动前被 main 使用的堆栈
	 在调度器启动后重新用作中断堆栈。


	 IAR 项目使用 configISR_STACK_SIZE_WORDS 常量来确定
	 静态分配的中断堆栈的大小。

其他注意事项：

	* vPortEndScheduler() 尚未实现。
	* RISC-V 项目中包含 Source/Portable/MemMang/heap_4.c，以提供
	 RTOS 内核所需的内存分配。
	 请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
	 获取完整信息。
	* 截至本文撰写之际，此演示尚不支持中断嵌套。

