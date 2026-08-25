---
title: FreeRTOS-Plus-FAT 配置
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

FreeRTOSFATConfig.h 头文件
  

使用 FreeRTOS-Plus-FAT 的应用程序必须提供 FreeRTOSFATConfig.h 头文件，
用于定义此页面上描述的参数：
   
* [ffconfigBYTE_ORDER](#ffconfigbyte_order)
* [ffconfigHAS_CWD](#ffconfighas_cwd)
* [ffconfigCWD_THREAD_LOCAL_INDEX](#ffconfigcwd_thread_local_index)
* [ffconfigLFN_SUPPORT](#ffconfiglfn_support)
* [ffconfigINCLUDE_SHORT_NAME](#ffconfiginclude_short_name)
* [ffconfigSHORTNAME_CASE](#ffconfigshortname_case)
* [ffconfigUNICODE_UTF16_SUPPORT](#ffconfigunicode_utf16_support)
* [ffconfigUNICODE_UTF8_SUPPORT](#ffconfigunicode_utf8_support)
* [ffconfigFAT12_SUPPORT](#ffconfigfat12_support)
* [ffconfigOPTIMISE_UNALIGNED_ACCESS](#ffconfigoptimise_unaligned_access)
* [ffconfigCACHE_WRITE_THROUGH](#ffconfigcache_write_through)
* [ffconfigWRITE_BOTH_FATS](#ffconfigwrite_both_fats)
* [ffconfigWRITE_FREE_COUNT](#ffconfigwrite_free_count)
* [ffconfigTIME_SUPPORT](#ffconfigtime_support)
* [ffconfigREMOVABLE_MEDIA](#ffconfigremovable_media)
* [ffconfigMOUNT_FIND_FREE](#ffconfigmount_find_free)
* [ffconfigFSINFO_TRUSTED](#ffconfigfsinfo_trusted)
* [ffconfigPATH_CACHE](#ffconfigpath_cache)
* [ffconfigPATH_CACHE_DEPTH](#ffconfigpath_cache_depth)
* [ffconfigHASH_CACHE](#ffconfighash_cache)
* [ffconfigHASH_FUNCTION](#ffconfighash_function)
* [ffconfigMKDIR_RECURSIVE](#ffconfigmkdir_recursive)
* [ffconfigBLKDEV_USES_SEM](#ffconfigblkdev_uses_sem)
* [ffconfigMALLOC](#ffconfigmalloc)
* [ffconfigFREE](#ffconfigfree)
* [ffconfig64_NUM_SUPPORT](#ffconfig64_num_support)
* [ffconfigMAX_PARTITIONS](#ffconfigmax_partitions)
* [ffconfigMAX_FILE_SYS](#ffconfigmax_file_sys)
* [ffconfigDRIVER_BUSY_SLEEP_MS](#ffconfigdriver_busy_sleep_ms)
* [ffconfigFPRINTF_SUPPORT](#ffconfigfprintf_support)
* [ffconfigFPRINTF_BUFFER_LENGTH](#ffconfigfprintf_buffer_length)
* [ffconfigINLINE_MEMORY_ACCESS](#ffconfiginline_memory_access)
* [ffconfigFAT_CHECK](#ffconfigfat_check)
* [ffconfigMAX_FILENAME](#ffconfigmax_filename)

---

#### ffconfigBYTE_ORDER

必须设置为 pdFREERTOS_LITTLE_ENDIAN 或 pdFREERTOS_BIG_ENDIAN，取决
于 FreeRTOS 运行架构的 Endian。


#### ffconfigHAS_CWD

设置为 1，即可维护当前各项任务的工作目录 (CWD)，
该目录可访问文件系统，允许使用相对路径。

设置为 0，即可禁用 CWD，在这种情况下，必须使用完整路径
访问每个文件。


#### ffconfigCWD_THREAD_LOCAL_INDEX

设置为 FreeRTOS 线程本地存储数组中的索引，该索引可
由FreeRTOS-Plus-FAT 使用。FreeRTOS-Plus-FAT 将使用
由 ffconfigCWD_THREAD_LOCAL_INDEX 设置的两个连续索引。线程本地存储指针
由 FreeRTOS 提供，其数量由 configNUM_THREAD_LOCAL_STORAGE_POINTERS 进行设置，
位于 FreeRTOSConfig.h。
 
  
#### ffconfigLFN_SUPPORT

设置为 1，即可支持长文件名。设置为 0，即可排除长
文件名。

如果不支持长文件名，则只能使用 8.3 文件名。
长文件名可以被识别，但会被忽略。

用户应熟悉可能存在的任何专利问题，如果
在启用 FAT 文件系统长文件名支持之前使用了长文件名，
就可能存在此类专利问题。


#### ffconfigINCLUDE_SHORT_NAME

仅当 ffconfigLFN_SUPPORT 设置为 1 时使用。

设置为 1，即可包含当
调用 findfirst()/findnext() 列出目录时的短文件名。短名称将存储在 FF_DIRENT 的 “pcShortName” 字段中。

设置为 0，即可仅包含文件的长名称。


#### ffconfigSHORTNAME_CASE

设置为 1，即可识别和应用使用 Windows XP+ 使用的大小写位（
当使用短文件名或将文件名在短文件名条目中存储为 "readme.TXT" 或
"SETUP.exe" 时）。此为推荐的
最大兼容性设置。

设置为 0，即可忽略大小写位。


#### ffconfigUNICODE_UTF16_SUPPORT

仅当 ffconfigLFN_SUPPORT 设置为 1 时使用。

设置为 1 可将 UTF-16（宽字符）用于文件和目录名称。

设置为 0 可将 8 位 ASCII 或 UTF-8 用于文件和目录名称
（请参阅 ffconfigUNICODE_UTF8_SUPPORT）。


#### ffconfigUNICODE_UTF8_SUPPORT

仅当 ffconfigLFN_SUPPORT 设置为 1 时使用。

设置为 1 即可使用文件和目录名称的 UTF-8 编码。

设置为 0 可将 8 位 ASCII 或 UTF-16 用于文件和目录
名称（请参阅 ffconfig_UTF_16_SUPPORT 设置）。


#### ffconfigFAT12_SUPPORT

设置为1 以支持 FAT12。

设置为 0 以不再支持 FAT12。

FAT16 和 FAT32 始终启用。


#### ffconfigOPTIMISE_UNALIGNED_ACCESS

当写入和读取数据时，如果使用了
512 字节以外的大小，输入/输出效率将降低。当设置为 1 时，每个文件句柄将
分配 512 字节的字符缓冲区以便于进行“非对齐访问”。


#### ffconfigCACHE_WRITE_THROUGH

输入和输出到磁盘所使用的缓冲区仅在
以下情况刷新：

* 当需要新的缓冲区且没有其他缓冲区可用时。
* 在读取模式下，为刚刚更改的扇区打开缓冲区时。
* 创建、删除或关闭文件或目录后。

一般来说，这个过程快速且高效。如果
ffconfigCACHE_WRITE_THROUGH 设置为 1，则缓冲区也将在每次释放缓冲区时刷新，
这种做法效率较低，但更安全。


#### ffconfigWRITE_BOTH_FATS

在大多数情况下， FAT 表在磁盘上有两个相同的副本，
可以在读取错误的情况下使用第二个副本。如果

设置为 1，即可使用两个 FAT，这样效率较低，但更安全。

设置为 0，即可仅使用一个 FAT，第二个 FAT 将永远不会被写入。


#### ffconfigWRITE_FREE_COUNT

设置为 1，即可使空闲簇数量和第一个空闲簇在每当其中有值发生变化时
被写入 FS 信息扇区。

设置为 0，即不将这些值存储在 FS 信息扇区中，会使启动
变慢，但更改速度更快。


#### ffconfigTIME_SUPPORT

设置为 1，即可维护文件和目录时间戳以进行创建、修改
和最后访问。

设置为 0，即可排除时间戳。

如果使用时间支持，则必须提供以下函数：

```c
time_t FreeRTOS_time( time_t *pxTime );

```

与标准 time() 函数语义相同的 FreeRTOS_time。


#### ffconfigREMOVABLE_MEDIA

如果媒体是可移除的（例如内存卡），则设置为 1。

如果媒体不可移除，则设置为 0。

当设置为 1 时，如果媒体已被移除，则
所有文件句柄都将被“无效化”。如果设置为 0 ，则文件句柄将不会被无效化。
在这种情况下，用户必须确认媒体在每次访问前
仍然存在。


#### ffconfigMOUNT_FIND_FREE

设置为 1，即可确认磁盘安装时的可用空间和其第一个空闲簇
。

设置为 0，即可在首次需要这两个值时查找确定
这些值可能需要一些时间。



#### ffconfigFSINFO_TRUSTED

设置为 1，即可“信任”ulLastFreeCluster 以及
ulFreeClusterCount 字段的内容。

设置为 0，即为不“信任”上述字段。


#### ffconfigPATH_CACHE

设置为 1，即可在缓存中存储最近的路径，从而
当路径位于目录结构体深处并需要使用
额外 RAM 时实现更快的访问。

设置为 0，则不使用路径缓存。



#### ffconfigPATH_CACHE_DEPTH

仅在 ffconfigPATH_CACHE 为 1 时使用。

设置补丁缓存中在任何时间点可以同时存在的最大路径数
。


#### ffconfigHASH_CACHE

设置为 1，即可计算每个现有短文件名的哈希值。
使用哈希值可以提高处理大型
目录或具有相似名称文件时的工作性能。

设置为 0，则不计算哈希值。


#### ffconfigHASH_FUNCTION

仅在 ffconfigHASH_CACHE 设置为 1 时使用。

设置为 CRC8 或 CRC16，即可分别使用 8 位或 16 位哈希值。


#### ffconfigMKDIR_RECURSIVE

设置为 1，即可向 ff_mkdir() 添加允许一次性创建整个目录树的参数，
而不必每次都在目录树中创建一个目录
。例如 mkdir( "/etc/settings/network", pdTRUE );。

设置为 0，即可使用普通 mkdir() 语义（不含其他
参数）。


#### ffconfigBLKDEV_USES_SEM

设置为 1，则每次调用 fnReadBlocks 和 fnWriteBlocks 时
均使用信号量锁。

设置为 0，则每次调用 fnReadBlocks 和 fnWriteBlocks 时不使用
额外信号量。


#### ffconfigMALLOC

设置一个函数，用于所有动态内存的分配。
设置为 pvPortMalloc()，则使用与 FreeRTOS 相同的内存分配器。
例如：

```c
#define ffconfigMALLOC( size ) pvPortMalloc( size )
```


#### ffconfigFREE

设置函数，与上述用 ffconfigMALLOC 定义的分配符相匹配
。设置为 vPortFree()，则将使用的内存释放函数
与 FreeRTOS 相同。例如：

```c
#define ffconfigFREE( ptr ) vPortFree( ptr )
```


#### ffconfig64_NUM_SUPPORT

设置为 1，即可以 64 位数计算空闲大小和卷大小。

设置为 0，即可以 32 位数计算上述的值。


#### ffconfigMAX_PARTITIONS

定义可识别分区的最大数量（以及逻辑分区）
。


#### ffconfigMAX_FILE_SYS

定义可组合的驱动器总数。应设置为
至少 2 个。


#### ffconfigDRIVER_BUSY_SLEEP_MS

如果低层次驱动器返回错误 "FF_ERR_DRIVER_BUSY"，
库将暂停若干毫秒，在重试前定义于
FFCONFIGDRIVER_BUSY_SLEEP_MS。


#### ffconfigFPRINTF_SUPPORT

设置为1，包含构建中的 ff_fprintf() 函数。

设置为 0，从构建中排除 ff_fprintf() 函数。

ff_fprintf() 是一个较重的函数，因为其可分配 RAM 并
引入大量字符串和变量参数处理代码。如果未使用
ff_fprintf()，则可通过设置
ffconfigFPRINTF_SUPPORT 为 0 来缩短代码。


#### ffconfigFPRINTF_BUFFER_LENGTH

ff_fprintf() 将分配一个此大小的缓冲区，并创建
其格式化字符串。缓冲区将在函数退出之前被释放
。


#### ffconfigINLINE_MEMORY_ACCESS

设置为 1，即可内联一些内部内存访问函数。

设置为 0，则不使用内联内存访问函数。


#### ffconfigFAT_CHECK

正式确认 FAT 类型的唯一标准（12、16 或 32 位）
为总簇数：

+ 如果 ( ulNumberOfClusters < 4085 )：卷为 FAT12

+ 如果 ( ulNumberOfClusters < 65525 ) ：卷为 FAT16

+ 如果 ( ulNumberOfClusters >= 65525 )：卷为 FAT32

并非所有格式化设备都遵循上述规则。

设置为 1，即可执行除检查
磁盘用于确定 FAT 类型的簇数量以外的额外检查。

设置为 0，则仅查看磁盘用于确定 FAT 类型的簇数量
。


#### ffconfigMAX_FILENAME

设置文件名（包括路径）的最大长度。
请注意，此定义的值与
+FAT 库使用的最大堆栈数量直接相关。在某些 API 中，大小为 'ffconfigMAX_FILENAME' 的字符缓冲区将 
在堆栈上声明。

