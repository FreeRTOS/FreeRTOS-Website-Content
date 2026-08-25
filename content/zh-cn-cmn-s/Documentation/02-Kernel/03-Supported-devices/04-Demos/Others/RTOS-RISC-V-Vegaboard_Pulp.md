---
title: "RISC-V RV32M1 VEGAboard 演示（RI5CY 核心）"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

 [[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![RISC-V RV32M1-Vega Pulp RI5CY 核心](/media/2019/RISC-V-RV31M1-VEGA-board.png)

本页记录了一个预配置的 FreeRTOS Eclipse/GCC 项目，该项目针对 RISC-V 核心
（位于 [RV32M1 VEGAboard](https://open-isa.org/order/) 上）。
RV32M1 包含一个 Pulp RI5CY RISC-V 核心、
一个 Pulp Zero RISCY RISC-V 核心、一个 Arm Cortex-M4 核心以及
一个 Arm Cortex-M0+ 核心。在撰写本文时，本演示仅针对 RI5CY RISC-V 核心。

---

### 重要！使用 FreeRTOS Pulp RI5CY RISC-V 移植的注意事项

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [在 RISC-V 核心上使用 FreeRTOS 的说明](#重要使用-freertos-pulp-ri5cy-risc-v-移植的注意事项)
2. [源代码组织](#源代码组织)
3. [RTOS 演示应用程序功能](#vegaboard-ri5cy-risc-v-演示应用程序)
4. [构建和运行 RTOS 演示应用程序](#构建和调试演示应用程序)
5. [RTOS 配置和使用详情](#配置和使用详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？](/Why-FreeRTOS/FAQs/Troubleshooting)”。

---

### 在 RISC-V 核心上使用 FreeRTOS 的说明

如果您不满足于仅仅运行本页所描述的演示，或者
如果想要创建自己的 RISC-V FreeRTOS 项目，请阅读相关文档页面。
这些页面会介绍[在 RISC-V 核心上运行 FreeRTOS 内核的基本信息](Using-FreeRTOS-on-RISC-V)。


### 源代码组织

FreeRTOS zip 文件下载内容中包含所有 FreeRTOS 移植的源代码及
所有演示应用程序。这意味着其包含的文件远多于
使用 FreeRTOS VEGAboard RI5CY RISC-V 移植所需的文件。

详情请参见
[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)页面，
了解 zip 文件的目录结构信息。Eclipse 项目
位于 /Demo/RISC-V_RV32M1_Vega_GCC_Eclipse 目录中。如需了解更多信息，
请参阅下文[构建说明](#构建和调试演示应用程序)
部分。

在 RISC-V 架构中，额外的 [freertos_risc_v_chip_specific_extensions.h 头文件](/Using-FreeRTOS-on-RISC-V#RISC_V_SOURCE_FILES)
用于扩展基本的 RISC-V RTOS 移植，以支持目标 RISC-V 芯片
可能实现的任何芯片特定扩展。RV32M1 VEGAboard 上使用的 RI5CY RISC-V 核心
除了基本 RISC-V 架构定义的寄存器外，还包括六个额外的寄存器，
但不包括 CLINT。因此，该项目使用
/FreeRTOS/Source/portable/GCC/RISC-V/chip_specific_extensions/Pulpino_Vega_RV32M1RM 目录中的 freertos_risc_v_chip_specific_extensions.h
头文件。

---

### VEGAboard RI5CY RISC-V 演示应用程序

#### 功能

常量 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 在 main.c 文件顶部定义，
用于在简单 "blinky" 风格的入门项目
和更全面的测试和演示应用程序之间切换。

#### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 时

mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 时，main() 会调用 main_blinky()。
main_blinky() 会创建使用两项任务和一个队列的基本示例。
* 队列发送任务：

 队列发送任务由 prvQueueSendTask() 函数实现。
 该任务在一个循环中运行，
 每 1000 毫秒（即 1 秒）会发送值 100 至队列。
* 队列接收任务：

 队列接收任务由 prvQueueReceiveTask()
 函数实现。该任务在一个循环中运行，尝试从队列读取数据时会被阻塞
 （任务被阻塞时不会消耗 CPU 周期），
 每次从队列发送任务接收到值 100 时，
 会将 "blink" 写入VEGAboard 的 UART 并切换 LED。由于队列发送任务每 1000 毫秒向队列写入一次，
 因此队列接收任务会每 1000 毫秒解除阻塞
 写入 UART，并切换一次 LED。

#### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时

mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时，main() 会调用 main_full()。
main_full() 会实现一个全面测试和演示应用程序，此应用程序会演示和/或
测试（以及其他功能）：
* [消息缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers)
* [流缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers)
* [任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)
* [队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues)
* [信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores)
* [互斥锁](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes)
* [事件组](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups)
* [软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)

创建的任务来自一组[标准演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
任务。所有 FreeRTOS 移植演示应用程序都使用标准演示任务。
这些任务没有特定的功能，创建它们仅为演示如何使用 FreeRTOS API，
以及测试 RTOS 移植。

创建“检查”任务，用于定期检查标准
演示任务（包含自我监控代码），以确保所有任务
都按预期运行。检查任务切换 LED，并在每次执行时
向 UART 输出“.”字符或错误消息。
这为系统运行状况提供了
直观反馈。**如果 LED 每 3 秒切换一次，则表示
检查任务未发现任何问题。如果 LED 每 500 毫秒
切换一次，则表示检查任务
在至少一个任务中发现问题。
UART 将输出错误消息，而不是“.”。**

#### 构建和调试演示应用程序

**重要提示：**
如果目录结构与
在官方 FreeRTOS zip 文件版本中使用的目录结构不同，则不会构建项目。
确保在将项目导入 Eclipse 工作区时，
不勾选 "copy projects into workspace"
复选框。

要打开并构建 RI5CY 项目：

1. [请按照](https://open-isa.org/get-started/)
 open-isa.org 网站上的说明，安装
 必要的 GCC、OpenOCD 和 Eclipse 开发工具，
 并将主计算机（运行开发工具的计算机）连接到目标硬件 (VEGAboard)。
 有关使用相关工具配置 Eclipse 环境的更详细说明，
 请参阅[此 open-isa 指南](https://github.com/open-isa-org/open-isa.org/blob/master/RV32M1_Vega_Develop_Environment_Setup.pdf)。
2. 启动 Eclipse，根据提示选择现有工作区，
 或创建新的工作区。
3. 在 Eclipse 的 "File" 菜单中选择 "Import"。"Import" 对话框
 随即打开。
4. 在 "Import" 对话框中，依次选择 "General" 和 "Existing Project into Workspace"，
 "Import Projects" 对话框随即打开。

![](/media/2019/Importing-an-existing-project-into-Eclipse-TriCore.jpg)

 将现有项目导入工作区
5. 在 "Import Projects" 对话框中，
 导航到 FreeRTOS/Demo/RISC-V_RV32M1_Vega_GCC_Eclipse/projects/RTOSDemo_ri5cy
 并选中该目录，确保不勾选 "copy projects into workspace"
 复选框。

[\![](/media/2019/opening_risc-v-vega_project_in_eclipse.png)](/media/2019/opening_risc-v-vega_project_in_eclipse.png)

 在 "Import Project" 对话框中选择
 目录和项目。点击放大。
6. 在 "Import Projects" 对话框的 "Projects" 窗口中，选择 RTOSDemo_ri5cy 项目，然后点击 "Finish"。
7. 在 Eclipse 的 "Project" 菜单中选择 "Rebuild All"。项目的构建
 应不会出现任何错误或警告，并输出名为 RTOSDemo_ri5cy.elf 的文件。
8. 最后，要启动调试会话，请在 Eclipse 项目资源管理器中右击 "RTOSDemo_ri5cy.launch" 文件，
 然后从弹出菜单中依次选择 "Debug As" 和 "RTOSDemo_ri5cy"
 。

[\![](/media/2019/starting_debugger_vega_board_risc-v.png)](/media/2019/starting_debugger_vega_board_risc-v.png)

 在弹出窗口中依次选择 "Debug As" 和 "RTOSDemo_ri5cy"，
 右击 "RTOSDemo_ri5cy.launch" 即可弹出该窗口。点击放大。

### 配置和使用详情

#### RTOS 移植的特定配置

本节内容与“[在 RISC-V 核心上运行 FreeRTOS](/Using-FreeRTOS-on-RISC-V)”
文档页面的信息息息相关。
* 此演示的特定配置项位于 FreeRTOS/Demo/RISC-V_RV32M1_Vega_GCC_Eclipse/projects/RTOSDemo_ri5cy/FreeRTOSConfig.h 中。您可以编辑
 [该文件中定义的常量](/Documentation/02-Kernel/03-Supported-devices/02-Customization)，以适配您的应用程序。尤其是 configCLINT_BASE_ADDRESS 和 configMTIMECMP_BASE_ADDRESS
 设置为 0，因为 VEGAboard 上的 RI5CY 内核不包括定时器 (MTIMER)。
* 除
 基础 RISC-V 架构定义的寄存器之外，RI5CY 内核还有六个额外的寄存器。这些寄存器
 由 freertos_risc_v_chip_specific_extensions.h 头文件中包含的宏保存和恢复，
 该文件位于 /FreeRTOS/Source/portable/GCC/RISC-V/chip_specific_extensions/Pulpino_Vega_RV32M1RM 目录中，
 因此该目录在汇编器的包含路径中。
* VEGAboard 软件开发套件 (SDK) 中提供的中断处理程序
 名为 SystemIrqHandler()，因此汇编器的命令行选项包括
 -DportasmHANDLE_INTERRUPT=SystemIrqHandler。
* VEGAboard 包括矢量中断控制器。FreeRTOS_startup_RV32M1_ri5cy.S 文件
 是 startup_RV32M1_ri5cy.S 的编辑版本，该文件将 FreeRTOS 陷阱处理程序
 设置为每个矢量的中断处理程序。FreeRTOS 陷阱处理程序名为 freertos_risc_v_trap_handler()。

 文件 RV32M1_ri5cy_flash.ld 是随开发板
 一起提供的链接器脚本的一个版本，经过编辑，添加了 __freertos_irq_stack_top 链接器变量，
 以确保在调度器启动之前由 main 使用的堆栈
 在调度器启动后重新用作中断堆栈。

其他注意事项：

* vPortEndScheduler() 尚未实现。
* RISC-V 项目中包含 Source/Portable/MemMang/heap_4.c，以提供
 RTOS 内核所需的内存分配。
 请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
 获取完整信息。
* 截至本文撰写之际，此演示尚不支持中断嵌套。
