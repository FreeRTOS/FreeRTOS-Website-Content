---
title: "适用于 Raspberry Pi Pico 开发板的 SMP 演示"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

### 引言


这些演示使用 [FreeRTOS 对称多处理 (SMP) 版本](/Documentation/02-Kernel/02-Kernel-features/13-Symmetric-multiprocessing-introduction/)的
 内核。演示面向
 [Raspberry Pi Pico](https://www.raspberrypi.com/products/raspberry-pi-pico/) 开发板，该板使用
 配备双核 ARM Cortex M0+ 处理器的 [RP2040](https://www.raspberrypi.com/documentation/microcontrollers/rp2040.html#welcome-to-rp2040) 微控制器
 （RP2040 微控制器由 [Raspberry Pi](https://www.raspberrypi.com/) 提供）
 。

这些演示应用程序使用
 [GNU ARM 嵌入式工具链](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads)构建 FreeRTOS
 Raspberry Pi Pico 移植。演示了
 [FreeRTOS 内核中的对称多处理 (SMP) 支持](https://github.com/FreeRTOS/FreeRTOS-Kernel/tree/smp) 。

### 源代码组织

本演示的项目文件位于 `FreeRTOS/Demo/CORTEX_M0+_RP2040`
 目录，该目录位于 [FreeRTOS SMP 演示 Git 存储库](https://github.com/FreeRTOS/FreeRTOS-SMP-Demos)中。项目中编译的 FreeRTOS 移植文件
 位于 `FreeRTOS/Source/portable/ThirdParty/GCC/RP2040` 目录中。

### 演示应用程序

该项目包括以下演示：

1. Blinky 演示。
2. 综合演示。
3. 多核演示。

#### Blinky 演示

Blinky 演示使用两个任务和一个队列。

* 队列发送任务：

队列发送任务由 `prvQueueSendTask()` 函数实现。该
 任务每 1000 毫秒将值 100 发送
 到队列。
* 队列接收任务：

队列接收任务由 `prvQueueReceiveTask()` 函数实现。
 该任务位于一个循环中，
 该循环会阻塞读取队列的尝试（任务被阻塞时不会消耗 CPU 周期），
 队列接收任务每次接收到值 100 时都会切换一次 LED。由于队列发送任务
 每 1000 毫秒向队列写一次，
 队列接收任务每 1000 毫秒切换一次 LED。

#### 综合演示

综合演示可实现全面的测试和演示应用程序，
 除此之外，用于演示和/或测试以下功能：

* [消息缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers)
* [流缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers)
* [任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)
* [队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)
* [信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)
* [互斥锁](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/)
* [事件组](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups)
* [软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)

创建的任务来自一组[标准演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
 所有 FreeRTOS 移植演示应用程序都使用这些任务。这些任务
 没有特定的功能，之所以创建，只是为了演示如何
 使用 FreeRTOS API，并测试 RTOS 移植。

创建“检查”任务，定期检查标准演示任务（包含自监控代码），
 以确保所有任务
 都按预期运行。检查任务在每次执行时都会切换 LED。这直观地反映出了系统的
 运行状况。**如果 LED 每 3 秒切换一次，则表示
 检查任务未发现任何问题。如果 LED 
 每 200 毫秒切换一次，则表示检查任务已
 在一个或多个任务中发现了问题。**

#### 多核演示

多核演示应用程序在一个内核上运行 FreeRTOS 任务，
 该任务使用 Raspberry Pico SDK 同步基元与另一个内核上运行的代码
 进行交互。同一演示有两个版本：一个版本在内核 0 上运行 FreeRTOS，
 另一个版本在内核 1 上运行 FreeRTOS 。

### 构建和运行RTOS演示应用程序

#### 构建

1. 按照以下说明设置 Raspberry Pi Pico SDK 构建环境：
 [Pico 入门](https://datasheets.raspberrypi.org/pico/getting-started-with-pico.pdf)。
 确保在您的环境中设置了 `PICO_SDK_PATH`，或通过
 CMake 命令行上的 `-DPICO_SDK_PATH=xxx` 进行传递。
2. 运行以下命令：

```c
$ cd FreeRTOS/Demo/CORTEX_M0+_RP2040
$ mkdir build
$ cd build
$ cmake ..
$ make
```

这将为每个演示应用程序生成 `.uf2` 文件：

	* Blinky 演示 - `FreeRTOS/Demo/CORTEX_M0+_RP2040/build/Standard/main_blinky.uf2`。
	* 全面演示 - `FreeRTOS/Demo/CORTEX_M0+_RP2040/build/Standard/main_full.uf2`
	* 多核演示


		+ `FreeRTOS/Demo/CORTEX_M0+_RP2040/build/OnEitherCore/on_core_zero.uf2`
		+ `FreeRTOS/Demo/CORTEX_M0+_RP2040/build/OnEitherCore/on_core_one.uf2`

#### 运行

1. 按住 `BOOTSEL`
 按钮，将 Raspberry Pi Pico 连接到您的电脑。这将强制开发板进入 USB 大容量存储模式。
2. 将要运行的演示的 `.uf2` 文件拖放到
 大容量存储设备上。

### RTOS 配置和使用详情

* Blinky 演示和全面演示的特定配置项目位于
 `FreeRTOS/Demo/CORTEX_M0+_RP2040/Standard/FreeRTOSConfig.h` 文件，
 多核演示的特定配置项目位于 `FreeRTOS/Demo/CORTEX_M0+_RP2040/OnEitherCore/FreeRTOSConfig.h` 文件。
 可根据应用程序的需要，编辑[本文件中定义的常量](/Documentation/02-Kernel/03-Supported-devices/02-Customization)
 。以下配置选项仅适用于 FreeRTOS 内核中对 SMP 的支持：
	+ `configNUM_CORES` - 设置核心数量。
	+ `configRUN_MULTIPLE_PRIORITIES` - 启用/禁用同时运行具有多个优先级的任务。
	+ `configUSE_CORE_AFFINITY` - 启用/禁用为任务设置特定核心的亲和性。
* 项目中包含 `Source/Portable/MemMang/heap_4.c`，
 用于分配 RTOS 内核所需的内存。具体请参阅
 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
 获取完整信息。
* vPortEndScheduler() 尚未实现。
