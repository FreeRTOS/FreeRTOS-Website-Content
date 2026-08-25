---
title: "ff_rmdir()"
description: FreeRTOS+FAT ff_rmdir API documentation
---
[FreeRTOS-Plus-FAT Standard API Reference](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
int ff_rmdir( const char *pcPath );
```

Remove a directory from the embedded FAT file system. A directory can
 only be removed if it does not contain any files.

## Parameters
+ *pcDirectory*

  A pointer to a standard null terminated C string that holds the name of the
  directory being removed. The string can include a relative path.

## Returns

If the directory was removed successfully then zero is returned.

If the directory could not be removed then -1 is returned and the task's
 [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno)
 is set to indicate the reason. A task can obtain it's errno value using the
 [stdioGET_ERRNO()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO) API function.

## Example usage

```c
void vExampleFunction( void )  
{  
    /* Create a sub directory called subfolder, and sub directory within  
       subfolder called sub1. */  
    ff_mkdir( "subfolder" );  
    ff_mkdir( "subfolder/sub1" );
    /* The directories can be accessed here. */
    /* Delete the two sub directories again. */  
    ff_rmdir( "subfolder/sub1" );  
    ff_rmdir( "subfolder" );  
}  
```
*Example use of the ff_rmdir() API function to delete a directory*
