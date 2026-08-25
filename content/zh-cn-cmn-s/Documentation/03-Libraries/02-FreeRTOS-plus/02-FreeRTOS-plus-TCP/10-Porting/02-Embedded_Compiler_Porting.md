---
title: 将 FreeRTOS-Plus-TCP 移植到新的嵌入式 C 编译器
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


### 要点总结

* FreeRTOS-Plus-TCP 源代码有两个编译器依赖项：

  1. 编译器需要被告知如何打包 C 结构体，
     即在结构体成员之间不留任何
     对齐字节。打包
     结构体至关重要，可确保数据
     在 TCP、UDP、IP 和以太网帧中能够正确显示。

  2. 编译器和 MCU RTOS 移植如何定义中断
     服务程序 (ISR)。
     嵌入式 IP 堆栈仅使用中断来管理
     以太网驱动，因而该主题在此不赘述。

* 用于确保正确打包 C 结构体的语法
  位于编译器特定的头文件中，以确保非可移植
  代码未包含在核心嵌入式 IP 堆栈源代码中。

* 每个嵌入式 C 编译器需要两个头文件。

  1. pack_struct_start.h 包含需要在必须
     打包的 C 结构体的定义之前显示
     的关键字。
  2. pack_struct_end.h 包含需要在必须
     打包的 C 结构体的定义之后显示
     的关键字。

* 嵌入式 TCP/IP 堆栈配备的编译器特定头文件位于
  FreeRTOS-Plus/FreeRTOS-Plus-TCP/portable/Compiler
  目录树中。


### 详细说明和示例

FreeRTOS-Plus-TCP 实现使用 C 结构体映射到以太网帧中的 TCP、IP、
ARP、DNS、DHCP 等协议标头。C
编译器通常会布局用于保存 C 结构体的内存，以根据
运行嵌入式软件的 MCU 架构优化对
C 结构体成员的访问。这意味着空填充字节
位于 C 结构体成员之间，以自然而然实现
MCU 的字节对齐。

例如，考虑以下
在 32 位 MCU 上定义的结构体：

```c
    struct a_struct  
    {  
        uint8_t Member1;  
        uint8_t Member2;  
        uint8_t Member3;  
        uint32_t Member4;  
    }  
  
```
*C 结构体定义示例*


前三个成员各为 8 位，且最有可能出现在
同一个 32 位字的三个连续字节中。第四个成员为 32 位，
且如果它位于 32 位的（四字节）边界上，访问效率通常会更高
（具体取决于 MCU，但大多数情况下都是如此）。
因此，在没有结构体作为数据包的情况下，编译器
很可能会在 Member3 和 Member4 之间添加一个“填充”字节
以将 Member4 的起始地址向上移动一字节，并以此方式移动到 32 位边界上。
然后，该结构体将出现在内存中，如下所示：

```c
    struct a_struct  
    {  
        uint8_t Member1;  At address 0 (first byte of first 32-bit word)  
        uint8_t Member2;  At address 1 (second byte of first 32-bit word)  
        uint8_t Member3;  At address 2 (third byte of first 32-bit word)  
        **Padding byte At address 4 (forth byte of the first 32-bit word)**  
        uint32_t Member4; Now at address 4, the first byte of the second 32-bit word  
    }  
  
```
*C 结构体如何出现在 MCU 内存中的示例*

然而，TCP/IP 协议标头没有填充字节，因此必须指示
编译器不要在映射到以太网帧写入或读取的
IP 协议标头的结构体中添加额外的
字节。不包含填充字节的结构体需要“打包”。确保
结构体被打包所需的语法取决于嵌入式 C
编译器。FreeRTOS-Plus-TCP 实现不能在通用
（非 MCU 移植特定）文件中使用任何 C 编译器的特定语法，
相反，它让用户可以将他们自己的打包指令定义为两个
非常简单的头文件，该头文件随后会包含在 C 文件中。

需要打包的结构体在 FreeRTOS-Plus-TCP 代码中显示，如下所示：

```c
    #include "pack_struct_start.h"  
    struct a_struct  
    {  
        uint8_t Member1;  
        uint8_t Member2;  
        uint8_t Member3;  
        uint32_t Member4;  
    }  
    #include "pack_struct_end.h"  

```
*封装于 pack_struct_start.h 和 pack_struct_end 头文件中的结构体*

然后可以为每个编译器提供包含编译器特定语法的 pack_struct_start.h 和 pack_struct_end.h
版本。

例如，目录 FreeRTOS-Plus/FreeRTOS-Plus-UDP/portable/Compiler/GCC
包含适用于与 GCC 编译器一起使用的定义。
因为 GCC 在结构体的起始部分不需要任何特殊语法，因此 pack_struct_start.h 为空。
pack_struct_end.h 包含以下
单行代码：

```c
    __attribute__( (packed) );
```

因此，经过预处理后，C 源代码对编译器的显示方式如下
（以 GCC 语法为例）：

```c
    struct a_struct  
    {  
        uint8_t Member1;  
        uint8_t Member2;  
        uint8_t Member3;  
        uint32_t Member4;  
    }  
    __attribute__( (packed) );  
  
```
*GCC 如何看待经过 pack_struct_start.h 和 pack_struct_end.h 包装的打包结构体*

FreeRTOS-Plus/FreeRTOS-Plus-TCP/portable/Compiler/GCC 已包含在
FreeRTOS-Plus-TCP 的下载中，可以在移植到其他嵌入式 C 编译器时
用作参考。

**pack_struct_end.h 必须至少包含一个分号 ( ; )
 以标记结构体定义的结束。**它对于
pack_struct_start.h 为空有时有效，但 pack_struct_end.h 完全为空
则永远无效。
