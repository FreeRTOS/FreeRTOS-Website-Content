---
title: "ff_rename()"
description: FreeRTOS+FAT ff_rename API 文档
---
[FreeRTOS-Plus-FAT 标准 API 引用](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
int ff_rename( const char *pcOldName, const char *pcNewName );
```

移动文件。文件可以在不同目录之间移动，但不能在不同文件系统之间
移动。

## 参数
+ *pcOldName*

  指向以 null 结尾的标准 C 字符串的指针，该字符串包含
  源文件的名称。该字符串可以包含相对路径。

+ *pcNewName*

  指向以 null 结尾的标准 C 字符串的指针，该字符串包含
  目标文件的名称。该字符串可以包含相对路径。

## 返回

如果文件移动成功，则返回零。

如果文件无法移动，则返回 -1，并设置任务的
 [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno) 值，以指示原因。任务
 可以使用 [stdioGET_ERRNO()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO) API 函数
 获取其 errno 值。
