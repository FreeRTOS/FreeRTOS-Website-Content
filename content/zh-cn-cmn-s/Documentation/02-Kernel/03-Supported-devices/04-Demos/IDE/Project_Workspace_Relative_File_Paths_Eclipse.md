---
title: "使用 Eclipse 构建 FreeRTOS 使用相对路径引用  RTOS 源代码"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

 [[RTOS 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)]

### 引言

[FreeRTOS 下载内容](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)包含各种预配置演示应用程序
项目，但出于维护和完整性考虑，
它只包含一份 RTOS 源代码。理想情况下，每个演示项目
都可引用并构建单个 RTOS 源代码副本，而这正是
大多数预配置 [RTOS 演示项目](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos)所做的事情。但从过去的经验来看，
要在 Eclipse 中做到这一点并不容易（尽管并非不可能），
基于旧版 EclipseRTOS 演示项目使用批处理文件将所有必要的源文件
从它们在 [FreeRTOS 目录树](/Documentation/02-Kernel/05-Coding-guidelines/01-Source-code-organization)中的默认位置复制到
Eclipse 项目目录中。

最新版 Eclipse 在某种程度上通过定义变量缓解了
这些问题，这些变量可在包含
Eclipse .project 文件的目录中向上、向下解析目录树
。我们已对使用基于 Eclipse 的 IDE 构建的新版 RTOS 演示应用程序进行预配置，
以使用此改良方法（尽管仍然比较笨拙），
摒弃之前使用的批处理文件方法。此页详细描述了
这些项目的创建过程。

**注意：** 本页内容仅供参考。RTOS 演示项目
（包含在 FreeRTOS 官方下载内容中）已预配置过，
它提供所用演示项目的特定[构建说明](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/03-Build-your-first-project)，
且其使用的 Eclipse 版本也是最新版，因此只要遵循相关说明，
就可直接构建。

### 创建在项目目录外构建文件的 Eclipse 项目

下文通过举例说明的方式展示如何引用 FreeRTOS
源文件，它驻留在 /FreeRTOS/Source 目录中
（从 /FreeRTOS/Demo/[project_name] 目录中的 Eclipse 项目文件引用）。

1. **打开项目属性窗口** 

 右键单击 Eclipse Project Explorer （Eclipse 项目资源管理器）窗口中的项目名称，
 然后从弹出菜单中选择 “Properties” （属性）。“属性”窗口
 随即被打开。
2. **定义新的 Eclipse 变量** 

 在属性窗口中，选择 “Resources->Linked Resources” （资源- >链接资源）以查看
 路径变量。单击 “New” （新建）按钮以创建一个新变量，
 用于指向 FreeRTOS 源文件目录
 树。

![定义新的 Eclipse 变量，用于引用 RTOS 源文件](/media/2018/Define_a_New_Eclipse_Variable.jpg)

**定义新的 Eclipse 变量** 

 将新变量命名为 FREERTOS_ROOT，并使用预定义的 PROJECT_LOC
 变量输入解析到 /FreeRTOS/Source 目录的路径
 。

![使用相对路径将 Eclipse 变量设置为 RTOS 源目录](/media/2018/Extend_PROJECT_LOC_Variable.jpg)

**扩展 PROJECT_LOC 变量，使其解析至 /FreeRTOS/Source 目录** 

 关闭“属性”窗口。
3. **创建一个虚拟文件夹** 

 Eclipse 托管使得项目可以构建所有
 显示在项目资源管理器窗口中的源文件。RTOS 源文件
 不在 Eclipse 项目目录中，因此不会自动显示在
 项目资源管理窗口上，必须使用虚拟
 文件夹手动添加它。

 右键单击项目资源管理器中
 您希望存放 RTOS 源文件的文件夹名称。选择 “New -> Folder” （新建- >文件夹）。打开
 新文件夹窗口。

 在“新建文件夹”窗口中，输入 FreeRTOS 作为此文件夹名称，然后选择
 “Folder is not located in the file system (Virtual Folder)”（文件夹不在文件系统（虚拟文件夹）中）
 按钮。

![在 Eclipse Project Explorer（Eclipse 项目资源管理器）中创建虚拟文件夹](/media/2018/Create_A_Virtual_Folder.jpg)

**在 Eclipse Project Explorer（Eclipse 项目资源管理器）中创建虚拟文件夹**
4. **将 RTOS 源代码目录关联到虚拟文件夹** 

 右键单击新创建的虚拟文件夹，然后从弹出菜单中选择 “New -> Folder” （新建- >文件夹）
 再次打开新建文件夹窗口。

![在 Eclipse 中创建链接资源](/media/2018/Create_New_Folder_In_The_Eclipse_Project_Explorer.jpg)

**右键单击虚拟文件夹以查看弹出菜单** 

 在新文件夹窗口中，输入 Source 作为目录名称，
 然后选择  “Link to alternative location (Linked Folder)”（关联到备用位置（关联文件夹））
 按钮。输入新创建的 FREERTOS_ROOT 变量作为文件夹的位置。

![使用相对路径将文件添加到 Eclipse 项目](/media/2018/Link_To_Alternative_Location.jpg)

**使用相对路径将关联文件夹添加到 Eclipse 项目中**
5. **选择要构建的文件** 

 FreeRTOS/Source 目录现在
 可在 Eclipse 项目资源管理器中看到。该目录包含
 使用每个 RTOS 移植的源文件，因此下一步是使用 Eclipse 资源过滤器
 来确保只有构建 FreeRTOS 移植过程中实际用到的文件
 是可见的。

 右键单击可移植目录，再次查看弹出菜单，
 然后选择 “Properties”（属性）。跳出显示可移植目录属性的弹出窗口
 。

![查看 RTOS 源代码目录的属性](/media/2018/Select_RTOS_Source_Portable_Directory.jpg)

**查看 RTOS 源代码的可移植目录的属性** 

 在“属性”窗口中，选择  “Resources->Resource Filters” （资源- >资源过滤器）查看以
 此目录的资源过滤器。创建两个 “Include Only” 资源过滤器，
 以便只显示与文本 'MemMang' 和 '[compiler]' 相匹配的目录，
 其中 [compiler] 指用于构建源文件的编译器。例如，
 下文中的两张图片
 展示了使用
 Renesas 编译器构建项目时所要用到的设置。

![添加 Eclipse 资源过滤器以向下选择正在构建的 RTOS 源文件](/media/2018/Add_Eclipse_Resource_Filters.jpg)

**在目录上定义 'Include Only’ 资源过滤器** 

![Eclipse 项目资源过滤器](/media/2018/Resource_Filters_Defined.jpg)

**定义了
 两个过滤器之后的资源过滤器窗口。** 

 在本文写作时， MemMang 目录包含 4 个 .c 文件，
 每一个
 [都为堆内存管理提供一个选项（共有四个不同的选项）](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)。
 将资源过滤器添加至 MemMang 目录
 以确保四个 .c 文件中只有一个是可见的。

![确保只构建一个 RTOS 堆源文件](/media/2018/Only_Include_One_Heap_File.jpg)

**使用资源筛选器确保只构建一个 heap_x.c 文件，在所述的情况中为 
 heap_4。** 

 [compiler] 目录将包含
 FreeRTOS 使用此编译器支持的每个架构的子目录。将资源过滤器添加至
 [compiler] 目录以确保只有实际所使用的架构目录
 是可见的。例如，
 如果 Renesas 编译器被
 用于构建以 RX600 系列微控制器为目标的项目，那么下图中创建的资源过滤器就是正确的。

![确保只显示 RTOS 正在构建的架构的源文件](/media/2018/Repeat_For_Any_Subdirectories.jpg)

**创建资源过滤器，确保 [compiler] 目录下
 只有一个子目录可见。**
6. **将关联目录添加至编译器的包含路径中** 

 可以通过常规方式将虚拟文件夹和关联文件夹添加至编译器的包含路径中
 。

![将 RTOS 的标头源文件添加到项目的包含路径](/media/2018/Linked_Folders_Can_Be_Added_In_Include_Path.jpg)

**将虚拟文件夹和链接文件夹中的目录添加到
 编译器的包含路径中。**

[Google](https://plus.google.com/106895663740671259833?  rel=author target=)
[简介](https://profiles.google.com/106895663740671259833)

