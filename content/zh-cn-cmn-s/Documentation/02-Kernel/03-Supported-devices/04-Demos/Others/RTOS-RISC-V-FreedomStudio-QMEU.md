---
title: "适用于 RISC-V QEMU sifive&nbsp;e 型号的 RTOS 演示"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

 [[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![RISC-V HiFive SiFive QMEU](/media/2019/freedom_studio_risc-v.png)

此页面记录了一个预配置的 SiFive Freedom Studio 项目，
此项目使用 GCC 和 GDB 在 sifive_e QEMU 模型中构建并运行 FreeRTOS RISC-V 演示。

---

### 重要提示！使用 SiFive RISC-V 移植的注意事项

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [在 RISC-V 核心上使用 FreeRTOS 的说明](#重要提示使用-sifive-risc-v-移植的注意事项)
2. [源代码组织](#源代码组织)
3. [演示应用程序功能](#sifive_e-qemu-risc-v-演示应用程序)
4. [构建 RTOS 演示应用程序](#构建演示应用程序-rtos)
5. [在 QEMU 仿真器中运行/调试 RTOS 演示](#在-qemu-仿真器中运行-rtos-演示应用程序)
6. [RTOS 配置和使用详情](#配置和使用详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？](/Why-FreeRTOS/FAQs/Troubleshooting)”。

---

### 在 FreeRTOS 核心上使用 RISC-V 的说明

如果您不满足于仅仅运行本页所描述的演示，或者
如果想要创建自己的 RISC-V FreeRTOS 项目，请阅读相关文档页面。
这些页面会介绍[在 RISC-V 核心上运行 FreeRTOS 内核的基本信息](Using-FreeRTOS-on-RISC-V)。


### 源代码组织

FreeRTOS zip 文件下载内容中包含所有 FreeRTOS 移植的源代码及
所有演示应用程序。这意味着它包含的文件比使用
FreeRTOSsifive_e QEMU RISC-V 演示所需的文件多得多。

请参阅
[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)页面，
了解 zip 文件的目录结构体信息。sifive_e RISC-V QEMU Freedom Studio 项目位于
/Demo/RISC-V-Qemu-sifive_e-FreedomStudio 目录下。如需了解更多信息，
请参阅下文[构建说明](#构建演示应用程序-rtos)
描述。

在 RISC-V 架构中，额外的 [freertos_risc_v_chip_specific_extensions.h 头文件](/Using-FreeRTOS-on-RISC-V#RISC_V_SOURCE_FILES)
用于将基础 RISC-V RTOS 移植扩展到目标 RISC-V
芯片可能实现的任意芯片特定扩展。QEMU sive5_e 模型未实现任何
超过基础 RISC-V 架构定义的寄存器，并且确实仿真了 CLINT。
因此，该项目使用 freertos_risc_v_chip_specific_extensions.h
头文件，该文件位于 FreeRTOS//Source/portable/GCC/RISC-V/chip_specific_extensions/RV32I_CLINT_no_extensions
目录下。

---

### Sifive_e QEMU RISC-V 演示应用程序

#### 功能

常量 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 在 main.c 文件顶部定义，
用于在简单 "blinky" 风格的入门项目
和更全面的测试和演示应用程序之间切换。

#### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 时

mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 时，main() 会调用 main_blinky()。
main_blinky() 会创建使用两项任务和一个队列的基本示例。
* 队列发送任务：

 队列发送任务由 prvQueueSendTask() 函数实现。
 它位于一个循环中，每秒都会向队列发送值 100
 每 1000 仿真毫秒（1 仿真秒）会发送值 100 至队列。
* 队列接收任务：

 队列接收任务由 prvQueueReceiveTask()
 函数实现。它位于一个循环中，
 该循环会阻塞读取队列的尝试（任务被阻塞时不会消耗 CPU 周期），
 会在每次从队列发送任务接收到值 100 时，
 将 "blink" 写入 QEMU 控制台。

 由于队列发送任务每 1000 仿真毫秒会向队列写入一次，
 因此队列接收任务会每 1000 仿真毫秒解除阻塞并写入
 QEMU 控制台。

#### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时

mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时，main() 会调用 main_full()。
main_full() 会实现一个全面测试和演示应用程序，此应用程序会演示和/或
测试（除此之外）：
* [流缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers)
* [消息缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers)
* [任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)
* [事件组](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups)
* [信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores)
* [互斥锁](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes)
* [软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)
* [队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues)

创建的任务来自一组[标准演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
任务。所有 FreeRTOS 移植演示应用程序都使用标准演示任务。
这些任务没有特定的功能，创建它们仅为演示如何使用 FreeRTOS API，
以及测试 RTOS 移植。

创建“检查”任务，用于定期检查标准
演示任务（包含自我监控代码），以确保所有任务
都按预期运行。每次执行检查任务时，都会向 QEMU 控制台
输出 "." 字符或错误消息。
为系统健康提供了
直观反馈。**如果“.”每 3 个模拟秒出现在控制台上（
可能与实际秒不同），则
检查任务未发现任何问题。如果控制台显示错误
信息，则表示检查任务
在至少一个任务中发现了问题。**

#### 构建演示应用程序 RTOS

**重要提示：**
如果目录结构体与
在官方 FreeRTOS zip 文件版本中使用的目录结构不同，则不会构建项目。
确保在将项目导入 Eclipse 工作区时，
不勾选 "copy projects into workspace"
复选框。

想要打开并构建 Freedom Studio RISC-V 项目，则需：

1. [下载并安装 Freedom Studio 开发工具](https://www.sifive.com/boards)（下滑查看软件下载）。
2. 启动 Freedom Studio，根据提示选择现有工作区，
 或创建新的工作区。
3. 在 Freedom Studio 的 "File" 菜单中选择 "Import..."。"Import" 对话框
 会打开。
4. 在 "Import" 对话框中，依次选择 "General" 和 "Existing Project into Workspace"，
 "Import Projects" 对话框随即打开。

![](/media/2019/Importing-an-existing-project-into-Eclipse-TriCore.jpg)

 将现有项目导入工作区
5. 在 "Import Projects" 对话框中，导航到
 FreeRTOS/Demo/RISC-V-Qemu-siFive_e-FreedomStudio
 并选中该目录，确保不勾选 "copy projects into workspace"
 复选框。

[\![](/media/2019/opening_risc-v_project_Freedom_Studio.png)](/media/2019/opening_risc-v_project_Freedom_Studio.png)

 在 "Import Project" 对话框中选择
 目录和项目。点击放大。
6. 在 "Import Projects" 对话框的 "Projects" 窗口中，选择 RTOS 演示项目，然后点击 "Finish"。
7. 在 Freedom Studio 的 "Project" 菜单中选择 "Build all"。项目的构建
 不应出现任何错误或警告，并创建一个名为 RTOSDemo.elf 的文件。

#### 在 QEMU 仿真器中运行 RTOS 演示应用程序

1. [下载 QEMU](https://www.qemu.org/download/)。
 该项目使用
 [预建的 Windows 二进制文件创建和测试](https://qemu.weilnetz.de/w64/)。
2. 使用下面的命令行启动 QEMU，将 "path/to"
 替换为按照上文构建说明输出的、到 RTOSDemo.elf
 的实际路径：

```c
qemu-system-riscv32 -kernel path/to/RTOSDemo.elf -S -s -machine sifive_e

```
3. 最后，右键单击 Eclipse 项目资源管理器中的 "Hardware_QEMU.launch" 文件，
 然后从弹出菜单中选择 "Debug As->Hardware_QEMU"
 从弹出菜单中选择 "Build Project"。调试器应启动并连接到 QEMU
 （假设上一步已让 QEMU 运行）。

[\![](/media/2019/starting_debugger_freedom_studio_qemu.png)](/media/2019/starting_debugger_freedom_studio_qemu.png)

 创建调试启动配置。点击
 放大。

### 配置和使用详情

#### RTOS 移植的特定配置

本节内容与“[在 RISC-V 核心上运行 FreeRTOS](/Using-FreeRTOS-on-RISC-V)”
的文档页面信息相关。
* 此演示的特定配置项位于 FreeRTOS/Demo/RISC-V-Qemu-sifive_e-FreedomStudio/FreeRTOSConfig.h 。
 [可对该文件中定义的常量](/Documentation/02-Kernel/03-Supported-devices/02-Customization)
 可进行编辑以适配您的应用程序。特别是，由于仿真 SiFive 核心包括一个硬件定时器 (MTIMER)，configMTIME_BASE_ADDRESS 和 configMTIMECMP_BASE_ADDRESS 分别定义为 (CLINT_CTRL_ADDR) + 0xBFF8 和 (CLINT_CTRL_ADDR) + 0x4000。
* 仿真 SiFive 核心不包括任何超出
 基础 RISC-V 架构定义的寄存器。因此该项目使用
 freertos_risc_v_chip_specific_extensions.h
 头文件（位于 /FreeRTOS/Source/portable/GCC/RISC-V/chip_specific_extensions/RV32I_CLINT_no_extensions 目录下），
 因此该目录在汇编器的包含路径中。
* SiFive 软件开发套件 (SDK) 中提供的中断处理程序
 被称为 trap_handler，因此汇编器的命令行选项包括
 -DportasmHANDLE_INTERRUPT=handle_trap。
* 文件 flash.lds 是随开发工具一起提供的链接器脚本的一个版本，
 经过编辑，添加了必要的 __ freertos_irq_stack_top
 链接器变量，以确保在调度器启动前被 main 使用的堆栈
 在调度器启动后重新用作中断堆栈。

其他注意事项：

* vPortEndScheduler() 尚未实现。
* RISC-V 项目中包含 Source/Portable/MemMang/heap_4.c，以提供
 RTOS 内核所需的内存分配。
 请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
 获取完整信息。
* 截至本文撰写之际，此演示尚不支持中断嵌套。
