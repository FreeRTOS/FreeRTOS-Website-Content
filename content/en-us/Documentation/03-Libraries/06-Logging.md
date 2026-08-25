---
title: Logging Functionality
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

The following FreeRTOS Libraries use this logging functionality:

* [coreMQTT](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/00-coreMQTT)
* [coreHTTP](/Documentation/03-Libraries/03-FreeRTOS-core/04-coreHTTP/01-coreHTTP)
* [corePKCS11](/Documentation/03-Libraries/03-FreeRTOS-core/08-corePKCS11/01-corePKCS11)
* [AWS IoT Device Shadow](/Documentation/03-Libraries/04-AWS-libraries/03-AWS-IoT-Device-Shadow/01-AWS-IoT-device-shadow)
* [AWS IoT Device Defender](/Documentation/03-Libraries/04-AWS-libraries/05-AWS-IoT-Device-Defender/01-AWS-IoT-device-defender)


## Logging Macros

The FreeRTOS libraries use the following 4 logging macros, listed in increasing order of verbosity.
For example, LogError() is only called when there is an error so is the least verbose, whereas `LogDebug()`
is called more frequently to provide debug level information and is therefore the most verbose.

* LogError
* LogWarn
* LogInfo
* LogDebug

Logging macros are used with a variable number of arguments, just like printf() (with the exception that
they use double parenthesis). For example, the libraries call the logging macros in the following way:

```c
LogInfo( ( “This prints an integer %d”, 100 ) );
```

You do not need to define the four logging macros individually. By including the `FreeRTOS-Plus/Source/Utilities/logging/`
logging\_stack.h header file you can instead define a single macro called `SdkLog()`, which will then be
applied to all four verbosity levels. When this is done, the verbosity level is set separately by the
definition of LIBRARY\_LOG\_LEVEL, as described below.


**Note** the header file ordering in the code snippet at the end of this page.


###  Defining the SdkLog macro

The `logging_stack.h` header file should be included and the logging configuration macros should be defined
within the configuration file of the library in use. For example, to obtain log output from the coreMQTT
library, include `logging_stack.h` and define the logging macros in `core_mqtt_config.h`.

To obtain logging SkdLog() must be defined to call a thread safe platform specific print function. For
example, the print function may output characters to a serial port, or to a TCP socket. As the logging
macros accept a variable number of parameters and are used just like printf(), the platform specific print
function must have the same prototype (parameters list) as printf(). For example, if your application has
a thread safe version of printf() that writes to a serial port you can define SdkLog as:

```c
#define SdkLog( X ) printf X
```

Logging macros left undefined are defaulted to be empty macros that do not generate any code.

**NOTE:** If you don’t use the logging utility headers
in [FreeRTOS-Plus/Source/Utilities/logging/](https://github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS-Plus/Source/Utilities/logging)
you can define the four logging macros individually for the logging levels you want by defining the macros
in your application - but that is not the recommended method as doing so will prevent LIBRARY\_LOG\_LEVEL
and LIBRARY\_LOG\_NAME from having any effect.


### Setting the Verbosity Level

To set the verbosity level define the LIBRARY\_LOG\_LEVEL macro to one of the following values in the same
configuration file used to define SdkLog(). Valid values for LIBRARY\_LOG\_LEVEL are:

* LOG\_NONE (turns logging off)
* LOG\_ERROR
* LOG\_WARN
* LOG\_INFO
* LOG\_DEBUG

For example:

```c
#define LIBRARY_LOG_LEVEL  LOG_NONE
```


###  Setting the Text Name

To set the text name define the LIBRARY\_LOG\_NAME macro to a string within the same configuration file
used to define SdkLog(). Each log message prints the name, so it is normal to set the name to the name
of the library. For example:

```c
#define LIBRARY_LOG_NAME “MQTT”
```

Setting the name to an empty string will save program space.


### Setting the Metadata in logs

To add metadata in log messages (like source code location of log messages), the LOG\_METADATA\_FORMAT
and LOG\_METADATA\_ARGS macros can be defined.

The LOG\_METADATA\_FORMAT macro should be defined to specify the metadata format string, whereas
the LOG\_METADATA\_ARGS macro should be defined to pass the metadata arguments for the format string.
Both these macros are prefixed in the log messages passed to the platform specific print function defined
for the SdkLog macro.

For example, the following definitions add the function name and line number file of the source file that
emits the log message.

* #define LOG\_METADATA\_FORMAT “[%s:%d]”
* #define LOG\_METADATA\_ARGS \_\_FUNCTION\_\_, \_\_LINE\_\_

Setting the metadata macros to empty values will save program space.


### Reference Examples

Notice in the examples links and the template code below that there are `#ifndef` guards around the logging
macro definitions. These are there to avoid multiple definition of the same macro in translation units
that include multiple config files. (For example, the MutualAuthMQTTExample.c, includes the `demo_config.h`
through direct inclusion and core\_mqtt\_config.h through indirect inclusion of core\_mqtt.h. For such cases
in application code, it is IMPORTANT to include the config file that contains logging configuration for the
affected translation unit file at top of the file (i.e. before other header includes) so that the correct
configurations are applied.

For an examples in FreeRTOS codebase for logging configuration, refer to
the [MQTT over TLS Mutual Authentication](/Documentation/03-Libraries/03-FreeRTOS-core/02-coreMQTT/02-Demos/03-Mutual-authentication)  demo which configures
logging for the demo application task (defined in MutualAuthMQTTExample.c) in
the [demo\_config.h](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Mutual_Auth/demo_config.h#L33-L54)
file, and for the coreMQTT library in
the [core\_mqtt\_config.h](https://github.com/FreeRTOS/FreeRTOS/blob/main/FreeRTOS-Plus/Demo/coreMQTT_Windows_Simulator/MQTT_Mutual_Auth/demo_config.h)
file.

Below is an template of using the logging configuration.

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
