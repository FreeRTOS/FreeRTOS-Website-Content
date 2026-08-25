---
title: FreeRTOS 上的 micro-ROS
created: 2020-09-02 00:00:00.0 UTC
feature: blog
categories:
- 长期支持
authors:
- francesca-finocchiaro
relatedLinks:
- title: FreeRTOS 简介
  link: /Why-FreeRTOS/What-is-FreeRTOS/
---

本帖由 [Francesca Finocchiaro](https://www.linkedin.com/in/francesca-finocchiaro-44b27b14b/) (eProsima)、[Pablo Garrido-Sanchez](https://www.linkedin.com/in/pgarridosan/) (eProsima)、[José Antonio Moral Parras](https://www.linkedin.com/in/joseamoral/) (eProsima) 发表于 2020 年 9 月 2 日


## 引言

[机器人操作系统](https://www.ros.org/) (ROS) 是用于机器人 
应用程序开发的开源软件框架。ROS 2 是第二代 ROS，采用分层架构设计， 
可将 ROS 客户端层（RCL 和 RCLCPP/RCLCPY）与 ROS 中间件层 (RMW) 分开。 
客户端层提供开发者接口，而 RMW 则可与不同的 
可互换低级通信协议兼容。RMW 基于 
[数据分发服务](https://www.dds-foundation.org/) (DDS)，这是 
专为安全关键系统设计的实时发布/订阅协议。开发者可利用该分层方法专注于 
应用程序，而不是底层细节。截至本文撰写之时，[Foxy Fitzroy](https://index.ros.org/doc/ros2/Releases/Release-Foxy-Fitzroy/) 
是 ROS 2 的最新版本。

[micro-ROS](https://micro-ros.github.io/) 是 [ROS 2](https://index.ros.org/doc/ros2/) 的衍生版， 
该机器人操作系统可提供全面部署的 
ROS 2 生态系统所具有的大多数诱人工具和功能，并具有适应嵌入式和低资源设备的卓越能力 
。传统上，尽管机器人中有许多微控制器，ROS 并没有扩展到微控制器层面 
。微控制器往往通过串行协议与旧版 ROS 中的 ROS-serial 等工具集成 
。

如果能在微控制器中拥有 ROS 2 的所有强大功能和相同 API，岂不是很好？这正是 
micro-ROS 所能提供的优势：在机器人系统嵌入式部分内部提供 ROS 开发生态系统。 
开发者可以利用 micro-ROS 在接近硬件层面运行 ROS 2 节点。这使得所有硬件 
外围设备都可供应用程序使用，因此应用程序能够直接 
与 SPI 或 I²C 等低级总线交互，以与传感器和执行器建立接口。

micro-ROS 是一组分层库，可直接重用 ROS 2 的库，也可以 
根据资源受限设备的功能和需求进行调整。具体而言，在 ROS 2 架构中， 
micro-ROS 维护的层包括 ROS 客户端库 (RCL) 和 ROS 中间件接口 (RMW)。 
此外，RCLCPP 是基于 RCL 的 C++ 抽象层，可供 micro-ROS 应用程序组件使用， 
即使大多数组件直接与 RCL 建立接口，也不例外。 
相对于 ROS 2，这一层可在 RCLC 中提供额外功能。RCLC 是一个用 C99 编写的库，其功能  
与 RCLCPP 提供的功能类似，例如便利函数或执行器， 
这些功能专为适应微控制器而设计和开发。

![](/media/2020/eprosima_microros_stack-300x169.png)

因此，无论是在硬件层面还是软件层面，micro-ROS 可与大多数嵌入式平台兼容 
。

然而，最终决定 micro-ROS 架构的是 RMW 实现，该实现基于  
名为 [Micro XRCE-DDS](https://micro-xrce-dds.docs.eprosima.com/en/latest/) 的中间件库。 
Micro XRCE-DDS 是 [DDS-XRCE](https://www.omg.org/spec/DDS-XRCE/1.0/Beta1/PDF) 
（用于资源极其受限环境的 DDS）协议的 C/C++ 实现， 
由[对象管理组](https://www.omg.org/) (OMG) 定义和维护。

顾名思义，DDS-XRCE 是一种有线协议，可用于将以数据为中心的 
发布者-订阅者 [DDS 模型](https://www.dds-foundation.org/) 引入嵌入式环境。DDS-XRCE 依赖于 
客户端-服务器架构，其中客户端是用 C99 编写的轻量级实体， 
可在低资源设备上运行，而代理（用 C++ 11 编写的应用程序）则充当客户端 
和 DDS 环境之间的桥梁。DDS-XRCE 协议负责在这两个实体之间 
传递请求和消息。反过来，代理能够通过标准 DDS 有线协议 
与 DDS 全局数据空间进行通信。在 DDS 环境中，代理代表客户端行事， 
让其与其他 DDS 参与者通信。此通信由客户端代理调解， 
模拟 DDS 应用程序能够通过所有标准 DDS 实体与 DDS 进行交互。 
代理将客户端的状态保存在其内存中，这样即使客户端断开连接， 
代理也能保持活动状态。代理和客户端之间的通信遵循请求-响应模式， 
即基于操作和响应的双向模式。

![](/media/2020/eprosima_microros_dds_topology-300x106.png)


## 为什么使用 FreeRTOS？

得益于其轻量级特性，XRCE-DDS 客户端库和 micro-ROS 都适合在实时操作系统上运行， 
因此能够满足其典型目标应用程序所施加的对时间要求严格的需求， 
例如需要在特定截止时间之前完成或需要确定性响应的任务。

具体而言，FreeRTOS 位列首批 [RTOS](https://micro-ros.github.io/docs/concepts/rtos/) 名单， 
得到 micro-ROS 项目的支持，因此已集成到其软件堆栈中。这可确保 
micro-ROS 重用 FreeRTOS 社区和合作伙伴提供的所有工具和实现。由于 micro-ROS 
软件堆栈采用模块化设计，因此可以根据需要灵活更换或替换软件实体。

FreeRTOS 是开发 micro-ROS 和 Micro XRCE-DDS 应用程序的理想选择。  
首先，它可为多种不同的架构和开发工具提供独立的解决方案， 
编写方式非常清晰透明，并且拥有非常庞大的用户群，这可确保 
大量 FreeRTOS 用户能够将其应用程序与 micro-ROS 应用程序集成。 
此外，众所周知，它是高度可靠的 RTOS。关键是，FreeRTOS 对 ROM 和 RAM 的要求非常低，且处理 
开销也很低。通常，RTOS 内核二进制映像大小在 6K 到 12K 字节之间。这些内存 
数据对于尽量降低 MCU 上 micro-ROS 应用程序的内存占用非常理想， 
这是因为 micro-ROS 应用程序需要与 RTOS 竞争有限的资源。

接下来，我们将讨论 FreeRTOS 的几项功能，以及 micro-ROS 如何充分利用这些功能， 
以优化其堆栈中不同库所需的功能 
。


### 任务和调度器

FreeRTOS 提供了一组最基本的[任务实体](https://www.freertos.org/taskandcr.html)，这些实体 
与调度器一起使用，可提供在应用程序中实现确定性所需的工具。 
micro-ROS 客户端库（RCL、RCLC 和 RCLCPP）会访问 RTOS 的资源，以控制 
调度和电源管理机制，从而为开发者提供 
优化应用程序的可能性。

FreeRTOS 提供两种任务：标准任务和空闲任务。标准任务由用户创建， 
可视为 RTOS 上的应用程序。关键是，micro-ROS 应用程序 
可作为具有给定[优先级](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/03-Task-priorities) 的标准任务集成到 RTOS 中。 
另一方面，[空闲任务](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/15-Idle-task.html) 
则是优先级较低的任务，仅在没有其他任务运行时才进入运行模式 
。由于 micro-ROS 主要针对低功耗和 IoT 设备，空闲任务和相关的 
空闲钩子非常适合在 MCU 中启用深度睡眠状态。 得益于 
作为 micro-ROS 中间件实现的无状态 XRCE-DDS 客户端，这些深度睡眠状态具有内存易失性，也就是说， 
由于采用连接导向的中间件有线协议，因此可以使用没有 RAM 持久性的深度睡眠模式 
。

使用 FreeRTOS 调度器后，micro-ROS 能够管理其主要任务和负责传输层的 
任务的优先级。通常，负责网络堆栈或串行接口的任务 
必须优先于 micro-ROS 应用程序。


### 内存管理

FreeRTOS 提供许多颇受欢迎的功能，其中令 micro-ROS 开发者和用户深感兴趣的功能无疑是 
[堆栈管理](https://www.freertos.org/Stacks-and-stack-overflow-checking.html) 
和[静态堆栈创建](https://www.freertos.org/Static_Vs_Dynamic_Memory_Allocation.html) 功能。 
在处理 micro-ROS 任务创建时，堆栈分配通常是关键的设计决策。 
FreeRTOS 可用于精细管理堆栈大小，这反过来可让程序员了解 
程序执行期间使用了多少堆栈内存，还可以帮助程序员确定 
堆栈内存分配是在静态内存还是动态内存中进行，从而确保合理使用 MCU 内存， 
而这是嵌入式系统中的宝贵资源。至关重要的是，可以向 micro-ROS 等 
大量消耗堆栈的任务提供静态分配的堆栈，以防止将来出现堆和其他任务初始化问题。

在这方面，值得一提的是，这些内存管理工具 
可针对 micro-ROS 和 XRCE-DDS 的内存占用提供理想的基准测试框架。具体而言，我们已进行彻底的堆栈消耗分析， 
以评估 XRCE-DDS 客户端的内存消耗。堆栈是指 
程序员在运行应用程序之前无法预知的那部分内存。为测量堆栈， 
可以使用 FreeRTOS [uxTaskGetStackHighWaterMark](https://www.freertos.org/uxTaskGetStackHighWaterMark.html)() 函数， 
该函数可返回在执行期间 
XRCE-DDS 任务堆栈达到最大值时未使用的堆栈量。从总堆栈中减去此值，即可得到 
XRCE-DDS 应用程序使用的堆栈峰值。本帖发布的报告中总结了 
使用这种方法获得的结果。

我们还注意到，由于使用了可插拔[动态内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management) 方法 
（在 FreeRTOS 中），micro-ROS 能够完成管理内存所需的接口。 
如此一来，可以使用 
[heap_4](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management/#heap_4c) 作为参考实现 calloc() 或 realloc() 等函数 
。这些函数在馈送至 micro-ROS 内存管理 API 之前已封装， 
以便分析动态内存消耗。

与静态内存情况类似，FreeRTOS 的可交换动态内存管理方法可用于 
轻松在嵌入式系统中执行动态内存分析。实际上，在其他 RTOS 中， 
动态内存的分配和释放函数通常深藏在 RTOS 或标准库中，但在 FreeRTOS 中， 
这些函数却对用户公开并且易于定制，因此可简化处理和 
控制动态内存使用的过程。


### 传输资源

就像客户端支持库访问 FreeRTOS 的特定原语和 
函数（例如调度机制）一样，中间件实现 Micro XRCE-DDS 需要访问 
RTOS 的传输和时间资源才能正常运行。在 IP 传输方面， 
特别是在 FreeRTOS 的情况下，Micro XRCE-DDS 使用附加组件 
在该 RTOS 上实现 lwIP。[lwIP](https://savannah.nongnu.org/projects/lwip/)（轻量级 IP）是一种广泛使用的开源 
TCP/IP 堆栈，专为嵌入式系统设计，旨在减少资源使用，同时提供 
全面的 TCP 堆栈。因此，lwIP 特别适合 
micro-ROS 所针对的嵌入式系统和资源受限的环境。

除了 TCP/IP 堆栈， lwIP 还有其他几个重要部分，如网络接口、 
操作系统仿真层、缓冲区和内存管理部分。操作系统仿真层 
和网络接口可用于将网络堆栈移植到操作系统中， 
这是因为它们可提供通用接口，确保 lwIP 代码可以与操作系统内核进行无缝交互。

[FreeRTOS 与 lwIP 的集成](https://docs.aws.amazon.com/freertos/latest/portingguide/porting-lwip.html) 
从一开始就设计为采用广为熟知的标准接口（即 Berkeley 套接字）， 
且线程安全，目的是使其尽可能易于使用。此外，该集成将缓冲区管理 
保留在可移植层。

请注意，XRCE-DDS 客户端还支持 
[FreeRTOS-Plus-TCP](https://www.freertos.org/FreeRTOS-Plus/FreeRTOS_Plus_TCP/index.html) 网络 
堆栈。FreeRTOS-Plus-TCP 是官方 FreeRTOS 扩展库，用于为 TCP/IP 堆栈协议提供支持。

我们还努力确保 FreeRTOS-Plus-TCP 与 micro- ROS 兼容，比如支持 
TCP 和 UDP 连接，依靠 FreeRTOS-Plus-TCP API 来实现 
micro XRCE-DDS 客户端 API 所需的抽象层，以便能够使用这些协议与代理进行通信。

此外，还可能使用 
FreeRTOS 的[时间测量功能](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)， 
从而使 XRCE-DDS 库能够执行基于时间的任务，同时向用户隐藏实现过程 
。


### Posix 扩展

FreeRTOS 之所以可以无缝集成到 micro-ROS 中并提供诸多益处，另一个明显原因是 
可提供 [POSIX 扩展](https://www.freertos.org/FreeRTOS-Plus/FreeRTOS_Plus_POSIX/index.html)。 
可移植操作系统接口 (POSIX) 是 IEEE 计算机学会 
为维护不同操作系统之间的兼容性而指定的一系列标准。FreeRTOS-Plus-POSIX 层 
（由 FreeRTOS Labs 提供）可实现 POSIX API 的子集。

事实上，虽然 micro-ROS 中间件对 POSIX 的依赖性较低（仅需要 clock_gettime() 函数）， 
但整个 micro-ROS 堆栈在功能和类型定义方面对 POSIX 的依赖性较高。此外， 
由于 micro-ROS 项目的一项基本原则是移植或重用 ROS 2 代码 
（原本为 Linux 编写，Linux 是一种基本符合 POSIX 的操作系统） ，因此使用在某种程度上符合 POSIX 的 RTOS  
显然有益，因为代码的移植工作量很小。

为此，micro-ROS 使用了 [sleep()](https://pubs.opengroup.org/onlinepubs/9699919799/functions/sleep.html) 
和 [usleep()](https://pubs.opengroup.org/onlinepubs/000095399/functions/usleep.html) 等函数。 
micro-ROS 依赖 POSIX 进行类型定义体现在一些结构体上， 
比如 struct timeval 或 struct timespec，而这些结构体在 FreeRTOS 内核中未加定义。micro-ROS 还需要 types.h、signal.h 或 unistd.h 等文件 
来定义一些标准的类型和结构体。

对于 errno.h，出于编译的需要，micro-ROS 必须包含一些不可用的定义， 
尽管这些定义尚未在 FreeRTOS-Plus-POSIX 层实现，仍需包含在其中。

为实现与 FreeRTOS-Plus-POSIX 的完全兼容，应在 micro-ROS 堆栈内重构这些定义， 
这可通过使用 [FreeRTOS-Plus-FAT](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/01-FreeRTOS-plus-FAT) 库 
实现。通过这种方式，依赖于文件系统支持的高级 micro-ROS 功能（例如日志记录机制） 
可以得到完全支持。


## 结语

总之，FreeRTOS 是一款轻量级的理想 RTOS，可在其上运行 micro-ROS 应用程序， 
因为它可提供广泛的所需功能， 
micro-ROS 堆栈中的几乎所有模块化层都会在不同层次上使用这些功能。

随着 micro-ROS 和 FreeRTOS 的用户群迅速扩大，引人注目的用例不断涌现， 
可以预见，在不久的将来，micro-ROS 将与 FreeRTOS 和 FreeRTOS-Plus 提供的库 
进一步集成。 

在这些库中，利用 [FreeRTOS-Plus-FAT](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/01-FreeRTOS-plus-FAT) 
库似乎尤为可取，该库可用于添加虚拟文件系统组件， 
进而像在完全部署的 ROS 2 生态系统中一样可视化和管理日志记录操作。

micro-ROS 项目设想进一步利用内存管理工具（有专门章节进行介绍） 
来扩展 [XRCE-DDS 客户端的内存分析](https://www.eprosima.com/index.php/resources-all/performance/micro-xrce-dds-memory-profiling)， 
以便为 micro-ROS 客户端提供类似的分析。

micro-ROS 项目今后还计划采用经过认证的 
FreeRTOS 版本，即 [SafeRTOS](https://www.highintegritysystems.com/safertos/)。

最后但同样重要的是，值得一提的是两个将 FreeRTOS 成功集成到 
硬件中的案例，这些硬件与 micro-ROS 的典型目标应用程序相关， 
分别为功能强大的 [Crazyflie 2.1 无人机](https://www.bitcraze.io/products/crazyflie-2-1/) 和 
[ESP32 MCU](https://www.espressif.com/en/products/socs/esp32)。事实上，Crazyflie 软件有效利用了 
FreeRTOS 的多种工具和功能。如需查看在这款微型无人机 (MAV) 上将 micro-ROS 应用程序 
与 FreeRTOS 一起使用的演示示例，请点击[此处](https://www.youtube.com/watch?v=UDnSpWhkfZQ&t=14s)。 
第二种硬件（即 ESP32 MCU）与 FreeRTOS 原生集成，提供即用型 Wi-Fi 天线 
和蓝牙功能，最近已[在 ESP32 系统上完成 micro-ROS 的移植](https://discourse.ros.org/t/micro-ros-porting-to-esp32/16101)工作 
。

最后，有关如何在 FreeRTOS 上创建并运行首个 micro-ROS 应用程序 
（使用 [Olimex STM32-E407](https://www.olimex.com/Products/ARM/ST/STM32-E407/open-source-hardware) 
评估板）的完整指南，请点击[此处](https://micro-ros.github.io/docs/tutorials/core/first_application_rtos/freertos/)。


## 关于 eProsima

[eProsima](http://www.eprosima.com/) 是一家专注于网络中间件的公司，特别关注 
[OMG](http://www.omg.org/)（对象管理组）标准， 
即[实时系统数据分发服务 (DDS)](https://www.eprosima.com/index.php/resources-all/dds-all)。

eProsima 的主要产品是 eProsima [Fast DDS](https://www.eprosima.com/index.php/products-all/eprosima-fast-dds)， 
这是一款轻量级 DDS 开源实现，可直接访问底层协议， 
即实时发布订阅 (RTPS) 协议。

eProsima 是机器人操作系统 (ROS) 的重要贡献者，因为 **eProsima Fast DDS 被选为 [ROS 2](https://index.ros.org/doc/ros2/) 的默认中间件**。
由于这个原因和其他 
重要贡献，eProsima 获选为 **ROS 2 技术指导委员会**成员，以推动这一事实上的标准机器人框架的路线图。


eProsima 还主导 **[Micro-ROS 项目](https://micro-ros.github.io/)**，旨在将 ROS 2 扩展到微控制器， 
这种扩展基于全新 eProsima 中间件产品 
eProsima [Micro XRCE-DDS](https://eprosima.com/index.php/products-all/eprosima-micro-xrce-dds) 
（适用于资源极其受限环境的 DDS），该产品已被 ROS 社区采用。


## 作者简介

![](https://secure.gravatar.com/avatar/ef089a655d66d85a31cc1c1a7e01a4ac?s=200&d=mm&r=g)    
Francesca Finocchiaro 拥有物理学专业背景，在 eProsima 担任项目经理一职。目前， 
她负责领导 micro-ROS 团队，并协调 OFERA (http://www.ofera.eu/) 的欧盟项目，该项目旨在 
开发并积极维护 micro-ROS。  
[查看此作者的文章](../author/francesca-finocchiaro) 

FreeRTOS 论坛：获得行业领先的专家支持，并与全球同行 
合作。[查看论坛](https://forums.freertos.org/)

