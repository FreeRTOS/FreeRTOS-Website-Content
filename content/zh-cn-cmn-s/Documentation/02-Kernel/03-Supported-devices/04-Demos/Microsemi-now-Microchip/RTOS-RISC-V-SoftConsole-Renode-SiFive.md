---
title: "RISC-V MiFive M2GL025/Renode 的 RTOS演示"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

 [[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![RISC-V MiFive SiFive M2GL025](/media/2019/M2GL025_Creative_Board.png)

本页记录的预配置
[SoftConsole](https://www.microsemi.com/product-directory/design-tools/4879-softconsole)/GCC FreeRTOS项目，
最初目标是 Future Electronics 公司的 MiFive RISC-V 核心，位于 Microchip （前身为 MicroSemi）
[M2GL025 创意板](https://www.microsemi.com/existing-parts/parts/143948)
。该项目目标现已改为同一创意板的 [Renode](https://renode.io/ )软件仿真，
原因是项目太大，会耗尽目标 RAM（此时需要
使用 FPGA 工具将应用程序编程到目标硬件上）。
本例中已同时安装 Renode 与 SoftConole。

---

### 重要提示！MiFive RISC-V 移植使用注意事项

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [在 RISC-V 核心上使用 FreeRTOS 的说明](#重要提示mifive-risc-v-移植使用注意事项)
2. [源代码组织](#源代码组织)
3. [演示应用程序功能](#microchip-mifive-risc-v-演示应用程序)
4. [构建 RTOS演示应用程序](#构建rtos演示应用程序)
5. [在 Renode 仿真器中运行/调试RTOS演示](#rtos在-renode-仿真器中运行演示应用程序)
6. [RTOS 配置和使用详情](#配置和使用详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？](/Why-FreeRTOS/FAQs/Troubleshooting)”。

---

### 在 FreeRTOS 核心上使用 RISC-V 的说明

如果您不满足于仅仅运行本页所描述的演示，或者
如果想要创建自己的 RISC-V FreeRTOS 项目，请阅读相关文档页面。
这些页面会介绍[在 RISC-V 核心上运行 FreeRTOS 内核的基本信息](Using-FreeRTOS-on-RISC-V)。


### 源代码组织

FreeRTOS zip 文件下载内容中包含所有 FreeRTOS 移植的源代码及
所有演示应用程序。这意味着该下载包中所包含的文件远多于
使用 FreeRTOS Microchip （前身为 Microsemi）MiFive RISC-V 演示所需的文件。

请参阅
[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)页面，
zip 文件目录结构的信息。MiFive RISV-C SoftConsole 项目位于
/Demo/RISC-V_Renode_Emulator_SoftConsole 目录中。如需了解更多信息，
请参阅下文[构建说明](#构建rtos演示应用程序)
描述。

在 RISC-V 架构中，额外的 [freertos_risc_v_chip_specific_extensions.h 头文件](/Using-FreeRTOS-on-RISC-V#RISC_V_SOURCE_FILES)
用于将基础 RISC-V RTOS 移植扩展到目标 RISC-V
芯片可以实现的任意芯片特定扩展。M2GL025 板上使用的 RISC-V 核心无法实现
任何超出基础 RISC-V 架构定义的寄存器，而且该核心包括
CLINT。因此，该项目使用 freertos_risc_v_chip_specific_extensions.h
头文件，该文件位于 FreeRTOS//Source/portable/GCC/RISC-V/chip_specific_extensions/RV32I_CLINT_no_extensions
目录。

---

### Microchip MiFive RISC-V 演示应用程序

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
 每 1000 毫秒（在 Renode 仿真器中运行时模拟 1 秒）
 将值 100 发送到队列。
* 队列接收任务：

 队列接收任务由 prvQueueReceiveTask()
 函数实现。该任务在一个循环中运行，尝试从队列读取数据时会被阻塞
 （任务处于阻塞状态时不会消耗 CPU 周期），
 会在每次从队列发送任务接收到值 100 时，
 将 "blink" 写入 Renode 控制台。
 由于队列发送任务每 1000 毫秒（模拟秒数）向队列写入一次，
 队列接收任务每 1000 毫秒（模拟秒数，可能与实际毫秒数有差异）
 解除阻塞并写入 Renode 控制台。

#### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时

mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时，main() 会调用 main_full()。
main_full() 会实现一个全面测试和演示应用程序，此应用程序会演示和/或
测试（以及其他功能）：
* [消息缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers)
* [流缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers)
* [任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)
* [事件组](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups)
* [软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)
* [队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)
* [信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)
* [互斥锁](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/)

创建的任务来自[标准演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
集。所有 FreeRTOS 移植演示应用程序都使用标准演示任务。
这些任务没有特定的功能，创建它们仅为演示如何使用 FreeRTOS API，
以及测试 RTOS 移植。

创建“检查”任务，用于定期检查标准
演示任务（包含自我监控代码），以确保所有任务
都按预期运行。每次执行检查任务时，都会向 Renode 控制台
输出 "." 字符或错误消息。
这可以直观形式反馈
直观反馈。**如果“.”每3个模拟秒出现在控制台上（
与实际秒不同），则
检查任务未发现任何问题。如果控制台显示错误
信息，则表示检查任务
在至少一个任务中发现了问题。**

#### 构建RTOS演示应用程序

**重要提示：**
如果目录结构体与
在官方 FreeRTOS zip 文件版本中使用的目录结构不同，则不会构建项目。
确保在将项目导入 Eclipse 工作区时，
不勾选 "copy projects into workspace"
复选框。

要打开并构建 M2GL025 MiFive RISC-V 项目，请执行下列操作：

1. [下载并安装](https://www.microsemi.com/product-directory/design-tools/4879-softconsole#downloads)基于 SoftConsole Eclipse 的开发工具。
2. 启动 SoftConsole，在出现提示时，
 选择现有工作区或新建工作区。
3. 从 SoftConsole 的 "File“ 菜单中选择 "Import..."。"Import" 对话框
 会打开。
4. 在 "Import" 对话框中，依次选择 "General" 和 "Existing Project into Workspace"，
 "Import Projects" 对话框随即打开。

![](/media/2019/Importing-an-existing-project-into-Eclipse-TriCore.jpg)

 将现有项目导入工作区
5. 在 "Import Projects" 对话框中，导航到
 FreeRTOS/Demo/RISC-V_Renode_Emulator_SoftConsole
 并选中该目录，确保未勾选 "copy projects into workspace"
 复选框。

[\![](/media/2019/opening_risc-v_project_in_softconsole.png)](/media/2019/opening_risc-v_project_in_softconsole.png)

 在 "Import Project" 对话框中选择
 目录和项目。点击放大。
6. 在 "Import Projects" 对话框的 "Projects" 窗口中，选择 RTOS 演示项目，然后点击 "Finish"。
7. 从 SoftConsole 的 "Project" 菜单中选择 "Build all"。项目的构建
 应不会出现任何错误或警告，并输出名为 RTOSDemo.elf 的文件。

#### RTOS在 Renode 仿真器中运行演示应用程序

下方说明演示了如何首先启动 Renode，然后启动
连接到 Renode 的调试会话，所有这些都在 SoftConsole IDE 中进行。
自 SoftConsole 版本 6.0 起，Renode 仿真器随 SoftConsole 一起提供：
1. 从 SoftConsole 的 "Run" 菜单中选择 "External Tools->External Tools Configuration..."
 。"Create, manage and run configurations" 对话框
 随即打开。
2. 此步骤将在 SoftConsole IDE 中创建菜单项，
 点击该菜单项将启动 Renode 仿真器。

 在 "Create, manage and run configurations" 对话框中，双击 "Program" 以添加
 新配置，然后严格按照
 下图（点击图片即可查看大图）完成配置。图片中未显示的选项卡可以保留
 及其默认值。

[\![](/media/2019/softconsole_renode_menu_main.png)](/media/2019/softconsole_renode_menu_main.png)

 创建启动 Renode 仿真器的配置。点击
 放大。
3. 点击 "Run"，检查配置是否可启动 Renode。如果配置能够成功启动 Renode，
 请关闭
 对话框。**注意：**Renode 启动之后，
 需手动停止，但是现在可让其继续运行，
 因为下一步中需要用到它。
4. 此步骤可创建调试启动配置。

 右击 Eclipse 项目资源管理器中的 "RTOSDemo_Debug_Renode.launch" 文件，
 然后从弹出菜单中选择 "Debug As->RTOSDemo_Debug_Renode"
 从弹出菜单中选择 "Build Project"。调试器应启动并连接到 Renode
 （假设上一步已让 Renode 运行）。

[\![](/media/2019/softconsole_creating_renode_debug_configuration.png)](/media/2019/softconsole_creating_renode_debug_configuration.png)

 创建调试启动配置。点击
 放大。
5. 如果启动配置能够成功启动调试会话，
 则在 Eclipse "Debug" 视图中选择调试会话，
 然后点击 "terminate speed" 按钮（上面有一个红色正方形），即可停止调试会话；
 同样，在 Eclipse "Debug" 视图中选择 Renode，
 然后再次点击 "terminate speed" 按钮，即可关闭 Renode。

**注意：**停止调试
 会话并不会自动停止 Renode，必须在每次调试会话后
 手动停止 Renode。如果未手动停止，则会导致
 CPU 负载过高，且无法启动任何新的调试会话。

[\![](/media/2019/terminate_renode_debug_session.png)](/media/2019/terminate_renode_debug_session.png)

 终止调试会话和 Renode。
6. 至此，启动 Renode 的配置以及
 启动连接到 Renode 的调试会话的配置均已创建，并经过测试，
 此步骤会将两个配置连接起来。

 右击 Eclipse 项目资源管理器中的 "RTOSDemo-start-renode-emulator-and-attach.launch" 文件，
 然后从弹出菜单中选择 "Debug As->RTOSDemo-start-renode-emulator-and-attach"
 。随后，应能启动 Renode，然后启动
 连接到 Renode 的调试会话。

[\![](/media/2019/softconsole_start_renode_and_attach.png)](/media/2019/softconsole_start_renode_and_attach.png)

 启动 Renode 仿真器并附加调试器

### 配置和使用详情

#### RTOS 移植的特定配置

本节内容与“[在 RISC-V 核心上运行 FreeRTOS](/Using-FreeRTOS-on-RISC-V)”
文档页面：
* 此演示特定的配置项位于 FreeRTOS/Demo/RISC-V_Renode_Emulator_SoftConsole/FreeRTOSConfig.h 中。您可以编辑
 [在该文件中定义的常量，(/Documentation/02-Kernel/03-Supported-devices/02-Customization)]以适配您的应用程序。具体而言，由于 MiFive 核心包含机器定时器 (MTIMER)，configMTIME_BASE_ADDRESS 和 configMTIMECMP_BASE_ADDRESS 分别定义为 0xBFF8 和 0x4000，其中 PRCI_BASE 是Microchip （前身为）MicrosemiSDK 中定义的 clint 基地址。
* MiFive 核心不包含任何超出
 基础 RISC-V 架构定义的寄存器。因此该项目使用
 freertos_risc_v_chip_specific_extensions.h
 头文件（位于 /FreeRTOS/Source/portable/GCC/RISC-V/chip_specific_extensions/RV32I_CLINT_no_extensions 目录下），
 以便该目录位于汇编程序的包含路径中。
* MiFive 软件开发工具包 (SDK) 中提供的中断处理程序
 名为 handle_m_ext_interrupt，因此汇编程序的命令行选项包括
 -DportasmHANDLE_INTERRUPT=handle_m_ext_interrupt。
* 文件 microsemi-riscv-renode.ld 是
 随板提供的链接器脚本的一个版本，经过编辑，添加了 __freertos_irq_stack_top 链接器变量，
 以确保在调度器启动之前由 main 使用的堆栈
 在调度器启动后重新用作中断堆栈。

其他注意事项：

* vPortEndScheduler() 尚未实现。
* RISC-V 项目中包含 Source/Portable/MemMang/heap_4.c，以提供
 RTOS 内核所需的内存分配。
 请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
 获取完整信息。
* 截至本文撰写之际，此演示尚不支持中断嵌套。
