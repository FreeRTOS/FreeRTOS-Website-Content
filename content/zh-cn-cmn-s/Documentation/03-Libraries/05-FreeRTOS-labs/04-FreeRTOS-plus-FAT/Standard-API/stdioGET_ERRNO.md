---
title: "stdioGET_ERRNO()"
description: FreeRTOS+FAT stdioGET_ERRNO API 文档
---
[FreeRTOS-Plus-FAT 标准 API 引用](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

ff_stdio.h
```c
static portINLINE int stdioGET_ERRNO( void );
```

标准 C 库中的文件相关函数通常返回 0 表示成功，
-1 表示失败。如果返回 -1，则失败的原因
存储在名为 errno 的变量中，须单独检查。

FreeRTOS-Plus-FAT 的标准 stdio 样式接口为每项
RTOS 任务维护一个 errno 变量。static portINLINE() 返回
调用任务的 errno 值。

注意：
* 文件系统的 C 库样式 API 使用的 errno 值
  与标准 C 库所用的相同。这些值 
  [记录在单独的页面上](errno)。

* 文件系统的原生 API
  具有更复杂的错误代码体系，并  直接从其 API 函数返回错误代码。

## 用法示例

```c
void vAFunction( FF_FILE *pxFile, long lOffset, int iWhence )
{
    int iReturned;

    /* Attempt to seek a file using the parameters passed into this function. */
    iReturned = ff_fseek( pxFile, lOffset, iWhence );

    if( iReturned == 0 )
    {
        /* The call to ff_fseek() passed. */
    }
    else
    {
        /* The call to ff_fseek() failed. Obtain the errno to see why. */
        iReturned = stdioGET_ERRNO();

        if( iReturned == pdFREERTOS_ERRNO_ESPIPE )
        {
            /* The seek position was illegal - outside of the file's space. */
        }
        else if( iReturned == pdFREERTOS_ERRNO_EINVAL )
        {
            /* The value of iWhence was not legal. */
        }
    }
}
```
*stdioGET_ERRNO() API 函数的用法示例*
