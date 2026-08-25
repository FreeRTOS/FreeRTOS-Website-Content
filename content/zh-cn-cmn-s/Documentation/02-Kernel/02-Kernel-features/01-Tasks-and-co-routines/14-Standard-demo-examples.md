---
title: "FreeRTOS 协程"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: 适用于单核、非对称多核 (AMP) 和对称多核 (SMP) RTOS 配置的 FreeRTOS 调度算法
relatedLinks:
  - title: API 引用——协程
    link: /Documentation/02-Kernel/04-API-references/14-Co-routines/00-Co-routine API/
---

[[有关协程的更多信息](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/06-Co-routine-overview)]


### FreeRTOS 演示应用程序示例

下载内容中包含两个文件，使用含队列的协程进行演示：

1. **[crflash.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS/Demo/Common/Minimal/crflash.c)**

   其在功能上等同于[标准演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)文件 flash.c，但使用的是协程
   而非任务。此外，仅为了演示目的，应切换的 LED 数量通过队列
   传递给更高优先级的协程，而非直接从协程内部
   切换 LED （根据上述的快速示例所示）。

1. **[crhook.c](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS/Demo/Common/Minimal/crhook.c)**

   演示将数据从中断传递到协程的过程。使用 tick 钩子函数作为数据
   源。

[PC](/Documentation/02-Kernel/03-Supported-devices/04-Demos/x86/Industrial-PC-Port) 和旧版 [ARM Cortex-M3](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Texas-Instruments/portcortexkeil) 演示应用程序已
经过预先配置，以使用此类示例协程文件，且可用作参考。所有其他演示
应用程序都被配置为仅可使用任务，但根据以下流程可轻松转换为
演示协程的模式。这将 flash.c 中实现的功能替换为通过 crflash.c
实现的功能：

1. 在 FreeRTOSConfig.h 中，将 configUSE_CO_ROUTINES 和 configUSE_IDLE_HOOK 设置为 1。

1. 在 IDE 项目或项目生成文件中（取决于使用的演示项目）：

   1. 将对文件 FreeRTOS/Demo/Common/Minimal/flash.c 的引用替换为对 FreeRTOS/Demo/Common/Minimal/crflash.c 的引用。

   2. 将文件 FreeRTOS/Source/croutine.c 添加到构建中。

1. 在 main.c 中：

   1. 包含头文件 croutine.h，其中包含协程宏和函数原型。

   2. 将包含的 flash.h 替换为 crflash.h。

   3. 删除对创建 Flash 任务的函数 vStartLEDFlashTasks () 的调用……

   4. ……并替换为创建 Flash 协程的函数 vStartFlashCoRoutines (n)，
      其中 n 为应创建的协程数量。每个协程都将以不同的速度
      闪烁不同的LED。

   5. 添加一个空闲钩子函数，该函数将按以下方式调度协程：

      ```c
      void vApplicationIdleHook( void )
      {
          vCoRoutineSchedule( void );
      }
      ```
      如果 main () 已包含空闲钩子，则只需将 vCoRoutineSchedule() 的调用添加到现有
      钩子函数即可。

1. 用 Flash 协程替换 Flash 任务意味着需要分配的堆栈将至少减少两个，
   因此可以减少预留用于 RTOS 调度器使用的堆空间。如果您的
   项目 RAM 不足以在构建中加入 croutine.c，只需要
   降低 FreeRTOSConfig.h 中 portTOTAL_HEAP_SPACE by ( 2 * portMINIMAL_STACK_SIZE ) 的定义即可。
