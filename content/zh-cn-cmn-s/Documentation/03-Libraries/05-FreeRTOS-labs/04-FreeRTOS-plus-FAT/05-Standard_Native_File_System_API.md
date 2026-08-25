---
title: FreeRTOS-Plus-FAT 标准和原生 API
created: 2018-09-20 00:00:00.0 UTC
description: FreeRTOS+ FAT 标准和原生 API 概述
---

FreeRTOS-Plus-FAT 是一个 [FreeRTOS Labs](/Documentation/03-Libraries/05-FreeRTOS-labs/01-Introduction) 项目。虽然功能齐全，
相当成熟，但它是收购过来的产品（不是我们自己编写的），因此不一定
符合我们的生产代码或测试标准。它可从
GitHub 上的 [Lab-Project-FreeRTOS-FAT](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-FAT) 存储库获得。

## FreeRTOS-Plus-FAT 标准和原生 API

### 目录/文件夹函数

* [ff_mkdir()](Standard-API/ff_mkdir)
* [ff_chdir()](Standard-API/ff_chdir)
* [ff_rmdir()](Standard-API/ff_rmdir)
* [ff_getcwd()](Standard-API/ff_getcwd)


### 文件读写函数

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


### 文件实用程序函数

* [stdioGET_ERRNO()](Standard-API/errno)
* [ff_feof()](Standard-API/ff_feof)
* [ff_rename()](Standard-API/ff_rename)
* [ff_remove()](Standard-API/ff_remove)
* [ff_stat()](Standard-API/ff_stat)
* [ff_filelength()](Standard-API/ff_filelength)
* [ff_findfirst()](Standard-API/ff_findfirst)
* [ff_findnext()](Standard-API/ff_findnext)

## FreeRTOS-Plus-FAT 原生 API

### 磁盘管理函数

* [FF_Partition()](Native-API/FF_Partition)
* [FF_Format()](Native-API/FF_Format)
* [FF_Mount()](Native-API/FF_Mount)
* [FF_FS_Add()](Native-API/FF_FS_Add)
