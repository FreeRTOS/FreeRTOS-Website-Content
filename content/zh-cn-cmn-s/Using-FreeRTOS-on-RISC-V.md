---
title: 在 RISC-V 微控制器上使用 FreeRTOS
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


## 序言

正如在[升级到 FreeRTOS V10.3.0](/Documentation/04-Roadmap-and-release-note/02-Release-notes/04-FreeRTOS-V10.3.0)
页面上所指出的那样，configCLINT_BASE_ADDRESS 配置设置已经被弃用，
并被本页所述的 configMTIME_BASE_ADDRESS 和 configMTIMECMP_BASE_ADDRESS 设置取代
。如果旧版应用程序仍然使用 configCLINT_BASE_ADDRESS 设置，
会出现编译器警告，但应用程序还是会照旧
继续构建和运行。


## 简介

RISC-V 指令集架构 (ISA) 易于扩展，
并且没有指明物理 RISC-V 微控制器或片上系统 (SoC) 实现
的一切信息。因此，FreeRTOS RISC-V 移植也是可扩展的——
它提供了一个处理所有 RISC-V
实现所共有的寄存器的基本端口，以及[一组必须实现的宏](Using-FreeRTOS-on-RISC-V#PORTING_FREERTOS_TO_RISC_V)，
以处理硬件实现的特定功能和扩展，
如额外寄存器。


## 快速使用指南

此页面正文提供了关于
为 RISC-V 核心构建 FreeRTOS 的详细信息，但最简单的方法是
使用以下预配置的示例项目之一（在编写时
正确列出）：

* [MiFive M2GL025 Creative Board 和 Renode（使用 GCC 和 SoftConsole IDE）](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Microsemi-now-Microchip/RTOS-RISC-V-SoftConsole-Renode-SiFive)
* [VEGAboard PULP RI5CY 演示（使用 GCC 和 Eclipse）](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Others/RTOS-RISC-V-Vegaboard_Pulp)
* [SiFive sifive_e QEMU 模拟器（使用 Freedom Studio 和 GCC）](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Others/RTOS-RISC-V-FreedomStudio-QMEU)

示例 RISC-V 项目
位于以 "RISC-V" 开头的 FreeRTOS/Demo 子目录中，
该子目录在主 FreeRTOS zip 文件下载中。这些项目可以直接使用，
也可单纯用作下文详述的源文件、
配置选项和编译器设置的工作示例和参考。

总之，要为 RISC-V 核心构建 FreeRTOS，必须：

1. [在项目中包含核心 FreeRTOS 源文件和 FreeRTOS RISC-V 移植层源文件](#源文件)。
2. [确保汇编器的包含路径包括描述芯片特定实现细节的头文件路径](#源文件)。
3. [在 FreeRTOSConfig.h 中定义一个常量或一个链接器变量，以指定用作中断堆栈的内存](#中断系统堆栈设置)。
4. [在 FreeRTOSConfig.h](#freertosconfigh-设置) 中定义 configMTIME_BASE_ADDRESS 和 configMTIMECMP_BASE_ADDRESS。
5. [对于汇编器，#define（定义）portasmHANDLE_INTERRUPT 为芯片或工具供应商提供的用于处理外部中断的函数的名称](#所需的编译器和汇编器命令行选项)。
6. [安装 FreeRTOS 陷阱处理程序](#安装-freertos-陷阱处理程序)。


其他可能有用的链接包括：

* [FreeRTOS 内核快速入门指南](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/02-Quick-start-guide)
* [根据不同硬件调整 FreeRTOS 演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)
* [创建新的 FreeRTOS 项目](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project)

---

## 详细信息

### FreeRTOS RISC-V 移植的功能

FreeRTOS RISC-V 移植：

* 是为 GCC 和 [IAR](https://www.iar.com/iar-embedded-workbench/#!?architecture=RISC-V) 编译器提供的。

* 仅支持在 32 位和 64 位 RISC-V 内核上的机器模式整数执行，
  但正在积极开发中，未来的 FreeRTOS 版本
  将根据用户要求增加特性和功能。

* 实现一个单独的中断堆栈，这样会大大减少了
  小型微控制器的 RAM 使用量，
  这是因为每个任务无需有一个足够大的堆栈来容纳中断和非中断
  堆栈帧。

* 提供了一个可以轻松扩展的基本端口，可以容纳 RISC-V
  实现特定的架构扩展。


### 源文件

[FreeRTOS 内核源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)
页面包含有关向项目添加 FreeRTOS 内核的信息。除
该页面上的信息外，FreeRTOS RISC-V 移植还需要一份额外的
头文件。额外的头文件描述了芯片的具体细节，
这是必须的，因为 RISC-V 芯片通常包括芯片的特定架构扩展。

附加的头文件称为 freertos_risc_v_chip_specific_extensions.h。每个
支持的架构扩展都有一个该头文件的实现，
所有的实现都位于
/FreeRTOS/Source/Portable/[compiler]/RISC-V/chip_specific_extensions 目录的子目录中。

要为芯片包含正确的 freertos_risc_v_chip_specific_extensions.h 头文件，
只需将该头文件的路径添加到汇编器的包含路径中（请注意，这是**汇编器**的包含路径，
不是编译器的包含路径）。例如：

* 如果您的芯片使用基本的 RV32I 或 RV64I 架构，包含一个核心局部中断器 (CLINT)，
  但没有其他寄存器扩展，
  那么请将 /FreeRTOS/Source/Portable/[compiler]/RISC-V/chip_specific_extensions/**RV32I_CLINT_no_extensions**
  添加到汇编器的包含路径中。

* 如果您的芯片使用 RV32M1RM Vega 板上实现的 PULP RI5KY 核心，该核心包括六个额外的
  寄存器，并且不包括内核局部中断器 (CLINT)，
  那么请将 /FreeRTOS/Source/Portable/[compiler]/RISC-V/chip_specific_extensions/**Pulpino_Vega_RV32M1RM**
  添加到汇编器的包含路径中。

有关设置汇编器命令行选项的信息，请参阅下面的[编译器和汇编器命令行选项](#所需的编译器和汇编器命令行选项)部分；
有关创建自己的 freertos_risc_v_chip_specific_extensions.h 头文件的信息，
请参阅[将 FreeRTOS 移植到新的 RISC-V 实现](#移植到新的-32-位或-64-位-risc-v-实现)部分
。


### FreeRTOSConfig.h 设置

configMTIME_BASE_ADDRESS 和 configMTIMECMP_BASE_ADDRESS 必须在
[FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization) 中设置。
如果目标 RISC-V 芯片包括机器定时器 (MTIME)，那么请将
configMTIME_BASE_ADDRESS 设置为 MTIME 基地址，并把 configMTIMECMP_BASE_ADDRESS
设置为 MTIME 的比较寄存器 (MTIMECMP) 的地址。否则，将两者的定义都设置为
0。

例如，如果 MTIME 基地址为 0x2000BFF8，MTIMECMP 地址为 0x20004000，
则将以下行添加到 FreeRTOSConfig.h：

```c
#define configMTIME_BASE_ADDRESS        ( 0x2000BFF8UL )
#define configMTIMECMP_BASE_ADDRESS     ( 0x20004000UL )
```

如果没有 MTIME 时钟，则将以下行添加到 FreeRTOSConfig.h：

```c
#define configMTIME_BASE_ADDRESS        ( 0 )
#define configMTIMECMP_BASE_ADDRESS     ( 0 )
```


### 中断（系统）堆栈设置

FreeRTOS RISC-V 移植在
从中断服务程序 (ISR) 调用任何 C 函数之前，会切换到专用的中断（或系统）堆栈。

用作中断堆栈的内存可以在链接器脚本中定义，
也可以在 FreeRTOS 端口层中声明为静态分配的数组。编译在此项目中的
内存受限的 MCU 上，链接器脚本方法是首选方法，
因为它允许把在调度器启动前由 main() 使用的堆栈
（在调度器启动后不再用于此目的）重新用作中断堆栈
。

* 要使用静态分配的数组作为中断堆栈，请执行以下操作：

  在 FreeRTOSConfig.h 中将 configISR_STACK_SIZE_WORDS
  定义为要分配的中断堆栈的大小。请注意，大小是以
  字为单位定义的，而不是字节。

  例如，要使用一个 500 字（在 RV32 上为 2000 字节，每个字为 4 字节）
  的静态分配中断堆栈，请向
  FreeRTOSConfig.h 添加以下内容：

  ```c
  #define configISR_STACK_SIZE_WORDS ( 500 )

  ```

* 要在链接器脚本中定义中断堆栈——注意在写入时，
  只有 GCC 移植支持此方法：

  1. 声明一个名为 __freertos_irq_stack_top，
     保存中断堆栈最高地址的链接器变量，并
  2. 确保 configISR_STACK_SIZE_WORDS **未**定义。

  使用此方法需要编辑链接器脚本。如果您不
  熟悉链接器脚本，则在使用
  GCC 时，至少应知道 '**.**' 是
  [位置计数器](https://ftp.gnu.org/old-gnu/Manuals/ld-2.9.1/html_chapter/ld_3.html#SEC10)，
  用于保存链接器脚本中该点的
  内存地址的值。
  无需了解链接器脚本的细节，
  只需复制下面的示例即可。

  在调度器启动之前由 main() 使用的堆栈
  在调度器启动之后就不再需要了，所以理想的情况是
  通过设置 __freertos_irq_stack_top 等于分配给 main() 使用的堆栈的最高地址的值
  来重新使用该堆栈。例如，
  如果您的链接器脚本包含如下内容
  （实际使用的链接器脚本会有所不同）：

  ```c
  .stack : ALIGN(0x10)
  {
    __stack_bottom = .;
    . += STACK_SIZE;
    __stack_top = .;
  } > ram

  ```

  然后 __stack_top（仅为示例名称）是链接器变量，
  其值等于
  main() 使用的堆栈的最高地址（请记住 '.' 表示链接器脚本中
  任何指定位置的内存地址值）。在这种情况下，要给
  __freertos_irq_stack_top 赋予与 __stack_top 相同的值，
  只需在 __stack_top 后立即定义 __freertos_irq_stack_top 即可。
  请参阅下面的示例：

  ```c
  .stack : ALIGN(0x10)
  {
    __stack_bottom = .;
    . += STACK_SIZE;
    __stack_top = .;
    __freertos_irq_stack_top= .; /* ADDED THIS LINE. */
  } > ram

  ```

**注意**：写入时，与任务堆栈不同，内核不会检查
中断栈中的溢出。


### 所需的编译器和汇编器命令行选项

不同的 RISC-V 实现为外部中断提供了不同的处理程序，
因此，有必要告诉 FreeRTOS 内核应调用哪个外部中断处理程序
。要设置外部中断处理程序的名称，请执行以下操作：

1. 找到您的 RISC-V
   运行时软件发布版（通常是由芯片供应商提供的软件）提供的外部中断处理程序的名称
   。中断处理程序**必须**有一个参数，
   即进入中断时的 RISC-V * 原因*寄存器的值
   。例如，中断处理程序的原型应该是
   （仅为示例名称，
   请使用适合您软件的正确名称）：

  ```c
  void external_interrupt_handler( uint32_t cause );

  ```

2. 定义一个汇编器宏（请注意，这是一个**汇编器**宏，
   而不是一个编译器宏），名为 portasmHANDLE_INTERRUPT，使其名称与
   中断处理程序的名称相同。

   如果使用 GCC，则可以通过将以下内容添加到
   汇编器命令行来实现这一点，假设中断处理程序的名称为
   external_interrupt_handler：

   ```c
   -DportasmHANDLE_INTERRUPT=external_interrupt_handler

   ```

   如果使用 IAR，则可以通过打开项目选项对话框
   并添加以下行作为汇编器类别的定义符号来实现这一点，
   假设中断处理程序的名称为 vApplicationHandleTrap。

   ```c
   portasmHANDLE_INTERRUPT=vApplicationHandleTrap

   ```

   ![](/media/2020/IAR_RISC-V_Assembly_Options.jpg)
   *设置 IAR 汇编器选项*


还需要把正确的 freertos_risc_v_chip_specific_extensions.h
头文件（使用中的 RISC-V 芯片的头文件）的路径添加到汇编器的包含路径中（请注意，这是**汇编器的**包含路径，
不是编译器的包含路径）。请参阅上面的[源文件](#源文件)章节。


### 安装 FreeRTOS 陷阱处理程序

FreeRTOS 陷阱处理程序称为 freertos_risc_v_trap_handler()，
是所有中断和异常的中心入口点。当陷阱来源是外部中断时，FreeRTOS
陷阱处理程序会调用[外部中断处理程序](#所需的编译器和汇编器命令行选项)
。

要安装陷阱处理程序，请执行以下操作：

1. 如果使用的 RISC-V 核心包括一个核心局部中断器 (CLINT)，
   那么 portasmHAS_SIFIVE_CLINT
   可在 [freertos_risc_v_chip_specific_extensions.h](#移植到新的-32-位或-64-位-risc-v-实现) 中设置为 1，
   这会导致 freertos_risc_v_trap_handler() 自动安装，
   因此无需采取其他具体行动。

2. 在所有其他情况下，必须手动安装 freertos_risc_v_trap_handler()
   。可以通过编辑由您的芯片提供商提供的启动代码来完成该操作
   。

**注意：**如果 RISC-V 芯片使用向量中断控制器，则请安装
freertos_risc_v_trap_handler() 作为每个向量的处理程序。


### 移植到新的 32 位或 64 位 RISC-V 实现

在阅读本节之前，请阅读上面的 [FreeRTOS RISC-V 源文件](#源文件)章节
。

freertos_risc_v_chip_specific_extensions.h 文件包含以下
必须被定义的宏：

* portasmHAS_MTIME

  如果芯片具有机器定时器 (MTIME)，则请将 portasmHAS_MTIME 设置为 1，
  否则请将 portasmHAS_MTIME 设置为 0。

* portasmADDITIONAL_CONTEXT_SIZE

  RISC-V 指令集架构 (ISA) 是可扩展的，因此 RISC-V 芯片
  可以在基本架构规范要求的基础上
  包括额外的寄存器。

  #define（定义）portasmADDITIONAL_CONTEXT_SIZE 为
  目标芯片中存在的额外寄存器的数量（可能等于零）。例如，
  Vega 板上的 RI5CY 内核包括六个额外的寄存器，
  因此，提供的与该芯片一同使用的 freertos_risc_v_chip_specific_extensions.h
  包含以下行：

  ```c
  #define portasmADDITIONAL_CONTEXT_SIZE 6

  ```

* portasmSAVE_ADDITIONAL_REGISTERS

  portasmSAVE_ADDITIONAL_REGISTERS是一个**汇编**宏（而不是 #define），
  必须实现该宏才能保存任何特定的芯片额外寄存器。

  如果没有芯片特定的扩展寄存器（portasmADDITIONAL_CONTEXT_SIZE
  设置为零），则 portasmSAVE_ADDITIONAL_REGISTERS 必须为
  空汇编宏，如下所示：

  ```c
  .macro portasmSAVE_ADDITIONAL_REGISTERS
      /* No additional registers to save, so this macro does nothing. */
      .endm

  ```

  如果有芯片特定的扩展寄存器（portasmADDITIONAL_CONTEXT_SIZE
  大于零），则 portasmSAVE_ADDITIONAL_REGISTERS 必须：

  1. 递减堆栈指针，为额外的寄存器创造足够的堆栈空间
     ，然后……
  2. 将额外寄存器保存到创建的堆栈空间中。

  例如，如果芯片有三个额外的寄存器，
  则必须按照以下方式实现 portasmSAVE_ADDITIONAL_REGISTERS
  （其中，寄存器名称取决于
  芯片，而不是如此处所示）：

  ```c
  .macro portasmSAVE_ADDITIONAL_REGISTERS
      /* Use the portasmADDITIONAL_CONTEXT_SIZE and portWORD_SIZE
         macros to calculate how much additional stack space is needed,
         and subtract that from the stack pointer. This line can just
         be copied from here provided portasmADDITIONAL_CONTEXT_SIZE
         is set correctly. Note the minus sign ('-'). portWORD_SIZE
         is already defined elsewhere. */
      addi sp, sp, -(portasmADDITIONAL_CONTEXT_SIZE * portWORD_SIZE)

      /* Next save the additional registers, which here are assumed
         to be called xx0 to xx2, but will be called something different
         on your chip, to the stack. Assumes portasmADDITIONAL_CONTEXT_SIZE
         is 3. */
      sw xx0, 1 * portWORD_SIZE( sp )
      sw xx1, 2 * portWORD_SIZE( sp )
      sw xx2, 3 * portWORD_SIZE( sp )
      .endm
  ```

* portasmRESTORE_ADDITIONAL_REGISTERS

  portasmRESTORE_ADDITIONAL_REGISTERS 与 portasmSAVE_ADDITIONAL_REGISTERS 相反。

  如果没有芯片特定的扩展寄存器（portasmADDITIONAL_CONTEXT_SIZE
  设置为零），则 portasmRESTORE_ADDITIONAL_REGISTERS 必须为
  空汇编宏，如下所示：

  ```c
  .macro portasmRESTORE_ADDITIONAL_REGISTERS
      /* No additional registers to restore, so this macro does nothing. */
      .endm

  ```

  如果有芯片特定的扩展寄存器（portasmADDITIONAL_CONTEXT_SIZE
  大于零），则 portasmRESTORE_ADDITIONAL_REGISTERS 必须：

  1. 从
     portasmSAVE_ADDITIONAL_REGISTERS 使用的堆栈位置读取额外的寄存器，然后……
  2. 通过将堆栈指针按正确的数量递增，
     删除用于存放额外寄存器的堆栈空间。

  例如，如果
  芯片有三个额外的寄存器，则必须按照以下方式实现 portasmRESTORE_ADDITIONAL_REGISTERS
  （其中，寄存器名称取决于
  芯片，而不是如此处所示）：

  ```c
  .macro portasmRESTORE_ADDITIONAL_REGISTERS
      /* Restore the additional registers, which here are assumed
         to be called xx0 to xx2, but will be called something different
         on your chip from the stack. Assumes
         portasmADDITIONAL_CONTEXT_SIZE is 3. */
      lw xx0, 1 * portWORD_SIZE( sp )
      lw xx1, 2 * portWORD_SIZE( sp )
      lw xx2, 3 * portWORD_SIZE( sp )

      /* Use the portasmADDITIONAL_CONTEXT_SIZE and portWORD_SIZE
         macros to calculate how much space to remove from the stack.
         This line can just be copied from here provided
         portasmADDITIONAL_CONTEXT_SIZE is set correctly. portWORD_SIZE
         is already defined elsewhere. */
      addi sp, sp, (portasmADDITIONAL_CONTEXT_SIZE * portWORD_SIZE)
      .endm

  ```

您也可以选择在 freertos_risc_v_chip_specific_extensions.h 文件中包括：

* portasmHAS_SIFIVE_CLINT

  如果目标 RISC-V 芯片包括一个核心局部中断器 (CLINT)，则
  #define（定义）portasmHAS_SIFIVE_CLINT 为 1——如果您希望 FreeRTOS RISC-V
  陷阱处理程序自动安装，则可进行此设置。
