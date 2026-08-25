---
title: "ff_chdir()"
description: FreeRTOS+FAT ff_chdir API 文档
---
[FreeRTOS-Plus-FAT 标准 API 引用](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
int ff_chdir( const char *pcDirectoryName );	
```

更改嵌入式 FAT 文件系统中的当前工作目录。

## 参数
+ *pcDirectoryName*

  指向以 null 结尾的标准 C 字符串的指针，该字符串保存
  目录名称以生成当前工作目录。该字符串可包含
  相对路径。

## 返回
如果当前工作目录已更改成功，则返回零。

如果当前工作目录无法更改，则返回 -1，并
 可设置任务的 [errno](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/errno)
 以指示原因。任务 可使用
 [stdioGET_ERRNO](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/Standard-API/stdioGET_ERRNO)
 API 函数获取其 errno 值。

## 用法示例
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
*通过 ff_chdir() API 函数打开或创建文件的使用示例*
