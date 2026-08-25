---
title: "FreeRTOS_CLIRegisterCommand()"
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

FreeRTOS\_CLI.h


```c
BaseType_t FreeRTOS_CLIRegisterCommand( CLI_Command_Definition_t *pxCommandToRegister )
```

FreeRTOS-Plus-CLI is an extensible framework that allows the application writer to define and register
their own command line input commands. Functions that implement the behaviour of a user defined command
have to use a particular interface, which is described
 [on a separate page](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/02-Implementing-a-command).

This page describes `FreeRTOS_CLIRegisterCommand()`, which is the API function used to register commands
with FreeRTOS-Plus-CLI. A command is registered by associating the function that implements the command
behaviour with a text string, and telling FreeRTOS-Plus-CLI about the association. FreeRTOS-Plus-CLI
will then automatically run the function each time the command text string is entered. This will become
clear after reading this page.

**Note**: The `FreeRTOS_CLIRegisterCommand()` prototype that appears in the code take a const pointer
to a const structure of type `CLI_Command_Definition_t`. The const qualifiers
have been removed here to make the prototype easier to read.


### Parameters:

* `pxCommandToRegister`

   The command being registered, which is defined by a structure of type `CLI_Command_Definition_t`. The
   structure is described below this table.


### Returns:

* `pdPASS` is returned if the command was successfully registered.

* `pdFAIL` is returned if the command could not be registered because there
  was insufficient [FreeRTOS heap](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)
  available for a new list item to be created.


### CLI\_Command\_Definition\_t

Commands are defined by a structure of type `CLI_Command_Definition_t`.
The structure is shown below. The comments in the code describe the
structure members.

```c
typedef struct xCLI_COMMAND_DEFINITION
{
    /* The command line input string. This is the string that the user enters
       to run the command. For example, the FreeRTOS-Plus-CLI help function uses the
       string "help". If a user types "help" the help command executes. */
    const char * const pcCommand;

    /* A string that describes the command, and its expected parameters. This
       is the string that is output when the help command is executed. The string
       must start with the command itself, and end with "rn". For example, the
       help string for the help command itself is:
       "help: Returns a list of all the commandsrn" */
    const char * const pcHelpString;

    /* A pointer to the function that implements the command behaviour
       (effectively the function name). */
    const pdCOMMAND_LINE_CALLBACK pxCommandInterpreter;

    /* The number of parameters required by the command. FreeRTOS-Plus-CLI will only
       execute the command if the number of parameters entered on the command line
       matches this number. */
    char cExpectedNumberOfParameters;

} CLI_Command_Definition_t;
```
*The `CLI_Command_Definition_t` structure*


### Examples

One of the FreeRTOS-Plus-CLI featured demos implements a file system
"del" command. The command definition is given below.

```c
static const CLI_Command_Definition_t xDelCommand =
{
    "del",
    "del <filename>: Deletes <filename> from the diskrn",
    prvDelCommand,
    1
};
```
*The definition of the file system del command*


Once this command is registered:

* prvDelCommand() is executed each time the user types "del".

* "del &lt;filename&gt;: Deletes &lt;filename&gt; from the diskrn" is output to
  describe the del command when the user types "help".

* The del command expects one parameter (the name of the file being
  deleted). FreeRTOS-Plus-CLI will output an error string instead of executing
  prvDelCommand() if the number of input parameters is not exactly 1.

The del command is then registered with FreeRTOS-Plus-CLI using the following function call:

```c
FreeRTOS_CLIRegisterCommand( &xDelCommand );
```
*Registering the `xDelCommand` structure with FreeRTOS-Plus-CLI*
