---
title: "FreeRTOS Xilinx Zynq-7000 QEMU 演示 (Arm Cortex-A9) 使用基于 Xilinx Vitis Eclipse 的工具"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

 [[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![QEMU 上的 FreeRTOS](/media/2021/freertos-qemu.png)

本页记录了一种 FreeRTOS 内核演示，针对 Arm Cortex-A9
 [xilinx-zynq-a9 QEMU](https://www.qemu.org/) 型号，但此演示也可以在 Zynq-7000 硬件上运行。本
 演示使用提供的预配置 [Xilinx Vitis](https://www.xilinx.com/products/design-tools/vitis/vitis-platform.html) 项目进行构建和运行。Vitis 统一软件平台提供了多种集成工具，此演示只需要基于 Eclipse 的 C 开发 IDE。

 另有一个[较旧的 Xilinx Zynq-7000 演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Xilinx/RTOS-Xilinx-Zynq)，其中包含其他库，
 并且预配置为使用旧版 XSDK 工具进行构建。

---

#### *重要！QEMU Cortex-A9 RTOS 演示使用说明*

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#xilinx-zynq-a9-arm-cortex-a9-qemu-演示应用程序)
3. [RTOS 配置和使用详情](#rtos-配置和使用详情)

另请参阅常见问题中的[“我的应用程序无法运行，问题可能出在哪里？”](/Why-FreeRTOS/FAQs/Troubleshooting)，
请特别注意，
建议在开发过程中定义 [configASSERT()](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configassert)
（在 FreeRTOSConfig.h 中定义），并将 [configCHECK_FOR_STACK_OVERFLOW](Stacks-and-stack-overflow-checking.md)
设置为 2。

---

### 源代码组织

FreeRTOS [包](faq-github-repository-structure-versioning.md#question1)发行版包含所有 FreeRTOS 内核移植的源代码
以及所有 FreeRTOS 演示应用程序的项目，因此包含的文件
远超出此 Arm Cortex-A9 QEMU 演示所需的文件。
请参阅[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)部分，
获取目录结构的介绍以及有关创建
新 FreeRTOS 项目的信息。

Zynq-7000 xilinx-zynq-a9 QEMU 演示应用程序的 Vitis 项目位于
FreeRTOS/Demo/CORTEX_A9_Zynq_ZC702_Vitis_QEMU/RTOSDemo 目录中。这是
将项目导入 Vitis Eclipse IDE 时要选择的
目录。

---

### xilinx-zynq-a9 Arm Cortex-A9 QEMU 演示应用程序

#### 功能

此演示项目提供了简单的 blinky 和全面的测试/演示配置，
详见 [FreeRTOS 演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
文档页面。针对本页所记录的演示，"check" 任务
可在真实硬件上运行时切换 LED，
并在 QEMU 中运行时定期打印消息。消息的格式如下：

```c

AAAA - StatusMessageString:BBBB - CCCC

```

其中 AAAA 代表当前 RTOS 滴答计数，StatusMessageString 是描述性文本字符串， BBBB 是十六进制
位图值，其中每个位表示一个自检测试（如果设置了某个位，则
测试会报告错误，请参阅
[prvCheckTask()](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS/Demo/CORTEX_A9_Zynq_ZC702_Vitis_QEMU/RTOSDemo/src/full_demo/main_full.c#L262)），
CCCC 是应用程序检测到中断
嵌套的次数。

#### 构建并执行演示应用程序

Vitis 演示项目引用了 [ZC702 平台](https://www.xilinx.com/products/boards-and-kits/ek-z7-zc702-g.html)， 
该平台在 QEMU 中建模。该项目实际上将在不同的硬件平台以及 QEMU 上运行。
如果使用的是 ZC702 以外的真实硬件，则可能需要 
[更新
源代码以切换不同的 GPIO](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS/Demo/CORTEX_A9_Zynq_ZC702_Vitis_QEMU/RTOSDemo/src/ParTest.c#L51)，查看 LED 变化状态。 

要将 ZC702 平台添加到 Vitis 项目，
请执行以下操作：

1. 使用（干净的）新工作区启动 Xilinx Vitis IDE（**不是** Vitis HLS IDE）。
2. 从 "**File**" 菜单中依次选择 "**new**" 和
 "**Platform project...**"。
3. 输入 "zc702" 作为平台项目名称，然后单击 "Next" 按钮。

[\![](/media/2021/zynq-qemu-platform-project-name.jpg)](/media/2021/zynq-qemu-platform-project-name.jpg)
4. 从硬件规格列表中选择 "zc702"。由于项目已经
 包含 FreeRTOS，我们 
 不希望 Vitis 将 FreeRTOS 引入项目，因此将操作系统保持为独立。同时将处理器
 保留为 ps7_cortexa9_0。

[\![](/media/2021/selecting-zc702.jpg)](/media/2021/selecting-zc702.jpg)
5. 单击 "Finish" 按钮。

现在 Vitis Eclipse 项目已包含该平台，它是演示项目的依赖项。接下来导入 FreeRTOS 演示
项目本身：

1. 从 "**File**" 菜单中，选择 "**Import**"。
2. 在下一个窗口中，选择 "**Eclipse workspace or zip file**" 单选按钮，然后单击 "Next" 按钮。

[\![](/media/2021/importing-eclipse-workspace.jpg)](/media/2021/importing-eclipse-workspace.jpg)
3. 在下一个窗口中，选择 FreeRTOS/FreeRTOS/Demo/CORTEX_A9_Zynq_ZC702_Vitis_QEMU
 作为根目录，勾选 RTOSDemo 和 RTOSDemo_system 项目，
 请务必**不要勾选** "Copy projects into workspace" 复选框。

[\![](/media/2021/importing-zynq-qemu.jpg)](/media/2021/importing-zynq-qemu.jpg)
4. 单击 "Finish" 按钮，即可将项目导入 Vitis 中。

Vitis 工作区现已包含所需的一切，可以构建并执行项目了
。以下说明针对 QEMU。

1. 打开 main.c，并设置 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY，
 根据需要生成[简单的 blinky 演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview/#simple-blinky-demo-configuration)或[全面的测试和演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview/#comprehensive-testdemo-configuration)应用程序
 。
2. 从 "**Project**" 菜单中，选择 "**Build project**"。
 zc702 平台项目是 RTOSDemo 项目的依赖项，因此
 将在 RTOSDemo 项目之前构建。成功构建后，
 会创建 elf 文件 FreeRTOS/Demo/CORTEX_A9_Zynq_ZC702_Vitis_QEMU/Debug/RTOSDemo.elf。
3. 确保主机上已安装 QEMU。
4. 使用以下命令行启动 QEMU，将 [path-to] 替换为
 Vitis GCC 构建生成的 RTOSDemo.elf 文件的正确路径。

```c

qemu-system-arm -M xilinx-zynq-a9 -smp 1 -nographic -kernel [path_to]/RTOSDemo.elf -nographic -serial stdio -semihosting -semihosting-config enable=on,target=native -s -S  

```

QEMU 命令行

 如果只是
 希望在 QEMU 中运行 FreeRTOS 应用程序，而不连接调试器，
 请省略 "-s -S"。
5. 单击绿色 bug speed 按钮旁边的小箭头，然后从出现的菜单中选择 "Debug Configurations..."。

[\![](/media/2021/zynq-qemu-debug-config.jpg)](/media/2021/zynq-qemu-debug-config.jpg)
6. 在 Debug Configurations 窗口中，从 "GDB Hardware Debugging" 下选择 "zc702 Configuration QEMU"，
 然后单击 "Debug" 按钮。Eclipse 调试器即会创建与 QEMU 的 GDB 连接，
 启动调试会话，并在进入 main() 函数时中断。

[\![](/media/2021/zynq-qemu-debug-configuration.jpg)](/media/2021/zynq-qemu-debug-configuration.jpg)

---

### RTOS 配置和使用详情

#### FreeRTOS ARM Cortex-A 移植特定配置

请注意！请参阅
[在 ARM Cortex-A 嵌入式处理器上使用 FreeRTOS 的说明](Using-FreeRTOS-on-Cortex-A-Embedded-Processors.md)页面，
特别注意
configMAX_API_CALL_INTERRUPT_PRIORITY 设置的值和含义，**以及**
有关使用浮点单元与 GCC 的特殊说明。

此演示特定的配置项位于 /FreeRTOS/Demo/CORTEX_A9_Zynq_ZC702_Vitis_QEMU/RTOSDemo/src/FreeRTOSConfig.h 中。
[您可以编辑此文件中定义的常量，确保适配您的应用程序](/Documentation/02-Kernel/03-Supported-devices/02-Customization)。

#### 中断向量表

默认情况下， SDK 项目会将中断向量表定义为 BSP 的一部分。这会
增加安装 FreeRTOS 处理程序
（具体方法详见[“在 ARM Cortex-A 嵌入式处理器上
运行 FreeRTOS”页面](Using-FreeRTOS-on-Cortex-A-Embedded-Processors.md)）的难度。因此，此演示
会在 FreeRTOS_asm_vectors.S 中定义自己的中断向量表。
由 BSP 定义的向量表
会在运行时替换为 FreeRTOS_asm_vectors.S 中定义的向量表，这是通过调用 vPortInstallFreeRTOSVectorTable() 来实现的，
在演示中，这一步在 prvSetupHardware() 函数中完成。

FreeRTOS_asm_vectors.S 中定义的向量表放置在
名为 .freertos_vectors 的链接器区段中，而链接器脚本 lscript.ld
会将 .freertos_vectors 区段放置在 .text 区域的开头。

#### [应用程序定义的]中断服务程序

此演示使用 Xilinx 提供的驱动程序来配置中断控制器，
并安装应用程序定义的中断。示例位于
FreeRTOS/Demo/CORTEX_A9_Zynq_ZC702/RTOSDemo/src/Full_Demo/serial.c 和
FreeRTOS/Demo/CORTEX_A9_Zynq_ZC702/RTOSDemo/src/Full_Demo/IntQueueTimer.c 中。

Xilinx 驱动程序需要中断
服务程序 (ISR) 来接受 void * 参数，但是该参数
并不总是使用。因此，所需的 ISR 原型为：

```c

    void Interrupt_Handler( void *pvUnusedParameter );

```

serial.c 中名为 prvUART_Handler() 的中断处理程序
提供了一个不使用其参数的中断处理程序示例。
IntQueueTimer.c 中名为 prvTimerHandler() 的中断处理程序
提供了一个使用其参数确定
由哪个外围设备生成中断的中断示例。在这种情况下，可安装相同的中断处理程序实现，
并将其作为多个定时器的处理程序。

如果某任务的优先级等于或高于当前正在执行的任务，
并因 ISR 而解除阻塞状态，则 ISR 必须请求上下文切换，
方可退出。此时，中断服务程序会中断一项 RTOS 任务，
但返回另一项 RTOS 任务。

宏 portYIELD_FROM_ISR()（或 portEND_SWITCHING_ISR()）可用于
从 ISR 内部请求上下文切换。
下列源代码片段仅作为示例提供。ISR 示例
使用信号量与任务（未显示）同步，并调用 portYIELD_FROM_ISR()
以确保中断直接返回任务。引用的 prvUART_Handler()
和 prvTimerhandler() 函数提供了更多示例。

```c

void Dummy_IRQHandler( void *pvUnusedInThisExample )
{
long lHigherPriorityTaskWoken = pdFALSE;

    /* The parameter is not used in this case. */
    ( void ) pvUnusedInThisExample;

    /* Clear the interrupt if necessary. */
    Dummy_ClearITPendingBit();

    /* This interrupt does nothing more than demonstrate how to synchronise a
 task with an interrupt. A semaphore is used for this purpose. Note
 lHigherPriorityTaskWoken is initialised to pdFALSE. */
    [xSemaphoreGiveFromISR](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/17-xSemaphoreGiveFromISR)( xTestSemaphore, &lHigherPriorityTaskWoken );

    /* If there was a task that was blocked on the semaphore, and giving the
 semaphore caused the task to unblock, and the unblocked task has a priority
 higher than or equal to the currently Running task (the task that this
 interrupt interrupted), then lHigherPriorityTaskWoken will have been set to
 pdTRUE internally within xSemaphoreGiveFromISR(). Passing pdTRUE into the
 portYIELD_FROM_ISR() macro will result in a context switch being pended to
 ensure this interrupt returns directly to the unblocked, higher priority,
 task. Passing pdFALSE into portYIELD_FROM_ISR() has no effect. */
    portYIELD_FROM_ISR( lHigherPriorityTaskWoken );
}

```

只有以 "FromISR" 结尾的 FreeRTOS API 函数才能
从中断服务程序中调用，并且中断的优先级必须
小于或等于 configMAX_API_CALL_INTERRUPT_PRIORITY
配置常量设置的优先级（即数值更大）。

#### FreeRTOS 使用的资源

相关信息请参阅[在 ARM Cortex-A 嵌入式处理器上使用 FreeRTOS](Using-FreeRTOS-on-Cortex-A-Embedded-Processors.md) 页面。
此演示配置为从 SCU 定时器生成滴答中断。

#### 内存分配

ARM Cortex-A 演示应用程序项目中包含的 Source/Portable/MemMang/heap_4.c 可用于提供
RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
以获取完整信息。

#### 其他事项

请注意，vPortEndScheduler() 尚未实现。

