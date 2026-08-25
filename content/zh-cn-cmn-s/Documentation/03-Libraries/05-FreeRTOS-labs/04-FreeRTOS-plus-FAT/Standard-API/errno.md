---
title: "标准 API errno 值"
description: FreeRTOS+FAT errno API 文档
---
[FreeRTOS-Plus-FAT 标准 API 引用](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)

FreeRTOS-Plus-FAT 文件系统的标准 API
与标准 C 库使用相同的 errno 值。标准 C 库中的文件相关函数返回 0 表示通过，返回 -1 则表示失败。如果返回 -1，则失败的原因
存储在名为 errno 的变量中，必须单独检查。

同样，FreeRTOS-Plus-FAT 的标准 API 返回 0 表示通过，返回 -1 则表示失败，
该 API 还会针对各项 RTOS 任务维护 errno 变量。任务可以通过调用 stdioGET_ERRNO() 来检索其 errno 值。stdioGET_ERRNO() 返回的错误代码在 `projdefs.h` 文件中定义，如下所示。

|  |  |  |
| --- | --- | --- |
| **值** | **常量** | **说明** |
| 0 | pdFREERTOS_ERRNO_NONE | 没有此文件或目录 |
| 2 | pdFREERTOS_ERRNO_ENOENT | 没有此文件或目录 |
| 5 | pdFREERTOS_ERRNO_EIO | I/O 错误 |
| 6 | pdFREERTOS_ERRNO_ENXIO | 没有此设备或地址 |
| 9 | pdFREERTOS_ERRNO_EBADF | 文件编号错误 |
| 11 | pdFREERTOS_ERRNO_EAGAIN | 没有更多进程 |
| 11 | pdFREERTOS_ERRNO_EWOULDBLOCK | 操作将阻塞 |
| 12 | pdFREERTOS_ERRNO_ENOMEM | 内核不足 |
| 13 | pdFREERTOS_ERRNO_EACCES | 权限被拒绝 |
| 14 | pdFREERTOS_ERRNO_EFAULT | 地址错误 |
| 16 | pdFREERTOS_ERRNO_EBUSY | 挂载设备繁忙 |
| 17 | pdFREERTOS_ERRNO_EEXIST | 文件存在 |
| 18 | pdFREERTOS_ERRNO_EXDEV | 跨设备链接 |
| 19 | pdFREERTOS_ERRNO_ENODEV | 没有此设备 |
| 20 | pdFREERTOS_ERRNO_ENOTDIR | 不是目录 |
| 21 | pdFREERTOS_ERRNO_EISDIR | 是目录 |
| 22 | pdFREERTOS_ERRNO_EINVAL | 无效实参 |
| 28 | pdFREERTOS_ERRNO_ENOSPC | 设备上没有剩余空间 |
| 29 | pdFREERTOS_ERRNO_ESPIPE | 非法搜索 |
| 30 | pdFREERTOS_ERRNO_EROFS | 只读文件系统 |
| 42 | pdFREERTOS_ERRNO_EUNATCH | 未连接协议驱动器 |
| 50 | pdFREERTOS_ERRNO_EBADE | 无效数据交换 |
| 79 | pdFREERTOS_ERRNO_EFTYPE | 文件类型或格式不当 |
| 89 | pdFREERTOS_ERRNO_ENMFILE | 没有更多文件 |
| 90 | pdFREERTOS_ERRNO_ENOTEMPTY | 目录不为空 |
| 91 | pdFREERTOS_ERRNO_ENAMETOOLONG | 文件或路径名称太长 |
| 95 | pdFREERTOS_ERRNO_EOPNOTSUPP | 传输端点上不支持的操作 |
| 105 | pdFREERTOS_ERRNO_ENOBUFS | 没有可用的缓冲区空间 |
| 109 | pdFREERTOS_ERRNO_ENOPROTOOPT | 协议不可用 |
| 112 | pdFREERTOS_ERRNO_EADDRINUSE | 地址已在使用中 |
| 116 | pdFREERTOS_ERRNO_ETIMEDOUT | 连接超时 |
| 119 | pdFREERTOS_ERRNO_EINPROGRESS | 连接已在进行中 |
| 120 | pdFREERTOS_ERRNO_EALREADY | 套接字已连接 |
| 125 | pdFREERTOS_ERRNO_EADDRNOTAVAIL | 地址不可用 |
| 127 | pdFREERTOS_ERRNO_EISCONN | 套接字已连接 |
| 128 | pdFREERTOS_ERRNO_ENOTCONN | 套接字未连接 |
| 135 | pdFREERTOS_ERRNO_ENOMEDIUM | 未插入媒体 |
| 138 | pdFREERTOS_ERRNO_EILSEQ | 遇到无效的 UTF-16 序列 |
| 140 | pdFREERTOS_ERRNO_ECANCELED | 操作已取消 |

 
原生 API errno 值
-----------------------
[FreeRTOS-Plus-FAT 原生 API 引用](/Documentation/03-Libraries/05-FreeRTOS-labs/04-FreeRTOS-plus-FAT/05-Standard_Native_File_System_API)


文件系统的原生 API 具有更复杂的错误代码系统，并直接通过其 API 函数返回错误代码。原生 API 使用的错误代码在 `ff_error.h` 中定义。
