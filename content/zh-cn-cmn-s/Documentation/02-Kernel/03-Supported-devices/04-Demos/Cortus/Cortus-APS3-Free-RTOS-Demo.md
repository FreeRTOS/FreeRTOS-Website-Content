---
title: "FreeRTOS Cortus APS3 演示"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![](/media/2018/SPARTAN-3-starter-board.gif)  
移植开发期间所用 Digilent Spartan 3 Starter 板

此页面显示了适用于 [Cortus APS3](http://www.cortus.com/aps3.html) 处理器的 FreeRTOS 演示应用程序
。演示已预配置完成，可使用：

* [Digilent](http://www.digilentinc.com/Products/Detail.cfm?NavPath=2,400,799&Prod=S3BOARD) 推出的低成本 Spartan-3 Starter 板。
* Cortus 推出的基于 Eclipse 的 CortusIDE。
* 同样由 Cortus 推出的 GCC 编译器。

说明如下：
* 创建 Eclipse 托管的 make 项目期望查找的目录结构
 （这只涉及运行一个批处理文件）。
* 将项目和调试器设置导入 Eclipse 工作区。
* 构建演示应用程序。
* 调试演示应用程序。

---

### *重要提示！APS3 演示使用说明*

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [RTOS 配置和使用详情](#rtos-配置和用法详情)

另请参阅常见问题：[我的应用程序未运行，哪里出错了？ ](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

可将 APS3 Eclipse 项目置于 FreeRTOS/Demo/CORTUS_APS3_GCC 目录中。

下载的 FreeRTOS zip 文件包含所有移植文件和演示应用程序项目文件。因此，该文件所含文件
远超此演示所用的文件。请参阅[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)章节
了解下载文件的描述和有关创建新项目的信息。

---

### 演示应用程序

### 开发环境

如果您正在使用新版本 Cortus IDE 安装程序，请按照以下步骤
准备开发环境：

1. 须将 xstart-aps3-eval/fpga1000.mcs（由 Cortus 提供）文件编程到 Spartan-3 PROM 中。
2. 须编辑 .jtag_ini 以配置调试接口，便于使用适当电缆（USB 或并行电缆）。
 一旦 Cortus 和 Digilent 工具安装完成，即可从开始菜单访问 .jtag_ini。
3. 必须从 Windows System32 目录下将 dpcutil.dll 复制到 cortus-ide/toolchain/bin 目录下。
 请确保先备份现有的 dpcutil.dll 文件！

### 创建必要目录结构

使用 Eclipse 托管的 make 项目构建此演示应用程序。默认情况下，
托管的 make 项目应在与项目文件本身相同的目录树中，
查找完成构建所需的所有源文件。但是
标准 FreeRTOS 目录结构将核心 RTOS 内核源文件
与演示应用程序源和项目文件分离开来，这意味着如果
并未先执行一些相对复杂的配置步骤，则无法使用托管
make 项目。为了避免这种复杂情况，提供批处理文件从其默认位置
将所有必需的RTOS 内核文件复制到 APS3 项目目录。批处理
文件名为 CreateProjectDirectoryStructure.bat，位于
FreeRTOS/Demo/CORTUS_APS3_GCC 目录下。

CreateProjectDirectoryStructure.bat **必须**在
演示应用程序项目导入到 Eclipse 工作区之前执行。批处理文件
必须从命令行执行，而非从 Eclipse 本身执行。
请记住此后项目将使用 Demo/CORTUS_APS3_GCC 目录下的 RTOS 内核源文件，
而非正常的 FreeRTOS/Source 目录下的文件。

### 将演示项目导入 Eclipse 工作区

1. 启动 Cortus Eclipse。启动后，系统将提示您选择工作区位置。您可以使用现有工作区，
 或者在方便的位置创建一个新的工作区。
2. 在 Eclipse IDE 中，从 'File' 菜单中选择 'Import...'。
3. 此时将显示一个对话框。选择 Existing Projects Into Workspace，然后单击 Next（请参阅右侧图片）。
4. 浏览并选择 FreeRTOS/Demo/CORTUS_APS3_GCC 目录以完成导入过程。请注意：
 进行最后一步过程中，未勾选 Copy projects into workspace 复选框。

### 将调试器配置导入到 Eclipse 工作区

1. 在同一 Eclipse 工作区中，再次从 'File' 菜单中选择 'Import...'。
2. 此时将显示一个对话框。同样选择 Existing Projects Into Workspace，然后单击 Next。
3. 这次**选择 'Select Archive File' 单选按钮**，然后浏览并选择 FreeRTOS/Demo/CORTUS_APS3_GCC/BSP_ProjectForDebugging.zip zip 文件以完成导入过程。

![](/media/2018/RedSuite_Import.jpg)  
将 FreeRTOS 项目导入 Red Suite 工作区

### 硬件设置

演示包括标准的 “ComTest” 任务，其中
一个任务在 UART 上传输字符，然后由另一个任务接收。如果遗漏任何字符或者
或字符顺序错误，则会锁存错误。须将环回连接器安装到
UART，使该机制运转，只需将 UART Rx 引脚连接到
uART Tx 引脚（连接 UART 连接器 J2 上的引脚 2 和 3 ，
通常一个回形针便已足够）。

### 构建和执行演示应用程序

1. 首先，完成上述步骤来设置开发环境，并将演示应用程序和调试器设置项目导入
 Eclipse 工作区。
2. 在 Eclipse 的 'Build' 菜单中选择 'Build All'。应在不会产生任何错误的情况下构建此项目。
3. Eclipse 与硬件通信需要 GDB 服务器。若要开始这一过程，须
 从 “Cortus Eclipse IDE” 开始菜单项中选择 'Run GDB server' 链接。请注意，这一步骤在 Windows 启动菜单上，而非在 Eclipse IDE 内。
4. 从 Eclipse 'Run' 菜单中选择 'Debug Configurations...'。此时将显示一个对话框。  

![](/media/2018/Cortus-IDE-debug-setup.jpg)  
设置调试配置
5. 在对话框中，首先双击 “Cortus APS3 C/C++ Application”，生成一项新的调试配置。上图中
 以红色突出显示。然后，通过上图中突出显示的蓝色和绿色按钮分别设置项目和应用程序
 使其调试。最后，使用上图中突出显示的橙色按钮将 GDB 命令脚本设置为 “gdbinit-jtag”。
6. 单击 “Debug”，关闭当前对话框并启动调试会话。可能需要几秒钟才能开始调试会话。

### 演示功能

main() 在启动 RTOS 调度程序之前创建 29 个任务。任务内容主要包括
标准演示任务（参见[演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
章节，了解各个任务的详细信息）。各项任务的存在旨在示明如何使用 FreeRTOS API ，并
仅对 FreeRTOS 移植进行测试，但不包含应用程序特定的有用功能。

除了标准演示任务外，还创建了以下任务和测试：

* 检查任务
 检查任务包括提供系统状态的视觉反馈。
 检查任务在切换用户 LED LD7 之前，定期查询
 所有标准演示任务。如果用户 LED LD7 每三秒切换一次，则检查任务
 未发现任何错误。如果切换速率提升至每 500 毫秒，则
 已在至少一个任务中发现错误。这项机制可以
 通过从 UART 中移除环回连接器而进行测试，并在此过程中
 故意创建一项错误条件。
* RegTest 任务
 RegTest 任务属于检查上下文切换机制的测试任务。
 每个任务均采用已知值填充微控制器寄存器
 每个任务使用不同的值集。然后
 他们不断循环测试每个寄存器是否仍然包含
 其预期值。如果随时在任何寄存器中发现意外值，
 则会标记错误。
* 显示任务
 其中一项显示任务从 9999 倒数到 0，
 另一项定期将 “APS3” 写入显示器。

正确执行演示应用程序时，将显示以下特性：
* 标准“闪烁”任务控制 LD0 到 LD1 的 LED 灯。各灯
 将以固定但不同频率进行切换。
* “检查”任务控制 LED LD7。当系统中的所有
 其他任务无误执行时，
 它将每三秒切换一次。如果报告任何错误，切换速率将增至 500 毫秒。
* 显示屏将从 9999 倒计时到零，
 然后返回到 9999。因 “APS3” 显示几秒钟，
 计数将定期中断。

---

### RTOS 配置和用法详情

### RTOS 移植特定配置

此演示的特定配置项目位于 FreeRTOS/Demo/CORTUS_APS3_GCC/Demo/FreeRTOSConfig.h。您可以
编辑本文件中定义的常量，确保适配您的应用程序。特别是设置 RTOS tick 频率的 configTICK_RATE_HZ。
默认值 1000 对于测试 RTOS 移植很有帮助，但大多数应用程序要求的数值更快。此数值降低将提升
移植效率。

**注意：**FreeRTOSConfig.h 包含 [traceTASK_SWITCHED_IN()](/Documentation/02-Kernel/02-Kernel-features/09-RTOS-trace-feature) 宏的实现。
由 RegTest 的某个任务使用此实现，以确定
是否在适当时间关闭测试任务。实现仅适用于
此测试， RTOS 内核本身不需要实现。从
FreeRTOSConfig.h 中删除宏（仅
删除整个 traceTASK_SWITCHED_IN() 宏）将提升上下文切换
性能，但会导致 RegTest 任务错误地发出错误信号。

每个移植都'将 BaseType_t' 定义为该处理器的最有效数据类型。本移植将
BaseType_t 定义为长整型。

请注意，vPortEndScheduler() 尚未实现。

### 中断服务程序

中断服务程序可以使用以 “FromISR” 结尾的任何 API 函数，但
必须遵守以下几项规则方可实现：

1. 中断须配置为使用中断优先级 0。
2. 中断入口点必须是符合
 “裸”属性的函数。这是中断包装器。
3. 裸函数必须首先调用 portSAVE_CONTEXT() ，然后调用
 具有合格 "noinline" 属性的 C 句柄函数，最后
 调用 portRESTORE_CONTEXT() 并退出。

实践中的规则示例如下所述。本示例实现
极为简单的 UART Rx 中断。请注意，仅出于展示目的
而编写，不表示有效实现！

---

```c

/* UART Rx interrupt entry point is a function that is qualified with the
naked attribute. */
void interrupt6_handler( void ) __attribute__((naked));

void interrupt6_handler( void )
{
 /* The first line must be a call to portSAVE_CONTEXT(). */
 portSAVE_CONTEXT();

 /* The actual interrupt processing should be in a separate C function, which
 is defined using the "noinline" attribute to ensure it works at all
 optimisation levels. */
 prvRxHandler();

 /* The last line must be a call to portRESTORE_CONTEXT(). It might be that
 the interrupt saves the context of one task, but restores the context of
 another. */
 portRESTORE_CONTEXT();
}

```

---

中断入口点示例

---

```c

/* The actual interrupt processing should be placed in a separate C function that
is qualified with the noinline attribute. */
static void prvRxHandler( void ) __attribute__((noinline));

static void prvRxHandler( void )
{
signed char cChar;
BaseType_t xHigherPriorityTaskWoken = pdFALSE;

 /* A character has been received, capture the character from the UART. */
 cChar = uart1->rx_data;

 /* Send the character to a queue for processing at the task level.
 xQueueSendFromISR() will set xHigherPriorityTaskWoken to pdTRUE if a task
 was blocked on the queue waiting for data to arrive, and the task that was
 blocked has a priority that is greater than or equal to the currently
 executing task. */
 xQueueSendFromISR( xRxedChars, &cChar, &xHigherPriorityTaskWoken );

 /* This will cause a new task to be selected as the Running state task if
 xHigherPriorityTaskWoken is not pdFALSE. */
 portYIELD_FROM_ISR( xHigherPriorityTaskWoken );
}

```

---

由包装器调用 C 语言中断处理程序函数

### 在抢占式内核和协同式 RTOS 内核之间切换

将 FreeRTOS/Demo/CORTUS_APS3_GCC/Demo/FreeRTOSConfig.h 内的定义 configUSE_preemption 设置为 1 可使用抢占式调度，设置为 0
可使用协同式调度。

### 编译器选项

与所有的移植一样，使用正确的编译器选项至关重要。若要确保这一点，
最佳方法是基于提供的演示应用程序文件构建您的应用程序。

### 内存分配

Cortus 演示应用程序项目中内置 Source/Portable/MemMang/heap_2.c
以提供 RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)章节
获取完整信息。

