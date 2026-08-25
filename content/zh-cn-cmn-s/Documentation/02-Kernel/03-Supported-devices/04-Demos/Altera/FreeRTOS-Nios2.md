---
title: "Altera Nios II FreeRTOS 演示 在 Cyclone III FPGA 上运行"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

[[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![](/media/2018/DBC3C40.jpg)  

此演示是在 EBV Elektronik 的 [DBC3C40 参考设计](http://www.ebv.com/ru/produkty/categories/details/product/dbc3c40.html)的基础上开发的， 
基于 Altera Cyclone III FPGA。

可以使用免费 Web 版 
[Quartus II 和 Nios II 嵌入式设计套件](https://www.altera.com/support/software/download/nios2/dnl-nios2.jsp)来配置和编译 FPGA 和软件。

请注意，此移植最初是使用版本 9 之前的设计工具编写的。Calvin Ruben
一直很好地保持着项目的更新，[并在 FreeRTOS Interactive 页面上发布了一个版本](http://interactive.freertos.org/entries/242506-nios-updated-port-for-nioseds-9-1-and-10-0)，
该版本与 Altera 工具的 9.1 版和 10 版兼容。我谨代表 FreeRTOS 社区感谢 Calvin 所做的一切。

---

#### *重要！Altera Nios II 演示使用说明*

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [演示应用程序](#演示应用程序)
3. [RTOS 配置和使用详情](#rtos-配置和使用详情)

另请参阅常见问题：[我的应用程序无法运行，问题可能出在哪里？](/Why-FreeRTOS/FAQs/Troubleshooting)

---

### 源代码组织

Nios II IDE 项目文件位于 FreeRTOS/Demo/NiosII_CycloneIII_DBC3C40_GCC 目录中。这是 
将项目导入 IDE 工作区时要选择的目录。

下载的 FreeRTOS zip 文件包含所有移植文件和演示应用程序项目文件。因此，它包含的文件 
远超此演示所用的文件。请参阅[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)部分， 
获取下载文件的介绍以及有关创建新项目的信息。

---

### 演示应用程序

#### 创建项目目录结构

Nios II IDE 是 [Eclipse](http://www.eclipse.org/) 的定制版本。 
使用 Eclipse 托管 make 构建的最简单方法是在包含 Eclipse 项目文件的目录下找到所需的构建文件（C 源文件、头文件和链接器脚本）
。FreeRTOS 下载中包含一个名为 CreateProjectDirectoryStructure.bat 的批处理文件，
该文件将所有需要的构建文件从 FreeRTOS 目录结构中的正常位置复制到
Eclipse 项目目录的子目录中。批处理文件位于 FreeRTOS/Demo/NiosII_CycloneIII_DBC3C40_GCC 目录中，**必须在将项目
导入 Nios II IDE 之前执行**。

从命令提示符或 Windows 资源管理器执行 CreateProjectDirectoryStructure.bat。该文件无法
在 Eclipse 环境中成功执行。

**注意！**CreateProjectDirectoryStructure.bat 必须在演示项目导入 Nios II IDE 之前执行，否则
存储在项目中的包含路径将遭到破坏。

#### 将项目导入 Nios II IDE 工作区

1. **注意！**CreateProjectDirectoryStructure.bat 必须在演示项目导入 Nios II IDE 之前 
 执行。请参阅上文说明。
2. 启动 Nios II IDE。启动时，系统可能会提示您选择工作区位置。您可以使用现有工作区
 或在方便的目录中创建新工作区。
3. 在 Nios II IDE 中，从 "File" 菜单中选择 "Import..."。
4. 此时将显示一个对话框。选择 "Existing Projects Into Workspace"，然后单击 "Next"。
5. 浏览并选择 FreeRTOS/Demo/NiosII_CycloneIII_DBC3C40_GCC 目录。该目录包含两个项目：一个名为 RTOSDemo，另一个 
 名为 RTOSDemo_syslib。
6. 在完成导入过程之前，请确保已选中两个项目，请勿勾选 "Copy projects into workspace" 复选框。

![](/media/2018/RedSuite_Import.jpg)  
将 FreeRTOS 项目导入 Nios II IDE 工作区

#### 演示应用程序硬件设置

DBC3C40 参考设计随附的 CD 包含一系列 .sof 文件，这些文件可实现各种不同的 Nios II 配置。本页介绍的演示
是使用 TFT.sof 开发的。

演示使用内置于 DBC3C40 的 LED。控制 LED 的函数
在 FreeRTOS/Demo/NiosII_CycloneIII_DBC3C40_GCC/RTOSDemo/ParTest/ParTest.c 中实现。
如果使用的硬件平台具有不同的 IO 配置，则可能需要修改这些函数。

演示包括 "ComTest" 任务，其中一项任务在 UART 上传输字符，然后由另一项任务接收。如果
收到的任何字符不符合顺序或存在丢失的情况，则会锁定错误。要想该机制正常运行，必须在 UART 上安装环回连接器，只需将 UART Rx 引脚连接到
UART Tx 引脚即可。

#### 构建并执行演示应用程序

1. 打开 main.c 并搜索以 "#error" 开头的行。删除该行（提供了关于设置目录结构的说明，
 适用于那些没有阅读说明即使用项目的用户）。
2. 使用编程和调试接口将目标硬件连接到主机，此时可使用 Altera USB Blaster。
3. 要构建项目，只需在 "Project" 菜单中选择 "Build All" 即可。构建应用程序时，不应出现错误
 或警告（假设已删除 #error 语句，并已执行 CreateProjectDirectoryStructure.bat）。初始 
 构建将需要一些时间，因为它会生成整个系统库。
4. 需要创建启动配置才能启动调试会话。启动配置只需创建一次，此后
 只需单击 "Debug" 速度按钮即可启动调试会话。要创建启动配置，
 首先在 IDE 项目窗口中选择 "RTOSDemo" 项目，然后在 "Run" 菜单中选择 "Debug..."。
5. 在打开的对话框中，双击 "Nios II hardware" 以创建新配置。配置
 参数会自动设置。
6. 最后单击 "Debug" 以对 MCU 进行编程，并启动调试会话。

第一次下载尝试会导致 Nios II IDE 自动打开 Quartus II 编程器，从中可以打开 .sof 文件
并将其编程到 FPGA 中。下载 .sof 文件后，可以单击 debug 速度按钮
以重新运行调试启动配置。FPGA 首次通电后才需进行此操作。

![](/media/2018/NiosII-IDE-Debug-Configuration.jpg)  
设置启动配置

#### 功能

演示应用程序会在启动 RTOS 调度器之前创建 43 项任务。这些任务主要包括 
标准演示应用程序任务（请参阅[演示应用程序](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
部分，了解各任务详情）。这些任务的唯一目的是测试 RTOS 内核移植 
并演示如何使用各种 API 函数。

除了标准演示任务外，还创建了以下任务和测试：

* 检查任务
 此类任务每 5 秒执行一次。其主要功能是检查所有 
 标准演示任务是否仍在运行。如果系统中的所有任务都在无错误执行，
 则检查任务每 5 秒切换一次 LED 7。如果切换速度增加到 500 毫秒，则表示
 至少有一项任务报告了错误，该报错任务的名称会写入 
 Nios II IDE 终端。要测试此机制，可以从 UART 中移除环回连接器
 并故意引入错误。
* 寄存器测试任务
 在检查每个寄存器是否包含预期值之前，寄存器测试任务会用已知值填充 Nios II 寄存器。
 包含意外值的寄存器表示上下文切换机制中存在错误。创建两项寄存器测试任务，
 每项任务使用一组不同的寄存器值。

正确执行时，演示应用程序的表现如下：

* LED 0、1 和 2 受标准“闪烁”任务控制。各 LED 将以不同的固定频率切换。
* LED 4 和 5 受 ComTest 任务控制，每传输一个字符，其中一个 LED 就会切换，而另一个 LED 会在
 正确收到字符时切换。
* LED 7 受检查任务控制（如上所述）。每 5 秒切换一次。

---

### RTOS 配置和使用详情

#### RTOS 移植特定配置

此演示特定的配置项位于 FreeRTOS/Demo/NiosII_CycloneIII_DBC3C40_GCC/RTOSDemo/FreeRTOSConfig.h 中。您 
可以编辑此文件中定义的常量，确保适配您的应用程序，尤其是可以编辑 configTICK_RATE_HZ 以设置 RTOS 滴答的频率。 
提供的值 (1000Hz) 对测试 RTOS 内核功能非常有用，但该频率超过大部分应用程序所需的频率。降低此值可提高效率。

每个移植都会将 "BaseType_t" 定义为对处理器而言最有效的数据类型。本移植
将 BaseType_t 定义为长类型。

请注意，vPortEndScheduler() 尚未实现。

#### 中断服务程序

中断入口点包含在 RTOS 内核移植层（位于 FreeRTOS/Source/portable/GCC/Nios II/port_asm.S）中，并且编写为
与 Altera HAL 兼容。这意味着可按照 Altera HAL 文档编写中断服务程序， 
并可使用标准 HAL alt_irq_register() 函数进行注册。 

有时需要中断服务程序中断一项任务，但返回另一项任务。如果中断服务程序
导致任务解除阻塞，并且解除阻塞的任务的优先级高于当前正在执行的任务，就会出现这种情况。提供的宏 portEND_SWITCHING_ISR()
允许中断服务程序请求上下文切换，如果无需上下文切换，则向 portEND_SWITCHING_ISR() 传递 0；如果
需要上下文切换，则传递非零值。

请参阅 FreeRTOS/Demo/NiosII_CycloneIII_DBC3C40_GCC/RTOSDemo/serial.c，获取中断服务程序示例和 portEND_SWITCHING_ISR() 的用法示例。

#### 内存分配

演示应用程序项目中包含的 Source/Portable/MemMang/heap_2.c 可用于提供 
RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分， 
获取完整信息。

