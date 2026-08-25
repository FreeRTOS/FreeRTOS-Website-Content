---
title: "FreeRTOS_CLIGetParameter()"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

FreeRTOS\_CLI.h


```c
const char *FreeRTOS_CLIGetParameter( const char *pcCommandString,
                                         UBaseType_t uxWantedParameter,
                                         BaseType_t *pxParameterStringLength )
```

FreeRTOS-Plus-CLI is an extensible framework that allows the application writer to define and register
their own command line input commands. Functions that implement the behaviour of a user defined command
have to use a particular interface, which is described
 [on a separate page](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/02-Implementing-a-command).

Some commands take parameters. For example, a file system "copy" command needs the name of the source
file and the name of the destination file. This page describes a helper function called `FreeRTOS_CLIGetParameter()`
that is provided by FreeRTOS-Plus-CLI to make input parameter parsing easy.

`FreeRTOS_CLIGetParameter()` takes the full command string and the position of the requested parameter
as inputs, and produces a pointer to the start of the requested parameter and the length of the parameter
string in bytes as outputs.

**Parameters:**

+ *pcCommandString*

   A pointer to the entire command string, as entered by the user.

+ *ucWantedParameter*

  The position of the parameter being requested within the command string. For example, if the input
  command was "copy [source\_file] [destination\_file]", set `ucWantedParameter` to 1 to request the
  name and length of the source\_file parameter. Set `ucWantedParameter` to 2 to request the name and
  length of the destination\_file parameter.

+ *pucParameterStringLength*

  The string length of the parameter being requested is returned in `*pucParameterStringLength`. For example,
  if the parameter text was "filename.txt", then `*pucParameterStringLength` will be set to 12, as there
  are 12 characters in the string.


**Returns:**

A pointer to the start of the parameter being requested is returned. For example, if the full command
string is "copy file1.txt file2.txt", and `ucWantedParameter` is 2, `FreeRTOS_CLIGetParameter()` will
return a pointer to the 'f' of "file2.txt".


### Examples

An example is provided on
the [Implementing A Command](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/02-Implementing-a-command#Example_Of_Using_FreeRTOS_CLIGetParameter)
 page.
