---
title: "ff_chdir()"
description: FreeRTOS+FAT ff_chdir API documentation
---
[FreeRTOS-Plus-FAT Standard API Reference](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
int ff_chdir( const char *pcDirectoryName );	
```

Change the current working directory in the embedded FAT file system.

## Parameters
+ *pcDirectoryName*

  A pointer to a standard null terminated C string that holds the name of the
  directory to make the current working directory. The string can include a
  relative path.

## Returns
If the current working directory was changed successfully then zero is returned.

If the current working directory could not be changed then -1 is returned and
 the task's [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno)
 may be set to indicate the reason. A task can obtain its errno value using the
 [stdioGET_ERRNO](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO)
 API function.

## Example usage
```c
void vExampleFunction( void )  
{  
    /* Create a sub directory called subfolder. */  
    ff_mkdir( "subfolder" );

    /* Create a in subfolder called sub1. */  
    ff_mkdir( "subfolder/sub1" );

    /* Make subfolder/sub1 the current working directory. */  
    ff_chdir( "subfolder/sub1" );

    /* Make the route directory the current working directory again. This could
       also have used ff_chdir( "/" ); */
    ff_chdir( "../.." );  
}  
```
*Example use of the ff_chdir() API function to open or create a file*
