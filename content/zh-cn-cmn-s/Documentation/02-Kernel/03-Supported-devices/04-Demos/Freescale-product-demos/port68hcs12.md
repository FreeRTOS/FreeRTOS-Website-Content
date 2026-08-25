---
title: "Motorola/Freescale HCS12 RTOS 移植 内存块模型"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

*感谢 Uri Kogan 提供原装 MC9S12DP256B 移植。*

从 FreeRTOS V3.1.1 开始，HCS12 移植可同时支持小型内存模型和内存块模型。本页演示了内存块模型
在 mC9S12DP256B 处理器上的使用。请参阅 [MC9S12C32 RTOS 移植](porthcs12)页面，
获取小型内存模型的示例。

该移植是在 [M68KIT912DP256](http://www.freescale.com/webapp/sps/site/prod_summary.jsp?code=M68KIT912DP256&parentCode=MC9S12A512&nodeId=0162468636K100) 开发套件
（来自 Freescale）上开发的（如果希望使用其他开发板，请参考此处[说明](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)）。它使用
[CodeWarrior HC12 开发工具](http://www.codewarrior.com/MW/Develop/Embedded/HC12/Default.htm)
 和 P&E Multilink USB BDM 接口，两者
均包含在开发套件中。

---

### *重要！Freescale (Motorola) HCS12 RTOS 移植使用说明*

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [配置和使用详情](#配置和使用详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 源代码下载文件包含所有 FreeRTOS 移植的源代码。

请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)章节，获取
有关下载文件的说明和创建新项目的信息。

HCS12 CodeWarrior 内存块模型演示应用程序项目文件位于 FreeRTOS/Demo/HCS12_CodeWarrior_banked 目录中，
名为 RTOSDemo.mcp。

---

### 演示应用程序

FreeRTOS 源代码下载文件包括用于内存块 HCS12 RTOS 移植的完全抢占式多任务演示应用程序。

#### 演示应用程序硬件设置

演示应用程序包括通过串行端口发送和接收字符的任务。一个任务发送的字符
需要另一个任务来接收：如果遗漏任何字符或字符接收顺序错误，则会标记错误状态。串行端口上
需要一个环回连接器才能让此机制正常运行（只需在标记为 P1 的串行端口连接器上
将引脚 2 和 3 连接在一起即可）。

演示应用程序利用了原型板上构建的 LED。

#### 功能性

演示应用程序可创建 21 个任务，包括 20 个标准演示应用程序任务和一个空闲
任务。另外两项任务则由标准演示“创建”任务定期进行动态创建和删除。
一些简单的演示功能也通过空闲任务钩子包含在了空闲任务中。具体请参阅
 [演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)章节，获取标准演示实时任务的详细信息。

如果演示应用程序正确执行，将实现以下效果：

* LED D0、D1 和 D2 由 "flash" 任务控制。每个 LED 都将以恒定频率闪烁，LED D0
 速度最快，LED D2 速度最慢。
* 当回环连接器到位时，ComTest Tx 任务传输的每个字符都会被 ComTest Rx 任务
 接收。每个传输的字符均将导致 LED D3 进行切换，每个正确接收的字符均将导致 LED D4 进行
 切换。LED D4 仅在接收到的字符与 ComTest Rx 任务预期接收字符匹配时才会切换。
* 并非所有任务都会更新 LED 状态，所以没有可见的指示来表明它们运行正常。
 因此，系统创建了一个 "Check" 任务，用于确保所有其他任务中没有检测到任何错误。

 LED D7 由 "Check" 任务控制。每隔三
 “检查”任务就会检查一次系统中的所有任务，以确保任务均在正确执行，没有错误，随后
 切换至 LED D7。如果 LED D7 每三秒切换一次，则表示从未检测到错误。
 如果切换速率增加到 500 毫秒，则表示 "Check" 任务至少发现了
 至少发现了一个错误。

#### 构建演示应用程序

RTOSDemo.mcp 项目文件（位于 FreeRTOS/Demo/HCS12_CodeWarrior_banked 目录中）
应在 CodeWarrior IDE 中打开。

该项目最初使用 [UNIS Processor Expert](http://www.processorexpert.com/) 配置功能进行创建，
导致项目中包含大量自动生成的文件和文件夹。
而 FreeRTOS 实时内核
源文件则包含在 “Source->Kernel Source” 项目文件夹中，在下图中以红色突出显示。
演示应用程序源文件位于 "Source->RTOS Demo" 项目文件夹中，在下图中以绿色
突出显示。

![](/media/2018/cwproject.gif)

显示 RTOSDemo 源文件的 CodeWarrior 项目窗口

演示应用程序项目包含两个构建配置：

1. **模拟器构建**
 要模拟 RTOS 演示项目，首先在下拉列表中选择 'Simulator' 配置，
 如上图以蓝色突出显示部分。构建成功后，在 “Project” 菜单中选择 “Debug” 将自动打开
 模拟器并启动调试会话。
2. **远程调试构建**
 可以使用 USB BDM 接口直接在 HCS12 微控制器上执行和调试项目。要启动
 远程调试会话，首先从上图蓝色突出显示的下拉列表中选择 "P&E ICD"。
 构建成功后，从项目菜单中选择“调试”将自动将程序加载到微控制器
 闪存中，并启动调试会话（前提是您已使用提供的 USB 数据线为目标主板接通了电源并进行连接！）。

---

### 配置和使用详情

#### 内存模型

所下载的 MC9S12DP256B 演示使用了内存块模型。

若要使用内存块模型：

* BANKED_MODEL 必须在文件 FreeRTOS/Demo/HCS12_CodeWarrior_banked/FreeRTOSConfig.h 中进行定义。
* CodeWarrior 项目必须被配置为使用内存块模型。

只有 PPAGE 寄存器保存为任务上下文的一部分。

**请注意**：RTOSDemo.mcp 项目将大多数内存库定义为仅有 256 字节长度。这单纯是为了
强制代码位于不同的库中，以便测试 RTOS 内核库代码切换。用户应根据其应用程序的需求修改此
内存映射。

#### RTOS 移植特定配置

此移植的特定配置项位于 FreeRTOS/Demo/HCS12_CodeWarrior_banked/FreeRTOSConfig.h 中。可编辑
此文件中定义的常量，以适配您的应用程序。尤其是 configTICK_RATE_HZ 定义，
用于设置 RTOS 的 tick 频率。演示项目提供的值 1000 Hz 可用于测试 RTOS 内核功能，
但该值超出了大多数应用程序需要的速率。降低此值将提高效率。

每个移植都会将 "BaseType_t" 定义为对处理器而言最有效的数据类型。此移植将
BaseType_t 定义为 char 类型。

请注意，vPortEndScheduler() 尚未实现。

#### 中断服务程序

中断向量表包含在 Vectors.c 源文件中。Vectors.c 最初
由 Processor Expert 实用程序创建，但随后经手动修改，定制为能够与实时内核和
演示应用程序共同使用。如果再次使用 Processor Expert，它将重新创建文件并覆盖这些修改。
因此，建议保留 Vectors.c 写入保护，且仅使用手动更新。

不会引起上下文切换的中断服务程序没有特殊要求，可以按照
正常的 CodeWarrior 语法写入。

通常，上下文切换需要中断服务程序。例如，正在被接收的串行端口字符
可能会唤醒在等待该字符时被阻塞的高优先级任务。如果 ISR 中断了一个优先级较低的任务，
则其应立即返回到已被唤醒的任务。宏 portTASK_SWITCH_FROM_ISR() 用以允许
此项功能。请注意，portTASK_SWITCH_FROM_ISR() 只能在 ISR 结束时（且其未声明任何静态局部变量）
使用。如果 ISR 使用了局部变量，则调用 portYIELD() 可以
用于代替 portTASK_SWITCH_FROM_ISR() 宏。

以下是
来自演示应用程序的函数 vButtonPush() 的示例：

```c

/* ISR connected to PP0 button input. */
void interrupt vButtonPush( void )
{
    static UBaseType_t uxValToSend = 0;

    /* Send an incrementing value to the button push
    task each time the button is pushed. */
    uxValToSend++;

    /* Clear the interrupt flag. */
    PIFP = 1;

    /* Send the incremented value down the queue.  The
    button push task is blocked waiting for the data.
    As the button push task is high priority it will
    wake and a context switch should be performed before
    leaving the ISR. */
    if( xQueueSendFromISR( xButtonQueue, &uxValToSend, pdFALSE ) )
    {
        /* Posting the message caused a higher priority
        task to unblock.  This is the end of the ISR so
        we can perform the task switch here.  This can be
        used as the only local variable is static. */
        portTASK_SWITCH_FROM_ISR();
    }
}

```

请参阅 FreeRTOS/Demo/HCS12_CodeWarrior_banked/serial/serial.c 中的中断函数 vCOM0_ISR()，
获取如何使用局部堆栈变量的完整示例。

#### 在抢占式和协同式 RTOS 内核之间切换

将 FreeRTOS/Demo/HCS12_CodeWarrior_banked/FreeRTOSConfig.h 内的定义 configUSE_PREEMPTION 设置为 1，即可使用抢占式内核；设置为 0，即可使用
协同式内核。

#### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。要确保这一点，最佳方法是
以提供的演示应用程序项目文件为基础构建您的应用程序，如[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)部分所述。

#### SWI 指令

SWI 指令由 RTOS 内核使用，不能被应用程序代码使用。

#### 定时器的使用

用于生成 RTOS 滴答的定时器配置可以在 TickTimer.c 文件中查看，该文件是由 Processor Expert 生成的源文件
。

#### 内存分配

FreeRTOS/Source/Portable/MemMang/heap_2.c 包含在 HCS12 演示应用程序项目中，
以分配 RTOS 内核所需的内存。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)章节，
获取完整信息。

