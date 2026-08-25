---
title: "Atmel AVR (MegaAVR)/ IAR RTOS 移植"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![STK500.jpg](/media/2018/STK500.jpg)

ATmega323/ATmega32 和 ATmega128 目前有两种移植：一种使用 AVR 的 [IAR Embedded WorkbenchTM](http://www.iar.com/)，
另一种使用 [WinAVR (GCC)](http://winavr.sourceforge.net/)。此页仅提供 AVR IAR 嵌入式工作台 (EWAVR) 移植的相关信息。

此外还有一些移植可用于 [ATmega320x/480x](microchip-atmega-0-port-for-xc8-avr-gcc-and-iar-ewavr) 和
 [AVR Dx](microchip-avr-dx-port-for-xc8-avr-gcc-and-iar-ewavr)，适用于 WINAVR (AVR GCC)、MPLAB XC8 和 AVR 的 IAR 嵌入式工作台。

AVR IAR 演示应用程序配置为在 Atmel
[STK500](http://www.microchip.com/developmenttools/productdetails.aspx?partno=atstk500) 上运行。
使用运行频率为 8MHz 的 AVR ATMega323 嵌入式处理器的原型板（如需使用其他开发板，请参阅[相关说明](porting-a-freertos-demo-to-different-hardware.md)）
。如果
使用 ATMega32，频率可以提高到 16 MHz。此移植还与 ATMega128 处理器一起使用。

ATMega323 的 2 KBytes RAM 容量足够运行 10 个实时任务，包括空闲任务。

**注意：**如果项目构建失败，可能是因为您使用的 IAR 
嵌入式工作台版本过低。如果构建失败，
那么也可能是项目文件（在无提示的情况下）已经损坏，因此需要
将其恢复至初始状态，然后才能构建项目，即使使用新版本的 IAR。

---

### 重要提示！使用 AVR/IAR RTOS 移植的注意事项：

_使用此移植之前，请阅读以下所有要点。_

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [配置和使用详情](#配置和使用详情)

另请参阅常见问题：[我的应用程序未运行，哪里出错了？ ](/Why-FreeRTOS/FAQs/Troubleshooting)

---

## 源代码组织

FreeRTOS 下载文件包含所有 FreeRTOS 移植的源代码。

请参阅[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)章节，获取
已下载文件的描述和新项目创建的相关信息。

AVR WinAVR 演示应用程序 makefile 位于 Demo/AVR_ATMega323_IAR 目录下。

---

## 演示应用程序

FreeRTOS 源代码下载文件包含一个用于 Mega AVR IAR RTOS 移植的完全抢占式多任务演示应用程序。

### 演示应用程序硬件设置

STK500 原型板上必须提供以下链接才能确保演示应用程序能够运行——
如上图所示：

1. PORTB 到 LEDS 的链接
2. PORTD 第 0 位和第 1 位到 RS 的链接
3. SPROG3 到 ISP6PIN 的链接（对 AVR ATMega323 进行编程的正确链接）

演示应用程序包括通过串行端口发送和接收字符的任务。一个任务发送的字符
需要另一个任务来接收：如果遗漏任何字符或字符接收顺序错误，则会标记错误状态。串行端口上
需要一个环回连接器才能让此机制正常运行（只需在串行端口连接器上将引脚 2 和 3
连接在一起）。

### 构建 RTOS 演示应用程序

1. 在 IAR 嵌入式工作台中，打开项目 Demo/AVR_ATMega323_IAR/rtosdemo.eww。

2. 从项目 (Project) 菜单中选择选项 (Options) 就会弹出项目选项对话框。

3. 在项目选项对话框中，选择 XLINK 类别。如需创建一个调试版本，请选择
   调试信息 (Debug Info) 单选按钮。如需创建一个发布版本，请选择“其他 (other)”单选按钮，并确保
   输出设置为 Intel- Extended。

4. 关闭选项对话框，然后从项目 (Project) 菜单中选择生成 (Make)。

### 功能

RTOS 演示应用程序创建 10 个标准演示任务。

1. LED 0-2 由标准的 ‘flash’ 协程控制，以固定的频率闪烁。
   每个 LED 都由单独的任务控制闪烁。

2. LED 4 和 5 由标准的 'comtest' 任务控制。每次传输 RS232 字符时，
   LED 4 都会切换。每次收到并验证 RS232 字符时，
   LED 5 都会切换。

3. 并非所有任务都会更新 LED 的状态，所以没有可见的指示表明它们运行正常。
   因此系统创建了一个 ‘Check’ 任务，用于确保在任何其他任务中
   均未检测到错误。

LED 7 由 'check' 任务控制。如果任何其他实时任务中都没有检测到错误，
LED 7 将每隔几秒钟闪烁一次。如果在任何其他任务中检测到错误，则 LED 7 将
停止闪烁。

请参阅[标准演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)章节，了解
演示应用程序任务的全部详情。

---

## 配置和使用详情

### RTOS 移植特定配置

此移植的特定配置项目位于 Demo/AVR_ATMega323_IAR/FreeRTOSConfig.h 中。
您可以编辑此文件中定义的常量，确保适配您的应用程序。特别是
用于设置 RTOS tick 的频率的 configTICK_RATE_HZ 定义。提供的数值 1000 Hz 可用于
测试 RTOS 内核功能，但这超过了大部分应用程序的频率要求。降低此值将有助于提高效率。

每个移植都会将 "BaseType_t" 定义为该处理器的最有效数据类型。此移植将
BaseType_t 定义为 char 类型。

### 使用嵌入式工作台模拟器

嵌入式工作台模拟器需要通过模拟器 (Simulator) 菜单项
或使用宏配置中断源。如需在模拟器中运行演示应用程序，您必须首先通过模拟器中断菜单项
手动“安装”定时器 1 比较匹配 A 中断 | 。

### 使用 AVR ATMega323 以外的部件

1. 在嵌入式工作台项目文件中更改了 MCU 定义。

2. 在 Demo/AVR_ATMega323_IAR/FreeRTOSConfig.h 中设置正确的时钟频率

3. 滴答 ISR 由定时器 1 上的比较匹配生成。所有 AVR 设备上的定时器配置并不相同
   。检查 Source/portable/IAR/ATMega323/port.c 中的函数 prvSetupTimerInterrupt() 以确定
   您选择的设备是否需要任何修改。

4. 确保设置后的 configTOTAL_HEAP_SIZE 定义能够匹配可用的 RAM。

5. 将 Demo/AVR_ATMega323_IAR/FreeRTOSConfig.h **和**
   Source/portable/IAR/ATMega323/portmacro.s90 中的 iom323.h 头文件替换成您所选微控制器的正确标头。

无论使用哪个零件，确保熔断 MCU 保险丝以提供正确的时钟频率（这可以从
AVR Studio 开发工具完成）。

### 抢占式内核和协同式 RTOS 内核之间的切换

将 Demo/AVR_ATMega323_IAR/FreeRTOSConfig.h 内的定义 configUSE_PREEMPTION 设置为 1 可使用抢占式调度，
设置为 0 可使用协同式调度。

### 内存管理

MegaAVR 演示应用程序 makefile 中包含 Source/Portable/MemMang/heap_1.c，用于提供
RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)章节获取
了解完整的信息。

### 开发工具

IAR 移植改编自 WinAVR 移植。IAR 编译器是一种更专业、更具针对性的产品，
但在灵活性方面不如更通用的基于 GCC 的 WinAVR 编译器。因此，对代码进行改编后需要考虑
以下要点：

1. **双任务堆栈**  
    IAR 编译器假设存在两个堆栈。“硬件”堆栈用作调用堆栈，“软件”
   堆栈用于本地变量和函数参数。

   每个任务的堆栈分为两个部分。硬件堆栈部分的大小由
    Demo/AVR_ATMega323_IAR/FreeRTOSConfig.h 文件中的 configCALL_STACK_SIZE 设置。剩余的空间用于
   软件堆栈。在确定堆栈大小时必须小心！有关这一问题的更多注释请参阅
   本页底部。

2. **锁定寄存器 (R15)**  
   项目文件将寄存器 R15 定义为“锁定”，因此编译器无法使用它。R15 也不该
   用于任何应用程序集代码。请参阅本页底部的注释，了解解除此限制的方法
   。

3. **汇编程序文件**  
    IAR 内联汇编程序功能受限，导致需要为移植源代码
   提供一个汇编程序文件。这个文件称为 portmacro.s90，位于 Source/portable/IAR/ATMega323 目录下。

4. **中断向量表**  
   理想情况下，抢占式滴答 ISR 将通过 __task 和 __interrupt 这两个关键字来定义，但这两个
   关键字在使用时是相互排斥的。因此，滴答 ISR 仅使用 __task 关键字来定义，而且
   中断向量需手动填充。不过这意味着必须手动将所有 ISR 添加到向量表中
   而且无法使用 '#pragma vector="ISRName"' 指令。

   想要编写 ISR，需要使用 __interrupt 关键字声明这一 ISR，
   然后在 Source/portable/IAR/ATMega323/portmacro.s90 中定义的向量表内填入 ISR 的名称。
   这一操作的具体说明请参阅 portmacro.s90 文件的顶部。演示应用程序中的
   串行 ISR 可以用作示例。

5. **编译器警告**  
   构建 FreeRTOS 源代码必须使用大量不同的编译器。IAR 编译器拥有特别强大的
   (pedantic) 源检查功能，在编译 FreeRTOS 源代码时会生成几个警告。

   遗憾的是，仅仅修改源代码无法修复这些警告，因为这些警告主要与良性代码有关，
   添加这些良性代码是为了修复其他编译器生成的警告（主要与类型转换有关）。
   因此，项目文件中已经禁用部分警告。

   - 提供的标准库预期 char 参数未签名（在 strncpy() 等函数中）。
     可能可以用已签名的普通 char 重新编译这些库。
   - 链接器投诉（也许是对的）数据隐藏使用的 QueueHandle_t 有两个不同定义。
   - 使用 __interrupt 关键字的函数没有明确分配到中断向量。由于上述原因，
     此警告已在项目文件中关闭。

   - 在指针投放中使用 'volatile' 关键字。此警告也已在项目文件中关闭。
     这只是您省略了关键字后另一个编译器投诉而引起的 quirk。

### 开发工具选项

与所有的移植一样，使用正确的编译器选项至关重要。确保这一点的最佳方法是基于提供的演示应用程序项目
搭建您的应用程序。

### 演示应用程序串行驱动程序

演示应用程序中包含的串行驱动程序使用 AVR ATMega323 手册中详细说明的计算方式来设置波特
率寄存器。在某些波特率下，我发现有必要稍微调整已计算的设置。我怀疑这是因为
安装在我的参考板上的 8MHz 晶体不准确，以及计算中的四舍五入的误差。

此外还需注意的是，编写串行驱动程序的是为了测试部分实时内核功能，并不是
为了提供一个优化的解决方案。

---

## 注释：

无需阅读本节即可使用移植！

### 更多关于双堆栈的信息

原本可以采用两种方法实现双堆栈要求。所选方法为每个任务维护两个堆栈。
这个操作有以下优势：

- 上下文切换的速度提高。

和以下缺点：

- 复杂性增加。必须计算两个堆栈的大小要求。
- 所有任务的硬件堆栈大小均相同。
- 内存效率降低，因为两个独立的堆栈区域都必须内置安全余量，而一般情况下只有一个堆栈区域需要。

另一种方法是可以添加一个由所有任务共享的单一硬件堆栈区域。在上下文切换期间，
硬件堆栈将被复制到软件堆栈并从软件堆栈中还原。
这种方法具有以下优势：

- 设置更简单。
- 内存效率提高。

和以下缺点：

- 上下文切换的速度变慢。
- 硬件堆栈需要单独的内存分配。这里无法使用 main() 使用的堆栈，
  因为无法确定其起点的位置。

### 锁定的 R15 寄存器

RTOS 调度器根据 WinAVR 编译器可用的 \_\_tmp_reg\_\_ 使用 R15。进入关键区域时，R15 寄存器用作
擦写寄存器。

将中断标志存入硬件堆栈而非软件堆栈后就无须执行 R15 的锁定要求
（然后在操作过程中就可以将 R15 存入软件堆栈并从软件堆栈中还原）。然而，这意味着需要将
硬件堆栈用作软件堆栈，两者之间的明确界限变得模糊。
