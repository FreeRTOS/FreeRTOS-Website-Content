---
title: "ff_deltree()"
description: FreeRTOS+FAT ff_deltree API documentation
---
[FreeRTOS-Plus-FAT Standard API Reference](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
int ff_deltree( const char *pcDirectory )	
```
Remove a directory from the embedded FAT file system, and recursively all of the directory's contents.

## Parameters 
+ *pcDirectory*

  A pointer to a standard null terminated C string that holds the name of the
  directory being removed. The file name can include a relative path to the directory.

## Returns

If the directory and the directory's contents were removed then zero is 
 returned. Otherwise -1 is returned.
