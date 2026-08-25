---
title: "Renesas (Hitachi) H8/S RTOS 移植"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![edk2329.jpg](/media/2018/edk2329.jpg)

EDK2329，配有 LED 适配卡和环回连接器

该移植是在原型嵌入式计算机 [EDK2329](http://america.renesas.com/fmwk.jsp?cnt=edk_2329_software_tools_root.jsp&fp=/products/tools/introductory_evaluation_tools/starterkits_evaluation_boards/edk2329/) 上开发的，
它来自 [Renesas](http://www.renesas.com/)（如果您希望使用替代开发板，我们也提供了[说明](/Documentation/02-Kernel/03-Supported-devices/04-Demos/04-Modifying-demos)）。它使用
开源 GNU H8 C 编译器以及免费的 HEW (High Performance Embedded Workbench) GUI。二者均可从
[KPIT Cummins](http://www.gnuh8.com/) 免费下载。

FreeRTOS 源代码下载文件包含针对 H8/S2329 RTOS 移植的综合演示应用程序，
该应用程序创建并执行 33 个实时任务，包括空闲任务和两个串口通信任务。

---

### *重要提示！使用 Renesas (Hitachi) H8/S RTOS 移植的注意事项*

*使用此 RTOS 移植前,请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [ 配置和使用详情](#配置和用法详情)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？]”。(/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

FreeRTOS 源代码下载文件包含所有 FreeRTOS 移植的源代码。

请参阅[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)章节，获取
下载文件的描述和有关创建新项目的信息。

H8/S 移植的 HEW 工作区位于 FreeRTOS/Demo/H8S 目录中。应
在 HEW IDE 中打开。请参阅下面关于使用 HEW 的说明。

---

### 演示应用程序

FreeRTOS 源代码下载文件包括 H8S GCC RTOS 移植的完全抢占式多任务演示应用程序。

#### 演示应用程序硬件设置

演示应用程序包括通过串行端口发送和接收字符的任务。一个任务发送的字符
需要另一个任务来接收：如果遗漏任何字符或字符接收顺序错误，则会标记错误状态。串行端口上
需要一个环回连接器才能让此机制正常运行（只需在串行端口连接器上将引脚 2 和 3
连接在一起）。

此演示应用程序使用一个原型板上内置的 LED。单个 LED 足以检查
演示是否正常运行，但为了达到最佳效果，还需要 5 个 LED
。这些应连接到处理器引脚 P2.3 至 P2.7。执行应用程序时，这些引脚被设置为输出
。

EDK2329 跳线应配置为适用于单芯片模式（模式 7）并禁用外部 SRAM。

#### 功能

演示应用程序会创建 33 个标准演示应用程序实时任务
 （有关各个任务的详细信息，请参阅[演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)部分）。

如果演示应用程序正确执行，其表现如下：

* LED P2.3、P2.4 和 P2.5 由 "flash" 任务控制。每个 LED 都将以恒定频率闪烁，LED P2.3
 频率最高，LED P2.5 频率最低。
* 安装回环连接器后，ComTest Rx 任务会接收 ComTest Tx 任务传输的每个字符
 。每传输一个字符都会切换 LED P2.6 的状态，每正确接收一个字符都会切换 LED P2.7 的状态
 。只有接收到的字符与 ComTest Rx 任务预期接收到的字符一致时，LED P2.7 才会切换状态。
* 并非所有任务都会更新 LED 状态，所以没有可见的指示来表明它们运行正常。
 因此，系统创建了一个检查 (Check) 任务，用于确保所有其他任务中没有检测到任何错误。

 LED P2.1 内置在 EDK2329 PCB 上，并标记为 USR1，由 "Check" 任务控制。每隔三秒，
 “检查”任务就会检查一次系统中的所有任务，以确保任务均在正确执行，没有错误，它
 之后会切换 LED P2.1 的状态。如果 LED P2.1 每三秒切换一次，则说明未检测到错误。
 如果切换频率提高到 500 毫秒，则表示“检查”任务
 至少发现了一个错误。可以通过将环回连接器从串行端口（如上述）移除来检查此机制，
 因为这样做是在故意制造一个错误。

#### 使用 HEW IDE 的注意事项

1. **路径名称**
 HEW 项目要包含项目目录下的源文件，必须使用绝对路径名称。
 在打开 HEW 项目之前，必须编辑安装的路径。

 在文本编辑器中打开 FreeRTOS/Demo/H8S/RTOSDemo/RTOSDemo.hwp 文件，
 使用正确的安装路径替换每处路径字符串 "e: devfreertos"
 。
2. **GNU 库路径**
 首次打开 FreeRTOS HEW 项目后，必须为安装 GNU 工具设置正确的库搜索路径
 安装使用该移植所需的所有文件。
 这可以使用 "Options | Linker | Archives" 菜单选项完成。例如，
 要使用 GNUH8-v0403 工具链，需要将路径更改为 $(TCINSTALL)h8300-elflibgcch8300-elf3.4-GNUH8_v0403h8300s。
 要使用 GNUH8-v0501 工具链，需要将路径更改为 $(TCINSTALL)h8300-elflibgcch8300-elf3.4-GNUH8_v0501h8300s。
3. **编译器选项**
 在 IDE 中打开和关闭选项对话框之前， HEW 不会应用配置的编译器选项。要使用正确的
 编译器选项，只需打开选项对话框（在 "Build" 菜单中选择 "Compiler"），然后关闭对话框。在熟悉该移植之前，
 不要改动任何选项。
4. **依赖扫描**
 HEW 会在每次构建之前更新每个源文件的依赖关系列表。此扫描
 过程会忽略预处理器指令。文件 FreeRTOS/Source/include/portable.h 包含
 一个头文件包含列表。每种移植对应一个包含列表。在构建特定的移植时，使用 #ifdef 来确保使用正确的头文件，
 但 HEW 会尝试扫描每个头文件。虽然这不会阻止演示
 构建，但它会大大增加构建时间，并导致大量警告消息。

 为了防止这种情况发生，
 可以注释掉所有与 H8/S 移植无关的头文件。例如，
 H8/S 移植实际使用的头文件包含在如下代码中：
```c

#ifdef GCC_H8S
   #include "../../Source/portable/GCC/H8S2329/portmacro.h"
#endif
```

 而且不得改动这些代码。例如，GCC ARM7 移植的头文件包含在
 以下代码中：
```c

#ifdef GCC_ARM7
   #include "../../Source/portable/GCC/ARM7/portmacro.h"
#endif
```

 这些代码可以被注释掉（如果您不打算使用 ARM7 移植，还可以删除它们）。

#### 构建演示应用程序

演示应用程序项目包含两个构建配置，一个调试构建用于 HEW 模拟器和另一个发布构建
下载到处理器闪存。

**创建和模拟调试构建**

1. 如上所述更新路径名称后，打开 RTOS 演示工作区 FreeRTOS/Demo/H8S/RTOSDemo.hws。
2. 在下拉列表中，选择 "Debug" 构建配置和 "Simulator" 调试会话。

![](/media/2018/DebugSim.gif)
选择 "Debug" 构建配置和 "Simulator" 调试会话
3. 在 "Build" 菜单中选择 "Build All"。项目应该成功构建，没有错误或警告。
4. 构建完成后，会显示一个对话框，询问 "Ok to download module?"，点击 "Yes"
 将构建加载到模拟器中。
5. 随后可以正常使用模拟器单步调试代码和设置断点。*然而*，
 模拟器不会模拟外围设备。因此 RTOS Tick 不会增加，最后
 只有空闲任务会执行。

**创建并下载发布构建**

1. 如上所述更新路径名称后，打开 RTOS 演示工作区 FreeRTOS/Demo/H8S/RTOSDemo.hws。
2. 在下拉列表中，选择 "Release" 构建配置和 "Release session"。

![](/media/2018/ReleaseRelease.gif)
选择 "Release" 配置和会话
3. 在 "Build" 菜单中选择 "Build All"。项目应该成功构建，没有错误或警告。
4. 使用合适的 RS232 数据线连接 EDK2329 目标硬件和主机。
5. 接通目标电源，然后按下标有 "Boot" 的按钮，使处理器进入启动模式。启动指示 LED
 会点亮。
6. 使用下面突出显示的连接按钮将 HEW 连接到目标。

![](/media/2018/h8connect.gif)
连接加速按钮
7. 连接成功后，可以使用下面突出显示的下载按钮下载闪存映像。

![](/media/2018/h8download.gif)
下载加速按钮
 要下载的文件名为 RTOSDemo.mot，将位于
 FreeRTOS/Demo/H8S/RTOSDemo/Release 目录。下载完成后，可以点击断开连接按钮（在连接按钮旁边）
 断开 HEW 和目标的连接。
8. 若要运行应用程序，先断开主板电源，取下 RS232 数据线并装上回环连接器，然后
 再通电。

---

### 配置和用法详情

#### RTOS 移植特定配置

此移植的特定配置项目位于 FreeRTOS/Demo/H8S/FreeRTOSConfig.h。可以编辑此文件中定义的常量，
以适配您的应用程序。尤其是 configTICK_RATE_HZ 定义用于
设置 RTOS 时钟滴答的频率。演示项目提供的数值 1000 Hz 可用于测试 RTOS 内核功能，
但高于大多数应用程序所要求的频率。降低此值可提高效率。

每个移植都会将 "BaseType_t" 定义为对处理器而言最有效的数据类型。此移植将
BaseType_t 定义为 char 类型。

请注意，vPortEndScheduler() 尚未实现。

#### 中断服务程序

仅使用 CCR 中的 I 位来屏蔽中断。未使用 EXR。

不会引起上下文切换的中断服务程序没有特殊要求，可以按照
正常的 GNU H8/S 语法编写。
例如：

```c

    static void vAnISR( void ) __attribute__ ( ( interrupt_handler ) );

    static void vAnISR( void )
    {
        /* ISR C code goes here. */
    }

```

通常情况下，您需要中断服务程序来引起上下文切换。例如，正在被接收的串行端口字符
可能会唤醒在等待该字符时被阻塞的高优先级任务。如果 ISR 中断了一个优先级较低的任务，
则其应立即返回到已被唤醒的任务。需要特殊语法才能使 ISR 具有
这种功能：

1. 必须使用 saveall 属性声明 ISR。
2. ISR 必须在函数的第一行包含 portENTER_SWITCHING_ISR() 宏，并
 在函数的最后一行使用 portEXIT_SWITCHING_ISR() 宏。
3. 在 ISR 中声明的变量必须声明为静态变量。

portEXIT_SWITCHING_ISR() 宏接受单个参数，如果此参数不为零，那么会切换上下文。

可以导致上下文切换的中断服务程序示例：

```c

    /* The ISR is defined using both the saveall and interrupt_handler attributes. */
    void vASwitchingISR( void ) __attribute__ ( ( saveall, interrupt_handler ) );

    void vASwitchingISR( void )
    {
        /* This MUST be the first line in the function. */
        portENTER_SWITCHING_ISR();

        /* Variables can then be declared, but MUST be declared as static. */
        static char cSwitch;

            /* ISR C code goes here... */
            /* If a context switch is required cSwitch should be set to a */
            /* non zero value, otherwise it should be set to zero. */

        /* This MUST be the last line in the function. */
        portEXIT_SWITCHING_ISR( cSwitch );
    }

```

请参阅文件 FreeRTOS/Demo/H8S/RTOSDemo/serial/serial.c，获取两种类型 ISR 的示例。

#### 使用 H8/S2329 以外的处理器

* 文件 FreeRTOS/Demo/H8S/FreeRTOSConfig.h 中包含了 '2329S.h' 头文件。其中定义了
 H8/S2329 处理器特定的寄存器位置，如果与其他处理器一同使用，则可能需要修改。
* HEW 模拟器需要定义内存映射和内存资源。目前提供的这两种都配置为适用于
 H8/S2329 在模式 7（单芯片模式）下执行，如果要模拟其他处理器或操作模式，则需要进行修改
 。
* 最后，链接器是根据 H8/S2329 内存映射配置的，需要更新才能与其他处理器一起使用。
 要查看链接器配置，请选择 "Options | Linker" 菜单项，然后在出现的窗口中选择 "Sections" 选项卡
 。

![](/media/2018/h8linker.gif)
更改内存映射

#### 在抢占式和协同式 RTOS 内核之间切换

将 FreeRTOS/Demo/H8S/FreeRTOSConfig.h 内的定义 configUSE_PREEMPTION 设置为 1，可使用抢占式调度；
设置为 0，则可使用协作式。

#### 编译器选项

与所有移植一样，使用正确的编译器选项至关重要。确保这一点的最佳方法是以
以提供的演示应用程序项目文件为基础构建您的应用程序，如[源代码组织](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)部分所述。

#### 陷阱 (Trap) 说明

下载文件中，RTOS 内核使用 TRAP 0。要使用其他数值，请更新此代码：
\#define portYIELD() asm volatile( "TRAPA #0" );

此行代码位于 FreeRTOS/Source/portable/GCC/H8S2329/portmacro.h。

#### 定时器的使用

处理器的时间处理器单元 (TPU) 定时器 1 用于生成 RTOS Tick。

#### 内存分配

H8/S 演示应用程序项目中包含 FreeRTOS/Source/Portable/MemMang/heap_2.c，以分配实时内核所需的
内存。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)章节，
以获取完整信息。

#### 串行端口驱动器

此外还需注意的是，编写串行驱动程序是为了测试部分实时内核功能，并不是
为了提供一个优化的解决方案。特别是它们不使用 DMA 外设。寄存器的比特率设置为
22.1184 MHz 时钟频率是合适的。
