---
title: "AT91SAM3U ARM Cortex-M3 FreeRTOS 演示"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

### 使用 IAR 编译器

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![](/media/2018/SAM3U-EK.jpg)

本页面的演示应用程序经过预配置可在 Atmel官方 SAM3U-EK 评估套件上执行。
该演示使用 FreeRTOS IAR ARM Cortex-M3 移植，可直接从 [IAR Embedded Workbench](http://www.iar.com/ewarm) for ARM 进行编译和调试。

**注意：**如果项目构建失败，则可能是使用的 IAR
嵌入式工作台版本过低。如果构建失败，
那么也可能是项目文件（在无提示的情况下）已经损坏，因此需要
还原到原始状态，然后才能使用新版本的 IAR 构建项目。

FreeRTOS ARM Cortex-M3 移植包括一个完全中断嵌套模型。必须按照
[自定义页面说明](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority) ，设置中断优先级才能正确操作。

Atmel 还为
[SAM3S-EK 评估套件](http://www.microchip.com/DevelopmentTools/ProductDetails.aspx?PartNO=ATSAM3S-EK2)
（使用 FreeRTOS 移植）提供了一个综合演示项目。这包括 GUI、QTouch、FAT 文件系统和 USB 函数。

---

### _重要提示！使用 Atmel ARM Cortex-M3_ 演示的注意事项

_使用此 RTOS 移植前,请阅读下述所有要点。_

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [RTOS 配置和使用详情](#rtos-配置和使用详情)

另请参阅常见问题：[我的应用程序未运行，哪里出错了？ ](/Why-FreeRTOS/FAQs/Troubleshooting)

---

## 源代码组织

SAM3 FreeRTOS 演示的 IAR 工作区文件称为 RTOSDemo.eww，位于  FreeRTOS/Demo/CORTEX_AT91SAM3U256_IAR 目录中。

下载的 FreeRTOS zip 文件包含所有移植文件和演示应用程序项目文件。因此，该文件所含文件
远超此演示所用的文件。请参阅[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)章节
了解下载文件的描述和有关创建新项目的信息。

---

## 演示应用程序

### 演示应用程序硬件设置

演示应用程序包括中断驱动的 UART 测试，其中一个任务传输随后由另一个任务接收的字符。
为确保此函数正确执行，必须将环回连接器安装到评估板上的 UART1 9 路连接器（9 路连接器上的
引脚 2 和 3 必须连接在一起，通常只需一个回形针）。

此演示应用程序使用了原型板上内置的 LED 和 LCD，因此无需使用其他硬件设置。

### 构建和执行演示应用程序

1. 从 Embedded Workbench IDE 中打开 FreeRTOS/Demo/CORTEX_AT91SAM3U256_IAR/RTOSDemo.eww
   项目。

2. 在 IDE 的 "Project" 菜单中选择 "Rebuild All"。项目应该成功构建，没有错误或警告。

3. 使用 J-Link JTAG 接口将主机（运行 IAR IDE 的计算机）连接到目标。

4. 在 IDE 的 "Project" 菜单中选择 "Debug"。微控制器闪存将使用演示应用程序进行编程，并且调试器会在
   main() 函数开始处中断。

### 函数

演示应用程序在启动 RTOS 调度器之前创建了 33 个任务。这些任务主要包含标准
演示应用程序任务（有关个别任务的详细信息，请参阅[演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)部分）。
其唯一目的是测试 RTOS 内核移植，并提供如何使用各种 API 函数的演示。

除了标准演示任务外，还创建了以下任务和测试：

- LCD 任务

  LCD 任务是一项“网关守卫”任务。这是唯一
  被允许直接访问 LCD 的任务。其他任务要向
  LCD 写入消息,需将消息发送到一条队列中,然后再向 LCD 任务发送该队列,而不是
  直接访问 LCD。LCD 任务只在队列中阻塞，
  等待消息，在消息到达时唤醒并显示消息。

- 检查函数 - 从[滴答钩子](/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions)调用

  每 5 秒执行一次。其主要功能是
  检查所有标准演示任务是否仍在运行。如果
  在演示任务中发现任何意外行为，检查任务将
  向 LCD 写入错误（通过 LCD 任务）。如果所有演示任务
  都执行其预期行为，检查任务将把 PASS
  写入 LCD （再次通过 LCD 任务），
  如上所述。可通过从 UART1 中移除环回连接器来测试该机制，
  这样做会故意在 COMTest 任务中生成错误。

  检查函数在中断服务程序的上下文中执行，因此能很好地
  说明如何使用网关守卫任务来控制 LCD 输出
  甚至中断输出 LCD 消息。

如果演示应用程序正确执行，将实现以下效果：

- “check”函数每 5 秒向显示器写入一次“PASS”。

- LED D2、D3 和 D4 由简单的“闪光灯”任务控制。每个 LED 灯将以不同但固定的频率切换。

---

## RTOS 配置和使用详情

### RTOS 移植特定配置

此演示的特定配置项目位于 FreeRTOS/Demo/CORTEX_AT91SAM3U256_IAR/FreeRTOSConfig.h。可
在本文件中定义的常量，以适配您的应用程序。特别是-

- **configTICK_RATE_HZ**

  可通过该常量设置 RTOS tick 的频率。提供的数值 1000 Hz 可用于
  测试 RTOS 内核功能，但这超过了大部分应用程序的频率要求。降低此值可提高效率。

- **configKERNEL_INTERRUPT_PRIORITY 和 configMAX_SYSCALL_INTERRUPT_PRIORITY**

  请参阅 [RTOS 内核配置](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configkernel_interrupt_priority-configmax_syscall_interrupt_priority-and-configmax_api_call_interrupt_priority)文档，以获取有关这些配置常量的完整信息。

注意：请记住 ARM Cortex-M3 核心使用低数值数字表示高
优先级中断，这似乎有悖直觉，而且很容易忘记！如果您希望将中断分配为低优先级，请不要将中断的
优先级指定为 0（或其他较小数值），因为这可能会导致中断实际上在系统中具有最高优先级 - 因此，如果该优先级
高于 configMAX_SYSCALL_INTERRUPT_PRIORITY，则可能会导致系统崩溃。

ARM Cortex-M3 核心的最低优先级实际上是 255，然而，不同的 ARM Cortex-M3 供应商采用了不同数量的优先位，
并提供了优先级指定方式不同的库函数。请使用提供的示例作为参考。

每个移植 #defines 'BaseType_t' 等于该处理器的最有效数据类型。本移植将
BaseType_t 定义为长整型。

请注意，vPortEndScheduler() 尚未实现。

### 中断服务程序

在演示应用程序中，向量表保存在闪存。

与大多数移植不同，导致上下文切换的中断服务程序没有特殊要求，可以根据编译器文档编写。
宏 portEND_SWITCHING_ISR() 可用于从 ISR 内请求上下文切换。名为 vSerialISR() 的示例 ISR 位于
FreeRTOS/Demo/CORTEX_AT91SAM3U256_IAR/serial/serial.c 中，应作为参考示例。

### 编译器选项

与所有的移植一样，使用正确的编译器选项至关重要。若要确保这一点，
最佳方法是基于提供的演示应用程序文件构建您的应用程序。

### 内存分配

Source/Portable/MemMang/heap_2.c 位于 ARM Cortex-M3 演示应用程序项目中，
以提供实时 RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) 章节
获取完整信息。
