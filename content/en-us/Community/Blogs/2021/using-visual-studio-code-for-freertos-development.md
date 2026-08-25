---
title: Using Visual Studio Code for FreeRTOS development
created: 2021-01-06
feature: blog
categories:
  - Long term support
authors: 
  - marc-goodner
relatedLinks:
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
---

by [Marc Goodner](../author/marc-goodner) on 06 Jan 2021

Visual Studio Code has become a very popular code editor. You may be using it for development tasks 
already, but perhaps not yet for embedded development work. Or perhaps you are using it for embedded 
development work as you prefer the editing environment over your existing embedded development tools, 
but you haven’t been able to determine how to configure it for building and debugging your projects. 
This post will show you how you can setup VS Code to be an effective development environment for a 
FreeRTOS project. It will cover some key extensions you should install, then cover a couple of options 
on how to get started, and close with some other options you might want to explore on your own.

If you are new to VS Code, you can find an overview of its general capabilities and downloads for your 
operating system on the [VS Code site](https://code.visualstudio.com/). VS Code is a lightweight editor 
that you tailor for your own needs through the adding extensions for additional language support or 
other capabilities. It supports debugging and has integration with Git for source control. VS Code works 
with your code as it is, there isn’t a project file format. Just open the folder on your machine that 
has your source code in it, File > Open Folder (Ctrl+K, Ctrl+O). VS Code will suggest extensions relevant 
to the code in the folder you have opened if they aren’t installed already. VS Code also has a lot of 
advanced editing capabilities such as multiple cursors. To learn more about these core capabilities from 
the Help menu open the Interactive Playground which will guide you through these features.


## Extensions and basic setup

As FreeRTOS is written in C you will want to install 
the [C++ extension for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools). 
If your FreeRTOS project uses CMake you should also install 
the [CMake Tools extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cmake-tools). 
If you want to deploy and debug to your target device from VS Code 
the [Cortex-Debug](https://marketplace.visualstudio.com/items?itemName=marus25.cortex-debug) extension 
is a good choice. These are the extensions I’ll show you how to configure for a FreeRTOS project.

You will also need to get your machine setup for embedded development if it isn’t already. This generally 
means installing a cross compiler and the appropriate flash/debug tools for your target device. This should 
be covered by the getting started guidance for your target device.


## Getting a FreeRTOS project

FreeRTOS provides a [getting started guide](/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/) with examples for many boards, 
and many different Integrated Development Environments (IDEs), compiler, and build choices. The documentation 
here is good, but you still might face the problem not finding something that matches the device you are 
using. If you do find one that works, focus on the GCC ones that use makefiles for trying with VS Code. 
Adapting a project intended for another IDE will be difficult as it likely uses a proprietary project 
file for the IDE.

An alternative to starting here is to start with your silicon vendor, many of them provide configuration 
tools that can generate a FreeRTOS project configured for their boards that is a great starting point. 
To use a generated project with VS Code choosing GCC as your target compiler usually provides an option 
for generating either a make or CMake based project that can be used easily in VS 
Code. [Shawn Hymel](https://www.digikey.com/en/maker/videos/shawn-hymel/getting-started-with-stm32-and-nucleo-part-3-how-to-run-multiple-threads-with-cmsis-rtos-interface) 
has a great overview of getting started with FreeRTOS with ST’s tools. In his demonstration he shows the 
STM32CubeIDE, but there is a standalone configuration tool 
called [STM32CubeMX](https://www.st.com/en/development-tools/stm32cubemx.html) that can generate the project 
as he shows but without direct IDE integration. This tool works the same way as what he demonstrates. 
The only thing you need to do differently is on the Project Manager tab select Makefile as the Toolchain / IDE 
option then select Generate Code.

![](/media/2020/image1-300x199.png)

NXP’s MCUXpresso Config Tools and Espressif’s IDF tool also can generate CMake based FreeRTOS projects for 
their devices. Another FreeRTOS getting started approach is to use the FreeRTOS AWS project that has demos 
for many boards.


## Using makefiles

Once you have your FreeRTOS project generated, open the root folder of the project in VS Code. From within 
VS Code you can open you folder via File > Open Folder (Ctrl+K, Ctrl+O), or via the command line navigate 
to the root of your project and enter:

```c
code .
```

![](/media/2020/image2-300x237.png)

The C++ extension enables IntelliSense for C and C++ files. IntelliSense does more than simple syntax 
highlighting as it provides smart code completions based on variable types, function definitions, etc. 
To configure IntelliSense for the C++ extension we need to let it know where our headers are, what the 
compile options are, etc. There isn’t any automatic processing of this information for makefiles but it 
is relatively easy to add. Open the .vscode/c\_cpp\_properties.json file. The first thing you will want 
to do is update the intelliSenseMode variable to be gcc-arm and provide your cross compiler in the 
compilerPath variable. Now open your makefile and look for the include list. Copy this into the includePath 
array in the c\_cpp\_properties.json file. Prefix each folder location with `${workspaceFolder}` to tell 
it to use the path relative to your project folder. A trick here is to use VS Code’s multiline cursor (go 
to Help, Interactive Playground to learn about this feature). You can also add defines to the defines array 
and compiler flags to the compilerArgs array to improve results further.

Below is an example c\_cpp\_properties.json file for a basic FreeRTOS project generated by STM32CubeMX.

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

To build your application, assuming all your tools are available on your path, go to the VS Code terminal 
window and run make. If the terminal is not visible it can be opened through the menu View &gt; Terminal (Ctrl+).

![](/media/2020/image3.png)

If there are compilation errors, they will be displayed in the Problems output window and support navigation 
directly to the line of code that caused the error.


## Using CMake

If you have a FreeRTOS project that uses CMake there is less to configure as the CMake Tools extension 
queries the CMake cache for the information we had to manually configure above. However, the extension 
will try to configure your project using compilers it finds on your system as a “kit”. If the extension 
prompts you for a kit you will want to choose “unspecified” so that you can configure some additional 
options that impact embedded projects.

One of the issues you will run into with CMake and embedded is it will try to compile a simple C program 
to verify you have a working C compiler. This won’t work with a cross compiler as the compiled program 
is for a different system. You can pass an option to tell CMake to not try that. Open .vscode/settings.json 
and add cmake.configureSettings if it is not present. Within that structure add the name value pair 
CMAKE\_C\_COMPILER\_WORKS TRUE to tell CMake this check is not necessary. You can also pass additional 
parameters to CMake via this structure e.g., any that are prefixed with -D in build instructions you see.

Below is an example settings.json for compiling the demo FreeRTOS AWS project. Note the options for 
compiler, vendor, and board are all particular to which demo you are running and are covered as part 
of the command line for building the project using CMake. Here they have been mapped into the 
cmake.configureSettings array so we can build the project from within VS Code.

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

After updating these settings, you can right click the CMakeLists.txt file or use the command pallet 
with F1 and choose CMake Delete cache and reconfigure. This will remove any artifacts from an unsuccessful 
cache generation when first opening the folder before we had the correct flags passed to CMake. Now 
you can build the project and IntelliSense should be working throughout.

If there are compilation errors, they will be displayed in the Problems output window and support navigation 
directly to the line of code that caused the error.


## Debugging

The [Cortex-Debug](https://marketplace.visualstudio.com/items?itemName=marus25.cortex-debug) extension 
is a good way to get started with deploying and debugging your FreeRTOS app on a device. This extension 
works with a few different hardware debuggers and corresponding software. You need to configure your 
environment for use with the probe you have, then configure the extension to use it. The best place 
to get started for your specific configuration is [the wiki for the extension](https://github.com/Marus/cortex-debug/wiki).

![](/media/2020/image4.png)

To get started change to the Debug perspective in VS Code and select create a launch.json file. This 
will prompt a list of options in the command pallet, there select Cortex Debug. This will generate a 
base launch.json file that you can configure for your hardware probe and target device.

The below example launch.json is configured for using OpenOCD with an STM32 board. Here the things that 
had to be configured were pointing to the executable in my build output and the config files for the 
debug hardware and the target. You will need to update these settings for your own environment. 
Cortex-Debug supports other probes for which the configuration will be different, see the wiki for more 
information.

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

You also need to update the settings.json to tell the Cortex-Debug extension where your cross compiler 
tools are so it can find the right gdb to use.

```json
{
     "cortex-debug.armToolchainPath": "/opt/arm-none-eabi/gcc-arm-none-eabi-9-2020-q2-update/bin"
}
```


## Other extensions

VS Code has many extensions and will often prompt you when you open files for the first time that there 
are registered extensions for. Within the context of FreeRTOS development you may come across assembler 
in .S files and linker scripts in .ld files, 
the [x86 and x86\_64 Assembly](https://marketplace.visualstudio.com/items?itemName=13xforever.language-x86-64-assembly) 
and [LinkerScript](https://marketplace.visualstudio.com/items?itemName=ZixuanWang.linkerscript) extensions 
can provide syntax highlighting to each of those respective file types.


## Getting Help

Most VS Code extensions have an overview page that includes a link to their repository where you can usually 
find an issues list. These overview pages are worth referring to for links to documentation, FAQs, known 
issues, and what features they contribute to VS Code.

![](/media/2020/image5.png)


## Conclusion

VS Code can be used with your code as it is without importing to a new project format, has many advanced 
editing capabilities, and includes git integration. You may already be using it for other types of 
development tasks or tried it for your embedded development but weren’t able to determine how to completely 
configure it. VS Code can be an effective environment for your embedded development with FreeRTOS. The 
key is to leverage the right extensions for your needs and learn how to configure them for your environment. 
Once setup it is easy to use CMake or make based FreeRTOS projects. Hopefully, this post has shown how 
you can try it with your own FreeRTOS projects.


## About the author

![](https://secure.gravatar.com/avatar/61ff7a643fd27ceb93f5fbd91be5c721?s=200&d=mm&r=g)   
Marc Goodner is a Program Manager on the [[C++ team at Microsoft]](https://devblogs.microsoft.com/cppblog/) 
working on improving embedded support in Visual Studio and Visual Studio Code.   
[View articles by this author](../author/marc-goodner) 

FreeRTOS forums: Get industry-leading support from experts and collaborate with peers around the 
globe. [View Forums](https://forums.freertos.org/)
