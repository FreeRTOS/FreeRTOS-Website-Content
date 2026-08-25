---
title: "面向 XMOS XCORE.AI Explorer 开发板的 SMP 演示"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

## 引言

本演示使用了
[对称多处理 (SMP) 版本](/Documentation/02-Kernel/02-Kernel-features/13-Symmetric-multiprocessing-introduction/)的 FreeRTOS 内核，
面向具有 16 个核心的 [XCORE.AI](https://www.xmos.ai/xcore-ai/)
。本演示项目使用 [XMOS XTC 工具](https://www.xmos.ai/software-tools/)构建 FreeRTOS XCORE.AI 移植（请注意，这些工具需要在 Linux 主机或类似 Linux 的环境中运行），
展示了内核对 [FreeRTOS 对称多处理 (SMP)](https://github.com/FreeRTOS/FreeRTOS-Kernel/tree/smp) 的支持。

## 源代码组织

本演示的项目文件位于 `FreeRTOS/Demo/XCORE.AI_xClang/RTOSDemo`
目录，该目录位于 [FreeRTOS SMP 演示 Git 存储库](https://github.com/FreeRTOS/FreeRTOS-SMP-Demos)中。
项目中编译的 FreeRTOS 移植文件
位于 `FreeRTOS/Source/portable/ThirdParty/xClang/XCORE.AI` 目录中。

## SMP 演示应用程序


常量 `mainCREATE_SIMPLE_BLINKY_DEMO_ONLY`
（在 `testing_main.h` 顶部定义）用于在简单的“blinky”入门项目
和更全面的测试与演示应用程序之间切换。

### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 时

当 `mainCREATE_SIMPLE_BLINKY_DEMO_ONLY` 设置为 1 时，演示应用程序
会创建两个任务，每个任务定期切换一个板载 LED（其中一个任务切换 LED 0，
另一个任务切换 LED 1）。

### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时

当 `mainCREATE_SIMPLE_BLINKY_DEMO_ONLY` 设置为 0 时，演示应用程序
会实现全面的测试和演示，其中包括但不限于以下内容的
演示和/或测试：

* [消息缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers)
* [流缓冲区](/Documentation/02-Kernel/02-Kernel-features/04-Stream-and-message-buffers/01-RTOS-stream-and-message-buffers)
* [任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)
* [队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)
* [信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)
* [互斥锁](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/)
* [事件组](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups)
* [软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)

创建的任务来自一组[标准演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
任务。所有 FreeRTOS 移植演示应用程序都使用标准演示任务。这些任务
没有特定功能，旨在演示如何使用
FreeRTOS API，并测试 RTOS 移植。

创建了两个“检查”任务，定期检查标准演示任务
（包含自我监控代码），以确保所有任务按预期
运行。一个检查任务监控在磁贴 0 上运行的演示任务，并在每次执行时
切换 LED 0。另一个检查任务监控在磁贴 1 上运行的演示任务，
并在每次执行时切换 LED 1。这为系统运行状况
提供了直观反馈。**如果两个 LED 每 3 秒切换一次，则表示检查任务未发现任何问题。
如果任一 LED 每 200 毫秒切换一次，则表示检查任务在至少一个任务中发现问题。
**

构建并运行 RTOS 演示应用程序
----------------------------------------------

### 硬件设置

将 xTAG 编程器插入评估板。确保 xTAG 和
评估板均通过 USB 连接到计算机。

### 工具链安装

开发工具需要在 Linux 主机或类似 Linux 的环境中运行。

1. 下载 [XMOS XTC 工具](https://www.xmos.ai/software-tools/)。
2. 将存档解压缩到所选的安装目录。下方示例
 将其安装到主目录：

```c
$ tar -xf archive.tgz -C ~
```
3. 配置默认环境变量：

```c
$ cd ~/XMOS/XTC/15.1.0
$ source SetEnv
```
4. 检查工具环境是否已正确设置：

```c
$ xcc --help
```
5. 确保所有用户都可以访问 xTAG 驱动程序。此步骤在每台
 开发计算机上只需执行一次。

```c
$ cd ~/XMOS/XTC/15.1.0/scripts
$ sudo ./setup_xmos_devices.sh
```
6. 检查 xTAG 设备是否可用且可访问：

```c
$ cd ~/XMOS/XTC/15.1.0/scripts
$ ./check_xmos_devices.sh
Searching for xtag3 devices...
0 found
Searching for xtag4 devices...
1 found
Success: User <username> is able to access all xtag4 devices
```
7. 检查设备是否可用于调试：

```c
$ xrun -l
Available XMOS Devices
----------------------

  ID  Name            Adapter ID    Devices
  --  ----            ----------    -------
  0   XMOS XTAG-4     2W3T8RAG      P[0]

```

### 构建并运行演示应用程序

1. 进入 RTOSDemo 目录：

```c
$ cd FreeRTOS/Demo/XCORE.AI_xClang/RTOSDemo
```
2. 构建演示：

```c
$ make
```
3. 运行演示：

```c
$ make run
```

## RTOS 配置和使用详情

* 本演示的特定配置项位于
`FreeRTOS/Demo/XCORE.AI_xClang/RTOSDemo/src/FreeRTOSConfig.h` 文件中。可以编辑
[该文件中定义的常量](/Documentation/02-Kernel/03-Supported-devices/02-Customization)，
以适配您的应用程序。以下配置选项
适用于 FreeRTOS 内核中的 SMP 支持：
	+ `configNUM_CORES` - 设置核心数量。
	+ `configRUN_MULTIPLE_PRIORITIES` - 启用/禁用同时运行具有多个优先级的任务。
	+ `configUSE_CORE_AFFINITY` - 启用/禁用为任务设置特定核心的亲和性。
* 项目中包含 `Source/Portable/MemMang/heap_4.c`，
用于分配 RTOS 内核所需的内存。请参阅
API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
获取完整信息。
* vPortEndScheduler() 尚未实现。
