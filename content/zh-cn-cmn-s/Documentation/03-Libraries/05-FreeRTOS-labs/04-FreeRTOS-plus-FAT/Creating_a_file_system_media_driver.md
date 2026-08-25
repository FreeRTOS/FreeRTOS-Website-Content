---
title: 创建 FreeRTOS-Plus-FAT 媒体驱动程序
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


FreeRTOS-Plus-FAT 是一个 [FreeRTOS Labs](/Documentation/03-Libraries/05-FreeRTOS-labs/01-Introduction) 项目。虽然功能齐全，
相当成熟，但它是收购过来的产品（不是我们自己编写的），因此不一定
符合我们的生产代码或测试标准。它可从
GitHub 上的 [Lab-Project-FreeRTOS-FAT](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-FAT) 存储库获得。


### 媒体驱动程序的结构体

![](/media/2018/Media_Driver.png)


**媒体驱动程序的结构体**

*媒体*是存储文件的物理设备。适用于
嵌入式文件系统的媒体的示例包括 SD 卡，
固态磁盘、NOR 闪存芯片、NAND 闪存芯片和 RAM
芯片。媒体驱动器是负责向媒体写入以及从媒体读取
的软件。

FreeRTOS-Plus-FAT 将所有媒体类型的公共信息存储在
FF_Disk_t 类型的结构体中。媒体驱动器的开发者可以扩展 FF_Disk_t 结构体，
从而包含其他特定于使用中媒体的信息
。

FF_Disk_t 结构体可引用一个名为输入/输出管理器
（ IO 管理器，或简称 IOMAN ）的对象。IO 管理器负责
缓冲和缓存文件及目录信息等。

实际从媒体读取数据并将数据写入媒体的机制
取决于媒体类型。因此，媒体驱动器的开发者
必须提供合适的读写函数。

许多媒体驱动器本身可利用外围驱动器
执行实际读取和写入操作。例如，
如果媒体是一张 SD 卡，那么可能
必须通过 SPI 外围设备来访问卡片。
实现 RAM 磁盘并不需要外围驱动器，
因为RAM 可以使用标准 C 库 memcpy() 函数进行读取和写入
。

某些媒体类型还需要更高级别的管理逻辑来执行操作，
例如[坏块管理](https://en.wikipedia.org/wiki/Bad_sector)
或[损耗均衡](http://en.wikipedia.org/wiki/Wear_leveling)。


### 创建新的媒体驱动器

媒体驱动器需要【至少】三个函数。

1. [从媒体读取扇区的函数](File_System_Media_Driver/Read_From_Disk)
2. [将扇区写入媒体的函数](File_System_Media_Driver/Write_To_Disk)
3. [初始化函数](File_System_Media_Driver/Media_Driver_Initialisation)

单击上面的每个项目了解更多信息，并查看工作示例。


### 准备媒体的首次使用

和台式计算机中的磁盘一样，在媒体可用于
嵌入式系统之前，必须首先进行[分区](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Native-API/FF_Partition)，
然后，必须对分区进行[格式化](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Native-API/FF_Format)
与[挂载](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Native-API/FF_Mount)。

FreeRTOS-Plus-FAT 实现了虚拟文件系统，
其中已挂载的分区必须进行[注册](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Native-API/FF_FS_Add)，
之后，它将
显示为嵌入式文件系统根目录中的一个目录。


## 驱动器 API 和结构体

* [FF_CreateIOManager()](File_System_Media_Driver/FF_CreateIOManager)
* [FF_Disk_t](File_System_Media_Driver/FF_Disk_t)
