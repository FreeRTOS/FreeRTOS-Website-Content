---
title: 使用 FreeRTOS-Plus-Trace
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

### 引言

FreeRTOS-Plus-Trace 包含两个组件：

* 追踪记录器源文件：

  追踪记录器负责收集追踪数据，
  并作为 RTOS 应用程序的一部分在目标硬件上运行。它以 C 源代码的形式提供，包含在主 FreeRTOS .zip 文件下载中。

  本网站上的示例使用数据的“快照”记录进行离线分析。FreeRTOS-Plus-Trace
  提供了一个用于备份记录数据的“流式”记录器。

* FreeRTOS-Plus-Trace PC 应用程序：

  追踪记录可在 Tracealyzer 应用程序中查看，该应用程序可从 [Percepio 网站](https://percepio.com/tracealyzer/download-tracealyzer/)下载。

本页面仅提供快速入门说明。有关详细信息，请参阅 FreeRTOS-Plus-Trace
应用程序的帮助菜单，以及 [Percepio](https://percepio.com/) 网站
。

对 RTOS 应用程序启用追踪的步骤：

1. [将追踪记录器源文件添加到 RTOS 项目中](#将追踪记录器源文件添加到-rtos-项目中)
2. [更新应用程序以初始化追踪，然后开始和停止追踪记录](#更新应用程序以初始化追踪然后开始和停止追踪记录)
3. [从目标中提取快照追踪记录，以在 FreeRTOS-Plus-Trace 中查看](#从目标中提取追踪记录以在-freertos-plus-trace-中查看)

 
### 将追踪记录器源文件添加到 RTOS 项目中

![](/media/2018/trace_source_files.png)
*在构建 FreeRTOS-Plus-Trace
[ Win32 模拟器演示的项目中查看的追踪记录器源文件](Free_RTOS_Plus_Trace_CLI_Example)*

[\![](/media/2018/include_file.png)](/media/2018/include_file.png)
*将 trcKernelPort.h 添加到同一项目中。（点击放大）。*
 
1. 将 *trcKernelPort.c* 添加到构建项目。要使用快照记录器，请将 *trcSnapshotRecord* 添加到
   项目；要使用流式记录器，请将 *trcStreamingConfig.h* 添加到项目。

2. 将 /FreeRTOS-Plus/Source/FreeRTOS-Plus-Trace/include 添加到编译器的 include 路径中。

3. 编辑
   `FreeRTOS-Plus/Source/FreeRTOS-Plus-Trace/config` 中提供的模板副本创建 trcConfig.h 配置文件。*trcConfig.h* 文件在下载的示例 zip 文件中使用
   。头文件中的注释提供了完整说明。

4. 要使用快照记录器，请编辑
   FreeRTOS-Plus/Source/FreeRTOS-Plus-Trace/config 中提供的模板副本，或编辑
   FreeRTOS zip 下载文件中的示例使用的 trcSnapshotConfig.h 文件，以创建 trcSnapshotConfig.h 配置文件。同样，完整说明请参阅
   头文件中的注释。或者，要使用流式记录器，请编辑同一目录下提供的模板副本，
   以创建 trcStreamingConfig.h 头文件。

5. 在 FreeRTOSConfig.h 中将 configUSE_TRACE_FACILITY 设置为 1。

6. 将 trcRecorder.h 头文件添加到项目 FreeRTOSConfig.h 配置文件的底部。

根据所使用的移植，可能还需要定义 TRACE_ENTER_CRITICAL_SECTION()
和 TRACE_EXIT_CRITICAL_SECTION() 宏。源文件中的 #error 会表明是否需要定义
并提供进一步说明。

同样，根据所使用的移植和开发环境，可能还需要使用预处理器
来防止从汇编文件中添加配置文件。例如，在 IAR 中，
可以如下操作……

```c
/* The IAR C compiler automatically defines __ICCARM__. */
#ifdef __ICCARM__
    #include "trcKernelPortFreeRTOS.h"
#endif

```
*使用 IAR 编译器时，防止从汇编文件中添加 RTOS 追踪头文件*

……在 MPLAB 中，可以如下操作：


```c
/* The MPLAB assembler automatically defines __LANGUAGE_ASSEMBLY. */
#ifndef __LANGUAGE_ASSEMBLY
    #include "trcKernelPortFreeRTOS.h"
#endif

```
*使用 MPLAB 编译器时，防止从汇编文件中添加 RTOS 追踪头文件*


###  更新应用程序以初始化追踪，然后开始和停止追踪记录

通过调用 vTraceEnable() 来初始化追踪记录器。必须**先**初始化追踪记录器，
才能调用 FreeRTOS API 函数，因此建议在 main() 函数的开头调用 vTraceEnable( TRC_INIT)。

要开始记录，请调用 vTraceStart()。要停止记录，请调用 vTraceStop()。在提取记录的数据之前，
不必停止记录。


###  从目标中提取追踪记录，以在 FreeRTOS-Plus-Trace 中查看

如果使用的是快照记录器（而非流式记录器），则记录的数据存储在
目标硬件中。记录的数据存储在目标硬件 RAM 中
名为 RecorderData 的变量中，而 RecorderDataPtr 变量指向这个 RecorderData 变量。要查看快照，
需要将目标 RAM 的内容转储到磁盘文件中，然后可以在该文件中使用
FreeRTOS-Plus-Trace 的 "File" 菜单打开快照。保存到文件中的 RAM 只需包含 RecorderData 变量，
该变量可以在任意内存地址开始和结束，因为 FreeRTOS-Plus-Trace
会自动在保存的数据中查找记录。

大多数调试器都能够将 RAM 内容保存到文件中，FreeRTOS-Plus-Trace 帮助文件提供了
**IAR**、**ST-Link**、Rowley **CrossStudio**、Keil **uVision** 和
Renesas **HEW** 工具的使用说明。还有一些其他环境通过内置功能或插件支持 FreeRTOS-Plus-Trace
，具体如下：

* J-Link 用户（所有构建环境和目标）

  如果使用 **J-Link** 调试接口，则可以直接
  在 FreeRTOS-Plus-Trace 中通过 J-Link 菜单检索记录的数据。

* Atmel Studio

  如果使用 **Atmel Studio 6**，则 Atmel 的 MemoryLogger 扩展（可通过 Atmel
  Gallery 获取）会自动检测 FreeRTOS-Plus-Trace 的路径（如果已安装），
  并支持一键上传和刷新。您可以在调试时使用此扩展，
  或者在 MCU 每次停止时允许自动刷新追踪数据。

* MPLAB X

  如果使用 **MPLAB X**，则可以利用 MPLAB 插件将记录的数据保存到磁盘，
  以在 FreeRTOS-Plus-Trace 中打开。

  要将插件安装到 MPLAB X，请执行以下操作：

  1. 从提供的 zip 文件中提取 .nbm 文件。
  2. 在 MPLAB 中选择 "Tools->Plugins"，在打开的 "Plugins" 对话框中选择 "Downloaded" 标签页，然后点击 "Add Plugins..."。
  3. 在 zip 文件中选择 org-percepio-freertostraceplugin.nbm。
  4. 重启 MPLAB 并选择 "Tools->Embedded->FreeRTOS-Plus-Trace Plugin" 以启用插件。

* Eclipse

  最后，虽然 Eclispe 暂无内置支持，但由于 Eclipse 用户众多，
  可以向他们强调如何在该环境中将 RAM 转储到磁盘。下图展示了这一过程
  （图像中显示的是 LPCXpresso）。

  ![](/media/2018/RTOS_Eclipse_Dump.png)
  *在 Eclipse 中使用内存导出功能将包含 RecorderData 的 RAM 保存到磁盘文件*

