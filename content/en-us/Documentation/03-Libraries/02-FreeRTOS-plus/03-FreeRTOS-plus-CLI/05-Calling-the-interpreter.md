---
title: "FreeRTOS_CLIProcessCommand()"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

FreeRTOS\_CLI.h

```c
BaseType_t FreeRTOS_CLIProcessCommand( char *pcCommandInput,
                                       char *pcWriteBuffer,
                                       size_t xWriteBufferLen  );
```


FreeRTOS-Plus-CLI is an extensible framework that allows the application writer to define and register
their own command line input commands. Separate documentation pages are provided that describe how
to [write a function that implements the behaviour of a user defined command](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/02-Implementing-a-command),
 how to [registers user defined commands with FreeRTOS-Plus-CLI](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/04-Registering-a-command),
 and how to [implement a FreeRTOS-Plus-CLI task](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/06-A-FreeRTOS-plus-CLI-task).

This page describes the FreeRTOS\_CLIProcessCommand() function. FreeRTOS\_CLIProcessCommand() is the
API function that takes the string entered by the user at the command prompt, and if the string matches
a registered command, executes the function that implements the command behaviour.


**Parameters:**

+ *pcCommandInput*

  The complete input string, exactly as entered by the user at the command prompt (which might be a
  UART console, keyboard, telnet client, or other user input client).

+ *pcWriteBuffer*

  If pcCommandInput does not contain a correctly formatted command, then FreeRTOS\_CLIProcessCommand()
  will output a null terminated error message into the pcWriteBuffer buffer. If pcCommandInput does
  contain a correctly formatted command, then FreeRTOS\_CLIProcessCommand() will execute the function
  that implements the command behaviour, which will place its generated output into the pcWriteBuffer buffer.

+ *xWriteBufferLen*

  The size of the buffer pointed to by the pcWriteBuffer parameter. Writing more than xWriteBufferLen
  characters into pcWriteBuffer will cause a buffer overflow.


**Returns:**

FreeRTOS\_CLIProcessCommand() executes a function that implements the behaviour of a command, and returns
the value returned by the function it executed. These values are described on
the [Implementing a Command](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/02-Implementing-a-command) page.


### Examples

The [FreeRTOS-Plus-CLI Task Implementation](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/06-A-FreeRTOS-plus-CLI-task) page contains
example code that includes a demonstration of how FreeRTOS\_CLIProcessCommand() is used.
