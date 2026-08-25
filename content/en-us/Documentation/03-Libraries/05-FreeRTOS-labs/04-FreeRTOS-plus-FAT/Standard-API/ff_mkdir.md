---
title: "ff_mkdir()"
description: FreeRTOS+FAT ff_mkdir API documentation
---
[FreeRTOS-Plus-FAT Standard API Reference](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
int ff_mkdir( const char *pcDirectory );
```
Create a new directory in the embedded FAT file system.
 
## Parameters 
+ *pcDirectory*
  A pointer to a standard null terminated C string that holds the name of the
  directory being created. The string can include a relative path.

## Returns
If the directory was created successfully then zero is returned.

If the directory could not be created then -1 is returned and the task's
 [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno)
 is set to indicate the reason. A task can obtain its errno value using the
 [stdioGET_ERRNO()](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO)
 API function.

## Example usage 
```c
void vExampleFunction( void )
{
    /* Create a sub directory called subfolder. */
    ff_mkdir( "subfolder" );

    /* Create three subdirectories called sub1, sub2 and sub three respectively
       inside the subfolder directory. */
    ff_mkdir( "subfolder/sub1" );
    ff_mkdir( "subfolder/sub2" );
    ff_mkdir( "subfolder/sub3" );

    /* Move into the subfolder/sub1 directory. */
    ff_chdir( "subfolder/sub1" );

    /* Create another directory called sub4 inside the subfolder/sub1 directory. */
    ff_mkdir( "sub4" );
}
```
*Example use of the ff_mkdir() API function to create a directory*
