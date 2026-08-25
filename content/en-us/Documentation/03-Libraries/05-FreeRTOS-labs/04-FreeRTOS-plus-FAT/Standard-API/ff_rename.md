---
title: "ff_rename()"
description: FreeRTOS+FAT ff_rename API documentation
---
[FreeRTOS-Plus-FAT Standard API Reference](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
int ff_rename( const char *pcOldName, const char *pcNewName );
```

Moves a file. A file can be moved across directories, but not across
file systems.

## Parameters
+ *pcOldName*

  A pointer to a standard null terminated C string that holds the name of the
  source file. The string can contain a relative path.

+ *pcNewName*

  A pointer to a standard null terminated C string that holds the
  name of the destination file. The string can contain a relative path.

## Returns

If the file is moved successfully then zero is returned.

If the file could not be moved then -1 is returned and the task's
 [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno)
 is set to indicate the reason. A task can obtain its errno value using the
 [stdioGET_ERRNO()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO)
 API function.
