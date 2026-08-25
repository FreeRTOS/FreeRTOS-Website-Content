---
title: "在 Eclipse 中导入并构建演示项目"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

本页介绍了如何使用 Eclipse 导入和构建多个作为 Eclipse 项目提供的 FreeRTOS 演示应用程序
。[演示应用程序特定文档](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)页面提供了给定演示的额外信息，
包括项目在 FreeRTOS 目录结构中的位置。以下演示使用
Windows 环境下的基础 Eclipse Embedded CDT 版本。

**注意：**不同供应商提供的特定 Eclipse 发行版可能与下方截图中的基础 Eclipse
版本不同。

## 前提条件：

1. 安装 Eclipse 发行版

   要下载基础 Eclipse 版本 Eclipse Embedded CDT（C/C++ 开发工具），
   请点击[此处](https://projects.eclipse.org/projects/iot.embed-cdt/downloads)。

   **注意：**大多数供应商特定的基于 Eclipse 的 IDE 在发行版中包含工具链，并
   自动透明地为您设置路径。请查看对应的演示页面，该页面
   链接位于[演示应用程序特定文档](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)。如果供应商特定的 IDE 提供了工具链和构建工具，
   则可以跳过以下步骤。

2. 安装 GCC 工具链

   请参阅[演示应用程序特定文档](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)页面，
   了解演示所需的特定工具链。

3. 安装构建工具 (Windows)

   POSIX 平台通常在系统发行版中包含 `make`，或者可能需要您安装
   一些开发者包（例如，在 macOS 上需要安装 Xcode 命令行工具）。按照
   此[指南](https://gnu-mcu-eclipse.github.io/install/)中的“Windows 构建工具”一节，安装 Make 构建
   工具。

   **注意：**如果安装了其他环境，如 MinGW 或 Cygwin，并希望使用
   该环境提供的 Make 工具，请确保将 `make` 程序命名为 "`make.exe`"。同样，
   对于 MinGW，请将 "`mingw32-make.exe`" 重命名（或创建副本并重命名）为 "`make.exe`"。

4. 管理 PATH 环境变量

   基础版 Eclipse 依赖于设置环境变量 `PATH` 来访问工具链的二进制文件。
   `PATH` 可以通过以下方式设置：

   - 系统全局的 `PATH` 设置或用户的 `PATH` 设置。
   - Eclipse 工作区所有项目的通用设置。
   - 项目的构建配置。强烈建议您通过项目的构建配置来设置 `PATH`，以避免
     在计算机上使用多个工具链时发生冲突。要在 Eclipse 中设置项目的 `PATH` 变量，
     请执行以下步骤：

   1. 右击 "Project Explorer" 中的演示项目，然后选择 "Properties"。

      ![](/media/2020/Screen-Shot-2020-08-26-at-6.22.25-PM.png)
      打开 "Project Properties"

   2. 在弹出窗口的左侧，选择 "C/C++ build --> Environment"，然后点击右侧的 "Add..." 按钮，
      添加新变量。

      ![](/media/2020/Screen-Shot-2020-08-26-at-5.52.10-PM.png)
      Project Properties

   3. 输入 "PATH" 作为变量名称，将值设置为指向工具链和构建工具二进制文件夹的路径
      。

      ![](/media/2020/Screen-Shot-2020-08-26-at-5.53.03-PM.png)
      添加 PATH 变量

## 导入并构建演示项目：

**重要提示！**FreeRTOS Eclipse 项目使用源文件的相对路径，因此
如果您的目录结构与官方 FreeRTOS zip 文件版本中使用的目录结构不同，将无法构建。请确保将项目导入到 Eclipse 工作区时，
未勾选 'Copy projects into workspace'
复选框。

1. 启动 Eclipse，根据提示选择现有工作区，或创建新的工作区。

2. 在 Eclipse 的 "File" 菜单中选择 "Import..."，随即打开 "Import" 对话框。

3. 在 "Import" 对话框中，选择 "General -> Existing Project into Workspace"，随即打开 "Import Projects"
   对话框。

   ![](/media/2020/Screen-Shot-2020-08-19-at-10.06.25-AM.png)
   将现有项目导入工作区

4. 在 "Import Projects" 对话框中，导航到 `FreeRTOS/Demo/<YOUR_PROJECT>`，
   并选择此目录，确保未勾选 'Copy projects into workspace' 复选框。

   ![](/media/2020/Screen-Shot-2020-08-19-at-10.07.29-AM.png)
   在 "Import Projects" 对话框中选择目录和项目。

5. 在 "Import Projects" 对话框的 "Projects" 窗口中，选择 RTOSDemo 项目，然后点击 "Finish"。

6. 在 Eclipse 的 "Project" 菜单中选择 "Build all"。确保在项目构建过程中不会出现任何错误或警告。

