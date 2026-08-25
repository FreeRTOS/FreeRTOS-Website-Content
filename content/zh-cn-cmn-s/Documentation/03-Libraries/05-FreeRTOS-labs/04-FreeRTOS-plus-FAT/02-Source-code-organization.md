---
title: 源代码组织
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


RTOS 的源代码按如下目录结构分布
。交付的预先打包项目结构可能稍有不同
。

```c
FreeRTOS-Plus-FAT    [Contains the source files that implement the FAT FS]  
  |  
  +-include          [Contains the header files for the FAT FS]  
  |  
  +-portable  
      |  
      +-common       [Contains source and header files used by all ports, inc. a RAM disk driver]  
      |  
      +-Platform_1   [Contains source file specific to the chip/compiler identified by the directory's name]  
      |  
      +-Platform_2   [Contains source file specific to the chip/compiler identified by the directory's name]  

```
*FreeRTOS-Plus-FAT 目录结构*
