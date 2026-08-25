---
title: "FreeRTOS 堆内存管理"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
description: FreeRTOS 内存管理
relatedLinks:
  - title: 静态内存分配 vs 动态内存分配
    link: /Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation/
  - title: 静态内存分配演示
    link: /Documentation/02-Kernel/02-Kernel-features/09-Memory-management/04-Static-allocation-demo/
---


[另请参阅[静态内存分配与动态内存分配](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation)页面，其中介绍了 
静态（不使用 FreeRTOS 堆）或动态分配 RTOS 对象的利弊、
[configAPPLICATION_ALLOCATED_HEAP](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configapplication_allocated_heap)
常量（可在 FreeRTOSConfig.h 中定义）以及 
[演示了如何在没有堆实现的情况下使用 FreeRTOS 的参考项目](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/04-Static-allocation-demo)。]

每次创建任务、队列、互斥锁、软件定时器、信号量或事件组时，RTOS 内核都需要 RAM
。RAM 可以
从 RTOS API 对象创建函数内的 RTOS 堆自动动态分配，
或者可以由[应用程序编写者提供](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation)。

如果 RTOS 对象是动态创建的，那么标准 C 库
malloc() 和 free() 函数有时可用于此目的，但是**...**

1. 它们在嵌入式系统上并不总是可用，
2. 它们占用了宝贵的代码空间，
3. 它们不是线程安全的，而且
4. 它们不是确定性的
   （执行函数所需时间将因调用而异）

**...**所以往往需要一个替代的内存分配实现。

一个嵌入式/实时系统的 RAM 和定时要求可能与另一个非常不同，所以单一的分配算法 
RAM 将永远只适用于一个应用程序子集。

为了避免此问题，FreeRTOS 将内存分配 API
保留在其可移植层。可移植层在实现核心
RTOS 功能的源文件之外，
允许提供适合于正在开发的实时系统的特定应用程序实现。当 RTOS 内核需要
RAM 时，它不调用 malloc()，而是调用 pvPortMalloc()。释放 RAM 时，
RTOS 内核调用 vPortFree()，而不是 free()。

FreeRTOS 提供了几种堆管理方案，
其复杂性和功能各不相同。您也可以提供自己的堆实现，
甚至同时使用两个堆实现。同时使用两个堆实现
允许将任务堆栈和其他 RTOS 对象放置在
内部 RAM 中，并将应用程序数据放置在较慢的外部 RAM 中。


## 包含在 RTOS 源代码下载中的内存分配实现

FreeRTOS 下载包含五个内存分配实现示例，
以下各小节描述了每个实现示例。这些小节还介绍了
所提供的每个实现方式何时选择可能最合适
。

每个提供的实现都包含在单独的源文件中 (分别是 heap_1.c、
heap_2.c、heap_3.c、heap_4.c 和 heap_5.c)，
位于主 RTOS 源代码下载内容的 Source/Portable/MemMang 目录下。
可根据需要添加其他实现方式。每次一个项目中，
只应包含其中一个源文件[这些可移植层函数定义的堆
将由 RTOS 内核使用，
即使用 RTOS 的应用程序选择使用自己的堆实现]。

以下是：

* [heap_1](#heap_1c)—— 最简单，不允许释放内存。
* [heap_2](#heap_2c)—— 允许释放内存，但不会合并相邻的空闲块。
* [heap_3](#heap_3c)—— 简单包装了标准 malloc() 和 free()，以保证线程安全。
* [heap_4](#heap_4c)—— 合并相邻的空闲块以避免碎片化。包含绝对地址放置选项。
* [heap_5](#heap_5c)—— 如同 heap_4，能够跨越多个不相邻内存区域的堆。


注意：
* heap_1 不太有用，因为 FreeRTOS 添加了[静态分配支持](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation)。
* heap_2 现在被视为旧版，因为较新的 heap_4 实现是首选。


---

### heap_1.c

heap_1 不太有用，因为 FreeRTOS 添加了[静态分配支持](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/03-Static-vs-Dynamic-memory-allocation)。

heap_1 是最简单的实现方式。内存一经分配，它*不*允许内存再被释放
。尽管如此，heap_1.c
还是适用于大量嵌入式应用程序。这是因为许多小型和深度嵌入的应用程序在系统启动时
创建了所需的所有任务、队列、信号量等，
并在程序的生命周期内使用所有这些对象
（直到应用程序再次关闭或重新启动）。任何内容
都不会被删除。

这个实现只是在要求使用 RAM 时将一个单一的数组细分为更小的块
。数组的总大小（堆的总大小）通过
configTOTAL_HEAP_SIZE （定义于 FreeRTOSConfig.h 中）设置 。
提供了 [configAPPLICATION_ALLOCATED_HEAP](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configapplication_allocated_heap)
FreeRTOSConfig.h 配置常量，
以允许将堆放置在内存中的特定地址。

xPortGetFreeHeapSize() API 函数返回未分配的堆空间总量，
允许优化 configTOTAL_HEAP_SIZE
设置。

heap_1 实现：

* 如果您的应用程序从未删除任务、队列、信号量、互斥锁等，则可以使用。
  （这实际上涵盖了使用 FreeRTOS
  的大多数应用程序）。

* 始终具有确定性（总是需要相同的时间来执行），
  不会导致内存碎片化。

* 非常简单，且从静态分配的数组分配内存，
  这意味着它通常适合用于不允许真实动态内存分配的应用程序
  。

---

### heap_2.c

heap_2 现在被视为旧版，因为 heap_4 是首选。

heap_2 使用最佳适应算法，并且与方案 1 不同，它允许释放先前分配的块，
它*不*将相邻的空闲块组合成一个大块。
有关不合并空闲块的实现，请参阅 heap_4.c。

可用堆空间的总量通过 configTOTA L_HEAP_SIZE（定义于
FreeRTOSConfig.h 中）设置。
提供了 [configAPPLICATION_ALLOCATED_HEAP](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configapplication_allocated_heap)
FreeRTOSConfig.h 配置常量，
以允许将堆放置在内存中的特定地址。

xPortGetFreeHeapSize() API 函数返回未分配的堆空间总量，
（允许优化 configTOTAL_HEAP_SIZE 设置），
但不提供关于未分配的内存如何被碎片化成小块的信息
。

pvPortCalloc() 函数的签名与标准库 calloc 函数相同。它为一个对象数组分配内存， 
并将分配的存储空间中的所有字节初始化为零。如果分配成功， 
它会返回指向分配的内存块中最低字节的指针。如果分配失败，它会返回一个空指针。

此实现：

* 即使应用程序重复删除任务、队列、
  信号量、互斥锁等，仍然可用，
  但要注意以下关于内存碎片化的信息。

* 如果正在分配和释放的内存为随机大小，则*不*应使用
  。例如：
  
  + 如果应用程序动态地创建和删除任务，
    且分配给正在创建任务的堆栈大小总是相同的，
    那么 heap2.c 可以在大多数情况下使用。但是，
    如果分配给正在创建任务的堆栈的大小不是总相同，
    那么可用的空闲内存可能会被碎片化成许多小块
    ，
    最终导致分配失败。这种情况下，
    heap_4.c 是更好的选择。
    
  + 如果应用程序动态地创建和删除任务，
    且队列存储区域在每种情况下都是相同的
    （队列存储区域是队列项大小乘以队列长度），
    那么 heap_2.c 可以在大多数情况下使用。但是，
    如果在每种情况下的队列存储区域不相同，
    那么可用的空闲内存可能会被碎片化成许多小块
    ，
    最终导致分配失败。这种情况下，
    heap_4.c 是更好的选择。

   + 应用程序直接调用 pvPortMalloc() 和 vPortFree()，
     而不是仅通过其他 FreeRTOS API 函数间接调用。

* 如果您应用程序的队列、任务、信号量、互斥锁等的顺序不可预测，
  可能会导致内存碎片化。这对几乎所有的应用程序来说都是不可能的，
  但应牢记这一点。

* 非确定性，但比大多数标准 C 库 malloc 实现更有效。

heap_2.c 适用于许多必须动态创建对象的小型实时系统
。请参阅 heap_4 了解类似实现，
该实现将空闲的内存块组合成单一的大内存块。


---

### heap_3.c

这为标准 C 库 malloc() 和 free() 函数实现了简单的包装器，
在大多数情况下，将与您选择的编译器一起提供。该
包装器只是使 malloc() 和 free() 函数线程安全。

此实现：

* 需要链接器设置堆，需要编译器库提供
  malloc() 和 free() 实现。.
* 不具有确定性。
* 可能会大大增加 RTOS 内核代码大小。

请注意，使用 heap_3 时，FreeRTOSConfig.h 中的 configTOTAL_HEAP_SIZE 设置无效
。

---

### heap_4.c

此方案使用第一适应算法，并且与方案 2 不同，
它确实将相邻的空闲内存块组成单个大内存块（它确实包含合并算法）。

可用堆空间的总量通过
configTOTAL_HEAP_SIZE （定义于 FreeRTOSConfig.h 中）设置。
提供了 [configAPPLICATION_ALLOCATED_HEAP](/Documentation/02-Kernel/03-Supported-devices/02-Customization/#configapplication_allocated_heap)
FreeRTOSConfig.h 配置常量，
以允许将堆放置在内存中的特定地址。

xPortGetFreeHeapSize() API 函数被调用时返回未分配的堆空间总量，
xPortGetMinimumEverFreeHeapSize()
API 函数返回
FreeRTOS 应用程序启动的系统中已存在的最小空闲堆空间量。这两个函数都没有提供关于未分配的
内存如何碎片化为小块的信息。

vPortGetHeapStats() API 函数提供了其他信息。它填充了一个
heap_t 结构体的成员，如下所示。

```c
/* Prototype of the vPortGetHeapStats() function. */  
void vPortGetHeapStats( HeapStats_t *xHeapStats );  

/* Definition of the Heap_stats_t structure. */  
typedef struct xHeapStats  
{  
	size_t xAvailableHeapSpaceInBytes;      /* The total heap size currently available - this is the sum of all the free blocks, not the largest block that can be allocated. */  
	size_t xSizeOfLargestFreeBlockInBytes; 	/* The maximum size, in bytes, of all the free blocks within the heap at the time vPortGetHeapStats() is called. */  
	size_t xSizeOfSmallestFreeBlockInBytes; /* The minimum size, in bytes, of all the free blocks within the heap at the time vPortGetHeapStats() is called. */  
	size_t xNumberOfFreeBlocks;		/* The number of free memory blocks within the heap at the time vPortGetHeapStats() is called. */  
	size_t xMinimumEverFreeBytesRemaining;	/* The minimum amount of total free memory (sum of all free blocks) there has been in the heap since the system booted. */  
	size_t xNumberOfSuccessfulAllocations;	/* The number of calls to pvPortMalloc() that have returned a valid memory block. */  
	size_t xNumberOfSuccessfulFrees;	/* The number of calls to vPortFree() that has successfully freed a block of memory. */  
} HeapStats_t;  
```

pvPortCalloc() 函数的签名与标准库 calloc 函数相同。它为一个对象数组分配内存， 
并将分配的存储空间中的所有字节初始化为零。如果分配成功， 
它会返回指向分配的内存块中最低字节的指针。如果分配失败，它会返回一个空指针。

heap_4：

* 即使应用程序重复删除任务、队列、信号量、互斥锁等等时也可使用

* 与 heap_2 实现相比，导致堆空间严重碎片化成多个小块的可能性小得多
  （即使正在分配和释放的内存是随机大小）
  。

* 不具有确定性，但比大多数标准 C 库 malloc 实现更有效。

heap_4.c 对于想在应用程序代码中直接使用可移植层内存分配方案的应用程序特别有用
（而不是
通过调用 API 函数
pvPortMalloc() 和 vPortFree() 来间接使用)。

---

### heap_5.c

此方案使用与 heap_4 相同的第一拟合和内存合并算法，
允许堆跨越多个不相邻（非连续）
内存区域。

Heap_5 通过调用 vPortDefineHeapRegions() 初始化，且**不得使用**，
直到 vPortDefineHeapRegions() 执行以后。创建
RTOS 对象（任务、队列、信号量等）将隐式调用 pvPortMalloc()，
因此，使用 heap_5 时，在创建任何此类对象之前调用 vPortDefineHeapRegions()
至关重要。

vPortDefineHeapRegions() 采用单一参数，该参数为
HeapRegion_t 结构体数组。HeapRegion_t 在 portable.h 中定义为

```c
typedef struct HeapRegion  
{  
    /* Start address of a block of memory that will be part of the heap.*/  
    uint8_t *pucStartAddress;  

    /* Size of the block of memory. */  
    size_t xSizeInBytes;  
} HeapRegion_t;  
```
*HeapRegion_t 类型定义*

数组使用空位零大小的区域定义终止，
数组中定义的内存区域**必须**按地址顺序，
从低地址到高地址显示。以下源代码片段提供了示例
。[MSVC Win32 模拟器演示](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)也使用
heap_5 ，因此可作参考。


```c
/* Allocate two blocks of RAM for use by the heap. The first is a block of  
   0x10000 bytes starting from address 0x80000000, and the second a block of  
   0xa0000 bytes starting from address 0x90000000. The block starting at  
   0x80000000 has the lower start address so appears in the array fist. */  
const HeapRegion_t xHeapRegions[] =  
{  
    { ( uint8_t * ) 0x80000000UL, 0x10000 },  
    { ( uint8_t * ) 0x90000000UL, 0xa0000 },  
    { NULL, 0 } /* Terminates the array. */  
};  

/* Pass the array into vPortDefineHeapRegions(). */  
vPortDefineHeapRegions( xHeapRegions );  
```
*定义了堆使用的内存块之后初始化 heap_5*

xPortGetFreeHeapSize() API 函数被调用时返回未分配的堆空间总量，
xPortGetMinimumEverFreeHeapSize()
API 函数返回
FreeRTOS 应用程序启动的系统中已存在的最小空闲堆空间量。这两个函数都没有提供关于未分配的
内存如何碎片化为小块的信息。

pvPortCalloc() 函数的签名与标准库 calloc 函数相同。它为一个对象数组分配内存， 
并将分配的存储空间中的所有字节初始化为零。如果分配成功， 
它会返回指向分配的内存块中最低字节的指针。如果分配失败，它会返回一个空指针。

vPortGetHeapStats() API 函数提供了有关堆状态的其他信息。
