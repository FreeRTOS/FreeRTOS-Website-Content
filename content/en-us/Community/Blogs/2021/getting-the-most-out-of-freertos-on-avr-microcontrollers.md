---
title: Getting the Most Out of FreeRTOS on AVR® Microcontrollers
created: 2021-02-11
feature: blog
categories:
  - Long term support
authors: 
  - jacoblassen
relatedLinks:
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
---

by [Jacob Lunn Lassen](../author/jacoblassen) on 11 Feb 2021

It was exciting to see two new [AVR](/Documentation/02-Kernel/03-Supported-devices/04-Demos/02-Supported-demos#ATMEL)® microcontroller (MCU) ports in FreeRTOS™ 
version 10.3.1, or rather six new ports. These ports not only cover the megaAVR® 0-series of MCUs and 
the brand-new AVR Dx devices, but also the three main compilers for AVR MCUs: MPLAB XC8 compiler, 
AVR-GCC, and IAR Embedded Workbench® for AVR. Why is this great news? Well, it’s because the ATmega323 
and ATmega128 MCUs that are supported in earlier versions of FreeRTOS are older devices. While these 
devices are still available products, AVR MCUs have evolved significantly - and who doesn’t want to 
use the latest generation of a product?

With this support for new devices and a new compiler, I could not help wondering how much memory the 
standard FreeRTOS demo examples consume on one of these new MCUs and how much the choice of compiler 
actually influences the code size. To keep this post concise, I'll focus on just the ports for the AVR 
Dx MCU families.


## AVR Dx: Is this a tinyAVR®, megaAVR or AVR XMEGA® MCU?

The most well-known AVR MCU is perhaps the ATmega328, which is the MCU used on 
the [Arduino® UNO](https://store.arduino.cc/arduino-uno-rev3) kit. The AVR Dx is the newest generation 
of AVR MCUs and it is similar to the latest tinyAVR 1-series, like the ATtiny817, which again is similar 
to the AVR XMEGA devices. So, it is a bit more sophisticated than the older megaAVR MCUs. This difference 
is most clearly seen in the peripherals and how they are better organized in the memory map.

There are currently two families of AVR Dx MCUs. 
The [AVR DA family](https://www.microchip.com/design-centers/8-bit/avr-mcus/device-selection/avr-da?utm_source=FreeRTOS&utm_medium=Blog&utm_campaign=AVR-DA-FREERTOS-BLOG) 
features the latest version of the Peripheral Touch Controller (PTC) module used to interface capacitive 
sensors for use in touch-enabled user interfaces. 
The [AVR DB family](https://www.microchip.com/design-centers/8-bit/avr-mcus/device-selection/avr-db?utm_source=FreeRTOS&utm_medium=Blog&utm_campaign=AVR-DA-FREERTOS-BLOG) 
has built-in op amps and multi-voltage I/O, which means that selected pins can be run from a separate 
voltage domain. This eliminates the need for expensive level converters.

AVR Dx MCUs offer a significant improvement over past AVR MCUs. The core logic runs from an internal 
regulated supply, which means that the maximum speed of the core is not limited by the external supply 
voltage. It can now run at 24 MHz, regardless of the supply voltage. In other words, you have more 
horsepower available, even in low-voltage applications, with a lower active mode power consumption.


### The IDEs and Compilers

The newest compiler to support AVR MCUs is 
the **[MPLAB XC8](https://www.microchip.com/en-us/tools-resources/develop/mplab-xc-compilers)** 
compiler, which is a variant of the GCC compiler. It is integrated into 
the [MPLAB X IDE](https://www.microchip.com/mplab/mplab-x-ide?utm_source=FreeRTOS&utm_medium=Blog&utm_campaign=AVR-DA-FREERTOS-BLOG) 
and was added to the v7.0.2542 release of Microchip Studio. The MPLAB XC8 compiler is available in a 
free version, which offers a subset of optimization options. The commercial version, called MPLAB XC8 
PRO, offers all the optimizations you’d expect from a professional grade compiler. While IAR EWAVR and 
Microchip Studio are available for use with Windows® OS only, MPLAB X and the MPLAB XC8 compiler is 
available for Linux® and macOS®, as well as Windows systems. By the way, MPLAB X IDE supports the AVR-GCC 
compiler as well.

The AVR-GCC variant of the GNU GCC compiler was maintained by the user community for many years, and the 
original WIN-AVR version still exists even though it is not actively maintained. Later Atmel decided to 
make AVR-GCC part of the Atmel Studio IDE and made AVR-GCC available to AVR MCU users as an Atmel Studio 
plug-in. The AVR-GCC compiler and Arduino boards contributed significantly to the popularity of AVR MCUs 
in the Maker community. In November 2020, Microchip rebranded Atmel Studio 7 
to [Microchip Studio for AVR and SAM Devices](https://www.microchip.com/mplab/microchip-studio?utm_source=FreeRTOS&utm_medium=Blog&utm_campaign=AVR-DA-FREERTOS-BLOG); 
I’ll refer to it as Microchip Studio. There are no functional changes, but it is worth mentioning a very 
nice added feature: support for the MPLAB XC8 compiler in Microchip Studio. This means that users who are 
familiar with Atmel Studio and AVR-GCC can stay in this well-known IDE while taking advantage of the MPLAB 
XC8 compiler’s benefits.

**[IAR Embedded Workbench for AVR](https://www.iar.com/iar-embedded-workbench/#!?architecture=AVR)** (IAR 
EWAVR for short) was the first C compiler for use with AVR MCUs. The inventors of the AVR core worked closely 
with IAR when the instruction set was defined, which resulted in a better instruction set that was optimized 
for C code. IAR EWAVR combines an IDE, a compiler and a simulator. Microchip’s debugging and programming tools 
can also be used in IAR EWAVR.

The compiler versions used are:

* AR EWAVR (v7.30)
* AVR-GCC (build v3.6.2.1778)
* MPLAB XC8 Compiler (v2.30)


### Finding the Right Port and Device

Looking at the supported devices on the [FreeRTOS](/Documentation/02-Kernel/03-Supported-devices/00-Supported-devices) website, I realized that you need to 
know your semiconductor company history. Although AVR MCUs are Microchip products, they were originally 
released by Atmel, which was acquired by Microchip in 2016. This is why AVR devices are listed under Atmel 
and not under Microchip on the FreeRTOS website. You will also find a comprehensive list of Microchip’s 
Arm® core-based MCUs here too.

![Figure 1: Microchip product lines with FreeRTOS ports.](/media/2021/figure1-300x51.png)   
*Figure 1: Microchip product lines with FreeRTOS ports.*

Navigating deeper into the FreeRTOS web structure I found the [port page for the AVR Dx](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Atmel-now-Microchip/microchip-avr-dx-demo), 
which supports both the AVR DA and the AVR DB devices. The demos that come with the port use 
the [AVR128DA48](https://www.microchip.com/wwwproducts/en/AVR128DA48?utm_source=FreeRTOS&utm_medium=Blog&utm_campaign=AVR-DA-FREERTOS-BLOG) 
device and the corresponding [AVR128DA48 Curiosity Nano Evaluation Board](https://www.microchip.com/DevelopmentTools/ProductDetails/PartNO/DM164151?utm_source=FreeRTOS&utm_medium=Blog&utm_campaign=AVR-DA-FREERTOS-BLOG). 
This board was used to confirm that the code is running, which it was for all ports.

![Figure 2: AVR128DA48 Curiosity Nano evaluation kit.](/media/2021/figure2-300x200.png)   
*Figure 2: AVR128DA48 Curiosity Nano evaluation kit.*


### Download (or Clone with Git)

I downloaded the standard distribution from the [FreeRTOS downloads page](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS). It is a zip file 
that contains all ports and demos, along with the kernel and FreeRTOS libraries. You can also clone it 
from the FreeRTOS GitHub project, if you prefer to have a local Git branch of the code.

Download the zip file, unpack it and navigate to the Demo folder. If you like working with MCU, this is 
like a candy store – there’s so much to choose from!

![Figure 3: The AVR MCU ports in the FreeRTOS folder structure.](/media/2021/figure3-300x211.png)   
*Figure 3: The AVR MCU ports in the FreeRTOS folder structure.*

Before going into details with compilers, it is worth mentioning the Demo examples.


### The Demo Examples

The AVR Dx ports come with three demos. They are integrated into on single code project for each compiler 
port. The three demos are:

* Blinky
* Minimal
* Full

You use the `mainSELECTED_APPLICATION` define to select the demo at compile time. In the main.c file 
you define `mainSELECTED_APPLICATION` to 0, 1 or 2 to select the demo you want before hitting the build 
button.

![Figure 4: Selecting the active demo in main.c](/media/2021/figure4-300x154.png)   
*Figure 4: Selecting the active demo in main.c*


## MPLAB X IDE (v5.40) and MPLAB XC8 Compiler (v2.31)

From the menu, **Open project** and navigate to the AVR\_Dx\_MPLAB project file. A project-file is in the 
MPLAB X IDE a folder with the extension ".X", in this case "**AVR\_Dx\_MPLAB.X**".

![Figure 5: The MPLAB X project “file” is the .X folder.](/media/2021/figure5-300x156.png)   
*Figure 5: The MPLAB X project “file” is the .X folder.*

The **Project Properties** describe how the compiler is configured. The **configuration** confirms that 
the project is configured to use the MPLAB XC8 v2.31 compiler and that the selected **device** is the 
AVR128DA48. The port page indicated that the MPLAB XC8 v2.20 compiler was used for the development and 
test of the port, but using v2.31 (the latest version at the writing of this article) did not cause any 
difficulties.

![Figure 6: Project properties dialog. Selection of the device and compiler toolchain.](/media/2021/figure6-300x193.png)   
*Figure 6: Project properties dialog. Selection of the device and compiler toolchain. Click to enlarge.*

So, what optimization level is enabled? The optimization options are located under 
the **XC8 Global Options** -> **XC8 Compiler** in the **Options category** drop-down.

![Figure 7: Project properties dialog - compiler optimization.](/media/2021/figure7-300x84.png)   
*Figure 7: Project properties dialog - compiler optimization. Click to enlarge*

All optimization checkboxes are checked, except the "Debug" options, which you would primarily want to 
check if you do debugging with an in-system debugger like 
the [MPLAB PICkit™ 4](https://www.microchip.com/developmenttools/ProductDetails/PG164140?utm_source=FreeRTOS&utm_medium=Blog&utm_campaign=AVR-DA-FREERTOS-BLOG), [MPLAB ICD 4](https://www.microchip.com/developmenttools/ProductDetails/dv164045?utm_source=FreeRTOS&utm_medium=Blog&utm_campaign=AVR-DA-FREERTOS-BLOG) 
or [Atmel-ICE programmers/debuggers](https://www.microchip.com/DevelopmentTools/ProductDetails/ATATMEL-ICE?utm_source=FreeRTOS&utm_medium=Blog&utm_campaign=AVR-DA-FREERTOS-BLOG), 
but that is a totally different story. The **Optimization level** is set to "s", which is the highest 
level of size optimization. This optimization level is accessible for the PRO version of 
the [MPLAB XC8 Pro compiler](https://www.microchip.com/developmenttools/ProductDetails/sw006021-sub?utm_source=FreeRTOS&utm_medium=Blog&utm_campaign=AVR-DA-FREERTOS-BLOG). 
The free version of the MPLAB XC8 compiler supports optimization level -O1 and -O2. Compiling with -Os 
causes warnings that some of the optimization settings used for -Os are ignored as they require the 
MPLAB XC8 PRO compiler, but it compiles without errors.

In addition, the -flto switch is specified in the **Additional Options** text box. I consulted with the 
MPLAB XC8 compiler user guide to see what the switch controls. The -flto switch turns on the "standard 
link-time optimizer," which is a feature that is found in the PRO version of the MPLAB XC8 compiler. As 
a side note, the -flto option is not documented for the AVR-GCC compiler, so this is a difference between 
the MPLAB XC8 compiler and AVR-GCC.

![Figure 8: Project properties dialog. Selecting the optimization level and enabling link time optimization using Additional options.](/media/2021/figure8-300x193.png)   
*Figure 8: Project properties dialog. Selecting the optimization level and enabling link time optimization 
using Additional options. Click to enlarge.*

Since Microchip has an online archive of all past versions of the MPLAB XC compiler with corresponding 
user guides, search engines may not serve you the latest version of the user guide; I recommend that you 
obtain the version you need directly from 
the [MPLAB XC Compiler product pages](https://www.microchip.com/en-us/tools-resources/develop/mplab-xc-compilers).


### Code Size Results

Since not everyone has a license for the MPLAB XC8 PRO compiler, I have provided the results of the 
code size both for the free compiler and the PRO compiler. The compiler does not produce any code size 
information in the Output window, but the Dashboard window shows a nice graphical and plain-text 
representation.

![Figure 9: MPLAB X Dashboard shows the memory size of the code project.](/media/2021/figure9-300x211.png)   
*Figure 9: MPLAB X Dashboard shows the memory size of the code project.*

The code size results for the three examples, so the size of the demo applications:

**MPLAB XC8 PRO Compiler (-Os)**
| Demo | Flash Size | SRAM Size |
| ---- | ---------- | --------- |
| Blinky | 6836 | 4271 |
| Minimal | 10230 | 4308 |
| Full | 13255 | 4332 |

**MPLAB XC8 Free Compiler (-Os)**
| Demo | Flash Size | SRAM Size |
| ---- | ---------- | --------- |
| Blinky | 9078 | 4287 |
| Minimal | 13840 (-O1) | 4319 |
| Full | 16691 | 4338 |

As you can see, the MPLAB XC8 PRO compiler clearly does a better job in producing a smaller program code 
than the Free version, while the data memory usage is virtually the same for the two settings.


## Microchip Studio (v7.0.2542) and AVR-GCC (v3.6.2.1778)

Now it’s time to open the Microchip Studio project. In Microchip Studio select **Open Project**, navigate 
to the FreeRTOS/Demo/AVR\_Dx\_Atmel\_Studio folder and open the RTOSDemo file.

![Figure 10: The Microchip Studio project file.](/media/2021/figure10-300x83.png)   
*Figure 10: The Microchip Studio project file.*

Open the compiler configuration by right-clicking on the project in the Solutions Explorer (navigation) 
and selecting **Properties**. From there, select the AVR/GNU C Compiler -> Optimization item. All check-boxes 
are checked and optimization is -Os.

![Figure 11: Project properties. Selected optimization setting.](/media/2021/figure11-300x160.png)   
*Figure 11: Project properties. Selected optimization setting.*

In the **Debugging** option the **debug level** is set to -g2, which is the default level.

![Figure 12: Project properties. Selected debug level.](/media/2021/figure12-300x102.png)   
*Figure 12: Project properties. Selected debug level.*

For the **Linker** -> **Optimization**, the "Garbage collection unused section" option is checked. The 
GUI seems to include most common GCC options, but also allows you to specify additional options manually.

![Figure 13: Project properties. Garbage collection enabled.](/media/2021/figure13-300x143.png)   
*Figure 13: Project properties. Garbage collection enabled.*


### Results

Microchip Studio and AVR-GCC generates a couple of warnings, which is also the case for the other compilers. 
Some warnings are concerning, like doing a longer shift than the width of the variable can support, but this 
is outside the scope of this blog post. Microchip Studio shows the code size in the compiler output window:

![Figure 14: Memory size of the code project displayed in the output window.](/media/2021/figure14-300x30.png)   
*Figure 14: Memory size of the code project displayed in the output window. Click to enlarge.*

A warning that states that the code size information may be inaccurate if code is placed in other segments 
than the standard .text segment used for program code. Using the avr-size tool to look into the ELF output 
file, I concluded that the code mainly uses the .text segment, so good enough for this comparison as the 
size error is very small.

**AVR-GCC**
| Demo | Flash Size | SRAM Size |
| ------- | ---- | ---- |
| Blinky  | 8026 | 4309 |
| Minimal  | 12490 | 4420 |
| Full  | 15152 | 4555 |


## IAR Embedded Workbench for AVR

In IAR EWAVR, the FreeRTOS port project is opened using the workspace file. The optimization settings 
are found by right-clicking the project and selecting **Options**. The GUI is very straightforward to 
use since the options are limited and it seems difficult miss anything crucial. Select the level of 
optimization and whether you want the code to be size or speed optimized, and then check all the checkboxes.

Porthardware.h includes FreeRTOSConfig.h, and for some reason the compiler was not able to locate that 
file by itself, so I had to specify the path for the code to compile. This is an easy fix, but I had 
expected the code to compile out of the box.

![Figure 15: Project options. Selected optimization level and additional optimization options.](/media/2021/figure15-300x269.png)   
*Figure 15: Project options. Selected optimization level and additional optimization options*

Hit **Rebuild all** in the **Project** menu…

**IAR EWAVR**
| Demo: | Flash Size | SRAM Size |
| ------ | ---- | ---- |
| Blinky | 7278 | 4636 |
| Minimal | 11341 | 4728 |
| Full | 11921 | 4863 |


## Since I am Not a Compiler Expert…

We cannot all be compiler experts, so I reached out to Microchip’s and IAR’s and compiler experts and 
asked if the optimization settings used for the ports could be improved further. These are optimization 
settings that many users may not be familiar with, so I have included what I learned as inspiration to 
those who need to shrink their code to a minimum.


## Expert Advice from Microchip

Microchip’s experts suggested adding the switches listed below to the MPLAB XC8 compiler’s Global Options:

![Figure 16: Project properties. Expert optimization in Additional options.](/media/2021/figure16-300x170.png)   
*Figure 16: Project properties. Expert optimization in Additional options. Click to enlarge.*

This significantly improved of the code size, reducing it by 7.9% to 10.6%:

**MPLAB XC8 PRO Compiler (Expert)**
| Demo | Flash Size | SRAM Size | Improvement |
| ------ | ---- | ---- | ---- |
| Blinky | 6242 | 4271 | 8.7% |
| Minimal | 9426 | 4308 | 7.9% |
| Full | 11847 | 4332 | 10.6% |


## Expert Advice from IAR

IAR’s experts proposed adding the following to the command line option:

![Figure 17: Project options. Expert optimization in the Command line options.](/media/2021/figure17-300x268.png)   
*Figure 17: Project options. Expert optimization in the Command line options.*

This results in a code size reduction of around 200 bytes for all three demo examples, which represents 
a 1.5% to 3.1% improvement:

**IAR EWAVR (Expert)**
| Demo: | Flash Size | SRAM Size | Improvement |
| ------ | ---- | ---- | ---- |
| Blinky | 7056 | 4636 | 3.1% |
| Minimal | 11099 | 4728 | 2.1% |
| Full | 11739 | 4863 | 1.5% |


## Summary

The quest was to find out how well suited the AVR Dx family is for running FreeRTOS in terms of memory 
consumption. So, let have a look at the code size results out of the box, without the expert feedback 
from IAR and Microchip:

**AVR-GCC**
| Demo: | Flash Size | SRAM Size |
| ------ | ---- | ---- |
| Blinky | 8026 | 4309 |
| Minimal | 12490 | 4420 |
| Full | 15152 | 4555 |

**MPLAB XC8 PRO Compiler**
| Demo: | Flash Size | SRAM Size |
| ------ | ---- | ---- |
| Blinky | 6836 | 4271 |
| Minimal | 10230 | 4308 |
| Full | 13255 | 4332 |

**MPLAB XC8 Free Compiler**
| Demo: | Flash Size | SRAM Size |
| ------ | ---- | ---- |
| Blinky | 9078 | 4287 |
| Minimal | 13840 | 4319 |
| Full | 16691 | 4338 |

**IAR EWAVR**
| Demo: | Flash Size | SRAM Size | 
| ----- | ---------- | --------- |
| Blinky | 7278 | 4636 |
| Minimal | 11341 | 4728 |
| Full | 11921 | 4863 |

One thing that stands out is that the SRAM consumption is more or less constant regardless of the demo 
example. Since all compilers agree that you need more than 4 KB of RAM, it is fair to conclude that you 
need a device with 8 KB or more. The Flash consumption depends on the demo example. Obviously, you will 
need more Flash for larger demo code. The Full demo example compiles to 12–13 KB of program memory (Flash). 
This means that the SRAM is driving the memory requirements when you select an MCU. You would need a 64 
KB AVR DA/DB to get enough SRAM, as these devices have an 8:1 ratio between Flash and SRAM. Some options 
are the AVR64DA48 (which is on the Curiosity Nano Development Board) or the AVR64DB32. The largest AVR 
DA/DB devices come with 128 KB of Flash and 16 KB of SRAM, so there is plenty of headroom to grow your 
applications. That said, FreeRTOS will use more or less SRAM depending on the number of threads used, 
so the SRAM consumption is not set in stone.

In addition to the ports for the AVR Dx devices, ports have been published for the megaAVR 0-series 
of MCUs, which means the ATmega1608/9, ATmega3208/9 and the ATmega4808/9. These are in many ways similar 
to the traditional AVR MCUs, however they also offer elements from the XMEGA series. Since FreeRTOS is 
a bit hungry for SRAM, it is fair to state that the ATmega480x devices are a good place to start as they 
have 6 KB of SRAM and 48 KB of Flash. The smaller siblings have less SRAM and would, therefore, require 
some adjustments of the FreeRTOS configuration to fit.

When it comes to the compilers, it was impressive to see how well the MPLAB XC8 PRO compiler performs. 
It generated smaller code for the Blinky and Minimal demos, while IAR EWAVR is better on the Full example, 
when using the out-of-the-box settings. When using the recommendations from the compiler experts, the 
MPLAB XC8 compiler stands stronger and generates much smaller code for the Blinky and Minimal demos (13% 
and 17.7% smaller respectively), while a 0.9% code size difference for the Full demo, in favor of IAR 
EWAVR, the is such a small difference that I would declare it a draw. Refer to the table below for details. 
The SRAM consumption was not affected by the expert settings, and the conclusion is that the MPLAB XC8 
compiler is able to save a fair amount of SRAM compared to IAR EWAVR (8.5% to 12.3%).

**MPLAB XC8 PRO Compiler (Expert)**
| Demo: | Flash Size | SRAM Size |
| ------ | ---- | ---- |
| Blinky | 6242 | 4271 | 
| Minimal | 9426 | 4308 | 
| Full | 11847 | 4332 | 

**IAR EWAVR (Expert)** 
| Demo: | Flash Size | SRAM Size | 
| ------ | ---- | ---- |
| Blinky | 7056 | 4636 |
| Minimal | 11099 | 4728 |
| Full | 11739 | 4863 |

**MPLAB XC8 Compiler vs. IAR EWAVR**
| Demo: | Flash | SRAM |
| ------ | ------ | ----- |
| Blinky | -13.0% | -8.5% |
| Minimal | -17.7% | -9.7% |
| Full | 0.9% | -12.3% |

As you can see, the MPLAB XC8 PRO compiler and IAR EWAVR both perform very well. For high-volume designs 
it is important to choose a commercial compiler that can save you the cost of moving to an MCU with a 
larger memory.

It is great to see that Microchip created FreeRTOS ports for their newest AVR MCUs. I will definitely 
keep an eye out for FreeRTOS-based AVR MCU projects in the future.


## Acknowledgements

The new FreeRTOS ports for AVR MCUs were released in v10.3.1 with contributions from Microchip’s PIC® 
and AVR MCUs applications team in Bucharest and the FreeRTOS team at Amazon. Thanks for putting in the 
effort.

Thanks to the compiler experts at Microchip and IAR for squeezing the last drops of the optimization out 
of the compilers.


## Disclaimer

The content and opinions in this blog are those of the third-party author and AWS is not responsible for 
the content or accuracy of this post. 


## About the author

![](https://secure.gravatar.com/avatar/cfa4d47b14862d65ab27765c400a75d8?s=200&d=mm&r=g)   
Jacob Lunn Lassen has a M.Sc.EE. from Aalborg University in Denmark. He joined Atmel’s AVR Applications 
team in 2000, and worked with key customer support, motor control, smart batteries, EMC research and 
product development. He joined Microchip’s PIC and AVR MCUs marketing team in 2016, now working on product 
definition, IoT and Functional Safety.   
[View articles by this author](../author/jacoblassen) 

FreeRTOS forums: Get industry-leading support from experts and collaborate with peers around the 
globe. [View Forums](https://forums.freertos.org/)
