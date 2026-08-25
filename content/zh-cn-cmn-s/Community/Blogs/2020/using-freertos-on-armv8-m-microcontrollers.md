---
title: 在 ARMv8-M 微控制器上使用 FreeRTOS
created: 2020-04-06 00:00:00.0 UTC
feature: blog
categories:
  - 长期支持
authors:
  - aggarg
relatedLinks:
  - title: FreeRTOS 简介
    link: /Why-FreeRTOS/What-is-FreeRTOS/
---

本帖由 [Gaurav Aggarwal](../author/aggarg) 发表于 2020 年 4 月 6 日

[另请参阅描述[如何在使用 FreeRTOS时设置 ARM Cortex-M 中断优先级](/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/RTOS-Cortex-M3-M4)]的页面。

ARM 在采用 ARMv8-M 架构的 Cortex-M 系列微控制器中引入了 TrustZone。TrustZone 
为可选安全扩展，能够在单个处理器中实现两个安全域。包含 TrustZone 的 Cortex-M 核心 
（包括 Cortex-M33 和 Cortex-M23）可使用 TrustZone 将执行空间划分为 
安全 ('s') 和非安全 ('ns') 分区（或“端”）。这种划分 
可在安全端执行受信任的软件，在非安全端执行不受信任的软件，并在两者之间实现完全隔离， 
从而增强安全性。安全端和非安全端都有独立的内存保护单元 (MPU)， 
可在两个安全域内实现进一步隔离。

在安全端运行的软件可以导出想要提供给 
在非安全端运行的软件的函数。这些函数必须放在明确标记为 
非安全可调用 (NSC) 的内存区域中。非安全软件只能通过 NSC 内存中这些导出的函数 
来访问安全软件。

ARMv8-M 架构还引入了堆栈限制寄存器，可确保应用程序软件 
在堆栈溢出时立即将其捕获。

以下小节描述了 
在 ARMv8-M 核心上运行 FreeRTOS 时可用的运行时和配置选项：
* [ARMv8-M 应用程序剖析](#armv8-m-应用程序剖析)
* [FreeRTOS ARMv8-M 移植特点](#freertos-armv8-m-移植特点)
* [快速入门](#快速入门)
* [FreeRTOS ARMv8-M 移植使用说明](#freertos-armv8-m-移植使用说明)
	+ [使用 FreeRTOS（有 TrustZone 支持）](#使用-freertos有-trustzone-支持)
	+ [使用 FreeRTOS（无 TrustZone 支持）](#使用-freertos无-trustzone-支持)
	+ [使用 FreeRTOS（有内存保护单元 (MPU) 支持）](#使用-freertos有内存保护单元-mpu-支持)
	+ [使用 FreeRTOS（有浮点单元 (FPU) 支持）](#使用-freertos有浮点单元-fpu-支持)
* [改进 FreeRTOS ARMv8-M 移植](#改进-freertos-armv8-m-移植)

---

<span id="APPLICATION_STRUCTURE"/>

## ARMv8-M 应用程序剖析

使用 TrustZone 的应用程序由两个单独的项目组成：

1. 在安全端运行的安全应用程序。
2. 在非安全端运行的非安全应用程序。

ARMv8-M 核心启动时，总是进入安全端。接下来，安全软件负责 
对安全属性单元 (SAU) 和实现定义属性单元 (IDAU) 进行编程， 
将内存空间划分为安全区和非安全区，然后分支到非安全软件。 
安全端的软件可以访问安全内存和非安全内存， 
而非安全端的软件只能访问非安全内存。

通常，在安全端执行的软件需要稳健且可靠，因此会尽可能保持 
小巧，往往只提供系统的信任根（安全启动、身份、加密 
功能等）。然后，非安全端的内存保护单元 (MPU) 用于 
在较低特权级别运行非安全任务，  并按线程 
（RTOS 任务）提供细粒度内存和外围设备访问控制。


<span id="FREERTOS_V8M_FEATURES" />

## FreeRTOS ARMv8-M 移植特点

FreeRTOS ARMv8-M（ARM Cortex-M33 和 ARM Cortex-M23）移植：
* 可以在安全端或非安全端运行。
* 允许非安全任务（或线程）调用安全端可信函数（通过 NSC 内存中的指定入口点）， 
  而这些函数可以反过来调用非安全函数，所有这些都不会违反 
  内核的优先调度策略。
* 可选支持 TrustZone（当 FreeRTOS 内核在非安全端运行时）。
* 可选支持内存保护单元 (MPU)。
* 可选支持浮点单元 (FPU)。
* 仅允许源自 FreeRTOS 内核代码的特权升级。

通常情况下，FreeRTOS 调度器在非安全端运行，并且所有非安全 
FreeRTOS 任务都可以调用由安全端软件导出的函数。因此，应用程序开发者 
能够将关键软件放在安全端，并确保非安全软件中的错误 
不会影响关键的安全软件。

如果使用 MPU，非安全端的任务具有较低的特权级别，可以彼此隔离， 
并与内核隔离。


<span id="QUICK_START"/>

## 快速入门

本页正文提供了为 ARMv8-M 微控制器构建 FreeRTOS 的详细信息， 
但是，最简单的入门方法是使用以下任一预配置的示例项目：

* [使用 Keil uVision IDE 的 Keil 模拟器](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Arm-Virtual-Hardware/RTOS-Cortex-M33-Keil-Simulator)
* [使用 MCUXpresso IDE 的 NXP LPCXpresso55S69 开发板](/Documentation/02-Kernel/03-Supported-devices/04-Demos/NXP/RTOS-Cortex-M33-LPC55S69-MCUXpresso-GCC)
* [使用 Keil uVision 和 IAR IDE 的 Nuvoton NuMaker-PFM-M2351 板](/Documentation/02-Kernel/03-Supported-devices/04-Demos/Nuvoton/RTOS-Cortex-M23-NuMaker-PFM-M2351-Keil)

示例 ARMv8-M 项目位于 FreeRTOS/Demo 
（位于主 [FreeRTOS zip 文件下载](/Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS)）的子目录中。这些项目可以直接使用， 
也可以单纯用作下文详述的源文件、配置选项和编译器设置的 
工作示例和参考。

---

<span id="FREERTOS_ARMv8M_PORTS" />

## FreeRTOS ARMv8-M 移植使用说明

FreeRTOS ARMv8-M 移植使用以下编译时宏启用或禁用 TrustZone、 
内存保护单元 (MPU) 和浮点单元 (FPU) 支持。本页后续章节会介绍 
相关使用详情。

```c
    /* Set to 1 when running FreeRTOS on the non-secure side to enable the  
     * ability to call the (non-secure callable) functions exported from secure side. */ 
     
    #define configENABLE_TRUSTZONE 1  

    /* Set to 1 when running FreeRTOS on the secure side. Note that in this case TrustZone is  
     * not supported as secure tasks cannot call non-secure code i.e. configENABLE_TRUSTZONE  
     * must be set to 0 when setting configRUN_FREERTOS_SECURE_ONLY to 1. */  

    #define configRUN_FREERTOS_SECURE_ONLY 1  

    /* Set to 1 to enable the Memory Protection Unit (MPU), or 0 to leave the Memory  
     * Protection Unit disabled. */  

    #define configENABLE_MPU 1  

    /* Set to 1 to enable the Floating Point Unit (FPU), or 0 to leave the Floating  
     * Point Unit disabled. */  

    #define configENABLE_FPU 1    
```
*在 FreeRTOS ARMv8-M 移植中启用对多种功能的支持*

---

<span id="FREERTOS_WITH_TRUSTZONE" />

## 使用 FreeRTOS（有 TrustZone 支持）

### 描述

当 FreeRTOS 在非安全端运行时，得益于 FreeRTOSARMv8-M 移植中的 TrustZone 支持， 
非安全 FreeRTOS 任务能够调用标记为非安全可调用 (NSC) 的安全函数。 
安全函数是指在安全端实现的函数。


### FreeRTOSConfig.h 设置

要启用 TrustZone 支持，请构建 FreeRTOS，并将 `configENABLE_TRUSTZONE` 设为 1 
（在 [FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization) 中）：

```c
#define configENABLE_TRUSTZONE 1  
```
*在 FreeRTOS 中启用 TrustZone 支持*

从 ARMv8-M MCU（ARM Cortex-M23 和 Cortex-M33）非安全端调用安全函数的任务 
有两种上下文，一种位于非安全端，另一种位于安全端。在 FreeRTOS 10.4.5 之前的版本中， 
ARMv8-M 安全端移植会在运行时分配引用安全端上下文的结构体。 
自 FreeRTOS 10.4.5 版本开始，编译时会静态分配结构体。 `secureconfigMAX_SECURE_CONTEXTS` 
可用于设置静态分配的安全上下文的数量。如果未定义，则 `secureconfigMAX_SECURE_CONTEXTS` 默认为 
为 8。仅在 ARMv8-M 微控制器非安全端使用 FreeRTOS 代码的应用程序 
（例如，在安全端运行第三方代码的应用程序）无需此常量。 

```c
#define secureconfigMAX_SECURE_CONTEXTS 8  
```
*定义安全上下文的最大数量*


### 构建移植

[FreeRTOS 内核源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)页面包含有关 
在项目中添加FreeRTOS 内核的信息。**除该页面的信息外**，FreeRTOS ARMv8-M 
移植（有 TrustZone 支持）还需要在安全项目和 
非安全项目中编译的其他移植文件。

* *在安全项目中编译的源文件*：FreeRTOS/Source/portable/[compiler]/[architecture]/secure
* *在非安全项目中编译的源文件*：FreeRTOS/Source/portable/[compiler]/[architecture]/non_secure

其中[架构]可以为 ARM_CM23，也可以为 ARM_CM33，具体取决于目标硬件是 
ARM Cortex-M23 还是 ARM Cortex-M33。

**注意 1：**GCC 移植也可与 ARM 编译器版本 6 及以上版本 (ARM CLANG) 一起使用。

**注意 2：**上述两个目录也必须包含在相应编译器项目的 include 路径中。


### 将安全函数定义为非安全可调用 (NSC)

使用 `secureportNON_SECURE_CALLABLE` 宏，可从非安全端调用安全函数。

```c
secureportNON_SECURE_CALLABLE void NSCFunction( void );  
```
*示例：使用 secureportNON_SECURE_CALLABLE 宏，可通过非安全任务调用安全端函数 NSCFunction()*


然后，安全项目的链接器脚本需要确保非安全可调用函数 
放置在明确标记为非安全可调用的内存区域中。以下 
GCC 语法可用于将非安全可调用函数放置在 NSC 内存中：

```c
MEMORY  
{  
    /* Define each memory region. */  
    PROGRAM_FLASH (rx)  : ORIGIN = 0x10000000, LENGTH = 0xfe00  
    veneer_table (rx)   : ORIGIN = 0x1000fe00, LENGTH = 0x200  
    Ram0 (rwx)          : ORIGIN = 0x30000000, LENGTH = 0x8000  
}  

/* Veneer Table Section (Non-Secure Callable). */  

.text_Flash2 : ALIGN(4)  

{  
    FILL(0xff)  
    *(.text_veneer_table*)  
    *(.text.$veneer_table*)  
    *(.rodata.$veneer_table*)  
} > veneer_table  
```
*用于将非安全可调用函数放置在 NSC 内存中的 GCC 语法*

主 FreeRTOS 发行版本中的预配置示例项目包含各种 
其他编译器的示例。


### 为非安全任务分配安全上下文

所有要调用安全端函数的非安全 FreeRTOS 任务必须首先 
通过调用 `portALLOCATE_SECURE_CONTEXT` 宏来分配安全上下文：

```c
/* This task calls secure side functions. So allocate a secure  
 * context for it. */  
portALLOCATE_SECURE_CONTEXT( configMINIMAL_SECURE_STACK_SIZE );  
```
*为非安全任务分配安全上下文*

建议非安全任务首先进行安全调用以分配
安全上下文。

---

<span id="FREERTOS_WITHOUT_TRUSTZONE" />

### 使用 FreeRTOS（无 TrustZone 支持）

#### 描述

应用程序编写者可以选择在硬件中禁用 TrustZone。禁用后，微控制器 
将以非安全方式启动，并且整个内存空间都为非安全。


#### 在无 TrustZone 支持的情况下，在非安全端运行 FreeRTOS 时的 FreeRTOSConfig.h 设置

要禁用 TrustZone 支持，请构建 FreeRTOS，并将 configENABLE_TRUSTZONE 设为 0 
（在 [FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization) 文件中）：

```c
#define configENABLE_TRUSTZONE 0  
```
*在 FreeRTOS 中禁用 TrustZone 支持*


### 在无 TrustZone 支持的情况下，在安全端运行 FreeRTOS 时的 FreeRTOSConfig.h 设置

如果应用程序编写者不希望使用 TrustZone，但硬件不支持禁用 
TrustZone，则整个应用程序（包括 FreeRTOS 调度器）可以在安全端运行， 
而无需分支到非安全端。为此，除了将 configENABLE_TRUSTZONE 设为 0 之外， 
还需将 `configRUN_FREERTOS_SECURE_ONLY` 设为 1。

```c
#define configENABLE_TRUSTZONE 0  

#define configRUN_FREERTOS_SECURE_ONLY 1  
```
*仅在安全端运行 FreeRTOS*

  
### 构建移植

[FreeRTOS 内核源代码组织](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization)页面包含有关 
在项目中添加 FreeRTOS 内核的信息。FreeRTOS ARMv8-M 移植（无 TrustZone 支持）的移植文件 
位于以下目录：FreeRTOS/Source/portable/[compiler]/[architecture]/non_secure

其中[架构]可以为 ARM_CM23_NTZ，也可以为 ARM_CM33_NTZ，具体取决于目标硬件是 
ARM Cortex-M23 还是 ARM Cortex-M33。

**注意 1：**GCC 移植也可与 ARM 编译器版本 6 及以上版本 (ARM CLANG) 一起使用。

**注意 2：**上述目录也必须包含在相应编译器项目的 include 路径中。

---

<span id="FREERTOS_WITH_MPU"></span>

## 使用 FreeRTOS（有内存保护单元 (MPU) 支持）

### 描述

得益于 FreeRTOS ARMv8-M 移植中的内存保护单元 (MPU) 支持，应用程序任务能够 
以特权或非特权（用户）模式执行，并按任务提供细粒度内存和外围设备 
访问控制。

非特权任务：

1. 使用 [xTaskCreateRestricted()](/Documentation/02-Kernel/04-API-references/13-FreeRTOS-MPU-specific/01-xTaskCreateRestricted) API 创建。
2. 默认情况下，除了访问自己的堆栈外，没有其他 RAM 访问权限。
3. 无法执行 MPU 标记为仅限特权访问的代码。
4. 可以选择性地获得最多三个其他内存区域的访问权限，这些区域可在运行时更改 
   。

每当非特权任务尝试访问未被授予访问权限的内存区域时， 
都会触发内存故障。应用程序编写者可利用故障处理程序采取适当的措施， 
例如终止所述违规任务。

请勿将任务的特权级别与其执行的安全域混淆。 
ARMv8-M 核心的安全端和非安全端各有其自身的 MPU，因此 
在安全端和非安全端都能以特权和非特权模式执行。

为了降低安全风险，减轻软件错误带来的影响，建议 
尽可能以非特权模式执行应用程序代码。从非特权执行变为特权执行的过程 
称为特权提升。软件发起的特权提升  只能在 
FreeRTOS 内核的 API 函数内发生，但每次硬件接受中断时也会发生 
特权提升。如果不希望应用程序提供的中断服务程序 (ISR) 以特权模式运行， 
请为每个中断程序安装子程序，这样可以降低特权级别后 
再调用应用程序提供的处理程序函数，也可以 
[推迟处理，在任务中执行应用程序提供的处理程序函数](../../deferred_interrupt_processing) 
（此功能需由应用程序编写者提供）。


### MPU 硬件限制

ARMv8-M MPU 比 ARMv7-M MPU 更灵活，内存区域的定义 
仅有以下限制：

* 可为 MPU 区域编程的最小大小为 32 字节。
* 任何 MPU 区域的最大大小为 4GB。
* MPU 区域的大小必须是 32 字节的倍数。
* 所有 MPU 区域必须以 32 字节对齐的地址开始。


### FreeRTOSConfig.h 设置

要启用 MPU 支持，请构建 FreeRTOS，并将 configENABLE_MPU 设为
1（在 [FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization) 文件中）：

```c
#define configENABLE_MPU 1  
```
*在 FreeRTOS 中启用内存保护单元 (MPU) 支持*


### 构建移植

如果应用程序使用 TrustZone 支持，请构建 FreeRTOS 源文件， 
如[“使用 FreeRTOS（有 TrustZone 支持）”](#使用-freertos有-trustzone-支持)一节所述。如果应用程序 
不使用 TrustZone 支持，请构建 FreeRTOS 源文件， 
如[“使用 FreeRTOS（无 TrustZone 支持）”](#使用-freertos无-trustzone-支持)一节所述。**此外，** 
请在非安全项目中构建以下文件：FreeRTOS/Source/portable/Common/mpu_wrappers.c。


### 为非特权任务分配堆栈

MPU 移植中的 ARMv8-M 支持使用 MPU 区域向非特权任务授予对其堆栈的访问权限。 
因此，应用程序编写者必须确保提供给 
[xTaskCreateRestricted()](/Documentation/02-Kernel/04-API-references/13-FreeRTOS-MPU-specific/01-xTaskCreateRestricted) API 的堆栈缓冲区满足 
[MPU 硬件限制](#mpu-硬件限制)。以下 GCC 语法可用于 
将堆栈缓冲区放置在 32 字节边界上：

```c
StackType_t xTaskStackBuffer[ configMINIMAL_STACK_SIZE ] __attribute__( ( aligned( 32 ) ) );  
```
*用于将缓冲区放置在 32 字节边界上的 GCC 语法*


### 向非特权任务授予对其他内存区域的访问权限

在创建任务时，非特权任务最多可获得对三个其他内存区域的 
访问权限。为授予对这些内存区域的访问权限，需要使用三个 MPU 区域，因此 
这些内存区域必须满足 [MPU 硬件限制](#mpu-硬件限制)。以下 
示例演示了如何创建非特权任务并向其授予对 ucSharedMemory 的只读访问权限：

```c
static uint8_t ucSharedMemory[ SHARED_MEMORY_SIZE ] __attribute__( ( aligned( 32 ) ) );  

void vStartMPUDemo( void )  
{  
    static StackType_t xROAccessTaskStack[ configMINIMAL_STACK_SIZE ] __attribute__( ( aligned( 32 ) ) );  
    TaskParameters_t xROAccessTaskParameters =  
    {  
        .pvTaskCode     = prvROAccessTask,  
        .pcName         = "ROAccess",  
        .usStackDepth   = configMINIMAL_STACK_SIZE,  
        .pvParameters   = NULL,  
        .uxPriority     = tskIDLE_PRIORITY,  
        .puxStackBuffer = xROAccessTaskStack,  
        .xRegions       =   {  
                            { ucSharedMemory, 32, tskMPU_REGION_READ_ONLY | tskMPU_REGION_EXECUTE_NEVER },  
                            { 0,              0,  0                                                     },  
                            { 0,              0,  0                                                     },  
                        }  
    };  

    /* Create an unprivileged task with RO access to ucSharedMemory. */  
    xTaskCreateRestricted( &( xROAccessTaskParameters ), NULL );  
}  
```
*创建非特权任务*

请注意，代码需确保 `ucSharedMemory` 和 `xROAccessTaskStack` 
均满足 [MPU 硬件限制](#mpu-硬件限制)。


### 内存布局

具有 MPU 支持的应用程序的内存布局如下所示：

![](/media/2021/MemoryLayout.jpg)   
*具有 MPU 支持的应用程序的内存布局*

**内核代码** - 内核代码部分包含 FreeRTOS 内核可执行代码，并且只有 
特权软件才能访问。非特权软件需要通过内核系统 
调用（见下文）才能访问 FreeRTOS 内核提供的功能。所有 FreeRTOS 内核函数 
均放置在  名为 privileged_functions 的链接器部分，链接器脚本需要将这些函数放置在 
单独的闪存部分。

为确保只有特权软件才能访问 FreeRTOS 内核代码，需要使用 MPU 区域，因此 
链接器脚本必须确保包含 FreeRTOS 内核代码的闪存部分满足 
[MPU 硬件限制](#mpu-硬件限制)。此外，链接器脚本还需要 
导出两个变量，即 \_\_privileged_functions_start\_\_ 和 \_\_privileged_functions_end\_\_， 
分别表示 FreeRTOS 内核代码的开始和结束地址，FreeRTOS 内核会使用这些变量 
对 MPU进行编程。

以下 GCC 语法可用于将 FreeRTOS 内核代码放置于单独部分：

```c
/* Privileged functions - Section needs to be 32 byte aligned to satisfy  
 * MPU requirements. */  
.privileged_functions : ALIGN(32)  
{  
    . = ALIGN(32);  
    __privileged_functions_start__ = .;  
    *(privileged_functions)  
    . = ALIGN(32);  
    /* End address must be the last address in the region, therefore, -1. */  
    __privileged_functions_end__ = . - 1;  
} > PROGRAM_FLASH  
```
*用于将 FreeRTOS 内核代码放置于单独部分的 GCC 语法*

主 FreeRTOS 发行版本中的预配置示例项目包含各种 
其他编译器的示例。

**系统调用** - 系统调用部分包含所有 FreeRTOS 系统调用。非特权任务可利用系统调用 
访问原本仅供特权软件使用的 FreeRTOS API 
。非特权任务调用 FreeRTOS API 时会通过系统调用，该调用会暂时 
提高调用任务的特权，然后执行请求的 API， 
并在返回给调用者之前重置特权。所有 FreeRTOS 系统调用均放置在 
名为 freertos_system_calls 的链接器部分，链接器脚本需要将这些调用放置在单独的闪存部分。

为确保特权软件和非特权软件均可访问系统调用，需要使用 MPU 区域。 
因此，链接器脚本必须确保包含系统调用的闪存部分满足 
[MPU 硬件限制](#mpu-硬件限制)。此外，链接器脚本还需要 
导出两个变量，即 \_\_syscalls_flash_start\_\_ 和 \_\_syscalls_flash_end\_\_，分别表示 
FreeRTOS 系统调用的开始和结束地址，FreeRTOS 内核会使用这些变量 
对 MPU 进行编程。这些变量也用于确保非特权软件不能任意提升其特权， 
并且特权提升的范围仅限于 FreeRTOS 内核内部。

以下 GCC 语法可用于将 FreeRTOS 系统调用放置于单独部分：

```c
/* FreeRTOS System calls - Section needs to be 32 byte aligned to satisfy  
 * MPU requirements. */  
.freertos_system_calls : ALIGN(32)  
{  
    . = ALIGN(32);  
    __syscalls_flash_start__ = .;  
    *(freertos_system_calls)  
    . = ALIGN(32);  
    /* End address must be the last address in the region, therefore, -1. */  
    __syscalls_flash_end__ = . - 1;  
} > PROGRAM_FLASH  
```
*用于将 FreeRTOS 系统调用放置于单独部分的 GCC 语法*

主 FreeRTOS 发行版本中的预配置示例项目包含各种 
其他编译器的示例。

**内核数据** - 内核数据 (RAM) 部分包含所有 FreeRTOS 内核数据，只有 
特权软件才能访问。所有 FreeRTOS 内核数据均放置在名为 privileged_data 的链接器部分， 
链接器脚本需要将这些数据放置在单独的 RAM 部分。  

为确保只有特权软件才能访问 FreeRTOS 内核数据，需要使用 MPU 区域， 
因此链接器脚本必须确保包含 RAM 内核数据的 FreeRTOS 部分满足 
[MPU 硬件限制](#mpu-硬件限制)。此外，链接器脚本还需要 
导出两个变量，即 \_\_privileged_sram_start\_\_ 和 \_\_privileged_sram_end\_\_，分别表示 
FreeRTOS 内核数据的开始和结束地址，FreeRTOS 内核会使用这些变量对 MPU 进行编程。

以下 GCC 语法可用于将 FreeRTOS 内核数据放置于单独部分：

```c
/* Main Data section (Ram0). */  
.data : ALIGN(4)  
{  
    /* Privileged data - It needs to be 32 byte aligned to satisfy  
     * MPU requirements. */  
    . = ALIGN(32);  
    __privileged_sram_start__ = .;  
    *(privileged_data);  
    . = ALIGN(32);  
    /* End address must be the last address in the region, therefore, -1. */  
    __privileged_sram_end__ = . - 1;  
} > Ram0 AT>PROGRAM_FLASH  
```
*用于将 FreeRTOS 内核数据放置于单独部分的 GCC 语法*

主 FreeRTOS 发行版本中的预配置示例项目包含各种其他编译器的示例。

---

<span id="FREERTOS_WITH_FPU"></span>

## 使用 FreeRTOS（有浮点单元 (FPU) 支持）

### 描述

如果目标微控制器包括浮点单元 (FPU) ，并且您将选项传递给编译器， 
指示其生成浮点指令（而非使用仿真浮点运算）， 
则必须启用 FPU 支持。


### FreeRTOSConfig.h 设置

要启用 FPU 支持，请构建 FreeRTOS，并将 `configENABLE_FPU` 设为 1 
（在 [FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization) 文件中）：

```c
#define configENABLE_FPU 1  
```
*在 FreeRTOS中启用浮点单元 (FPU) 支持*


### 构建移植

如果应用程序使用 TrustZone 支持，请构建 FreeRTOS 源文件， 
如[“使用 FreeRTOS（有 TrustZone 支持）”](#使用-freertos有-trustzone-支持)一节所述。如果应用程序 
不使用 TrustZone 支持，请构建 FreeRTOS 源文件， 
如[“使用 FreeRTOS（无 TrustZone 支持）”](#使用-freertos无-trustzone-支持)一节所述。

---

<span id="CONTRIBUTION"></span>

## 改进 FreeRTOS ARMv8-M 移植

FreeRTOS ARMv8-M 移植组织如下：

* **主副本** - 在 FreeRTOS/Source/portable/ARMv8M 中进行维护。
* **副本** - 主副本在多个[编译器]/[架构]目录中复制，以确保 
  用户可以轻松找到其编译器和架构组合所需的移植文件。

如果希望为 FreeRTOS ARMv8-M 移植做出贡献，请对主副本进行更改， 
然后使用 FreeRTOS/Source/portable/ARMv8M/copy_files.py 脚本来复制主副本。

## 作者简介

![](https://secure.gravatar.com/avatar/ec2b9cace8c52148e35991ba7595c481?s=200&d=mm&r=g)   
Gaurav Aggarwal 是 IoT 边缘设备团队的 FreeRTOS 内核和嵌入式连接专家， 
该团队隶属于 Amazon Web Services。他在将 ARM Cortex-M33 和 Cortex-M23 
FreeRTOS 内核移植推向市场方面功不可没，目前为这些移植的使用提供支持服务，同时他还在 
FreeRTOS 库产品组合的开发和改进中发挥积极作用。  
[查看此作者的文章](../author/aggarg) 


FreeRTOS 论坛：获得行业领先的专家支持，并与全球同行 
合作。[查看论坛](https://forums.freertos.org/)

