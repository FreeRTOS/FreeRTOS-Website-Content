---
title: "Freescale (Motorola) HCS12 (MC9S12C32) 小型内存模型"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![](/media/2018/softec.jpg)

从 FreeRTOS V3.1.1 开始，HCS12 移植可同时支持小型内存模型和内存块模型。此页面演示了如何在 MC9S12C32 处理器上
使用小型内存模型。请参阅 [MC9S12DP256B RTOS 移植](port68hcs12)页面，
获取使用内存块模型的示例。

此移植是在 [PK-HCS12C32](http://www.softecmicro.com/products.html?type=detail&title=PK-HCS12C32)
入门套件（来自 [SofTec Microsystems](http://www.softecmicro.com/)）上开发的（如果希望使用其他开发版，可以参考此处[说明](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)），使用了
[CodeWarrior HC(S)12 开发工具](http://www.codewarrior.com/MW/Develop/Embedded/HC12/Default.htm)。

---

### *重要！Freescale (Motorola) HCS12 RTOS 移植使用说明*

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [配置和使用详情](#配置和用法详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 源代码下载文件包含所有 FreeRTOS 移植的源代码。

请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)章节，获取
下载文件的描述和有关创建新项目的信息。

HCS12 CodeWarrior 小型内存模型演示应用程序项目文件位于 FreeRTOS/Demo/HCS12_CodeWarrior_small 目录中，
名为 RTOSDemo.mcp。

---

### 演示应用程序

FreeRTOS 源代码下载文件包括用于内存块 HCS12 RTOS 移植的完全抢占式多任务演示应用程序。

#### 演示应用程序硬件设置

演示应用程序使用内置在原型板上的 LED 和按钮，无需特别设置。

#### 功能

演示应用程序可创建 13 个任务，包括 11 个标准演示应用程序任务、一个“按钮推送”任务（如下）和空闲
任务。功能通过空闲任务钩子包含在了空闲任务中。请参阅
 [演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)章节，获取标准演示实时任务的详细信息。

包含其他 FreeRTOS 移植的演示应用程序使用
标准 ComTest 任务。它们使用环回连接器来在两个任务之间
传输和接收 RS232 字符。执行此测试是因为两个重要
原因：

1. 它在应用程序中断服务程序中测试上下文切换的机制。
2. 它随机分配执行时间和排序。

用于开发 HCS12 移植的原型板不容易包含 RS232 接口，
因此不使用 ComTest 任务。相反，简单的“按钮推送”任务引入了 ISR 上下文切换
和随机分配的元素。

“按钮推送”任务只在等待数据到达的队列上阻塞。连接到
入门套件板上的 PP0 输入的简单中断程序
在每次按下 PP0 按钮时将数据放置于队列中（此按钮
内置于入门套件板上）。由于“按钮推送”任务是使用
较高优先级创建的，它将取消阻塞，并希望在数据到达队列后立即执行，
从而导致 PP0 输入中断服务程序内的
上下文切换。如果从队列中攫取到的数据符合预期，则“按钮推送”
任务会切换 LED PB5。

如果演示应用程序正确执行，其表现如下：

* LED PB0、PB1 和 PB2 由 "flash" 任务控制。每个 LED 都将以恒定频率闪烁，LED PB0
 速度最快，LED PB2 速度最慢。
* 每当按下连接到输入 PP0 的按钮时， LED PB5 应切换，如上所述。
* 并非所有任务都会改变 LED，所以没有可见的指示来表明它们运行正常。
 因此，系统创建了一个检查 (Check) 任务，用于确保所有其他任务中没有检测到任何错误。

 LED PB7 由“检查”任务控制。每隔三秒，
 “检查”任务就会检查一次系统中的所有任务，以确保任务均在正确执行，没有错误，然后
 切换 LED PB7 的状态。如果 LED PB7 每三秒切换一次，则表示从未检测到错误。
 如果切换频率提高到 500 毫秒，则表示“检查”任务
 至少发现了一个错误。

#### 构建演示应用程序

RTOSDemo.mcp 项目文件（位于 FreeRTOS/Demo/HCS12_CodeWarrior_small 目录中）
应从 CodeWarrior IDE 中打开。

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
 远程调试会话，首先在下拉列表中选择 "SofTec"，如上图以蓝色突出显示部分。
 构建成功后，在 “Project” 菜单中选择 “Debug” 会自动将程序加载到微控制器
 闪存并启动调试会话（前提是您使用提供的 USB 数据线连接了目标主板！ ）。

---

### 配置和用法详情

#### 内存模型

所下载的 MC9S12C32 演示使用小型内存模型。请参阅 MC9S12DP256B 文档，了解如何使用
内存块模型。

#### RTOS 移植特定配置

此移植的特定配置项目位于 FreeRTOS/Demo/HCS12_CodeWarrior_small/FreeRTOSConfig.h。可以编辑
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
获取使用局部堆栈变量的完整示例。

#### 在抢占式和协同式 RTOS 内核之间切换

将 FreeRTOS/Demo/HCS12_CodeWarrior_small/FreeRTOSConfig.h 中的定义 configUSE_PREEMPTION 设置为 1，可使用抢占式内核；
设置为 0，可使用协同式内核。

#### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。要确保这一点，最佳方法是
以提供的演示应用程序项目文件为基础构建您的应用程序，如[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)部分所述。

#### SWI 指令

SWI 指令由 RTOS 内核使用，不能被应用程序代码使用。

#### 定时器的使用

用于生成 RTOS 滴答的定时器配置可以在 TickTimer.c 文件中查看，该文件是由 Processor Expert 生成的源文件
。

#### 内存分配

FreeRTOS/Source/Portable/MemMang/heap_1.c 包含在 HCS12 演示应用程序项目中，
以分配 RTOS 内核所需的内存。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)章节，
获取完整信息。

