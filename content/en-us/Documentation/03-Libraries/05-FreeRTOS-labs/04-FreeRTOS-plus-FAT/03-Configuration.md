---
title: FreeRTOS-Plus-FAT Configuration
created: 2018-09-20
categories:
  - kernel
relatedLinks: 
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

The FreeRTOSFATConfig.h header file
  

Applications that use FreeRTOS-Plus-FAT must provide a FreeRTOSFATConfig.h header file -
in which the parameters described on this page can be defined:
   
* [ffconfigBYTE\_ORDER](#ffconfigbyte_order)
* [ffconfigHAS\_CWD](#ffconfighas_cwd)
* [ffconfigCWD\_THREAD\_LOCAL\_INDEX](#ffconfigcwd_thread_local_index)
* [ffconfigLFN\_SUPPORT](#ffconfiglfn_support)
* [ffconfigINCLUDE\_SHORT\_NAME](#ffconfiginclude_short_name)
* [ffconfigSHORTNAME\_CASE](#ffconfigshortname_case)
* [ffconfigUNICODE\_UTF16\_SUPPORT](#ffconfigunicode_utf16_support)
* [ffconfigUNICODE\_UTF8\_SUPPORT](#ffconfigunicode_utf8_support)
* [ffconfigFAT12\_SUPPORT](#ffconfigfat12_support)
* [ffconfigOPTIMISE\_UNALIGNED\_ACCESS](#ffconfigoptimise_unaligned_access)
* [ffconfigCACHE\_WRITE\_THROUGH](#ffconfigcache_write_through)
* [ffconfigWRITE\_BOTH\_FATS](#ffconfigwrite_both_fats)
* [ffconfigWRITE\_FREE\_COUNT](#ffconfigwrite_free_count)
* [ffconfigTIME\_SUPPORT](#ffconfigtime_support)
* [ffconfigREMOVABLE\_MEDIA](#ffconfigremovable_media)
* [ffconfigMOUNT\_FIND\_FREE](#ffconfigmount_find_free)
* [ffconfigFSINFO\_TRUSTED](#ffconfigfsinfo_trusted)
* [ffconfigPATH\_CACHE](#ffconfigpath_cache)
* [ffconfigPATH\_CACHE\_DEPTH](#ffconfigpath_cache_depth)
* [ffconfigHASH\_CACHE](#ffconfighash_cache)
* [ffconfigHASH\_FUNCTION](#ffconfighash_function)
* [ffconfigMKDIR\_RECURSIVE](#ffconfigmkdir_recursive)
* [ffconfigBLKDEV\_USES\_SEM](#ffconfigblkdev_uses_sem)
* [ffconfigMALLOC](#ffconfigmalloc)
* [ffconfigFREE](#ffconfigfree)
* [ffconfig64\_NUM\_SUPPORT](#ffconfig64_num_support)
* [ffconfigMAX\_PARTITIONS](#ffconfigmax_partitions)
* [ffconfigMAX\_FILE\_SYS](#ffconfigmax_file_sys)
* [ffconfigDRIVER\_BUSY\_SLEEP\_MS](#ffconfigdriver_busy_sleep_ms)
* [ffconfigFPRINTF\_SUPPORT](#ffconfigfprintf_support)
* [ffconfigFPRINTF\_BUFFER\_LENGTH](#ffconfigfprintf_buffer_length)
* [ffconfigINLINE\_MEMORY\_ACCESS](#ffconfiginline_memory_access)
* [ffconfigFAT\_CHECK](#ffconfigfat_check)
* [ffconfigMAX\_FILENAME](#ffconfigmax_filename)

---

#### ffconfigBYTE\_ORDER

Must be set to either pdFREERTOS\_LITTLE\_ENDIAN or pdFREERTOS\_BIG\_ENDIAN, depending
on the endian of the architecture on which FreeRTOS is running.
 

#### ffconfigHAS\_CWD

Set to 1 to maintain a current working directory (CWD) for each task that
accesses the file system, allowing relative paths to be used.
 
Set to 0 not to use a CWD, in which case full paths must be used for
each file access.
 

#### ffconfigCWD\_THREAD\_LOCAL\_INDEX

Set to an index within FreeRTOS's thread local storage array that is free for
use by FreeRTOS-Plus-FAT. FreeRTOS-Plus-FAT will use two consecutive indexes from this
that set by ffconfigCWD\_THREAD\_LOCAL\_INDEX. The number of thread local storage
pointers provided by FreeRTOS is set by configNUM\_THREAD\_LOCAL\_STORAGE\_POINTERS
in FreeRTOSConfig.h.
 
  
#### ffconfigLFN\_SUPPORT

Set to 1 to include long file name support. Set to 0 to exclude long
file name support.
 
If long file name support is excluded then only 8.3 file names can be used.
Long file names will be recognised, but ignored.
 
Users should familiarise themselves with any patent issues that may
potentially exist around the use of long file names in FAT file systems
before enabling long file name support.
 

#### ffconfigINCLUDE\_SHORT\_NAME

Only used when ffconfigLFN\_SUPPORT is set to 1.
 
Set to 1 to include a file's short name when listing a directory, i.e. when
calling findfirst()/findnext(). The short name will be stored in the 'pcShortName' field of FF\_DIRENT.
 
Set to 0 to only include a file's long name.
 

#### ffconfigSHORTNAME\_CASE

Set to 1 to recognise and apply the case bits used by Windows XP+ when
using short file names - storing file names such as "readme.TXT" or
"SETUP.exe" in a short-name entry. This is the recommended setting for
maximum compatibility.
 
Set to 0 to ignore the case bits.
 

#### ffconfigUNICODE\_UTF16\_SUPPORT

Only used when ffconfigLFN\_SUPPORT is set to 1.
 
Set to 1 to use UTF-16 (wide-characters) for file and directory names.
 
Set to 0 to use either 8-bit ASCII or UTF-8 for file and directory names
(see the ffconfigUNICODE\_UTF8\_SUPPORT).
 

#### ffconfigUNICODE\_UTF8\_SUPPORT

Only used when ffconfigLFN\_SUPPORT is set to 1.
 
Set to 1 to use UTF-8 encoding for file and directory names.
 
Set to 0 to use either 8-bit ASCII or UTF-16 for file and directory
names (see the ffconfig\_UTF\_16\_SUPPORT setting).
 

#### ffconfigFAT12\_SUPPORT

Set to 1 to include FAT12 support.
 
Set to 0 to exclude FAT12 support.
 
FAT16 and FAT32 are always enabled.
 

#### ffconfigOPTIMISE\_UNALIGNED\_ACCESS

When writing and reading data, i/o becomes less efficient if sizes other
than 512 bytes are being used. When set to 1 each file handle will
allocate a 512-byte character buffer to facilitate "unaligned access".
 

#### ffconfigCACHE\_WRITE\_THROUGH

Input and output to a disk uses buffers that are only flushed at the
following times:
 
* When a new buffer is needed and no other buffers are available.
* When opening a buffer in READ mode for a sector that has just been changed.
* After creating, removing or closing a file or a directory.

Normally this is quick enough and it is efficient. If
ffconfigCACHE\_WRITE\_THROUGH is set to 1 then buffers will also be flushed each
time a buffer is released - which is less efficient but more secure.
 

#### ffconfigWRITE\_BOTH\_FATS

In most cases, the FAT table has two identical copies on the disk,
allowing the second copy to be used in the case of a read error. If
 
Set to 1 to use both FATs - this is less efficient but more secure.
 
Set to 0 to use only one FAT - the second FAT will never be written to.
 

#### ffconfigWRITE\_FREE\_COUNT

Set to 1 to have the number of free clusters and the first free cluster
to be written to the FS info sector each time one of those values changes.
 
Set to 0 not to store these values in the FS info sector, making booting
slower, but making changes faster.
 

#### ffconfigTIME\_SUPPORT

Set to 1 to maintain file and directory time stamps for creation, modify
and last access.
 
Set to 0 to exclude time stamps.
 
If time support is used, the following function must be supplied:
 
```c
time_t FreeRTOS_time( time_t *pxTime );
```

FreeRTOS\_time has the same semantics as the standard time() function.
 

#### ffconfigREMOVABLE\_MEDIA

Set to 1 if the media is removable (such as a memory card).
 
Set to 0 if the media is not removable.
 
When set to 1 all file handles will be "invalidated" if the media is
extracted. If set to 0 then file handles will not be invalidated.
In that case the user will have to confirm that the media is still present
before every access.
 

#### ffconfigMOUNT\_FIND\_FREE

Set to 1 to determine the disk's free space and the disk's first free
cluster when a disk is mounted.
 
Set to 0 to find these two values when they are first needed. Determining
the values can take some time.


#### ffconfigFSINFO\_TRUSTED

Set to 1 to 'trust' the contents of the 'ulLastFreeCluster' and
ulFreeClusterCount fields.
 
Set to 0 not to 'trust' these fields.
 

#### ffconfigPATH\_CACHE

Set to 1 to store recent paths in a cache, enabling much faster access
when the path is deep within a directory structure at the expense of
additional RAM usage.
 
Set to 0 to not use a path cache.


#### ffconfigPATH\_CACHE\_DEPTH

Only used if ffconfigPATH\_CACHE is 1.
 
Sets the maximum number of paths that can exist in the patch cache at any
one time.
 

#### ffconfigHASH\_CACHE

Set to 1 to calculate a HASH value for each existing short file name.
Use of HASH values can improve performance when working with large
directories, or with files that have a similar name.
 
Set to 0 not to calculate a HASH value.


#### ffconfigHASH\_FUNCTION

Only used if ffconfigHASH\_CACHE is set to 1
 
Set to CRC8 or CRC16 to use 8-bit or 16-bit HASH values respectively.
 

#### ffconfigMKDIR\_RECURSIVE

Set to 1 to add a parameter to ff\_mkdir() that allows an entire directory
tree to be created in one go, rather than having to create one directory in
the tree at a time. For example mkdir( "/etc/settings/network", pdTRUE );.

Set to 0 to use the normal mkdir() semantics (without the additional
parameter).


#### ffconfigBLKDEV\_USES\_SEM

Set to 1 for each call to fnReadBlocks and fnWriteBlocks to be performed
with a semaphore lock.
 
Set to 0 for each call to fnReadBlocks and fnWriteBlocks not to use an
additional semaphore.
 

#### ffconfigMALLOC

Set to a function that will be used for all dynamic memory allocations.
Setting to pvPortMalloc() will use the same memory allocator as FreeRTOS.
For example:

```c
#define ffconfigMALLOC( size ) pvPortMalloc( size )
```


#### ffconfigFREE

Set to a function that matches the above allocator defined with
ffconfigMALLOC. Setting to vPortFree() will use the same memory free
function as FreeRTOS. For example:

```c
#define ffconfigFREE( ptr ) vPortFree( ptr )
```


#### ffconfig64\_NUM\_SUPPORT

Set to 1 to calculate the free size and volume size as a 64-bit number.

Set to 0 to calculate these values as a 32-bit number.
 

#### ffconfigMAX\_PARTITIONS

Defines the maximum number of partitions (and also logical partitions)
that can be recognised.
 

#### ffconfigMAX\_FILE\_SYS

Defines how many drives can be combined in total. Should be set to at
least 2.
 

#### ffconfigDRIVER\_BUSY\_SLEEP\_MS

In case the low-level driver returns an error 'FF\_ERR\_DRIVER\_BUSY',
the library will pause for a number of ms, defined in
ffconfigDRIVER\_BUSY\_SLEEP\_MS before re-trying.
 

#### ffconfigFPRINTF\_SUPPORT

Set to 1 to include the ff\_fprintf() function in the build.
 
Set to 0 to exclude the ff\_fprintf() function from the build.
 
ff\_fprintf() is quite a heavy function because it allocates RAM and
brings in a lot of string and variable argument handling code. If
ff\_fprintf() is not being used then the code size can be reduced by setting
ffconfigFPRINTF\_SUPPORT to 0.
 

#### ffconfigFPRINTF\_BUFFER\_LENGTH

ff\_fprintf() will allocate a buffer of this size in which it will create
its formatted string. The buffer will be freed before the function
exits.
 

#### ffconfigINLINE\_MEMORY\_ACCESS

Set to 1 to inline some internal memory access functions.
 
Set to 0 not to use inline memory access functions.
 

#### ffconfigFAT\_CHECK

Officially the only criteria to determine the FAT type (12, 16, or 32
bits) is the total number of clusters:
 
+ if( ulNumberOfClusters < 4085 ) : Volume is FAT12

+ if( ulNumberOfClusters < 65525 ) : Volume is FAT16

+ if( ulNumberOfClusters >= 65525 ) : Volume is FAT32

Not every formatted device follows the above rule.
 
Set to 1 to perform additional checks over and above inspecting the
number of clusters on a disk to determine the FAT type.
 
Set to 0 to only look at the number of clusters on a disk to determine the
FAT type.
 

#### ffconfigMAX\_FILENAME

Sets the maximum length for file names, including the path.
Note that the value of this define is directly related to the maximum stack
use of the +FAT library. In some API's, a character buffer of size 'ffconfigMAX\_FILENAME' will be 
declared on stack.
 
