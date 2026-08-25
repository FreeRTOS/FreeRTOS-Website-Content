---
title: FreeRTOS 和 Reliance Edge 演示
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

**结合使用故障安全文件系统与 FreeRTOS Windows 移植**


[![Tuxera 徽标](/media/2021/tuxera_logo.png)](https://www.tuxera.com/)
[![故障安全嵌入式文件系统](/media/2021/Reliance_Edge_logo.png)](https://www.tuxera.com/products/reliance-edge/)
[下载 Reliance Edge 开发者指南](https://www.tuxera.com/resources/reliance-edge-developers-guide/)
[立即评估！](Fail_Safe_Embedded_File_System_demo)
[许可证信息](safety_critical_embedded_file_system_license)
[观看视频](https://www.youtube.com/watch?v=KITEPryc1jI)


<blockquote>
    <span class="content">
        “我们的产品曾遍历深海之底、空间深处和
        厂房地板，最后轻轻落到您的口袋中。”
    </span>
    <span class="attribution">Ken Whitaker, Tuxera</span>
</blockquote>

<blockquote>
    <span class="content">
        “Tuxera 的 Reliance 故障保护文件系统系列
        已为数亿台设备提供了经严格验证的可靠性。”
    </span>
    <span class="attribution">Kerri McConnell, Tuxera</span>
</blockquote>

<blockquote>
    <span class="content">
        “Reliance Edge 的设计目标和实现
        意味着它并不只是普通的文件系统。Reliance Edge 将
        成为我们用户的宝贵资源，因此我们很乐意
        将其收录为官方 FreeRTOS-Plus 组件。”
    </span>
    <span class="attribution">Richard Barry, Amazon Web Services Inc.</span>
</blockquote>


本页介绍了一个在 Windows 环境中运行 FreeRTOS 和 Datalight 的
Reliance Edge 故障安全文件系统的项目。

FreeRTOS Windows 移植提供了一个方便且非嵌入式
目标特定的评估平台。它允许 FreeRTOS 和一些 FreeRTOS-Plus 组件
使用功能丰富且免费的
开发工具在标准 Windows 计算机上执行。然而，与在真正的嵌入式硬件上执行 FreeRTOS 不同，
Windows 移植
并未展示真正的实时行为。

## 源代码和项目文件

此页面上描述的项目位于
 [FreeRTOS .zip 主文件下载的以下文件夹中](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)：
FreeRTOS-Plus/Demo/FreeRTOS_Plus_Reliance_Edge_and_CLI_Windows_Simulator


## 目标硬件

该项目创建 RAM 磁盘，
——使用[FreeRTOS Windows 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)创建。
Windows 移植提供了一个方便的评估平台，但
不显示实时操作。模拟时间可能比实际时间慢。


## 编译器/工具链

已预配置此项目，以使用
[Microsoft Visual C++ (MSVC) 的免费 Express 版本](http://www.microsoft.com/visualstudio/eng/products/visual-studio-express-products)
进行构建。使用的是 MSVC Express Edition 2010。


## 功能

演示：

1. 创建并格式化 RAM 磁盘。

2. 创建然后在 RAM 磁盘的根目录中读取一组示例文件。

3. 创建子目录。

4. 创建然后从创建的子目录读取一组示例文件。

5. 创建一个命令控制台（使用 [FreeRTOS-Plus-CLI](../FreeRTOS_Plus_CLI/FreeRTOS_Plus_Command_Line_Interface)）
   来实现下述命令：

   |  命令和参数  |  描述  |
   | --- | --- |
   | *dir \<filename\>* |  列出命名目录中的文件  |
   | *type \<filename\>* |  将文件内容打印到终端  |
   | *append \<filename\>*  |  将数据附加到文件(如果文件不存在，则创建文件)  |
   | *del \<filename\>* |  删除文件或目录  |
   | *copy \<source file\> \<dest file\>* |  将 \<source file\> 复制到 \<dest file\>  |
   | *create \<filename\>* |  创建空文件  |
   | *mkdir \<filename\>* |  创建空目录  |
   | *rename \<source file\> \<dest file\>* |  将 \<source file\> 重命名为 \<dest file\>  |
   | *link \<source file\> \<dest file\>* |  创建指向 \<source file\> 的硬链接 \<dest file\>  |
   | *stat \<filename\>* |  显示文件信息  |
   | *statfs* |  显示文件系统信息  |
   | *format* |  重新格式化文件系统卷。将删除所有文件！  |
   | *transact* |  提交 Reliance Edge 事务点  |
   | *transmaskget* |  检索 Reliance Edge 自动事务掩码  |
   | *transmaskset \<hex mask\>* |  设置 Reliance Edge 自动事务掩码  |
   | *abort* |  回滚不属于上一事务点的所有更改  |
   | *test-fs* |  执行文件系统测试。将删除所有文件！  |


## 命令控制台输入和输出

从 UDP 终端访问命令控制台。
请参阅下面的[使用说明](#使用说明)部分。


## 构建说明

1. 主 [FreeRTOS .zip 文件下载](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/)中提供了演示应用程序。

2. 从 Visual Studio IDE 中打开 Visual Studio 解决方案文件 FreeRTOS_Plus_Reliance_Edge_with_CLI.sln 
   。该解决方案文件位于
   "FreeRTOS-Plus/Demo/FreeRTOS_Plus_Reliance_Edge_and_CLI_Windows_Simulator"
   目录中。

3. 在 IDE 的 Build 菜单中选择 "Build Solution"（或按 F7 ）
   以构建应用程序。


## 调试说明

在 Visual Studio 中，按 F10 开始调试会话，并在进入 main() 时中断。

可使用同一台主机构建应用程序、调试应用程序
以及运行应用程序（因为使用了 FreeRTOS Win32 移植）。
无特殊调试说明。


## 使用说明

1. 演示应用程序在
   RAM 磁盘上创建一组文件和目录，在运行过程中向 Windows 控制台输出信息。

   ![创建故障安全文件系统文件和目录时生成的输出](/media/2018/safety_critical_file_system_console_output.jpg)
   *故障安全嵌入式文件系统演示应用程序启动时在 Windows 控制台中生成的输出*

2. 使用本地 UDP 连接连接到 FreeRTOS-Plus-CLI
   命令行接口。使用 Windows TCP/IP 堆栈
   而不是 FreeRTOS-Plus-TCP ，以确保
   演示的重点仍然是文件系统。使用
   FreeRTOS Windows 移植和 FreeRTOS-Plus-TCP 创建
   命令控制台的演示应用程序[可在本网站的 FreeRTOS-Plus-TCP 部分中找到](/Documentation/03-Libraries/02-FreeRTOS-plus/02-FreeRTOS-plus-TCP/01-FreeRTOS-Plus-TCP)。

   免费哑终端程序，适合
   使用 UDP 连接到命令行接口，包括 [YAT](https://sourceforge.net/projects/y-a-terminal/)
   和 [Hercules](http://www.hw-group.com/products/hercules/index_en.html)。

   可使用标准的本地主机 IP 地址 (127.0.0.1)，因为
   （模拟）演示应用程序和 UDP 终端都在
   同一台计算机上执行。FreeRTOS-Plus-CLI 侦听字符
   到达 UDP 端口 5001 的字符并将其输出发送到 UDP 端口 5002。
   所需的终端配置如下所示。

   ![安全关键文件系统演示所需的设置](/media/2018/yat_settings_to_connect_to_the_safety_critical_file_system_demo.jpg)
   *将 YAT 终端配置为与 FreeRTOS-Plus-CLI 命令行接口进行通信*

3. 键入 "help" 查看已注册命令的列表。

   ![查看安全关键文件系统相关 RTOS 命令](/media/2018/view_safety_critical_file_system_commands.png)
   *在 UDP 终端键入 "help" 查看已注册命令的列表。*

4. 尝试使用文件系统命令！示例会话如下所示。

   ![运行安全关键文件系统 RTOS 命令](/media/2018/running_safety_critical_file_system_commands_in_yat.png)
   *在 YAT 终端中运行安全关键文件系统命令*
