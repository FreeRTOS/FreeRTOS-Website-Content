---
title: FreeRTOS+POSIX
---

**注意**：FreeRTOS-Plus-POSIX 是由 [FreeRTOS Labs](/Documentation/03-Libraries/05-FreeRTOS-labs/01-Introduction) 开发的项目，希望对您有所帮助。该项目并不是完整的 pthreads 实现，也不一定符合产品级代码质量标准。FreeRTOS-Plus-POSIX 可在
GitHub 上的 [Lab-Project-FreeRTOS-POSIX](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-POSIX) 存储库中找到。

## 引言
可移植操作系统接口 (POSIX) 是 IEEE 计算机学会为维护操作系统之间的兼容性而指定的一系列标准。FreeRTOS-Plus-POSIX 可实现 [POSIX 线程 API](http://pubs.opengroup.org/onlinepubs/7908799/xsh/threads.html) 的*小*子集。借助此子集，熟悉 POSIX API 的应用程序开发者可使用类似线程原语的 POSIX 开发 FreeRTOS 应用程序。FreeRTOS-Plus-POSIX 仅实现了约 20% 的 POSIX API。因此，无法仅使用此包装器将现有的 POSIX 兼容应用程序或 POSIX 兼容库移植到 FreeRTOS 内核上运行。

![FreeRTOS 架构描述](/media/2019/POSIX.jpg)

**与 [FreeRTOS](/Why-FreeRTOS/FAQs/Amazon) 库一起使用时的 FreeRTOS-Plus-POSIX 位置**

## 预配置示例项目

FreeRTOS-Plus-POSIX 预配置示例在单独的 [zip 文件下载](/media/2019/190820_FreeRTOS_plus_POSIX_demo.zip)中提供。

## 当前支持的功能

FreeRTOS-Plus-POSIX 实现了 [IEEE 标准 1003.1-2017 版《开放组技术标准基础规范》，第 7 期](http://pubs.opengroup.org/onlinepubs/9699919799/)的部分内容。FreeRTOS-Plus-POSIX 包括以下 POSIX 线程标头文件的实现，请参阅 [FreeRTOS-Plus-POSIX API 文档](/Documentation/03-Libraries/05-FreeRTOS-labs/03-FreeRTOS-plus-POSIX/01-API-Reference/00-API-Reference)详细了解每个标头文件中支持的功能：

| * errno.h<br/>* fcntl.h<br/>* mqueue.h<br/>* pthread.h<br/>* sched.h<br/>* semaphore.h<br/> | * signal.h<br/>* sys/types.h<br/>* time.h<br/>* unistd.h<br/>* utils.h<br/> |
| --- | --- |

## FreeRTOS-Plus-POSIX 源代码组织
移植相关标头和实现源代码

```
/lib/FreeRTOS-Plus-POSIX
        |-- include
        |   |
        |   +- FreeRTOS_POSIX.h
        |   +- FreeRTOS_POSIX_internal.h
        |   +- FreeRTOS_POSIX_types.h
        |   +- portable
        |        |
        |        +- [target]
        |        |    |
        |        |    +- [development board]
        |        |            |
        |        |            +- FreeRTOS_POSIX_portable.h
        |        |
        |        +- FreeRTOS_POSIX_portable_default.h
        |
        +- source
            +- FreeRTOS_POSIX_clock.c
            +- FreeRTOS_POSIX_mqueue.c
            +- FreeRTOS_POSIX_pthread_barrier.c
            +- FreeRTOS_POSIX_pthread.c
            +- FreeRTOS_POSIX_pthread_cond.c
            +- FreeRTOS_POSIX_pthread_mutex.c
            +- FreeRTOS_POSIX_sched.c
            +- FreeRTOS_POSIX_semaphore.c
            +- FreeRTOS_POSIX_timer.c
            +- FreeRTOS_POSIX_unistd.c
            +- FreeRTOS_POSIX_utils.c
```

FreeRTOS-Plus-POSIX 标头
```
	/lib/include/FreeRTOS_POSIX
                    +- errno.h
                    +- fcntl.h
                    +- mqueue.h
                    +- pthread.h
                    +- sched.h
                    +- semaphore.h
                    +- signal.h
                    +- sys
                    |    |
                    |    +- types.h
                    |
                    +- time.h
                    +- unistd.h
                    +- utils.h
```

## 依赖

在 [FreeRTOSConfig.h](/Documentation/02-Kernel/03-Supported-devices/02-Customization) 中，configUSE_POSIX_ERRNO 和 configUSE_APPLICATION_TASK_TAG 均须设置为 1。

## 开发者参考和 API 文档
请参阅 [API 引用](01-API-Reference/00-API-Reference)。

## 移植
### 移植相关头文件

| **FreeRTOS 平台特定的 POSIX 配置** | **高级描述** |
| --- | --- |
| include/FreeRTOS_POSIX.h | 此标头文件包含 FreeRTOS-Plus-POSIX 所需的依赖项。此文件必须在所有其他 FreeRTOS-Plus-POSIX 之前包含。 |
| include/FreeRTOS_POSIX_internal.h | FreeRTOS-Plus-POSIX 的内部结构体和初始化器。建议用户不要更改此文件。 |
| include/FreeRTOS_POSIX_portable_default.h | FreeRTOS-Plus-POSIX 移植特定配置默认值。 |
| include/portable/[vendor-directory]/FreeRTOS_POSIX_portable.h | FreeRTOS-Plus-POSIX 移植特定配置覆写。例如，include/portable/pc/windows/FreeRTOS_POSIX_portable.h，Windows 模拟器使用默认值，因此不需要覆写任何内容。 |

### FreeRTOS-Plus-POSIX 包含路径
* /lib/FreeRTOS-Plus-POSIX/include
* /lib/FreeRTOS-Plus-POSIX/source
* /lib/include/FreeRTOS_POSIX/

请注意，项目只需要来自此路径 `/lib/FreeRTOS-Plus-POSIX/include/portable` 的平台特定标头。

## 代码大小（以字节为单位）

| 文件 | 优化关闭 | 优化开启 |
| --- | --- | --- |
| FreeRTOS_POSIX_clock.c | 412 | 296 |
| FreeRTOS_POSIX_mqueue.c | 2016 | 1612 |
| FreeRTOS_POSIX_pthread_barrier.c | 294 | 200 |
| FreeRTOS_POSIX_pthread.c | 980 | 660 |
| FreeRTOS_POSIX_pthread_cond.c | 696 | 496 |
| FreeRTOS_POSIX_pthread_mutex.c | 848 | 608 |
| FreeRTOS_POSIX_sched.c | 48 | 32 |
| FreeRTOS_POSIX_semaphore.c | 540 | 380 |
| FreeRTOS_POSIX_timer.c | 972 | 788 |
| FreeRTOS_POSIX_unistd.c | 92 | 68 |
| FreeRTOS_POSIX_utils.c | 1152 | 768 |
\| 总计 \| 8050 \| 5908 \|  \|
