---
title: MCUBoot Port API Reference
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


The bootloader can be ported to other hardware by implementing the following porting functions.
The port API can be found in `lib/mcuboot/boot/freertos/include/port`. Note, the
implementation of `flash_map_backend.h` is specific to MCUBoot, with documentation
available [here](https://github.com/mcu-tools/mcuboot/blob/main/docs/PORTING.md).


## Bootloader Porting API

#### Assertions

```c
/* Passed file name, line number, and function name of triggered assertion */
boot_port_assert_handler( const char *pcFile, int lLine, const char * pcFunc  );
```

This function defines the assert handler which can be exercised when `MCUBOOT_HAVE_ASSERT_H`
is set to 1 in `mcuboot_config.h`.


#### Heap

```c
/* Called prior to any heap usage, should the heap require setup */
void  boot_port_heap_init( void );

/* Perform standard malloc/free/realloc responsibilities */
void *boot_port_malloc( size_t size );
void  boot_port_free( void *mem );
void *boot_port_realloc( void *ptr, size_t size );
```

In the demo's default configuration, heap is unnecessary. However if the bootloader is instead
configured to use MBEDTLS, rather than TinyCrypt, the definitions above must implement the functions'
standard responsibilities.


#### Logging

```c
/* Configure HW so log messages output on choice channel */
void boot_port_log_init( void );

/* Primitive logging function that is built upon in mcuboot\_logging.h */
int vLog( const char *pcFormat, ...);
```

Logging can be omitted by setting `MCUBOOT_HAVE_LOGGING` to 0 in `mcuboot_config.h`.
Logging is enabled by default and the log level can also be modified by setting `MCUBOOT_LOG_LEVEL`
to any of the levels defined in `mcuboot_logging.h`.


#### Loader and Miscellaneous Hardware

```c
/* Called at start of bootloader configuring any extra desired hardware such as watchdog */
void boot_port_init( void );

/* Responsible for loading the application specified in rsp */
void boot_port_startup( struct boot_rsp *rsp );
```


#### Watchdog

```c
/* Feed the watchdog, resetting the watchdog timer */
void boot_port_wdt_feed( void );

/* Disable watchdog */
void boot_port_wdt_disable( void );
```

Watchdog protection is optional, but suggested. The application is expected to disable the bootloader
watchdog, to prevent it from being reset and potentially reverted.


## Serial Mode Porting API

The following porting functions are only required if `MCUBOOT_SERIAL` is set to 1 in `mcuboot_config.h`.
They can be omitted, leaving out interface capability with `mcumgr`.


#### UART Interface

```c
/* Initializes UART interface for mcumgr and gpio for serial boot pin */
void boot_port_serial_init( void );

/* Return true if serial boot pin was activated within some timeout */
bool boot_port_serial_detect_boot_pin( void );

/* Returns pointer to static structure with boot\_uart\_funcs defined */
const struct boot_uart_funcs * boot_port_serial_get_functions( void );
```

The `boot_uart_funcs` structure has two members, `.read` and `.write`.
The signatures for these two functions can be found in MCUBoot's `boot_serial.h`. One small
caveat is that the read function should operate in a `readline` fashion, setting its `*newline`
input argument to 1 upon reading a full line.


#### Encoding

```c
int base64_port_encode( char * dst, size_t dlen, size_t * olen, char * src, size_t slen );
int base64_port_decode( char * dst, size_t dlen, int * olen, char * src, size_t slen );
uint16_t crc16_port_ccitt( uint16_t crc, char * data, uint32_t len);
```

These functions are hardware independent and should be standardized in the FreeRTOS ecosystem soon.
For now, they have existing implementations that can be copied from this demo's `port` directory.


#### System Interface

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
