---
title: 日志记录功能
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

以下 FreeRTOS 库使用日志记录功能：

* [coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT)
* [coreHTTP](/Documentation/03-Libraries/03-FreeRTOS-core/04-coreHTTP/01-coreHTTP)
* [corePKCS11](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/01-corePKCS11)
* [AWS IoT Device Shadow](/Documentation/03-Libraries/04-AWS-libraries/03-AWS-IoT-Device-Shadow/01-AWS-IoT-device-shadow)
* [AWS IoT Device Defender](/Documentation/03-Libraries/04-AWS-libraries/05-AWS-IoT-Device-Defender/01-AWS-IoT-device-defender)


## 日志记录宏

FreeRTOS 库使用以下 4 个日志记录宏，按详细程度递增的顺序排列。
例如，LogError() 仅在出现错误时调用，因此最不详细；而 `LogDebug()`
被频繁调用以提供调试级别信息，因此最详细。

* LogError
* LogWarn
* LogInfo
* LogDebug

在使用时，日志记录宏可以像 printf() 一样接受可变数量的实参，
只不过需要使用双括号。例如，库以如下方式调用日志记录宏：

```c
LogInfo( ( “This prints an integer %d”, 100 ) );
```

您无需单独定义这四个日志记录宏。包含位于 `FreeRTOS-Plus/Source/Utilities/logging/` 路径下的
logging_stack.h 头文件后，只需定义一个名为 `SdkLog()` 的宏，即可将其应用于
所有四个详细级别。完成此操作后，
可通过定义 LIBRARY_LOG_LEVEL 单独设置详细级别，如下所述。


**注意**本页末尾代码片段中的头文件顺序。


###  定义 SdkLog 宏

应在正在使用的库的配置文件中包含 `logging_stack.h` 头文件，
并定义日志记录配置宏。例如，要从 coreMQTT 库获取日志输出结果，
需要在 `core_mqtt_config.h` 中包含 `logging_stack.h` 并定义日志记录宏。

要获取日志记录，必须定义 SkdLog() 以调用线程安全平台特定的打印函数。例如，
打印函数可能会将字符输出到串行端口或 TCP 套接字。由于日志记录宏
接受可变数量的参数，并且使用方式与 printf() 相同，因此平台特定的
打印函数必须具有与 printf() 相同的原型（参数列表）。例如，如果您的应用程序具有
对串行端口写入的 printf() 的线程安全版本，则可以将 SdkLog 定义为：

```c
#define SdkLog( X ) printf X
```

未定义的日志记录宏默认为空宏，不生成任何代码。

**注意：**如果不使用
[FreeRTOS-Plus/Source/Utilities/logging/](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Source/Utilities/logging) 中的日志记录实用程序标头，
则可以通过在您的应用程序中定义宏来为您想要的日志记录级别单独定义四个日志记录宏，
但不推荐这种方法，因为这样会阻止 LIBRARY_LOG_LEVEL
和 LIBRARY_LOG_NAME 发挥作用。


### 设置详细级别

若要设置详细级别，在用于定义 SdkLog() 的同一配置文件中，
将 LIBRARY_LOG_LEVEL 宏定义为以下任一值。LIBRARY_LOG_LEVEL 的有效值包括：

* LOG_NONE（关闭日志记录）
* LOG_ERROR
* LOG_WARN
* LOG_INFO
* LOG_DEBUG

例如：

```c
#define LIBRARY_LOG_LEVEL  LOG_NONE
```


###  设置文本名称

要设置文本名称，请在用于定义 SdkLog() 的同一配置文件中
将 LIBRARY_LOG_NAME 宏定义为字符串。每条日志消息都会打印名称，因此通常将名称设置为
库的名称。例如：

```c
#define LIBRARY_LOG_NAME “MQTT”
```

将名称设置为空字符串可节省程序空间。


### 设置日志中的元数据

要在日志消息中添加元数据（如日志消息的源代码位置），可以定义 LOG_METADATA_FORMAT
和 LOG_METADATA_ARGS 宏。

LOG_METADATA_FORMAT 宏应被定义为表示元数据格式字符串，
而 LOG_METADATA_ARGS 宏应被定义为传递格式字符串的元数据实参。
在传递给为 SdkLog 宏定义的平台特定打印函数的日志消息中，
这两个宏都有前缀。

例如，以下定义添加了发出日志消息的源文件的
函数名称和行号文件。

* #define LOG_METADATA_FORMAT “[%s:%d]”
* #define LOG_METADATA_ARGS \_\_FUNCTION\_\_, \_\_LINE\_\_

将元数据宏设置为空值可节省程序空间。


### 参考示例

请注意，在下面的示例链接和模板代码中，日志记录宏定义周围有 `#ifndef` 保护符
。这些都是为了避免在包含多个配置文件的转换单元中
对同一个宏进行多次定义。（例如，MutualAuthMQTTExample.c 直接包含 `demo_config.h`，
并通过 core_mqtt.h 间接包含 core_mqtt_config.h。）对于这种情况，
务必确保在应用程序代码文件开头（即在包含其他头文件之前）先包含相关配置文件，即含有
受影响转换单元文件日志记录配置的配置文件，
以应用正确的配置。

有关 FreeRTOS 代码库中日志记录配置的示例，请参阅
[基于 TLS 的 MQTT 双向验证](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication) 演示，  该演示
在
[demo_config.h](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Mutual_Auth/demo_config.h#L33-L54) 文件中为演示应用程序任务（在 MutualAuthMQTTExample.c 中定义）配置了日志记录，
并在
[core_mqtt_config.h](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Mutual_Auth/demo_config.h) 文件中为 coreMQTT 库配置了日志记录
。

以下是使用日志记录配置的模板。

```c
/**************************************************/
/******* DO NOT CHANGE the following order ********/
/**************************************************/

/* Include logging header files and define logging configurations in the
 * following order:
 * 1. Include the header file "logging_levels.h".
 * 2. Define the logging configurations for your application. It is required
 *    to define LIBRARY_LOG_NAME, LIBRARY_LOG_LEVEL and SdkLog macros.
 * 3. Include the header file "logging_stack.h".
 */

#include "logging_levels.h"

/* Logging configurations for the application. */

/* Set the application log name. */
#ifndef LIBRARY_LOG_NAME
    #define LIBRARY_LOG_NAME "MyApplication"
#endif

/* Set the logging verbosity level. */
#ifndef LIBRARY_LOG_LEVEL
    #define LIBRARY_LOG_LEVEL LOG_INFO
#endif

/* Define the metadata information to add in each log.
 * The example here sets the metadata to [:]. */
#if !defined( LOG_METADATA_FORMAT ) && !defined( LOG_METADATA_ARGS )
    #define LOG_METADATA_FORMAT "[%s:%d]"
    #define LOG_METADATA_ARGS __FILE__, __LINE__
#endif

/* Define the platform-specific logging function to call from
 * enabled logging macros. */
#ifndef SdkLog
    #define SdkLog( message )   MyLogger message
#endif

/************ End of logging configuration ****************/

```
