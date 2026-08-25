---
title: "ff_deltree()"
description: FreeRTOS+FAT ff_deltree API 文档
---
[FreeRTOS-Plus-FAT 标准 API 引用](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
int ff_deltree( const char *pcDirectory )	
```
从嵌入式 FAT 文件系统中删除一个目录，然后以递归方式删除目录中的全部内容。

## 参数 
+ *pcDirectory*

  指向以 null 结尾的标准 C 字符串的指针，该字符串保存
  正在删除的目录的名称。文件名可以包括该目录的相对路径。

## 返回

如果目录和目录的内容被删除，则返回 0 
 。否则返回 -1。
