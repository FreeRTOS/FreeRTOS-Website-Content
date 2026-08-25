---
title: 将 Visual Studio Code 用于 FreeRTOS 开发
created: 2021-01-06 00:00:00.0 UTC
feature: blog
categories:
- 长期支持
authors:
- marc-goodner
relatedLinks:
- title: FreeRTOS 简介
  link: /Why-FreeRTOS/What-is-FreeRTOS/
---

本帖由 [Marc Goodner](../author/marc-goodner) 发表于 2021 年 1 月 6 日

Visual Studio Code 已成为非常流行的代码编辑器。您或许已将其用于开发任务， 
但可能尚未用于嵌入式开发工作中。亦或许您正在将其用于嵌入式 
开发工作，因为相较于现有的嵌入式开发工具，您更喜欢这种编辑环境， 
但却无法确定如何进行配置以构建和调试项目。 
本帖将介绍如何设置 VS Code， 
使其成为针对 FreeRTOS 项目的有效开发环境，其中会介绍一些应该安装的关键扩展，然后介绍一些入门选项， 
最后介绍一些您可能想要自行探索的其他选项。

如果您初次使用 VS Code ，要简要了解其常规功能以及适用于您所用操作系统的下载内容， 
请访问 [VS Code 网站](https://code.visualstudio.com/)。VS Code 是一款轻量级编辑器， 
您可以根据需求定制，通过添加扩展获得额外的语言支持或 
其他功能。它支持调试，可与 Git 集成以进行源代码控制。VS Code 可以直接使用 
您的代码，没有项目文件格式。只需依次点击“文件”(File) > “打开文件夹”(Open Folder)（Ctrl+K、Ctrl+O）， 
打开计算机上包含源代码的文件夹。VS Code 建议安装 
与所打开文件夹中的代码相关的扩展（如果尚未安装）。VS Code 还具有许多 
高级编辑功能，如多光标。要了解有关这些核心功能的详细信息， 
请在“帮助”(Help) 菜单中打开“互动练习场”(Interactive Playground)，它可引导您了解这些功能。


## 扩展与基本设置

由于 FreeRTOS 以 C 语言编写，您需要安装 
[VS Code 的 C++ 扩展](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools)。 
如果您的 FreeRTOS 项目使用 CMake，您还应安装 
[CMake Tools 扩展](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cmake-tools)。 
如果您想从 VS Code 直接部署和调试目标设备， 
[Cortex-Debug](https://marketplace.visualstudio.com/items?itemName=marus25.cortex-debug) 扩展 
是不错的选择。以上扩展可用于 FreeRTOS 项目，稍后我将演示具体配置方式。

此外，要进行嵌入式开发，您还需要设置计算机，即 
安装交叉编译器以及适用于目标设备的闪存/调试工具。相关内容 
将在目标设备的入门指南中介绍。


## 获取 FreeRTOS 项目

FreeRTOS 提供[入门指南](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/)，其中包含许多开发板 
以及不同集成开发环境 (IDE)、编译器和构建选项的示例。该文档 
很有用，但您可能仍然找不到与所用设备匹配的示例 
。如果您找到了有效匹配示例，建议关注那些使用 makefile 的 GCC 示例，以在 VS Code 中进行尝试。 
将原本用于其他 IDE 的项目转换为在 VS Code 中使用会很困难，因为项目很可能会使用该 IDE 的专有 
项目文件。

除了上述入门方式以外，另一种入门方式是咨询芯片供应商，许多芯片供应商会提供配置工具， 
可以生成针对其开发板配置的 FreeRTOS 项目。您可以利用这些工具快速入门。 
要在 VS Code 中使用生成的项目，请选择 GCC 作为目标编译器，这通常会提供一个选项， 
需要选择是生成基于 make 还是 CMake 的项目，生成的项目可以轻松在 VS Code 中使用 
。不妨参阅 [Shawn Hymel](https://www.digikey.com/en/maker/videos/shawn-hymel/getting-started-with-stm32-and-nucleo-part-3-how-to-run-multiple-threads-with-cmsis-rtos-interface) 
提供的概览，了解如何通过 ST 的工具使用 FreeRTOS。在演示中，他展示了 
STM32CubeIDE， 
其中一款名为 [STM32CubeMX](https://www.st.com/en/development-tools/stm32cubemx.html) 的独立配置工具可以像他展示的那样生成项目， 
但无需直接集成在 IDE 中。该工具的使用方式与演示中一样， 
唯一不同的是，需要在“项目管理器”(Project Manager) 选项卡中选择 Makefile 作为工具链/IDE 选项， 
然后选择“生成代码”(Generate Code)。

![](/media/2020/image1-300x199.png)

NXP 的 MCUXpresso 配置工具和 Espressif 的 IDF 工具也可以为其设备生成基于 CMake 的 FreeRTOS 项目 
。另一种 FreeRTOS 入门方法是使用 FreeRTOS AWS 项目，该项目 
针对许多开发板提供演示。


## 使用 makefile

生成 FreeRTOS 项目后，在 VS Code 中打开项目的根文件夹。在 
VS Code 中，您可以通过“文件”(File) > “打开文件夹”(Open Folder)（Ctrl+K、Ctrl+O）打开文件夹，也可以通过命令行导航到 
项目的根目录，然后输入：

```c
code .
```

![](/media/2020/image2-300x237.png)

C++ 扩展可用于为 C 和 C++ 文件启用 IntelliSense。IntelliSense 不仅提供简单的语法突出显示， 
还可以根据变量类型、函数定义等提供智能代码补全。 
要为 C++ 扩展配置 IntelliSense，需要告知其标头的位置 
以及编译选项等。对于 makefile，没有自动处理这些信息的方式， 
但手动添加相对容易。打开 .vscode/c_cpp_properties.json 文件。首先，需要 
将 intelliSenseMode 变量更新为 gcc-arm， 
并在 compilerPath 变量中提供交叉编译器。现在打开 makefile 并查找 include 列表。将该列表复制到 c_cpp_properties.json 文件的 
includePath 数组中。在每个文件夹位置前加上 `${workspaceFolder}` 前缀， 
告知 VS Code 使用路径（相对于您的项目文件夹）。 此处有一个技巧，即使用 VS Code 的多行光标功能。 
如需了解此功能，请依次点击“帮助”(Help) 和“互动练习场”(Interactive Playground)。您还可以在 defines 数组中添加定义， 
在 compilerArgs 数组中添加编译器标记，以进一步改进结果。

以下是由 STM32CubeMX 生成的基本 FreeRTOS 项目的示例 c_cpp_properties.json 文件。

```json
{
    "configurations": [
        {
            "name": "Linux",
            "includePath": [
                "${workspaceFolder}/**",
                "${workspaceFolder}/Core/Inc",
                "${workspaceFolder}/Drivers/STM32F7xx_HAL_Driver/Inc",
                "${workspaceFolder}/Drivers/STM32F7xx_HAL_Driver/Inc/Legacy",
                "${workspaceFolder}/Middlewares/Third_Party/FreeRTOS/Source/include",
                "${workspaceFolder}/Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS_V2",
                "${workspaceFolder}/Middlewares/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM7/r0p1",
                "${workspaceFolder}/Drivers/CMSIS/Device/ST/STM32F7xx/Include",
                "${workspaceFolder}/Drivers/CMSIS/Include"
            ],
            "defines": [
                "USE_HAL_DRIVER",
                "STM32F767xx"
            ],
            "compilerPath": "/opt/arm-none-eabi/gcc-arm-none-eabi-9-2020-q2-update/bin/arm-none-eabi-gcc",
            "compilerArgs": [
                "-mcpu=cortex-m7",
                "-mthumb",
                "-mfpu=fpv5-d16",
                "-mfloat-abi=hard"
            ],
            "cStandard": "gnu11",
            "cppStandard": "gnu++14",
            "intelliSenseMode": "gcc-arm"
        }
    ],
    "version": 4
}
```

假设路径上所有工具都可用，要构建应用程序，请转到 VS Code 终端 
窗口并运行 make。如果未看到终端，可以通过菜单的“视图”(View) &gt; “终端”(Terminal) 打开（快捷键为 Ctrl 加某个键）。

![](/media/2020/image3.png)

编译错误（如有）将显示在“问题”(Problems) 输出窗口中，且支持直接导航到 
引起错误的代码行。


## 使用 CMake

如果您的 FreeRTOS 项目使用 CMake，则需要配置的内容较少，这是因为 CMake Tools 扩展 
会查询 CMake 缓存中的信息，如前文所述，这些信息必须手动配置。但是，该扩展 
会尝试使用在系统上找到的编译器作为“套件”对项目进行配置。如果扩展 
提示您选择套件，请选择“未指定”(unspecified)，这样就可以配置一些 
可影响嵌入式项目的其他选项。

使用 CMake 进行嵌入式开发时，您可能会遇到一个问题：CMake 会尝试编译简单的 C 程序， 
以验证您的 C 编译器是否可以正常工作。这对于交叉编译器不起作用，因为交叉编译器编译的程序 
是针对其他系统的。您可以传递一个选项，告诉 CMake 不要尝试此操作。打开 .vscode/settings.json， 
然后添加 cmake.configureSettings（如果不存在）。在该结构中添加名称值对 
CMAKE_C_COMPILER_WORKS TRUE，告诉 CMake 此检查不必要。您还可以通过此结构 
向 CMake 传递其他参数，例如构建指令中以 -D 为前缀的参数。

以下是用于编译演示 FreeRTOS AWS 项目的 settings.json 示例。请注意， 
编译器、供应商和开发板选项都特定于您运行的演示，并且 
包含在使用 CMake 构建项目的命令行中。本例中，它们映射到 
cmake.configureSettings 数组，因此我们可以在 VS Code 中构建项目。

**Settings.json**

```json
{
    "cmake.configureOnOpen": true,
    "cmake.configureSettings": {
        "COMPILER": "xtensa-esp32",
        "CMAKE_C_COMPILER_WORKS": "TRUE",
        "VENDOR": "espressif",
        "BOARD": "esp32_wrover_kit"
    },
    "C_Cpp.default.configurationProvider": "ms-vscode.cmake-tools"
}
```

更新这些设置后，可以右键单击 CMakeLists.txt 文件，或按 F1 打开命令托盘， 
然后选择“CMake 删除缓存并重新配置”(CMake Delete Cache and Reconfigure)。此操作会删除 
在最初打开文件夹时因尚未将正确标记传递给 CMake 而缓存失败所生成的遗留文件。现在 
可以构建项目了，在整个过程中，IntelliSense 应该可以正常工作。

编译错误（如有）将显示在“问题”(Problems) 输出窗口中，且支持直接导航到 
引起错误的代码行。


## 调试

[Cortex-Debug](https://marketplace.visualstudio.com/items?itemName=marus25.cortex-debug) 扩展 
不失为开始在设备上部署和调试 FreeRTOS 应用程序的好方法。此扩展 
适用于一系列不同的硬件调试器和相应软件。您需要配置 
适用于探针的环境，配置扩展后即可使用。开始进行特定配置的最佳位置是 
[扩展的维基页面](https://github.com/Marus/cortex-debug/wiki)。

![](/media/2020/image4.png)

要开始使用，请切换到 VS Code 中的调试视角，然后选择创建 launch.json 文件。这 
会在命令托盘中提示一系列选项，请从中选择“Cortex Debug”。系统随即生成 
基础的 launch.json 文件，您可以为硬件探针和目标设备配置该文件。

以下示例 launch.json 文件配置为使用 OpenOCD 调试 STM32 开发板。此文件中 
需要配置的内容包括指向“我的构建输出”中的可执行文件以及 
调试硬件和目标设备的配置文件。您需要根据自己的环境更新这些设置。 
Cortex-Debug 支持其他探针，配置会有所不同。有关详细信息， 
请参阅相应的维基页面。

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Cortex Debug",
            "cwd": "${workspaceRoot}",
            "executable": "./build/nucleo-f767zi-freertos-blink.elf",
            "request": "launch",
            "type": "cortex-debug",
            "servertype": "openocd",
            "configFiles": [
                "/usr/share/openocd/scripts/interface/stlink-v2-1.cfg",
                "/usr/share/openocd/scripts/target/stm32f7x.cfg"
            ]
        }
    ]
}
```

您还需要更新 settings.json，向 Cortex-Debug 扩展告知交叉编译器工具所在的位置， 
这样它才能找到合适的 gdb 来使用。

```json
{
     "cortex-debug.armToolchainPath": "/opt/arm-none-eabi/gcc-arm-none-eabi-9-2020-q2-update/bin"
}
```


## 其他扩展

VS Code 有很多扩展，当您首次打开文件时，通常会提示您 
有可用的已注册扩展。在 FreeRTOS 开发的上下文中，您可能会 
在 .S 文件中遇到汇编器代码，在 .ld 文件中遇到链接器脚本， 
[x86 和 x86_64 汇编](https://marketplace.visualstudio.com/items?itemName=13xforever.language-x86-64-assembly) 
以及 [LinkerScript](https://marketplace.visualstudio.com/items?itemName=ZixuanWang.linkerscript) 扩展 
可为这些相应的文件类型提供语法突出显示。


## 获取帮助

大多数 VS Code 扩展都有相应的概览页面，其中会附上存储库链接，您可以在存储库中 
找到问题列表。这些概览页面值得参考，其中会附上相关链接，便于您快速查看文档、常见问题、已知 
问题及其为 VS Code 贡献的功能。

![](/media/2020/image5.png)


## 结语

VS Code 可以直接使用您现有的代码，无需导入为新的项目格式，具有许多高级编辑功能， 
并且包含 git 集成。您可能已经将其用于其他类型的开发任务， 
也可能尝试将其用于嵌入式开发，但无法确定如何对其进行完全 
配置。VS Code 可以成为您使用 FreeRTOS 进行嵌入式开发的有效环境。 
关键是利用适合您需求的扩展，并了解如何针对自己的环境进行配置。 
设置后，即可轻松使用基于 CMake 或 make 的 FreeRTOS 项目。希望您可以通过本帖 
了解如何在自己的 FreeRTOS 项目中尝试使用 VS Code。


## 作者简介

![](https://secure.gravatar.com/avatar/61ff7a643fd27ceb93f5fbd91be5c721?s=200&d=mm&r=g)   
Marc Goodner 是 [[Microsoft C++ 团队]](https://devblogs.microsoft.com/cppblog/) 的项目经理， 
致力于改进 Visual Studio 和 Visual Studio Code 中的嵌入式支持。  
[查看此作者的文章](../author/marc-goodner) 

FreeRTOS 论坛：获得行业领先的专家支持，并与全球同行 
合作。[查看论坛](https://forums.freertos.org/)

