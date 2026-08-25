---
title: "FreeRTOS_CLIGetOutputBuffer()"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

FreeRTOS\_CLI.h

```c
char *FreeRTOS_CLIGetOutputBuffer( void );
```

FreeRTOS-Plus-CLI is an extensible framework that allows the application writer to define and register
their own command line input commands. Separate documentation pages are provided that
describe [how to write a function that implements the behaviour](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/02-Implementing-a-command)
 of a user defined
command, [how to register user defined commands with FreeRTOS-Plus-CLI](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/04-Registering-a-command)
 and how to integrate FreeRTOS-Plus-CLI into a FreeRTOS task.

This page describes the optional FreeRTOS\_CLIGetOutputBuffer() function.

Command interpreter implementations require an output buffer that is used to hold any output generated
by running a command.

If FreeRTOS-Plus-CLI is used to implement a single command interpreter interface, the output buffer
can be defined locally to the task or file that executes
the [FreeRTOS\_CLIProcessCommand()](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/05-Calling-the-interpreter) API function.

If FreeRTOS-Plus-CLI is used to implement a command interpreter on multiple interfaces, a UART and a
TCP/IP socket for example, then both interfaces could provide their own output buffers in the same manner.
However, if only one of the interfaces is going to be used at a time, then RAM can be saved by having
both interfaces share a single output buffer. FreeRTOS\_CLIGetOutputBuffer() is provided to make this
easier.


**Parameters:**

 None.


**Returns:**

FreeRTOS\_CLIGetOutputBuffer() does nothing more than return the address of an output buffer that is
declared within the FreeRTOS-Plus-CLI code - removing the need for command interface implementations
to declare their own.

The size of the buffer is defined by the configCOMMAND\_INT\_MAX\_OUTPUT\_SIZE constant, which should
be defined in FreeRTOSConfig.h whenever FreeRTOS-Plus-CLI is used.

configCOMMAND\_INT\_MAX\_OUTPUT\_SIZE should be set to 1 to minimise RAM usage if all command interpreter
interfaces use their own locally defined buffers, and the FreeRTOS\_CLIGetOutputBuffer() API function
is not used.
