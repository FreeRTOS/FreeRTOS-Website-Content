---
title: "修改 FreeRTOS 演示以使用不同的编译器或在不同的硬件上运行"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

### 本页内容


[另请参阅“[创建新的 FreeRTOS 项目](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project)”]

FreeRTOS 包含*多个*演示应用程序，每个应用程序都针对以下组件：



1. 特定的微控制器。
2. 特定的开发工具（编译器、调试器等）。
3. 特定的硬件平台（原型板或评估板）。



这些都记录在左侧菜单框中的“[支持的设备](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)”下。

遗憾的是，无法为微控制器、编译器和评估板的每种组合提供演示项目，
因此可能不存在完全匹配您所需设置的演示应用程序。本页记录了如何修改或组合现有的演示应用程序，
以更好地满足您的设置要求。



通常来说，对适用于某评估板的现有演示进行修改以在另一种评估板上运行是一项简单的任务，而对适用于某编译器的演示进行修改以用于另一种编译器
则稍微复杂一些。本页提供了有关此类和其他类似移植活动的说明。但是，将 FreeRTOS 移植
转换为在完全不同且尚不受支持的处理器核心架构上运行并非易事。因此，本页不涵盖创建
全新 RTOS 移植的主题，另有[单独页面](FreeRTOS-porting-guide.md)专门介绍
如何开展此类开发工作。





---


### 转换演示以使用不同的评估板



本节介绍了在不更改所使用微控制器或编译器的情况下将现有演示应用程序转换为在其他原型板上运行所需的步骤
。例如，可参照以下说明，将针对 SAM7S-EK 硬件的 IAR SAM7S 演示转换为
针对 Olimex SAM7-P64 原型板。


确保在成功完成每个步骤后再进行下一步：


1. **初始编译**：
 在进行转换练习时，不妨将现有的演示应用程序作为起点，因此在进行任何修改之前，
 请先检查在下载后能否成功编译现有的演示应用程序。
 在大多数情况下，演示应用程序在编译时不应出现任何错误或警告。

 本网站针对 FreeRTOS 下载中包含的[各演示应用程序提供了相应的文档页面](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)
 。请务必阅读全文。构建说明也包含在内。


2. **修改 LED IO**：
 LED 是直观了解演示应用程序是否正在运行的最简单方法，
 因此务必尽快让新硬件平台上的 LED 正常工作起来。

 如果要将演示移植到新的硬件平台，其 LED 不太可能与开发演示所用硬件平台上的 LED 使用相同的 IO 端口，
 因此需要进行少许修改。

 partest.c 中的 vParTestInitialise() 函数包含 IO 端口模式和方向配置。
 main.c 中的 prvSetupHardware() 函数包含更通用的硬件配置（例如，启用 IO 外设的时钟） ，
 也可能需要根据使用的端口进行一些修改。

 对上段中突出显示的两个函数进行必要的更改，然后编写一个非常简单的程序来检查 LED 输出是否正常工作。这个简单的程序
 无需使用 FreeRTOS。此阶段唯一的目标是确保 LED 正常工作，因此请注释掉现有的 main() 函数，
 并将其替换为类似于以下示例的内容：


```c

    int main( void )
    {
    volatile unsigned long ul; /* volatile so it is not optimized away. */

        /* Initialise the LED outputs - note that prvSetupHardware() might also
 have to be called! */
        vParTestInitialise();

        /* Toggle the LEDs repeatedly. */
        for( ;; )
        {
            /* We don't want to use the RTOS features yet, so just use a very
 crude delay mechanism instead. */
            for( ul = 0; ul < 0xfffff; ul++ )
            {
            }

            /* Toggle the first four LEDs (on the assumption there are at least
 4 fitted. */
            vParTestToggleLED( 0 );
            vParTestToggleLED( 1 );
            vParTestToggleLED( 2 );
            vParTestToggleLED( 3 );
        }

        return 0;
    }

```
3. **RTOS 调度器简介**：
 确定 LED 可以正常工作后，便可以删除虚拟 main() 函数，并恢复原来的 main() 函数。

 建议从最简单的多任务应用程序开始。标准 'flash test' 任务最初通常用作相当于
 'hello world' 类型应用程序的多任务。

 标准 'flash test' 是由 3 项非常简单的任务组成的一组任务，每项任务以固定频率切换单个 LED，
 其中每项任务使用不同的频率。这些任务存在于几乎所有演示应用程序中，并且在 main() 内通过调用函数
 vStartLEDFlashTasks()（如果使用协程版本，则调用函数 vStartFlashCoRoutines()）启动。如果所使用演示的 main() 函数未调用
 vStartLEDFlashTasks() （或者 vStartFlashCoRoutines()），则只需将 FreeRTOS/Demo/Common/Minimal/Flash.c 文件添加到构建中，
 并手动添加对 vStartLEDFlashTasks() 的调用。

 除 vStartLEDFlashTasks() 外，注释掉用于启动一项或多项演示任务的其他所有函数。main() 很可能只会调用三个函数：
 prvSetupHardware()、vStartLEDFlashTasks() 和 vTaskStartScheduler()。例如（[基于先前介绍的
 典型 main()](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview/#comprehensive-testdemo-configuration)）：


```c

int main( void )
{
   /* Setup the microcontroller hardware for the demo. */
   prvSetupHardware();

   /* Leave this function. */
   vCreateFlashTasks();

   /* All other functions that create tasks are commented out.
   vCreatePollQTasks();
   vCreateComTestTasks();
   Etc.
   xTaskCreate( vCheckTask, "check", STACK_SIZE, NULL, TASK_PRIORITY, NULL );
   */

   /* Start the RTOS scheduler. */
   vTaskStartScheduler();

   /* Should never get here! */
   return 0;
}

```


 如果 LED 0 到 LED 2（含）处于 'flash' 任务的控制之下，并且每个 LED 都以固定但不同的频率切换，则表示这个非常简单的应用程序运行正常。


4. **完毕任务**：

 执行完简单的 'flash' 演示后，
 可以恢复完整的演示应用程序，并创建所有演示任务，
 或者开始创建您自己的应用程序任务。

 请记住以下要点：

	* 如果演示应用程序最初并未调用 vTaskCreateFlashTasks()，并且手动添加了对此函数的调用，
	 则需再次删除此调用。原因有两点：首先，'flash' 任务所使用的 LED 输出可能已经在其他地方使用过；其次，
	 完整演示可能已经使用了所有可用的 RAM ，这意味着没有空间可用于创建其他任务。
	* 标准 'com test' 任务（如果包含在演示中）将使用其中一个微控制器 UART 外设。检查所使用的 UART 是否适用于
	 向其上移植演示的硬件。
	* 如果不针对硬件或接口差异进行修改，LCD 等外设不太可能正常运行。

---


### 合并或修改现有演示项目


本节重点介绍了在修改现有项目或合并两个现有项目时需要考虑的细节，
两者的目的都是创建特定于您需求的项目。例如，您可能希望创建一个使用 GCC 编译器的 STR9 演示项目。虽然 FreeRTOS 下载可能不会（在编写时）
包括 GCC STR9 演示，但它确实包括一个 IAR STR9 演示和一个 GCC STR75x 演示。创建 STR9 GCC 项目所需的信息可以
从这两个现有项目收集。可通过两种方式实现这一点：

1. 采用现有的演示项目（该项目使用正确的编译器，但针对不同的微控制器），然后将其重新定位，针对所需的微控制器。
2. 使用选择的编译器创建一个新项目。采用此选项时，即使现有项目使用不同的编译器。
 也可以使用现有演示项目作为所需文件和设置的指南。



以下说明重点介绍了无论使用哪种方法都需要考虑的信息：

* **识别针对所使用微控制器的 FreeRTOS 内核文件**：

 [FreeRTOS 源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)页面提供了
 理解 FreeRTOS 目录结构所需的全部信息。

 特定于单个移植的大多数（如果不是全部）代码包含在名为 FreeRTOS/source/portable/[compiler]/[microcontroller]/port.c 的文件中
 以及名为 FreeRTOS/source/portable/[compiler]/[microcontroller]/portmacro.h 的随附头文件中，
 其中 [compiler] 是所用编译器的名称，[microcontroller] 是所用微控制器系列的名称。

 对于某些编译器，只需 port.c 和 portmacro.h 文件即可。对于其他（功能不太灵活的）编译器，还需要一个汇编程序
 文件。此类汇编程序文件也称为 portasm.s 或 portasm.asm。

 最后，还需要一个仅针对  ARM7 GCC 移植的 portISR.c 文件。portISR.c 用于从 port.c 中分离出
 必须始终编译为 ARM 模式的代码，保留在 port.c 中的代码随后可编译为 ARM 或 THUMB 模式。
* **识别针对所使用编译器的文件**：
 面向嵌入式系统的编译器为 C 语言提供了某些扩展。例如，可能存在特殊关键字，用于识别
 特定函数是否应编译为中断处理程序。



 按照定义， C 语言的扩展不属于 C 标准的范畴，因此不同编译器之间会存在差异。包含此类非标准语法的 FreeRTOS 文件
 是 FreeRTOS/source/portable 目录树中的文件（如上所示）。此外，一些演示应用程序将安装不属于
 FreeRTOS 本身的中断处理程序。此类中断处理程序的定义和安装方法也可能
 特定于编译器。
* **低级文件**：
 C 启动文件和链接器脚本通常是特定于处理器和编译器。切勿尝试从头开始创建这些文件，
 请查看现有 FreeRTOS 演示项目，寻找适合修改的文件。



 尤其要注意 ARM7 C 启动文件。这些文件必须将 IRQ 处理程序配置为直接指向中断处理程序的矢量
 或指向公共入口点的矢量。演示中给出了两种方法的示例。无论哪种情况，跳转后执行的第一个代码必须是 FreeRTOS 上下文保存代码，而不是编译器提供的
 中间代码。再次提醒，请使用现有文件作为参考。



 必须调整链接器脚本，以正确描述所使用微控制器的内存映射。
* **项目设置**：

 每个项目通常都会定义一个预处理器宏，该预处理器宏特定于正在编译的移植。预处理器宏可识别将包含的 portmacro.h
 文件。例如，使用 GCC 编译 MegaAVR 移植时，必须定义 GCC_MEGA_AVR。使用 IAR 编译 MegaAVR 移植等时，必须定义 IAR_MEGA_AVR
 。请参阅现有的演示应用程序项目和文件 FreeRTOS/source/include/portable.h，查找
 适合您项目的正确定义。如果未定义预处理器宏，则相关 portmacro.h 文件所在的目录必须包含在
 预处理器包含搜索路径中。




 其他编译器设置（例如优化选项）也很重要。同样，请参考现有的演示应用程序项目以获取示例。



 具有基于 IDE 的界面的编译器通常会将目标微控制器作为项目设置的一部分，必须对其进行调整以适合新
 新目标。同样，在使用 makefile 的情况下，必须更新 makefile 中的选项，以适合新的微控制器目标。
* **配置滴答中断**：
 滴答中断由名为 prvSetupTimerInterrupt() 的函数配置，该函数位于 FreeRTOS/source/portable/[compiler]/[microcontroller]/port.c 中。
* **RAM 和 ROM 的使用**：
 [内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分提供了理解 FreeRTOS 如何使用 RAM
 以及如何将此 RAM 分配给 RTOS 内核所需的全部信息。



 如果要将现有的演示应用程序转换为在 RAM 较少的微控制器上运行，则可能需要降低 configTOTAL_HEAP_SIZE 值
 （位于 FreeRTOSConfig.h 中），并减少演示创建的任务数量。只需
 注释掉用于在 main() 中创建任务的函数调用即可减少创建的任务数量，如[之前演示](#合并或修改现有演示项目)所述。



 如果要将现有的演示应用程序转换为在 ROM 较少的微控制器上运行，
 则可能需要减少构建中包含的演示应用程序文件的数量。这些文件位于 FreeRTOS/Demo/common [目录树](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)中。从构建中删除演示应用程序文件时，还必须删除 main() 中用于创建不再包含的任务的调用。


  

  

  

  










