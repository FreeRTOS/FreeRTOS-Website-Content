---
title: Source Code Organization
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


The RTOS's FAT file system source code is distributed with the directory structure shown
below. Pre-packaged projects may be delivered with a slightly different
structure.
 
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
*The FreeRTOS-Plus-FAT Directory Structure*
