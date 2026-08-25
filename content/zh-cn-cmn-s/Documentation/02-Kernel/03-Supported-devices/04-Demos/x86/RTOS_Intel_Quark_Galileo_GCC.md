---
title: "在 Intel® Galileo (x86 Quark™ SoC X1000) 上运行的 FreeRTOS"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

 [[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

![Intel Galileo 第 2 代单板计算机](/media/2018/intel_galileo_gen_2.jpg)

### 简介

[![FreeRTOS 内核感知 RTOS 插件](/media/2018/Galileo_state_viewer.png)](/media/2018/Galileo_state_viewer.png)

**FreeRTOS Eclipse 插件显示

 在 Galileo

 Quark X1000 SoC 上运行的任务的状态。点击放大。**

本页记录了一个 RTOS 演示应用程序，它使用 FreeRTOS IA32 (x86)
平面内存模型移植，并预先配置为在 [Galileo Gen 2 单板计算机](https://software.intel.com/iot/hardware/galileo)上运行，
该计算机使用
[IntelQuark SoC X1000](http://www.intel.co.uk/content/www/uk/en/intelligent-systems/quark/quark-x1000-overview.html)
 (x86/IA32) CPU。

FreeRTOS IA32 移植实现了一个完整的中断嵌套模型，
利用独立的系统堆栈来节省 RAM，
并且从不全局禁用中断（尽管硬件本身在中断进入时禁用中断）。

---

### *重要提示！FreeRTOS IntelQuark SoC 演示*使用说明

*使用此 RTOS 移植前，请阅读下述所有要点。*

1. [源代码组织](#源代码组织)
2. [RTOS 演示应用程序](#功能)
3. [构建说明](#构建说明)
4. [在 Galileo Gen 2 板上运行 RTOS 演示](#创建初始可启动-sd-卡)
	* [创建初始可启动 SD 卡](#创建初始可启动-sd-卡)
	* [使用 SD 卡启动FreeRTOS](#使用-sd-卡启动freertos)
	* [使用 SCP 更新 RTOS 可执行程序](#使用-scp-更新-rtos-可执行程序在整个网络上)（在整个网络上）
5. [在 Galileo Gen 2 板上调试 RTOS 演示](#rtos-配置和使用详情)
6. [RTOS 配置和使用详情](#rtos-配置和使用详情)
	* [FreeRTOS Intel IA32 移植特定配置](#freertos-ia32-移植特定配置intel)
	* [中断服务程序](#中断服务程序)

另请参阅常见问题“[我的应用程序无法运行，问题可能出在哪里？](/Why-FreeRTOS/FAQs/Troubleshooting)”。

---

### 源代码组织

FreeRTOS .zip 文件下载中只有一小部分文件是
Intel Quark SoC 演示所需要的。[源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)页面描述
FreeRTOS zip 文件下载的结构。

用于构建和调试演示的 Eclipse 项目位于
FreeRTOS/Demo/IA32_flat_GCC_Galileo_Gen_2
目录中。请注意，RTOS 项目包含目录结构中其他位置的文件，
因此，如果目录结构已被更改，项目可能无法构建。

---

Intel Quark SoC X1000### 演示应用程序

### 硬件和软件设置

RTOS 演示使用内置在 Galileo 硬件上的 LED 和 UART，因此
无需特定的硬件设置。

UART 使用 115200 波特率、无奇偶校验位、8 个数据位和 1 个停止位。

### 功能

演示的行为取决于 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY
常量，它声明在 main.c 的顶部。

### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1 时的功能

如果 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 1，则 main() 将
调用 main_blinky()。
main_blinky() 函数会创建一个简单的演示，该演示创建两个
[任务](/Documentation/02-Kernel/02-Kernel-features/01-Tasks-and-co-routines/01-Tasks-overview) 和一个 [队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)，
具体如下：
* **“队列发送”任务**

 “队列发送”任务每 200 毫秒将值 100 发送到队列。
* **“队列接收”任务**

 “队列接收”任务从队列中读取值，并在每次收到数值 100 时，
 切换 LED，并将 LED 状态写入 UART。

如果简单的 blinky 演示正常工作，则 LED
将每 200 毫秒切换一次。

### mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 时的功能

如果 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY 设置为 0 ，则 main() 将
调用 main_full()。main_full() 创建一个全面的测试和演示应用程序
以展示：
* 中断嵌套
* 使用
 [中断服务程序](#中断服务程序)
 部分所述的两种方法设置中断。
* [直达任务通知](/Documentation/02-Kernel/02-Kernel-features/03-Direct-to-task-notifications/01-Task-notifications)。
* [软件定时器](/Documentation/02-Kernel/02-Kernel-features/05-Software-timers/01-Software-timers)。
* [队列](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/01-Queues/)。
* [信号量](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/02-Binary-semaphores/)。
* [互斥锁](/Documentation/02-Kernel/02-Kernel-features/02-Queues-mutexes-and-semaphores/04-Mutexes/)。
* [事件组](/Documentation/02-Kernel/02-Kernel-features/06-Event-groups)。
* [队列集](/Documentation/02-Kernel/04-API-references/07-Queue-sets/00-RTOS-queue-sets)。

演示创建的大多数 RTOS 任务来自[标准演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/01-Demo-overview)
任务集。这些任务由所有 FreeRTOS 演示应用程序使用，
除了演示正在使用的 FreeRTOS
API 和测试 RTOS 内核移植外，没有特定的功能或目的。

完整演示包含一个“检查”任务。检查任务定期
监测演示中的所有其他任务，然后切换 LED
并向 UART 打印状态代码。如果 LED 每五秒钟切换一次，且打印
状态代码为 0 ，则检查任务未检测到任何意外行为。
如果 LED 每秒切换一次，则检查任务已检测到
意外行为，并且导致潜在错误的原因被锁定在
状态代码值中-可以通过检查
main_full.c 源文件中 prvCheckTask() 的实现来确定状态代码的含义。

---

### 构建说明

Eclipse 项目[同时使用虚拟文件夹和链接](/Documentation/02-Kernel/03-Supported-devices/04-Demos/IDE/Project_Workspace_Relative_File_Paths_Eclipse)，它们从
FreeRTOS 目录结构内的其他位置引用文件。在 Eclipse 项目资源管理器中查看的[虚拟]文件结构
将与磁盘上查看的[实际]文件结构
不匹配。

请注意，演示是在 Windows 主机上开发和测试的。在
Linux 主机上构建演示的任何问题都很可能
与包含文件名或包含路径中使用的字母大小写有关。
[请报告](/Why-FreeRTOS/Support-options)
任何此类错误，以便予以纠正。

要构建 RTOS 演示应用程序：

1. 如果尚未安装，请下载并安装 [Eclipse CDT](https://eclipse.org/cdt/)
 发行版。
2. 如果尚未安装，请下载并安装 x86 GCC elf 编译器。
 项目的开发和项目预配置都使用
 从 osdev.org 网站引用的[预建 i686-elf-gcc GCC 工具链](http://wiki.osdev.org/GCC_Cross-Compiler#Prebuilt_Toolchains)
 。

**注意：**据发现，
 上面提到的编译器对不属于编译器包的 DLL
 有依赖性。解决这一问题最简单的方法是
 [安装 
 MingW](http://sourceforge.net/projects/mingw/files/latest/download) 编译器，并确保 MingW bin 目录也在您的路径中，
 因为它带有必要的 dll 文件。如果任何人知道
 没有这种外部依赖性的 elf 编译器，
 [请告诉我们](/Why-FreeRTOS/Support-options)。

 COFF 编译器（如 MingW），也可以用来构建该实例，
 但可能需要
 调整项目设置，而且不会提供这么好的
 调试体验。
3. 理想情况下，确保编译器的 bin 目录的路径包含在 Windows
 PATH 环境变量中。也可以将路径设置在
 Eclipse 项目本身中-稍后对此进行说明。
4. 如果您的主机系统没有提供 “rm” 实现（删除文件）
 命令，则可能需要提供或安装一个这种实现，以便执行
 "build clean" 操作。[UnxUtils](http://sourceforge.net/projects/unxutils/)
 软件包提供了一个适合在 Windows 上使用的预建版本。确保
 'rm' 可执行程序也位于包含在
 Windows PATH 环境变量中的路径中。
5. 打开 Eclipse IDE 并创建一个新的工作区或按提示选择一个现有的
 工作区。
6. 从 IDE 的 "File" 菜单中选择 "Import"，
 弹出导入对话框。
7. 在导入对话框中，选择 "General->Existing Projects Into Workspace"
 然后浏览并选择 FreeRTOS/Demo/IA32_FLAT_GCC_Galileo_Gen_2
 目录。您将看到一个名为 "RTOSDemo" 的项目。
8. 在点击 "Finish" 之前，确保已选中 RTOS 演示，
 并且未选中 "Copy Projects Into Workspace"。

![将 Intel Quark IA32 RTOS 演示项目导入 Eclipse 工作区](/media/2018/importing_intel_galileo_free_rtos_project.png)

**将 RTOS 演示导入 Eclipse 工作区，而没有
 将其复制入工作区。**
9. 如果您使用的是 GCC 编译器而非 i686-elf-gcc 发行版，
 或者如果您需要设置编译器的路径，
 那么您可以按照下列指示设置 Eclipse 项目的
 “交叉编译器”：

 从 IDE 的 "Project" 菜单中选择 "Properties"，
 弹出属性对话框。在对话框中选择 "C/C++Build->Settings->Cross Settings"，
 然后设置将要使用的编译器的名称，
 必要时设置路径。

![设置构建 Intel Quark RTOS 演示](/media/2018/setting_intel_quark_rtos_compiler.png)的编译器的路径

**在 RTOS 项目属性对话框中设置编译器路径**
10. 打开 main.c 并设置 mainCREATE_SIMPLE_BLINKY_DEMO_ONLY，根据需要生成
 简单的 blinky 演示或完整的测试和演示应用程序
 。
11. 在 IDE 的 "Project" 菜单中选择 "Build All"。该项目应在
 不产生错误的条件下构建-如果不是如此，
 请参阅下面的构建故障排除提示。

构建故障排除提示：

* GCC 编译器应自动定位标准库头文件，
 在这种情况下，头文件的路径将显示在项目选项中，
 如下图所示。点击图片
 放大：

|  |  |
| --- | --- |
| [![Intel Quark 项目](/media/2018/Intel_cross_settings_0.png)](/media/2018/Intel_cross_settings_0.png)的交叉编译器选项 | [![Intel Quark 项目](/media/2018/Intel_cross_settings_1.png)](/media/2018/Intel_cross_settings_0.png)的 GCC 编译器选项 |
\| < br/> < br/>**应自动设置的项目选项** < br/> < br/> \|

 如果您收到如 "Symbol NULL could not be resolved" （符号 NULL 无法解析）或
 "Type size_t could not be resolved" （类型 size_t 无法解析）等错误，那么您可能需要
 在项目选项中手动设置头文件的路径。
* 有报告指出，如果 Eclipse 不是以管理员权限运行，
 可能会出现构建错误。

在 Galileo Gen 2### 板上运行 RTOS 演示

可以从 SD 卡在 Galileo 主板上启动 RTOS 演示可执行程序。
为此使用一个多重启动 GRUB 镜像。GRUB 配置使 Galileo 能够
在 FreeRTOS 或 Linux 中启动。在 Linux 中启动允许 RTOS 演示
可执行程序通过网络更新。

关于创建 GRUB 映像的完整说明，
请参阅[此链接上提供的 pdf 文件](https://sourceforge.net/projects/freertos/files/FreeRTOS/Utils/FreeRTOS_Intel_Quark_Docs/FreeRTOS_Galileo_Boot_Instructions.pdf/download)。为了
简单起见，
[此链接上还提供了预建 SD 卡映像](https://sourceforge.net/projects/freertos/files/FreeRTOS/Utils/FreeRTOS_Intel_Quark_Docs/FreeRTOS_Galileo_Multiboot_GRUB_SD_Card_Image.7z/download)。
下面提供了有关使用预置 SD 卡映像的简要说明。
具体说明请参阅 pdf 文件。

在继续之前，可能需要更新 Galileo 固件-
在同一 pdf 文件中还提供了关于更新所述固件的说明。

SD 卡必须格式化为 FAT 或 FAT32，容量小于等于 32 G 字节，并采用 SDHC
规格。不支持 SDXC 规格。

### 创建初始可启动 SD 卡

要从 Windows 主机创建初始可启动 SD 卡：
1. 以管理员身份打开命令提示符 (cmd.exe)。
2. 在命令提示符中运行 diskpart.exe 以启动磁盘分区实用程序。
3. 输入以下磁盘分区命令：
	*选择磁盘卷 n       [其中 'n' 是
	 windows 分配给 SD 卡的盘符。例如，如果 SD 卡
	 是 z 盘，则您需输入 “select volume z”。]
	* clean
	* create part primary
	* active
	* format quick label="BOOTME"
	* exit
4. 解压缩[预建 SD 映像](https://sourceforge.net/projects/freertos/files/FreeRTOS/Utils/FreeRTOS_Intel_Quark_Docs/FreeRTOS_Galileo_Multiboot_GRUB_SD_Card_Image.7z/download)
 到已分区和格式化的
 SD 卡的根目录中，这样 SD 卡的根目录
 就包含了启动文件夹，以及 bzImage（和其他）文件。
5. 将创建 RTOS 演示时生成的 RTOSDemo.elf 文件复制到
 SD 卡上的 /kernel 目录中。

### 使用 SD 卡启动FreeRTOS

要从 SD 卡启动 FreeRTOS：
1. 使用合适的串行电缆
 将 Galileo 连接到运行哑终端程序（如 Tera Term）的主机上。连接使用
 115200 波特，无奇偶校验，8 个数据位，无停止位。
2. 按照上述说明创建 SD 卡后，
 将 SD 卡插入 Galileo 第 2 代硬件的插槽中。
3. 重置 Galileo 主板。
4. 哑终端将显示启动选项菜单。选择 "Multiboot
 GRUB"，或者简单地让菜单超时，因为 Multiboot GRUB 是默认选项。

![Intel x86 启动选项上的 RTOS](/media/2018/Intel_Galileo_RTOS_boot_options.jpg)

**启动选项菜单**
5. 然后，终端将显示 Multiboot GRUB 菜单。选择 "FreeRTOS Demonstration"，
 或者简单地让菜单超时，因为 FreeRTOS 演示是默认选项。
 RTOS 演示将开始执行。

![使用 GRUB 启动 Galileo 硬件上的免费 RTOS](/media/2018/galileo_multiboot_grub_menu.jpg)

**多重启动 GRUB 菜单**

### 使用 SCP 更新 RTOS 可执行程序（在整个网络上）

可以将后续的 RTOS 演示 elf 文件复制到 SD 卡中，
具体做法是在 Linux 中启动 Galileo，然后使用 WinSCP。根据提供的信息，用于在 Galileo 主板上启动 FreeRTOS
的 SD 卡将使用 192.168.0.10 的 IP 地址，
因此主机将需要在同一本地网络中
拥有一个兼容的 IP 地址。

要使用 SCP 更新 RTOS 演示 elf 文件：

1. 如果尚未安装，请下载并安装 [WinSCP](https://winscp.net/eng/index.php)，
 或其他兼容的 SCP 客户端。
2. 重新启动 Intel Galileo 硬件，然后使用多重启动 GRUB 菜单
 选择 "Clanton SVP kernel"，这将启动 Linux 而不是 FreeRTOS。
3. 等待 Linux 启动，提示时，输入"root" 作为用户名，输入 "intel" 作为
 密码。
4. 确保在起动 WinSCP 之前，
 Galileo 主板与主机连接到同一网络。
5. 使用下图所示的设置创建并连接一个 WinSCP 会话。
 密码是 'intel'。

![使用 WinSCP 复制 Intel RTOS 映像](/media/2018/using_winscp_to_copy_intel_rtos_image.png)

**必要的 WinSCP 会话设置**
6. 连接 WinSCP 后，将新的 RTOS 演示 elf 文件复制到 "/media/realroot/kernel"
 目录，如下图所示。

![使用 WinSCP 更新 Intel RTOS 映像](/media/2018/Updating_RTOS_image_for_quark.jpg)

**更新的 FreeRTOS 映像必须复制到的目录**
7. 在 Linux 命令控制台中输入 "reboot"。这将确保
 在重启 Galileo 进入 FreeRTOS 之前，更新的 elf 文件被提交到 SD 卡。

在 Galileo Gen 2### 板上调试 RTOS 演示

Eclipse、OpenOCD 和 GDB 可用于下载、运行和调试更新的可执行程序，而无需
重新启动硬件。需要一个 JTAG 调试接口。该演示使用
Olimex 的 [ARM-USB-OCD-H](https://www.olimex.com/Products/ARM/JTAG/ARM-USB-OCD-H/) pod
（带有 [ARM-JTAG-20-10](https://www.olimex.com/Products/ARM/JTAG/ARM-JTAG-20-10/) 适配器）
创建和测试。

这些指令仅将镜像下载到 RAM 中，因此更新的镜像
不具有持久性，所以在 Galileo 重置后将不可用。

要将新的 RTOS 演示可执行程序下载到 RAM，请启动调试会话：

1. 如果尚未安装，请下载并安装 [OpenOCD](http://openocd.org/)。
2. 使用合适的基于 FTDI 的 JTAG 适配器
 将 Galileo 第 2 代评估板与主机相连。
3. 打开命令控制台，导航到安装有 openocd.exe
 的目录，并执行以下命令以
 按照要求配置启动 OpenOCD。请注意，该命令应在单行输入，
 并假设正在使用 ARM-USB-OCD-H 接口。

```c

openocd.exe -f ..scriptsinterfaceftdiolimex-arm-usb-ocd-h.cfg
                                         -f ..scriptsboardquark_x10xx_board.cfg

```
4. 在 FreeRTOS 中启动 Galileo，如上所述。
5. 在 Eclipse 中，使用 "Run->Debug Configurations..." 菜单项创建
 新的调试配置，如下图所示。
 **点击图像放大**

[![调试免费的 Intel RTOS 第 1 步](/media/2018/galileo_rtos_debug_configuration_1.jpg)](/media/2018/galileo_rtos_debug_configuration_1.jpg)

**创建调试配置——第 1 步**

[![调试免费的 Intel RTOS 第 2 步](/media/2018/galileo_rtos_debug_configuration_2.jpg)](/media/2018/galileo_rtos_debug_configuration_2.jpg)

**创建调试配置——第 2 步**

[![调试免费的 Intel RTOS 第 3 步](/media/2018/galileo_rtos_debug_configuration_3.jpg)](/media/2018/galileo_rtos_debug_configuration_3.jpg)

**创建调试配置——第 3 步。
映像中不可见的选项
 留空**
6. 单击 "Debug" 以使用 GDB 连接至 Galileo。请参阅下文的调试故障排除
 提示。
7. 在 Eclipse IDE 内有多个控制台可用。选择 GDB 控制台，
 如下图所示：

![调试免费的 Intel RTOS 第 3 步](/media/2018/selecting_the_gdb_console.jpg)

**在 Eclipse 中选择 GDB 控制台**
8. 在 GDB 控制台中，输入以下命令，
 用您安装的 RTOS 演示 elf 文件的正确路径替换 [输入路径]。
 请参阅下文的调试故障排除提示。为了简单起见，
 可以在脚本中加入以下命令。

```c

monitor reg eflags 0x0
flushregs
echo Downloading elf file.  Please wait.
monitor load_image C:[enter path]/RTOSDemo.elf 0
symbol-file C:[enter path]/RTOSDemo.elf
set $eip=_restart
c

```

 RTOS 演示 elf 文件应下载到 RAM（这需要一些时间），
 然后开始执行。

调试故障排除提示：

* 如果第一次启动调试会话时，
 没有显示正确的源码行，或汇编代码行，
 那么请尝试在调试器中进行单步操作。有时候，这会导致刷新，然后
 正确代码将显示。
* 留意 OpenOCD 运行的控制台窗口。如果它
 开始显示 "invalid memory" （无效内存）错误，则可能需要重置
 并重新启动 OpenOCD。
* 如果您是通过下载镜像到 RAM 来开发，
 并且您想让调试器在进入 main 时停止，
 则请在上面说明的第 8 步的 "c"（继续）命令前
 加上 "b main"（在 main 上断点）命令。
* 如果您是通过将新 RTOS 镜像复制到 SD 卡来开发，
 则请重新启动 Galileo，并且如果您希望调试器在进入 main 时停止，
 请在 main.c 原文件顶部将 #define mainWAIT_FOR_DEBUG_CONNECTION
 设置为 1。这将导致应用程序在 main() 的顶部出现一个循环，
 使您有机会在应用程序开始正常执行之前
 连接调试器。一旦调试器被连接，
 它可以用来将 ulExitResetSpinLoop 的值改为任何非零值，
 这样就可以退出循环。也可以通过
 按下控制台中的一个键来退出循环。

---

### RTOS 配置和使用详情

### FreeRTOS Intel IA32 运行时模型

FreeRTOS IA32 (x86) 移植使用平面 32 位内存空间， [当前]
以完整权限运行所有任务，并且不使用 MMU。

### FreeRTOS IA32 移植特定配置Intel

此演示的特定配置项目包含在 FreeRTOS/Demo/IA32_flat_GCC_Galileo_Gen_2/FreeRTOSConfig.h 中。
您可以编辑此文件中定义的常量，使其适合您的应用程序。

需要以下 Intel IA32 目标特定常量
（除了标准 [FreeRTOS 配置常量](/Documentation/02-Kernel/03-Supported-devices/02-Customization)之外）：

* **configISR_STACK_SIZE**

 FreeRTOS 会在进入中断时将在用堆栈切换为专用中断/系统堆栈。
 configISR_STACK_SIZE 定义了
 可以存储在系统堆栈上的 32 位数值的数量，而且
 必须大到足以容纳一个潜在的嵌套中断堆栈帧。

 使用单独的系统堆栈意味着分配给任务的堆栈都可以更小，
 因为它们不需要包括嵌套的中断堆栈帧的空间
 。

改变这个参数就必须进行彻底的清理和重建，
 以确保编译文件也被重建。
* **configSUPPORT_FPU**

 如果 configSUPPORT_FPU 设置为 1，则任务可以选择
 浮点上下文（浮点寄存器将保存为
 任务上下文的一部分）。

 任务未使用 FPU 上下文创建，并且在它们调用
 vPortTaskUsesFPU() 之前，它们不可使用任何 FPU 指令。

```c

void vPortTaskUsesFPU( void );

vPortTaskUsesFPU() function prototype

```

 如果 configSUPPORT_FPU 设置为 0，
 那么决不能使用浮点指令。

更改此参数必须进行彻底的清理和重建，
 以确保装配文件也被重建。
* **configUSE_COMMON_INTERRUPT_ENTRY_POINT**

 如果 configUSE_COMMON_INTRUPT_ENTRY_POINT 设置为 0，
 则所有中断服务程序都需要一个简短的汇编代码入口点。
 汇编代码将中断处理程序封装在 FreeRTOS
 portFREERTOS_INTERRUPT_ENTRY 和 portFREERTOS_INTERRUPT_EXIT 宏中，
 它们分别处理中断进入和退出。示例请参阅
 [中断服务程序](#中断服务程序)部分。

 如果 configUSE_COMMON_INTRUPT_ENTRY_POINT 设置为 1，则中断
 服务程序也可以写成标准 C 函数，
 在这种情况下，中断的进入和退出由
 FreeRTOS 端口层的通用代码处理。示例请参阅[中断服务程序](#中断服务程序)部分
 。

 编写一个提供自己的汇编文件包装器的中断处理程序
 比使用普通的中断入口点稍微复杂一些，
 但中断入口会更快，而且总是确定性的。

* **configMAX_API_CALL_INTERRUPT_PRIORITY**

 FreeRTOS Quark 移植实现了完整的中断嵌套模型。

 被分配的优先级等于或低于
 configMAX_API_CALL_INTERRUPT_PRIORITY 的中断可以调用中断安全的 API 函数，
 并且会嵌套。

 被分配的优先级高于
 configMAX_API_CALL_INTERRUPT_PRIORITY 的中断无法调用任何 FreeRTOS API 函数，
 将嵌套，并且不会被 FreeRTOS 的关键部分掩盖（尽管所有
 中断在进入中断时会被硬件本身短暂掩盖）。

 可以从中断中调用的 FreeRTOS 函数以 "FromISR" 结尾。
 FreeRTOS 维持一个独立的中断安全 API，
 以便更短、更快地进入中断，
 并简化、缩小所有 API 函数。

 用户可定义的中断优先级范围从 2 （最低）到 15
 （最高）。

### 中断服务程序

可以用如下所示的两种方式来编写中断服务程序 (ISR)：
1. 作为标准 C 函数

 此方法只能在 configUSE_COMMON_INTRUPT_ENTRY_POINT 设置为
 1 时使用。中断处理程序必须通过
 xPortRegisterCInterruptHandler() 函数来安装。

```c

/*

 * pxHandler: Pointer to the function that implements the ISR.

 * ulVectorNumber: The interrupt vector number to which the ISR will be

 * assigned. Vector numbers can be between 34 (in the

 * lowest priority group) and 255 (in the highest priority

 * group).

 */

BaseType_t xPortRegisterCInterruptHandler( ISR_Handler_t pxHandler,

                                           uint32_t ulVectorNumber );

The xPortRegisterCInterruptHandler() function prototype

```

 这是两种方法中最简单的方法，但需要稍微长一点
 中断输入时间。在调用 ISR （C 函数）
 之前启用中断。

 下面的示例是
 RTOS 演示项目中所使用中断的精简版。

```c

/* The function that implements the ISR is a standard C function. */

static void vHPETIRQHandler0( void )

{

    /* Perform ISR processing here. */

    /* Clear the interrupt in the IP API. It is not necessary to

 clear the interrupt in the local API - that is done by FreeRTOS. */

    hpetIO_APIC_EOI = hpetHPET_TIMER0_ISR_VECTOR;

}

/*-----------------------------------------------------------*/

/* The C function is then installed as the handler for vector 100 using the

following code. */

xPortRegisterCInterruptHandler( vHPETIRQHandler0, 100 );

Implementing an ISR as a standard C function

```
2. 作为从汇编代码入口点调用的标准 C 函数

 汇编代码将中断处理程序封装在 FreeRTOS
 提供的 portFREERTOS_INTERRUPT_ENTRY 和 portFREERTOS_INTERRUPT_EXIT 宏中。必须使用
 xPortInstallInterruptHandler() 函数
 来安装中断处理程序。

```c

/*

 * pxHandler: Pointer to the assembly code stub that wraps the ISR.

 * ulVectorNumber: The interrupt vector number to which the ISR will be

 * assigned. Vector numbers can be between 34 (in the

 * lowest priority group) and 255 (in the highest priority

 * group).

 */

BaseType_t xPortInstallInterruptHandler( ISR_Handler_t pxHandler,

                                         uint32_t ulVectorNumber );

The xPortInstallInterruptHandler() function prototype

```

 总是可以使用这种方法。它比
 方法 1 稍微复杂一点，但可以因为更快和确定的中断进入时间而受益。
 如果需要，应用程序编写者可以
 在调用 ISR 的 C 部分之前重新启用中断。

 下面的示例是 RTOS
 演示项目中所使用中断的精简版。

```c

/* The function that implements the C portion of the ISR. This is the

function called from the assembly code wrapper. */

void vHPETIRQHandler1( void )

{

    /* Perform ISR processing here. */

    /* Clear the interrupt in the IP API. It is not necessary to clear the

 interrupt in the local API - that is done by FreeRTOS. */

    hpetIO_APIC_EOI = hpetHPET_TIMER1_ISR_VECTOR;

}

/*-----------------------------------------------------------*/

/* The assembly code wrapper that calls the C function shown immediately

above. **The wrapper must be implemented in an assembly file, not a C file.**

The interrupt entry point assembly code makes use of the

portFREERTOS_INTERRUPT_ENTRY and portFREERTOS_INTERRUPT_EXIT macros,

so ISR_Support.h must be included. ISR_Support.h is located in the

FreeRTOS/source/portable/GCC/IA32_flat directory. */

#include "ISR_Support.h"

.align 4

.func vApplicationHPETTimer1Wrapper

.extern vHPETIRQHandler1

vApplicationHPETTimer1Wrapper:

    /* FreeRTOS macro that handles interrupt entry. Must be called

 first. */

    portFREERTOS_INTERRUPT_ENTRY

    /* It is safe to enable interrupts here, if desired. */

    sti

    /* The rest of the ISR is implemented in C. Call the C function

 now. */

    call vHPETIRQHandler1

    /* FreeRTOS macro that handles interrupt exit. Must be called

 last. */

    portFREERTOS_INTERRUPT_EXIT

.endfunc

/*-----------------------------------------------------------*/

/* Finally, the assembly code wrapper is then installed as the handler

for vector 100 using the following code. This code must be in a C

file. */

extern void vApplicationHPETTimer1Wrapper( void );

xPortInstallInterruptHandler( vApplicationHPETTimer1Wrapper, 100 );

The C function called from the assembly code wrapper

```

如果一个 ISR 导致一个和当前执行的任务具有相同或更高优先级的 RTOS
任务离开阻塞状态（请参阅 API 文档中对 pxHigherPriorityTaskWoken 参数的描述，
如
[xSemaphoreGiveFromISR()](/Documentation/02-Kernel/04-API-references/10-Semaphore-and-Mutexes/17-xSemaphoreGiveFromISR)），
那么 ISR 必须在 ISR 退出前请求进行上下文切换，
如果它希望未阻塞的任务立即执行。该操作完成后，
中断将中断一个 RTOS 任务，但会返回到另一个
RTOS 任务。

宏 portYIELD_FROM_ISR()（或 portEND_SWITCHING_ISR()）用于
请求从 ISR 中进行上下文切换。
请参阅以下源代码片段示例。示例中的 ISR
使用一个任务通知来与一个任务同步（未显示），并调用 portYIELD_FROM_ISR()
以确保中断直接返回到无阻塞任务中。

如果知道该中断不需要立即处理，
应用程序编写者可以选择不调用 portYIELD_FROM_ISR() -
例如，如果中断是一个正在到达的字符，
但在正在接收的信息完成并准备处理之前需要更多的字符时。

```c

void Dummy_IRQHandler( void )

{

long lHigherPriorityTaskWoken = pdFALSE;

    /* Clear the interrupt if necessary. */

    Dummy_ClearITPendingBit();

    /* This interrupt does nothing more than demonstrate how to synchronise a

 task with an interrupt. A task notification is used for this purpose.

 Note lHigherPriorityTaskWoken is initialised to pdFALSE. */

    [vTaskNotifyGiveFromISR](/Documentation/02-Kernel/04-API-references/05-Direct-to-task-notifications/02-vTaskNotifyGiveFromISR)( xTaskHandle, &lHigherPriorityTaskWoken );

    /* If the notified task was blocked waiting for the notification, and the

 unblocked task has a priority higher than or equal to the currently Running

 task (the task that this interrupt interrupted), then

 lHigherPriorityTaskWoken will have been set to pdTRUE internally within

 vTaskNotifyGiveFromISR(). Passing pdTRUE into the portYIELD_FROM_ISR() macro

 will result in a context switch being pended to ensure this interrupt returns

 directly to the unblocked, higher priority, task. Passing pdFALSE into

 portYIELD_FROM_ISR() has no effect. */

    portYIELD_FROM_ISR( lHigherPriorityTaskWoken );

}

An example interrupt handler

```

只有以 "FromISR" 结尾的 FreeRTOS API 函数可以从
从中断服务程序中调用，并且中断的优先级必须
小于或等于 configMAX_API_CALL_INTERRUPT_PRIORITY 配置常量设置的
优先级，才能调用。

### FreeRTOS 使用的资源

FreeRTOS 使用本地 APIC 定时器以及中断向量 0x20 和 0x21。此外，
演示项目使用 UART、GPIO、Legacy GPIO、I2C 和 HPE 定时器。

### 内存分配

Intel IA32 演示应用程序项目中包含 Source/Portable/MemMang/heap_4.c，
以提供 RTOS 内核所需的内存分配。
请参阅 API 文档的[内存管理](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)部分，
以获取完整信息。

### 其他事项

请注意，vPortEndScheduler() 尚未实现。