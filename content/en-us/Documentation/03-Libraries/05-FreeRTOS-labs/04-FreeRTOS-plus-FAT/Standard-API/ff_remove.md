---
title: "ff_remove()"
description: FreeRTOS+FAT ff_remove API documentation
---
[FreeRTOS-Plus-FAT Standard API Reference](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
int ff_remove( const char *pcPath );
```
Remove (delete, or unlink) a file from the embedded FAT file system. A file
 cannot be removed if it is open.

## Parameters
+ *pcDirectory*

  A pointer to a standard null terminated C string that holds the name of the
  file being removed. The file name can include a relative path to the 
  directory.

## Returns
If the file was removed successfully then zero is returned.

If the file could not be removed then NULL is returned and the task's
 [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno)
 is set to indicate the reason. A task can obtain its errno value using the
 [stdioGET_ERRNO()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO)
 API function. A file cannot be removed if it is open.

## Example usage

```c
void vExampleFunction( void )
{
    /* Delete a file. */
    ff_remove( "/ram1/filename.txt" );
}
```
*Example use of the ff_remove() API function to delete a file*
