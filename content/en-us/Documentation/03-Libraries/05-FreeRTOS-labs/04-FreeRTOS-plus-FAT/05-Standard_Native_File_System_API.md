---
title: FreeRTOS-Plus-FAT Standard and Native APIs
created: 2018-09-20
description: Overview of the FreeRTOS+FAT Standard and Native APIs
---

FreeRTOS-Plus-FAT is a [FreeRTOS Labs](/Documentation/03-Libraries/05-FreeRTOS-labs/01-Introduction) project. It is fully functional,
and quite mature, but as an originally acquired (rather than authored) product it does not necessarily
meet our production code or testing standards. It is available from
the [Lab-Project-FreeRTOS-FAT](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-FAT) repository on GitHub.

## FreeRTOS-Plus-FAT Standard and Native APIs

### Directory/Folder Functions

* [ff_mkdir()](Standard-API/ff_mkdir)
* [ff_chdir()](Standard-API/ff_chdir)
* [ff_rmdir()](Standard-API/ff_rmdir)
* [ff_getcwd()](Standard-API/ff_getcwd)


### File Read and Write Functions

* [ff_fopen()](Standard-API/ff_fopen)
* [ff_fclose()](Standard-API/ff_fclose)
* [ff_fwrite()](Standard-API/ff_fwrite)
* [ff_fread()](Standard-API/ff_fread)
* [ff_fputc()](Standard-API/ff_fputc)
* [ff_fgetc()](Standard-API/ff_fgetc)
* [ff_fgets()](Standard-API/ff_fgets)
* [ff_fprintf()](Standard-API/ff_fprintf)
* [ff_fseek()](Standard-API/ff_fseek)
* [ff_ftell()](Standard-API/ff_ftell)
* [ff_seteof()](Standard-API/ff_seteof)
* [ff_rewind()](Standard-API/ff_rewind)
* [ff_truncate()](Standard-API/ff_truncate)


### File Utility Functions

* [stdioGET_ERRNO()](Standard-API/errno)
* [ff_feof()](Standard-API/ff_feof)
* [ff_rename()](Standard-API/ff_rename)
* [ff_remove()](Standard-API/ff_remove)
* [ff_stat()](Standard-API/ff_stat)
* [ff_filelength()](Standard-API/ff_filelength)
* [ff_findfirst()](Standard-API/ff_findfirst)
* [ff_findnext()](Standard-API/ff_findnext)

## FreeRTOS-Plus-FAT Native APIs

### Disk Management Functions

* [FF_Partition()](Native-API/FF_Partition)
* [FF_Format()](Native-API/FF_Format)
* [FF_Mount()](Native-API/FF_Mount)
* [FF_FS_Add()](Native-API/FF_FS_Add)
