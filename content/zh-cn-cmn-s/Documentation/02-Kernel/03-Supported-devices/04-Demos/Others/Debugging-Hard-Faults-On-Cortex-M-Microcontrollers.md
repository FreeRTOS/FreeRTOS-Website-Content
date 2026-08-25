---
title: "调试 ARM Cortex-M3 和 ARM Cortex-M4 微控制器上的硬故障和其他异常"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


## 简介

ARM Cortex-M 核心实现了一组故障异常。每个异常都涉及
一个错误条件。如果发生错误，ARM Cortex-M 核心停止执行当前
指令，并跳转到异常处理函数。这项机制就如同
中断所用机制一般，ARM Cortex-M 内核在接受中断时
会跳转到中断处理程序。

故障处理程序的 CMSIS 名称如下：

- UsageFault_Handler()
- BusFault_Handler()
- MemMang_Handler()
- HardFault_Handler()

ARM Cortex-M 核心调用这些处理程序的具体情况
本文档暂不讨论。如果您对相关细节感兴趣，请参阅 ARM 的 ARM Cortex-M 文献以及
其他来源。就本文档而言，
本文内容足以说明如果您的应用程序出现了任何一个上述处理程序，
那说明出现了问题。最常见的故障类型是硬故障，
原因是其他未单独启用的故障类型将升级为
硬故障。

尽管许多人提出了大量 RTOS 支持请求，当
使用 RTOS 内核时，硬故障处理程序导致其应用程序中断，
我们解决问题时，总是发现
硬件故障原因并非内核，而是以下原因之一：

- 对 ARM Cortex-M 核心中断优先级存在误解（极易发生） ，
  或对如何使用 FreeRTOS 中断嵌套模型存在误解。可参阅
  “[在 ARM Cortex-M Core 上运行 RTOS](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4)”
  文档页面来帮助解决此问题。

- 常规 RTOS 用户错误。另请参阅常见问题
  “[我的应用程序未运行，可能出了什么问题？](/Why-FreeRTOS/FAQs/Troubleshooting)”
  页面来帮助解决此问题。

- 应用程序代码错误。

硬故障调试应首先确保软件应用程序遵循
上述前两项要点中链接的两个页面
上提供的指南。如果此后硬故障仍然存在，则须
确定故障发生时的系统状态。调试器并非
始终都能做到这一点；鉴于此，本页其余部分描述了
一种可用于此目的的软件技术。

## 确定正在执行的异常处理程序

中断向量表通常会为每个中断/异常源安装相同的处理程序
。默认处理程序属于
[弱符号](https://en.wikipedia.org/wiki/Weak_symbol)，
可以允许应用程序编写者仅需通过实现具有正确名称的函数
来安装自己的处理程序。如果因应用程序编写者
并未提供其自有处理程序而导致中断，则将执行
默认处理程序。

通常以无限循环的方式执行默认中断处理程序。如果
应用程序出现了上述默认处理程序，则须首先确定
实际执行的是哪个中断。

下述代码片段演示了如何向默认无限循环处理程序中加一些指令，
以便在进入无限循环之前
将执行中断的编号加载到寄存器 2 (r2)。

以这种方式从 NVIC 读取的中断号
涉及向量表的开头，其中
系统异常（例如硬故障）条目在外设中断条目之前。
如果 r2 包含数值 3，则正在处理硬故障异常。
如果 r2 包含等于或大于 16 的数值，那么正在处理外设中断——
可以通过从中断号中减去
16 来确定中断的外设。

```c
Default_Handler:
  /* Load the address of the interrupt control register into r3. */
     ldr r3, NVIC_INT_CTRL_CONST
  /* Load the value of the interrupt control register into r2 from the
     address held in r3. */
  ldr r2, [r3, #0]
  /* The interrupt number is in the least significant byte - clear all
     other bits. */
  uxtb r2, r2
Infinite_Loop:
  /* Now sit in an infinite loop - the number of the executing interrupt
     is held in r2. */
  b  Infinite_Loop
  .size  Default_Handler, .-Default_Handler

.align 4
/* The address of the NVIC interrupt control register. */
NVIC_INT_CTRL_CONST: .word 0xe000ed04
```

## 调试 ARM Cortex-M 硬故障

故障处理程序的栈帧包含故障发生时的
ARM Cortex-M 寄存器的状态。下述代码显示了如何将寄存器值
从栈中读取到 C 变量中。完成此操作后，
如同其他变量一样，可以在调试器中检查变量值。

首先，定义了一个非常短的汇编函数，用以确定
故障发生时正在使用的栈。完成此操作后，故障处理程序汇编代码
将指向栈的指针传递到名为 prvGetRegistersFromStack() 的 C 函数中。

使用 GCC 语法的故障处理程序如下所述。请注意，该函数属于
为裸函数，因此该函数不包含任何编译器生成的代码（例如，
无函数入口序言代码）。

```c
/* The prototype shows it is a naked function - in effect this is just an
   assembly function. */
static void HardFault_Handler( void ) __attribute__( ( naked ) );

/* The fault handler implementation calls a function called
   prvGetRegistersFromStack(). */
static void HardFault_Handler(void)
{
    __asm volatile
    (
        " tst lr, #4                                                \n"
        " ite eq                                                    \n"
        " mrseq r0, msp                                             \n"
        " mrsne r0, psp                                             \n"
        " ldr r1, [r0, #24]                                         \n"
        " ldr r2, handler2_address_const                            \n"
        " bx r2                                                     \n"
        " handler2_address_const: .word prvGetRegistersFromStack    \n"
    );
}
```

PrvGetRegistersFromStack() 的实现如下所示。prvGetRegistersFromStack()
将寄存器值从堆栈复制到 C 变量中，然后置于
循环中。命名各变量，指示变量保存的寄存器值。
自发生故障后，其他寄存器将保持不变，并且可
直接在调试器的 CPU 寄存器窗口中查看。

```c
void prvGetRegistersFromStack( uint32_t *pulFaultStackAddress )
{
/* These are volatile to try and prevent the compiler/linker optimising them
   away as the variables never actually get used. If the debugger won't show the
   values of the variables, make them global my moving their declaration outside
   of this function. */
volatile uint32_t r0;
volatile uint32_t r1;
volatile uint32_t r2;
volatile uint32_t r3;
volatile uint32_t r12;
volatile uint32_t lr; /* Link register. */
volatile uint32_t pc; /* Program counter. */
volatile uint32_t psr;/* Program status register. */

    r0 = pulFaultStackAddress[ 0 ];
    r1 = pulFaultStackAddress[ 1 ];
    r2 = pulFaultStackAddress[ 2 ];
    r3 = pulFaultStackAddress[ 3 ];

    r12 = pulFaultStackAddress[ 4 ];
    lr = pulFaultStackAddress[ 5 ];
    pc = pulFaultStackAddress[ 6 ];
    psr = pulFaultStackAddress[ 7 ];

    /* When the following line is hit, the variables contain the register values. */
    for( ;; );
}
```

## 使用寄存器值

[另请参阅下述[“处理不精确故障](#处理不精确故障)”]

第一个密切相关的寄存器是程序计数器。上述代码中，
所述变量 pc 包含程序计数器值。当故障是
精确故障时， pc 包含
硬故障（或其他故障）时执行的指令
的地址。当故障为不精确故障时，
需要执行[额外步骤
来](#处理不精确故障)查找导致故障的指令的地址。

如欲在 pc 变量中包含的地址中找到指令，或者...

1. 在调试器中打开一个汇编代码窗口，然后手动输入
   地址，查看该地址的汇编指令，或者

2. 打开调试器中的断点窗口，并在该地址
   手动定义执行或访问断点。设置断点后，重新启动应用程序
   查看指令涉及的代码行。

了解故障发生时正在执行的指令，
可知晓重点关注其他寄存器值，这一点也至关重要。例如，
如果指令使用 R7 的值作为地址，则需要知晓 R7 的值。
此外，检查汇编代码代码和产生汇编代码的 C 代码将显示
r7 实际包含的值（例如可能是变量的值）。

## 处理不精确故障

ARM Cortex-M 故障可以是精确故障，也可以是不精确故障。如果在 BusFault 状态寄存器
（或 BFSR，可在地址 0xE000ED29 处进行字节访问）中
设置了 IMPRECISERR 位（位 2），则故障不精确。

由于故障不一定会与导致故障的指令同时发生，
因此，确定不精确故障的原因更是
难上加难。例如，如果对内存的写入
进行缓存，在启动写入内存的汇编指令
和实际发生的写入内存之间可能会存在延迟。
如果此类延迟写入操作无效（例如
正在尝试写入无效的内存位置) ，则会发生写入
不精确故障，并且使用上述代码获得的程序计数器值
将不是发起写入操作的汇编指令
。

在上述示例中，通过设置辅助控制寄存器（或 ACTLR）中的 DISDEFWBUF 位（位 1）来关闭写缓冲，
将导致不精确故障变为精确故障，使得
故障更易于调试，但是程序执行会较慢。
