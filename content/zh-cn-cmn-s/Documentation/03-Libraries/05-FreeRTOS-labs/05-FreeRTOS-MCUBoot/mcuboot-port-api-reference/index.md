---
title: MCUBoot 移植 API 引用
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


通过实现以下移植函数，可将 Bootloader 移植到其他硬件上。
移植 API 位于 `lib/mcuboot/boot/freertos/include/port`。请注意，
`flash_map_backend.h` 的实现特定于 MCUBoot，相关文档
参见[此处](https://github.com/mcu-tools/mcuboot/blob/main/docs/PORTING.md)。


## 引导加载程序移植 API

#### 断言

```c
/* Passed file name, line number, and function name of triggered assertion */
boot_port_assert_handler( const char *pcFile, int lLine, const char * pcFunc  );
```

此函数定义了 `MCUBOOT_HAVE_ASSERT_H`
在 `mcuboot_config.h` 中设置为 1 时可以执行的断言处理程序。


#### 堆

```c
/* Called prior to any heap usage, should the heap require setup */
void  boot_port_heap_init( void );

/* Perform standard malloc/free/realloc responsibilities */
void *boot_port_malloc( size_t size );
void  boot_port_free( void *mem );
void *boot_port_realloc( void *ptr, size_t size );
```

在演示的默认配置中，并不需要堆。但是，如果将引导加载程序
配置为使用 MBEDTLS，而不是 TinyCrypt ，则上述定义必须实现函数的
标准职责。


#### 日志记录

```c
/* Configure HW so log messages output on choice channel */
void boot_port_log_init( void );

/* Primitive logging function that is built upon in mcuboot_logging.h */
int vLog( const char *pcFormat, ...);
```

可以通过在 `mcuboot_config.h` 中将 `MCUBOOT_HAVE_LOGGING` 设置为 0 来省略日志记录。
默认情况下，日志记录处于启用状态，也可以将 `MCUBOOT_LOG_LEVEL` 设置为
`mcuboot_logging.h` 中定义的任何级别来修改日志级别。


#### 加载器和其他硬件

```c
/* Called at start of bootloader configuring any extra desired hardware such as watchdog */
void boot_port_init( void );

/* Responsible for loading the application specified in rsp */
void boot_port_startup( struct boot_rsp *rsp );
```


#### 看门狗 (Watchdog)

```c
/* Feed the watchdog, resetting the watchdog timer */
void boot_port_wdt_feed( void );

/* Disable watchdog */
void boot_port_wdt_disable( void );
```

看门狗保护为可选，但建议使用。应用程序应禁用引导加载程序看门狗，
以防止其被重置并可能还原。


## 串行模式移植 API

仅在 `mcuboot_config.h` 中将 `MCUBOOT_SERIAL`设置为 1 时才需要下列移植函数。
这些函数可以省略，从而省略与 `mcumgr` 接口的功能。


#### UART 接口

```c
/* Initializes UART interface for mcumgr and gpio for serial boot pin */
void boot_port_serial_init( void );

/* Return true if serial boot pin was activated within some timeout */
bool boot_port_serial_detect_boot_pin( void );

/* Returns pointer to static structure with boot_uart_funcs defined */
const struct boot_uart_funcs * boot_port_serial_get_functions( void );
```

`boot_uart_funcs` 结构体有两个成员：`.read` 和 `.write`。
可在 MCUBoot 的 `boot_serial.h` 中找到这两个函数的签名。需要注意的是，
读取函数应以 `readline` 的方式运行，在读取整行时将其 `*newline`
输入实参设置为 1。


#### 编码

```c
int base64_port_encode( char * dst, size_t dlen, size_t * olen, char * src, size_t slen );
int base64_port_decode( char * dst, size_t dlen, int * olen, char * src, size_t slen );
uint16_t crc16_port_ccitt( uint16_t crc, char * data, uint32_t len);
```

这些函数独立于硬件，应很快会在 FreeRTOS 生态系统中实现标准化。
目前，它们已有实现，这些实现可从此演示的 `port` 目录中复制。


#### 系统接口

```c
/* Converts x from big endian to system's endianness */
uint16_t system_port_ntohs( uint16_t x );

/* Converts x from system endianness to big endian */
uint16_t system_port_htons( uint16_t x );

/* Sleep the device for usec microseconds */
void system_port_usleep( uint32_t usec );

/* Trigger a soft reset of the device */
void system_port_reset( void );
```
