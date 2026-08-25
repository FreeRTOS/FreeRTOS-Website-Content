---
title: "使用消息缓冲区进行核心到核心通信的 ST STM32H745 双核 AMP 演示"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

 [[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![来自 ST 的 STM32H745I Discovery 板](/media/2019/STM32H745I-DISCO.jpg)

**STM32H745I Discovery 板**

本页记载了简单的非对称多处理 (AMP) 核心间
通信演示，
该演示使用 [FreeRTOS 消息缓冲区实现](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers)。
随附一篇[另外的文章](/Community/Blogs/2020/simple-multicore-core-to-core-communication-using-freertos-message-buffers)
详细描述一些内部实施细节。

此演示经过预配置可在 [STM32H745I
发现板]()上运行，并使用 IAR 编译器https://www.st.com/en/evaluation-tools/stm32h745i-disco.html
[Embedded Workbench IDE 进行构建](https://www.iar.com/products/architectures/arm/)。
STM32H7xx 有一个 ARM Cortex-M4 核心和一个 ARM Cortex-M7 核心。两个核心运行同一
ARMv7-M FreeRTOS 移植。

Embedded Workbench 提供了高效且功能丰富的开发环境；
它随附一个具有充分线程感知能力的 FreeRTOS 内核插件，
允许同时调试两个 MCU 核心。

---

### 重要提示！使用FreeRTOS ARMv7-M （Cortex-M4 和 M7）移植的注意事项

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序功能](#stm32h745-双核演示应用程序)
3. [构建和运行 RTOS 演示应用程序](#构建和运行-rtos-演示应用程序)
4. 调试演示应用程序 - STLink
5. 调试演示应用程序 - I-jet
6. [RTOS 配置和使用详情](#配置和用法详情)

另请参阅常见问题：[我的应用程序未运行，哪里出错了？](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS zip 文件下载内容中包含所有 FreeRTOS 移植的源代码及
所有演示应用程序。这意味着它包含的文件数量远多于
使用 FreeRTOS STM32H745I 双核 AMP 演示所需的文件。

请参阅
[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)页面，
了解 zip 文件的目录结构体信息。此演示的 IAR Embedded Workbench 工作区
位于 FreeRTOS/Demo/CORTEX_M7_M4_AMP_STM32H745I_Discovery_IAR
目录下。工作区中的项目包含两个配置，一个用于 Cortex-M4 核心，另一个用于 Cortex-M7 核心。

---

### STM32H745 双核演示应用程序

### 功能

消息缓冲区用于传递递增数字的 ASCII 表示（因此 "0"，
后面是 "1"，再后面是 "2" 等等），即从单一“发送”RTOS 任务（或“线程”）
（在 Arm Cortex-M7 核心上运行）传递到两个“接收”RTOS 任务
（在 Arm Cortex-M4 核心上运行）。字符串长度随位数个数的增加而变化。数据信息缓冲区有两个，
每个缓冲区都对应一个接收任务。为区分两个接收任务，
将一个任务的编号指定为 0 ，另一个任务的编号指定为 1。

[![AMP 多核配置中两个核心上的 rtos](/media/2019/dual_core_AMP_topology.png)](/media/2019/dual_core_AMP_topology.png)

 硬件拓扑。点击放大。

Cortex-M7 任务位于向每个 Cortex-M4 任务发送 ascii 字符串的循环中。如果一个
接收任务在序列中接收到下一个预期值，
它会将其任务编号打印到 uART。如果接收任务接收到其他任何东西，或者
其数据接收超时，那它会命中一个 assert()，
在停止 Cortex-M4 上的所有后续处理之前向 UART 打印错误消息
。以下伪代码片段分别演示了发送
任务和接收任务的结构体。

|  |
| --- |
| <br/>```c<br/>SendingTask()<br/>{<br/>    for ever<br/>    {<br/>        Generate the next string in the sequence<br/><br/>        /* The message buffers become full so a block time is used.<br/> on each send. */<br/>        Send the generated string to the first message buffer<br/>        Send the generated string to the second message buffer<br/>    }<br/>}<br/>				<br/>```<br/><br/><br/><br/>简化过的伪代码，显示发送任务结构体<br/> <br/> |

|  |
| --- |
| <br/>```c<br/>ReceivingTask()<br/>{<br/>    for ever<br/>    {<br/>        Read next message from the message buffer<br/><br/>        /* Failed asserts print an error and stop execution. */<br/>        configASSERT( Received message is next expected in sequence );<br/>        Write task number (0 or 1) to the UART<br/>    }<br/>}<br/>				<br/>```<br/><br/><br/><br/>简化过的伪代码，显示接收任务结构体<br/> <br/> |

当执行正确时，
分配到任务编号 0 的接收任务会在 UART 写入一串 "0"，每次接收
任务接收序列中的下一个预期消息时就会时写入一个 0。同样的，
分配到任务编号 1 的接收任务也会在 UART 写入一串 "1"。该演示
会尽可能快地运行，将字符输出到 UART 所需的时间是一大
限制因素。由于
发送任务在 Cortex-M7 核心上运行，
且其运行速度是 Cortex-M4 核心速度的两倍，再加上发送任务不
受 UART 速度的限制，因此控制消息缓冲区（请参阅下文实现部分）会变满。

[\![](/media/2019/dual_core_uart_output_st.jpg)](/media/2019/dual_core_uart_output_st.jpg)

 执行演示时的 UART 输出

### 实施细节

[此演示附带的另一篇文章](/Community/Blogs/2020/simple-multicore-core-to-core-communication-using-freertos-message-buffers)
提供了详细的解释。

### 构建和运行 RTOS 演示应用程序

**重要提示：**
如果目录结构与
在官方 FreeRTOS zip 文件版本中使用的目录结构体不同，则不会构建项目。

构建和运行演示应用程序：

1. 确保包含在 IAR Embedded Studio for ARM 安装文件中的零件数据库
 包含 STM32H745。在编写时，
 您有必要手动下载
 [适用于 STM32H7 的 STM32Cube 程序包](https://www.st.com/en/embedded-software/stm32cubeh7.html)
 以获取 IAR 安装文件的更新补丁。如果
 您使用的是最新的 IAR 工具，则没有必要这么做。
2. 演示通过 STM32H745I Discovery 板上的 USB 连接器 CN14 （标记为 STLink）输出 UART 数据。
 使用 USB 数据线将 STM32H745I Discovery 板上的端口 CN14 连接至
 主机（用于查看 UART 输出的计算机)并给 Discovery 板充电，
 以使 USB（虚拟）COM 端口在主机上枚举
 。由
 JP8 跳线组设置的电源选项有好几个。
3. 使用主机上的 Teraterm 等哑串行终端，
 连接到连接 Discovery 板时被枚举的那个 COM 端口，
 并将端口设置为 115200 波特、8 数据位、1 停止位，没有奇偶校验位
 。查找 COM 端口号的一个简单方法
 就是查看
 STM32H745I Discovery 板充电和未充电时，哑终端分别提供了哪些端口号选项。
4. 打开 FreeRTOS/Demo/CORTEX_M7_M4_AMP_STM32H745I_Discovery_IAR/Project.eww
 ——在 IAR Embedded Workspace IDE 中（或在 Embedded Workbench
 中直接双击此文件打开它）。
5. 使用工作区窗口顶部的下拉菜单选择
 cortex-M4 核心的配置。

![](/media/2019/Dual_Core_Select_M4_Core.jpg)
6. 从 "Project" 菜单中选择 "Make" 以构建项目（或只需按下
 F7 即可）。
7. 右键单击工作区窗口中的项目，打开项目选项对话框，从弹出菜单中选择 "Options"
 。

![](/media/2019/Dual_Core_Project_Options.jpg)
8. 从选项对话框中的 "Debugger" 类别中选择调试接口
 。我使用内置的 STM32Link 和外部
 I -Jet 进行测试。

![](/media/2019/Dual_Core_Select_Debug_Interface.jpg)
9. 仍然在选项对话框中的 "Debugger" 类别中，选择
 您的调试接口的特定类别，确保选项被
 设置为 "connect under reset" 并使用 SWD（与 JTAG 不同）
 接口。
10. 最后在 "Debugger" 类别中，为准备调试
 嵌入式工作台（见下文），选择 "Plugins" 选项卡并确保
 已选择能充分进行线程感知的 FreeRTOS 内核插件。如果
 您已单独安装 WITTENSTEIN StateViewer 插件，请将它们也选上。

[\![](/media/2019/Selecting_Thread_Aware_FreeRTOS_Plugin.jpg)](/media/2019/Selecting_Thread_Aware_FreeRTOS_Plugin.jpg)
11. 从 "Project" 菜单中选择 "Download->Download Active Project"
 以对 Cortex-M4 核心进行编程。
12. 重复上述步骤，但此次是针对 Cortex-M7 核心（因此，
 先在工作区窗口顶部的下拉菜单选择
 cortex-M7 核心的配置）。
13. 按 STM32H745 Discovery 板上的重置按钮并查看
 哑终端中的输出。如果一切顺利，您将看到
 一串 1 和 0 正在终端窗口中快速向上滚动。

要使用内置的 STLink 调试接口调试演示应用程序：

1. 按照[上文说明](#构建和运行-rtos-演示应用程序)构建并运行应用程序，
 确保选择 STLink 作为调试接口且
 STM32H745 Discovery 板上的 STLink USB 连接器 CN14 已连接至主机。

 ST 提供应用程序笔记，描述如何配置项目选项中的 STLink
 调试设置以启用双核调试。在
 编写时，项目选项只允许一次调试一个核心
 。如果您使用 EWARM V8.40.1 或更高的版本，
 且按照下图配置调试选项，
 那进行双核调试是有可能的：

[\![](/media/2019/STLink_Settings_M4_Core.jpg)](/media/2019/STLink_Settings_M4_Core.jpg)

 在 Cortex-M4 项目中进行双核调试所需的 STLink
 的文件

[\![](/media/2019/STLink_Settings_M7_Core.jpg)](/media/2019/STLink_Settings_M7_Core.jpg)

 在 Cortex-M7 项目中进行双核调试所需的 STLink
 设置
2. 选择 Cortex-M7 项目作为活动项目，
 从 "Project" 菜单选择 "Download and Debug"。由
 Cortex-M4 核心打印到 UART 的消息应显示 Cortex-M4 核心也被重置了。
 调试器应在
 Cortex -M7 核心上的应用程序开始运行时中断，您可以像往常那样在该位置单步调试代码、设置断点以及
 检查变量等。
3. 请注意，如果应用程序被设置为正在运行，则 Cortex-M7 核心
 会在调试器中停止，同时 Cortex-M4 核心继续保持运行，
 然后
 Cortex-M4 核心上的接收任务将识别出
 来自 Cortex-M7 核心的消息已停止到达，且将命中 assert()。
 为防止这种情况发生，
 请将 prvM4CoreTasks() 中的 xShortBlockTime 变量值设置为 portMAX_DELAY，
 这样它就不会超时了。prvM4CoreTasks() 在 Cortex-M4 中的
 main.c 文件中找到。
4. 从 "FreeRTOS" 菜单中选择 "Task List" 以打开能够充分进行线程感知的 FreeRTOS 插件窗口。

要使用 I-jet（两个核心一起）调试演示应用程序，则需：

1. 按照[上文说明](#构建和运行-rtos-演示应用程序)构建并运行应用程序，
 确保选择 I-jet 作为调试接口。
2. 选择 Cortex-M7 项目作为活动项目，再次打开
 项目选项。
3. 在项目选项 "Debugger" 类别中选择 "Multicore" 选项卡，
 然后按下文所示配置选项卡（点击放大）- 将
 FreeRTOS/Demo/CORTEX_M7_M4_AMP_STM32H745I_Discovery_IAR/Project.eww
 当作从属工作区使用，以及将 FreeRTOS/Demo/CORTEX_M7_M4_AMP_STM32H745I_Discovery_IAR/Project.ewp
 当作从属项目使用
 （与 Cortex-M7 核心使用的工作区和项目相同 - 只是配置不同）。

[\![](/media/2019/dual_core_i-jet_setup.jpg)](/media/2019/dual_core_i-jet_setup.jpg)
4. 关闭项目选项对话框后，
 从 "Project" 菜单选择 "Download and Debug"。Embedded Workbench 的[主]实例
 将进行编程，然后启动
 适用于 Cortex-M7 核心的调试会话。Embedded Workbench 的第二个[从属]实例
 将自动打开，并对 Cortex-M4 核心进行同样的操作。
 Embedded Workbench 的主实例和从属实例是同步的，
 因此，您现在可以单独启动、停止和调试每个核心，也可以同时启动、停止
 并调试两个核心。请参阅
 [IAR 多核调试](https://www.iar.com/support/resources/articles/multicore-debugging/)部分
 （在 IAR 网站上）以了解更多信息。
5. 请注意，如果应用程序被设置为正在运行，则 Cortex-M7 核心
 会在调试器中停止，同时 Cortex-M4 核心继续保持运行，
 然后
 Cortex-M4 核心上的接收任务将识别出
 来自 Cortex-M7 核心的消息已停止到达，且将命中 assert()。
 为防止这种情况发生，
 请将 prvM4CoreTasks() 中的 xShortBlockTime 变量值设置为 portMAX_DELAY，
 这样它就不会超时了。prvM4CoreTasks() 在 Cortex-M4 中的
 main.c 文件中找到。
6. 从 "FreeRTOS" 菜单中选择 "Task List" 以打开能够充分进行线程感知的 FreeRTOS 插件窗口。

### 配置和用法详情

### RTOS 移植特定配置

专用于 Cortex-M4 构建的配置项目包含在 FreeRTOS/Demo/CORTEX_M7_M4_AMP_STM32H745I_Discovery_IAR/cm4/INCLUDE/FreeRTOSConfig.h 中，
专用于 Cortex-M7 构建的配置项目包含在 FreeRTOS/Demo/CORTEX_M7_M4_AMP_STM32H745I_Discovery_IAR/CM7/INCLUDE/FreeRTOSConfig.h 中。
[可以编辑此文件中定义的常量，以适配您的应用程序](/Documentation/02-Kernel/03-Supported-devices/02-Customization)。尤其是以下常量：

* **configTICK_RATE_HZ**

 此常量可用于设置 RTOS 滴答中断的频率。提供的值 (1000 Hz) 对于
 测试 RTOS 内核功能，但此频率比大多数应用程序所需的频率都要高。
 降低频率会提高效率。
* **configKERNEL_INTERRUPT_PRIORITY 和 configMAX_SYSCALL_INTERRUPT_PRIORITY**

 请参阅 [RTOS 内核配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)文档，以获取有关这些配置常量的完整信息。
* **configLIBRARY_LOWEST_INTERRUPT_PRIORITY 和 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY**

 鉴于 configKERNEL_INTERRUPT_PRIORITY 和 configMAX_SYSCALL_INTERRUPT_PRIORITY
 是完整的八位未移位值，且被定义为作为原始数据直接在 ARM CORTEX-M NVIC 寄存器中使用，
 因此，configLIBRARY_LOWEST_INTERRUPT_PRIORITY
 和 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY
 是等效物，它们被定义为仅使用 STM32H7 NVIC 中实现的 4 个优先级位
 。
 提供这些值是因为 CMSIS 库函数 NVIC_SetPriority()
 需要未偏移的 4 位格式。

请注意：请参阅[说明如何在 ARM Cortex-M 设备上设置中断优先级的页面](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4)。
我们还建议确保将所有优先级位指定为
抢占式优先级位，不要将任何优先级位指定为次优先级位，
正如在演示项目中通过函数调用进行这样的设置

```c
**HAL_NVIC_SetPriorityGrouping( NVIC_PRIORITYGROUP_4 );**
```

每个移植都使用 #define 将 "BaseType_t" 定义为对该处理器最有效的数据类型
。此移植将 BaseType_t 定义为长类型。

### 中断服务程序

与许多 FreeRTOS 移植不同的是，引发上下文切换的中断服务程序
无特殊要求，可根据编译器文档进行编写。
宏 portYIELD_FROM_ISR() 可用于在
中断服务例程内请求上下文切换。

请注意，portYIELD_FROM_ISR() 将使中断处于启用状态。

下列源代码片段仅作为示例提供。中断
使用[直达任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)
以与任务（未显示）同步，并调用 portYIELD_FROM_ISR
以确保中断直接返回任务。

```c
void Dummy_IRQHandler(void)
{
long lHigherPriorityTaskWoken = pdFALSE;

    /* Clear the interrupt if necessary. */
    Dummy_ClearITPendingBit();

    /* This interrupt does nothing more than demonstrate how to synchronise a
 task with an interrupt. A task notification is used for this purpose. Note
 lHigherPriorityTaskWoken is initialised to zero. */
    [vTaskNotifyGiveFromISR()](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/02-vTaskNotifyGiveFromISR)( xTaskToNotify, &lHigherPriorityTaskWoken );

    /* If the task with handle xTaskToNotify was blocked waiting for the notification
 then sending the notification will have removed the task from the Blocked
 state. If the task left the Blocked state, and if the priority of the task
 is higher than the current Running state task (the task that this interrupt
 interrupted), then lHigherPriorityTaskWoken will have been set to pdTRUE
 internally within vTaskNotifyGiveFromISR(). Passing pdTRUE into the
 portYIELD_FROM_ISR() macro will result in a context switch being pended to
 ensure this interrupt returns directly to the unblocked, higher priority,
 task. Passing pdFALSE into portYIELD_FROM_ISR() has no effect. */
    portYIELD_FROM_ISR( lHigherPriorityTaskWoken );
}

```

[只有以 "FromISR" 结尾的 FreeRTOS API 函数可以从
中断服务程序调用](FAQ_API.md#IQRAPI)，并且只有当中断的优先级
小于或等于 configMAX_SYSCALL_INTERRUPT_PRIORITY
配置常量（或 configLIBRARY_MAX_SYSCALL_INTERRUPT_PRIORITY）设置的优先级。

### FreeRTOS 使用的资源

FreeRTOS 需要独占 SysTick 和 PendSV 中断，使用 SVC 编号 #0。

### 抢占式内核和协同式 RTOS 内核之间的切换

将 FreeRTOSConfig.h 中的定义 configUSE_PREEMPTION 设置为 1 可使用抢占式调度，设置为 0
可使用协同式调度。选择协同式 RTOS 调度器时，完整的演示应用程序可能
无法正确执行。

### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。要确保这一点，
最佳方法是基于提供的演示应用程序文件构建应用程序。

### 内存分配

Source/Portable/MemMang/heap_4.c 包含在 ARM Cortex-M7 和 ARM Cortex-M4 配置中，
以提供 RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
以获取完整信息。

### 其他事项

请注意，vPortEndScheduler() 尚未实现。

