---
title: "FreeRTOS 演示应用程序"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: FreeRTOS 演示应用程序简介
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: FreeRTOS简介
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: FreeRTOS 初学者指南
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: 下载 FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: 常见问题
    link: /Why-FreeRTOS/FAQs
---

### 引言

RTOS 源代码下载文件包含
每个 RTOS 移植的预配置演示项目。演示面向用于该移植开发的评估板。
创建时，每个预配置的项目都直接生成，下载时没有任何警告或错误，尽管后续
工具的更改可能意味着情况有所变化。还提供了一个[单独的页面](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Device-independent-demo/Hardware-independent-RTOS-example)，
介绍了如何创建一个独立的硬件演示项目。

演示项目如下：

1. **学习如何使用 FreeRTOS** 的帮助工具：每个源文件演示 RTOS 的一个组件。
2. **新应用程序的预配置起点** - 为确保正确的开发工具设置（编译器切换、
   调试器格式等），建议通过
   [修改现有的演示项目](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization/#creating-your-own-application)来创建新的应用程序。运行演示应用程序后，
   逐渐删除演示函数和源文件，并用您自己的应用程序代码来替换。注意：
   删除演示函数时，建议在 FreeRTOSConfig.h 中将 [configUSE_TICK_HOOK](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configuse_tick_hook) 设置为 0。
   停止执行滴答钩子函数可能会导致一些演示失败，但会
   阻止示例滴答钩子函数尝试与已从项目中删除的演示进行交互
   （否则可能会导致崩溃）。

### 查找演示应用程序

每个演示项目都有一个[文档页面](/Documentation/02-Kernel/03-Supported-devices/00-Supported-devices)，详细说明 FreeRTOS 下载中项目的位置，
以及其他演示特定的重要和省时的信息（例如如何设置硬件以及如何构建项目）。

所有仅限 RTOS 内核的演示（未演示任何其他库的演示）都位于
[FreeRTOS/Demo](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS/Demo) 目录中。
子目录的名称标识了目标设备和用于构建其包含的项目的编译器。请参阅
[FreeRTOS 源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)页面，获取 FreeRTOS 目录结构的完整说明，
以及[快速入门指南](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/02-Quick-start-guide)了解更多实用信息。

<p className="tips">
  <span className="display-6">Tip</span>
  <span className="content">
    移植文档页面按设备制造商分组。展开支持的设备列表，然后单击感兴趣的制造商，进入演示文档页面列表。
    <br />
    ![](/media/2024/supported-demo-list.png)
  </span>
</p>

### 演示应用程序的结构

大多数演示应用程序都在项目的 main.c 文件中使用 #define，
以便在构建基本的 "blinky" 风格项目和构建全面的测试和演示项目之间进行选择。

#### 简单的 "blinky" 演示配置

Blinky 演示项目包含在单个源文件中，并实现了
[硬件独立演示功能](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Device-independent-demo/Hardware-independent-RTOS-example)页面中所述的
功能子集。

Blinky 项目至少要演示如何使用 [FreeRTOS 队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)在两个任务之间传递数值——
每次接收到数值时都要切换 LED 或打印输出。许多 blinky 项目还演示了使用相同队列的单个[软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)
。

#### 综合测试/演示配置

综合演示项目创建
“[通用演示任务](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS/Demo/Common/Minimal)”的全部或子集，
之所以这样称呼，是因为这些任务对所有综合演示通用。创建的任务数量取决于资源
目标硬件（微控制器或微处理器）上可用的资源，限制因素是可用于任务堆栈的 RAM 量
。

早期通用演示任务仅包含如何使用 RTOS 功能的演示。
新的通用演示任务包含集成测试，这使得其实现更加复杂。

全面的演示应用程序创建了一个“检查”任务，或者更罕见的是，创建一个
从[滴答钩子](/Documentation/02-Kernel/02-Kernel-features/12-Hook-functions)调用的‘检查’函数。每个通用演示任务都包含自我监控代码，
检查任务的任务是定期（通常每三或五秒，具体取决于演示）查询每个任务，
首先确保所述任务仍在执行，然后确定任务是否检测到
任何错误。最后，检查任务通过切换 LED 或打印消息来
报告系统状态。如果检查任务切换 LED ，则切换速率将为
任务的原始周期（三秒或五秒，取决于演示）（如果不存在错误），
如果任何任务报错，则增加切换速率以每秒切换多次。

**注意：**通用演示任务中的自我监控代码可能纯粹因为任务
在处理时间上相互争用而报错。这可以通过调整任务之间的
相对优先级来避免。

下述伪代码显示了综合演示的结构。

```c
/* main_full() is called from main() if the #define in main.c is set to create
   the comprehensive demo, rather than simple blinky demo. */
int main_full( void )
{
    /* Setup the microcontroller hardware for the demo. */
    prvSetupHardware();

    /* Create the common demo application tasks, for example: */
    vStartInterruptQueueTasks();
    vStartMessageBufferAMPTasks()
    vCreatePollQTasks();
    Etc.

    /* Create any tasks defined within main.c itself, or otherwise specific to the
       demo being built. */
    xTaskCreate( vCheckTask, "check", STACK_SIZE, NULL, TASK_PRIORITY, NULL );
    Etc.

    /* Start the RTOS scheduler, this function should not return as it causes the
       execution context to change from main() to one of the created tasks. */
    vTaskStartScheduler();

    /* Should never get here! */
    return 0;
}
```

注意：

- 演示项目通常使用目标处理器上的所有可用 RAM ，需要将一些任务
  删除，然后才能添加更多内容。
- 大多数构建标准演示任务的项目仅演示和测试内核。有一些
  演示其他库的单独项目，例如 [TCP/IP 堆栈](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP)，
  或 [FreeRTOS 核心](/Security/01-Security-overview)库。
- 提供标准的演示项目文件是为了演示 RTOS 内核的使用和测试。并不
  旨在提供最佳解决方案的示例。对于 comtest.c（使用示例 UART 驱动程序）尤其如此，
  编写该文件的目的通常是为了强调（并因此测试） RTOS 内核实现，
  而不是提供最佳集成的实例（通常 UART 接口使用[流缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers)
  而不是队列）。

### 历史信息

#### Partest.c，访问 LED

较早的演示应用程序包括一个名为 partest.c 的文件（该名称具有历史意义，后来失去了其含义，
但它源于 'parallel port test'）。该文件包含用于设置、清除和切换 LED 的
界面函数。此处提及该文件是因为从其名称来看，该文件的功能并不明显。

#### "Full" vs "Minimal"演示应用程序文件

包含实现通用演示任务的源文件有两个目录。位于
FreeRTOS/Demo/Common/Full 目录中的文件采用托管环境，并且仅由在旧版 DOS 系统上运行的演示使用
（这也是为什么 Partest.c 文件名需要加密，只能使用 8.3 格式的短文件名）。
所有其他演示项目根据 FreeRTOS/Demo/Common/Minimal 目录构建通用演示源文件，
其中的文件都不采用托管环境。

#### 通用演示任务功能

有一些[旧版文档](/Documentation/02-Kernel/05-RTOS-implementation-tutorial/02-Building-blocks/06-GCC-naked-attributes)概述了原始
通用演示任务的行为。最近的通用演示任务更多地是专为集成测试而设计，而不是纯粹为
演示。这意味着这些演示可能很复杂，因此在源文件之外
不记录。
