---
title: "Atmel AT91SAM9 (ARM9) 移植"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

使用 [IAR 开发工具](http://www.iar.com/ewarm)

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![](/media/2018/AT91SAM9XE-RTOS.jpg)

本页展示 Atmel SAM9XE ARM9 微控制器的演示应用程序。

预置的演示项目使用 IAR 嵌入式工作台开发工具链，并
在 [AT91SAM9XE-EK 评估板](http://www.microchip.com/Developmenttools/ProductDetails.aspx?PartNO=AT91SAM9XE-EK)上运行。

**注意：**如果项目构建失败，可能是因为您使用的 IAR 
嵌入式工作台版本过低。如果构建失败，
那么也可能是项目文件（在无提示的情况下）已经损坏，因此需要
将其恢复至初始状态，然后才能构建项目，即使使用新版本的 IAR。

---

### _重要提示！关于使用 Atmel ARM9 RTOS 移植的注意事项_

_使用此 RTOS 移植前，请阅读下述所有要点。_

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [配置和使用详情](#配置和使用详情)

另请参阅常见问题：[我的应用程序未运行，哪里出错了？ ](/Why-FreeRTOS/FAQs/Troubleshooting)

---

## 源代码组织

FreeRTOS下载内容包含所有 FreeRTOS 移植的源代码，因此包含的文件比
本演示项目所需的多很多。请参阅[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)章节，
查阅已下载文件以及关于创建新项目的信息。

FreeRTOS AT91SAM9 演示项目的 IAR 工作区命名为 RTOSDemo.eww，位于 
FreeRTOS/Demo/ARM9_AT91SAM9XE_IAR 目录中。工作区包含一个单一项目，该项目具有两个配置：一个
在 ARM 模式下运行演示项目，另一个在 THUMB 模式下运行演示项目。

---

## 演示应用程序

### 演示应用程序硬件设置

演示应用程序包括通过串行端口发送和接收字符的任务。一个任务发送的字符
需要另一个任务来接收：如果遗漏任何字符或字符接收顺序错误，则会标记错误状态。UART
上需要回环连接器来运行此机制（只需要
将连接器 J20 的引脚 2 和引脚 3 连接在一起）。

演示应用程序使用原型板中内置的 LED，因此不需要其他硬件设置。

### 功能性

演示项目在启动 RTOS 调度程序之前会创建 37 个任务。这些任务大多数是“标准演示“任务，目的
是演示 RTOS API 和测试 RTOS 移植。这些任务内部并不执行任何实质性的功能。

演示项目还创建了一个“检查”任务。它
每三秒钟才执行一次，但由于优先级高，保证能够获得处理时间。
每次执行时，该任务都会检查系统中其他所有任务的状态，查看
是否有任务报告了错误。检查任务将每三秒钟切换一次 LED 状态，
前提是其他所有任务都按预期运行。如果在任何任务发现了错误，
LED 状态切换速率将更改为 500 毫秒切换一次。

如果演示项目正确执行，其表现如下：

- LED DS1 由“检查”任务控制。如果其他所有任务正常工作，
  它会每三秒钟切换一次状态。如果它的切换速率增加到每 500 毫秒切换一次，则至少有一个任务报告了错误。这个
  机制可以通过从串行端口中移除回环连接器来进行测试——这样做会人为地
  为标准 “comtest” 任务引入错误。

- LED DS5 处于标准 “comtest” 传输任务的控制之下。每当字符传输成功时，它都会切换状态。
  不过它的切换太快，无法在视觉上区分每个字符，但是 LED 确实提供了一些关于
  何时传输结束消息的反馈。

### 构建演示应用程序

1. 在 IAR 嵌入式工作台 IDE 中打开 FreeRTOS/Demo/ARM9_AT91SAM9XE_IAR/RTOSDemo.eww 工作区。

2. 根据需要选择 ARM 或 THUMB 配置。

   ![](/media/2018/SAM9-Free-RTOS-Select_Configuration.jpg)

   在 ARM 和 THUMB 配置之间进行选择。

3. 按 F7，项目构建时不应出现错误或警告。

### 运行演示应用程序

1. 确保 J-Link JTAG 调试接口已连接，并且原型板已接通电源。

2. 在 IDE 'Project' 菜单中选择 'Download and Debug'。

3. 微控制器 SDRAM 内存将自动写入演示应用程序，而且调试器
   会在 main 函数的开始处中断。

---

## 配置和使用详情

### RTOS 移植特定配置

该移植的特定配置项目包含在 DemoARM9_AT91SAM9XE_IARFreeRTOSConfig.h 中。您可以修改该文件中定义的常量
以适配您的应用程序。特别是，configTICK_RATE_HZ 定义用于
设置 RTOS tick 的频率。所提供的数值 1000 Hz 可用于测试 RTOS 内核功能，但该值
高于大多数应用程序要求的频率。降低该值将会提高效率。

每个移植都会将 "BaseType_t" 定义为该处理器的最有效数据类型。本移植将
BaseType_t 定义为长整型。

请注意，vPortEndScheduler() 尚未实现。

### 中断服务程序

通常，上下文切换需要中断服务程序。例如，正在被接收的串口字符
可以解除等待该字符资源的任务的阻塞状态。如果被 ISR 中断的任务
优先级低于被阻塞的任务，则 ISR 应直接返回到被阻塞的高优先级任务。中断程序将
中断一个任务，而返回到另一个任务。

在 ARM7 和 ARM9 上 FreeRTOS 有两种方式来实现这一点：

1. 可以配置 IRQ 向量直接跳转到发送中断的外围装置。在这种情况下，
   当前执行任务的上下文必须保存到中断入口，而新选取的任务的上下文
   必须在退出中断时还原。上下文保存和还原必须添加到每个
   可能执行让出 (yield) 操作的中断中。FreeRTOS 提供的宏可以用于执行所有必要的操作。

2. 可以配置 IRQ 向量始终跳转到单个中断入口点。完成配置后，IRQ 处理器
   先保存当前正在运行任务的上下文，然后调用用户定义的中断处理程序代码，最后当用户定义的处理程序代码返回时，还原
   下一个要运行任务的上下文。用户定义的任务只是
   标准 C 函数，无需担心它的上下文保存或还原。

本演示项目被配置为使用第二种方法。这意味着中心 IRQ 入口点负责上下文切换，
并且用户提供的中断处理程序可以是标准的 ARM 模式 C 函数。

#### 具备上下文切换功能的 ISR 示例

下文复制了演示项目提供的 UART 驱动的例子（请注意，这是为了演示 API 功能
并**不是**高效 ISR 实现的例子！）。

这只是一个 ARM 模式下的普通函数。它调用 END_SWITCHING_ISR 函数通知 RTOS 内核
应当选择一个不同的任务并且在退出中断时运行该任务。实质的任务上下文保存和恢复
是在此函数外自动完成的。

```c
/* This is a standard ARM mode function. Note that the __irq qualifier is not
   used. */
__arm void vSerialISR( void )
{
unsigned long ulStatus;
signed char cChar;
BaseType_t xHigherPriorityTaskWoken = pdFALSE;

    /* What caused the interrupt? */
    ulStatus = serCOM0->US_CSR;
    serCOM0->CSR &= serCOM0->US_IMR;

    if( ulStatus & AT91C_US_TXRDY )
    {
        /* The interrupt was caused by the THR becoming empty. Are there any
           more characters to transmit? */
        if( xQueueReceiveFromISR( xCharsForTx, &cChar, &xHigherPriorityTaskWoken )
                                                                       == pdTRUE )
        {
            /* A character was retrieved from the queue so can be sent to the
               THR now. */
            serCOM0->US_THR = cChar;
        }
        else
        {
            /* Queue empty, nothing to send so turn off the Tx interrupt. */
            vInterruptOff();
        }
    }

    if( ulStatus & AT91C_US_RXRDY )
    {
        /* The interrupt was caused by a character being received. Grab the
           character from the RHR and place it in the queue or received
           characters. */
        cChar = serCOM0->US_RHR;
        xQueueSendFromISR( xRxedChars, &cChar, &xHigherPriorityTaskWoken );
    }

    /* If a task was woken by either a character being received or a character
       being transmitted and the woken task has a higher priority than the current
       task then we need to switch to another task. xHigherPriorityTaskWoken will
        have automatically been set to pdTRUE if this is the case. */
    portEND_SWITCHING_ISR( xHigherPriorityTaskWoken );

    /* End the interrupt in the AIC. */
    AT91C_BASE_AIC->AIC_EOICR = 0;
}
```

### 编译器选项

与所有的移植一样，使用正确的编译器选项至关重要。确保这一点的最佳方法是以
提供的演示应用程序项目文件为基础构建您的应用程序，如[源组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)章节所示。

### 执行上下文

RTOS 调度器在监管者模式下执行，而任务在系统模式下执行。

**注意**：
启动 RTOS 调度器时（调用 vTaskStartScheduler），处理器必须处于监管者模式
。FreeRTOS 下载内容中所包含的演示应用程序
在调用 main() 之前切换到监管者模式。如果您没有使用
这些演示应用程序，那请在调用 vTaskStartScheduler() 之前确保处理器已进入监管者模式。

中断服务程序总是在 ARM 模式下运行。其他所有代码在 ARM 还是 THUMB 模式下执行，取决于
已经选择的配置。

SWI 指令由实时内核使用，不能被应用程序代码使用。

“系统中断”可以从多个来源生成。目前假设所有系统中断都源自
PIT（周期中断定时器）。使用任何其他系统中断都需要一些包装代码来确定
中断起点。

### 内存分配

Source/Portable/MemMang/heap_1.c 包含在 ARM7 演示应用程序项目中，用来为实时内核分配
所需的内存。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)章节
以获取完整信息。

### 串行端口驱动器

此外还需注意的是，编写串行驱动程序是为了测试部分实时内核功能，并不是
为了提供一个优化的解决方案。特别是，它们不使用外围数据控制器。
