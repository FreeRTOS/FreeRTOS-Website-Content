---
title: Implementing a Command
created: 2018-09-20
categories:
  - kernel
relatedLinks:
  - title: Why use FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---
 

FreeRTOS-Plus-CLI is an extensible framework that allows the application writer to define and register
their own command line input commands. This page describes how to write a function that implements the
behaviour of a command.


## Function inputs and outputs

Functions that implement the behaviour of a user defined command must have the following
interface (prototype):

```c
BaseType_t xFunctionName( char *pcWriteBuffer,
                          size_t xWriteBufferLen,
                          const char *pcCommandString );
```

Following is a description of the parameters that will be passed into the function when it is called,
and the value that must be returned.

**Parameters:**

+ *pcWriteBuffer*

  This is the buffer into which any generated output should be written. For example, if the function
  is simply going to return the fixed string "Hello World", then the string is written into pcWriteBuffer.
  Output **must always** be null terminated.

+ *xWriteBufferLen*

  This is the size of the buffer pointed to by the pcWriteBuffer parameter. Writing more than xWriteBufferLen
  characters into pcWriteBuffer will cause a buffer overflow.

+ *pcCommandString*

  A pointer to the entire command string. Having access to the entire command string allows the function
  implementation to extract the command parameters - if there are any. FreeRTOS-Plus-CLI
  provides [helper functions](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/03-Command-parameters) that accept the
  command string and return the command parameters - so explicit string parsing is not required. Examples
  are provided on this page.


**Returns:**

Executing some commands will result in more than a single line of output being produced. For example,
a file system "dir" (or "ls") command will generate a line of output for each file in a directory. If
there are three files in the directory, the output might look as below:

```c
file1.txt
file2.txt
file3.txt
```

To minimise RAM usage, and ensure RAM usage is deterministic, FreeRTOS-Plus-CLI allows functions that
implement command behaviour to output a single line at a time. The function return value is used to
indicate whether the output line is the end of the output, or if there are more lines to be generated.

Return **pdFALSE** if the generated output is the end of the output, meaning there are no more lines
to be generated, and the command execution is complete.

Return **pdTRUE** if the returned output is not the end of the output, and there are still one or more
lines to be generated before the command execution is complete.

To continue the example of the "dir" command that outputs three file names:

1. The first time the function that implements the dir command is called, it is possible to only output
   the first line (file1.txt). If this is done the function must return pdTRUE to indicate there are
   more lines to follow.

2. The second time the function that implements the dir command is called, it is possible to only output
   the second line (file2.txt). If this is done the function must return pdTRUE again to indicate there
   are more lines to follow.

3. The third time the function that implements the dir command is called, only the third line (file3.txt)
   will be output. This time, there are no more lines to output, so the function must return pdFALSE.

Alternatively, if there is sufficient RAM, and the value passed in xWriteBufferLen is large enough,
all three lines could have been returned at once - in which case the function must return pdFALSE on
its first execution.

Each time a command is executed, FreeRTOS-Plus-CLI will repeatedly call the function that implements
the command behaviour, until the function returns pdFALSE.


## Examples

The following examples are provided below:

1. A command that takes no parameters and returns a single string.
2. A command that takes no parameters and returns multiple strings, one line at a time.
3. A command that expects a fixed number of parameters.
4. A command that accepts a variable number of parameters, and returns a variable number of strings
   one line at a time.


### Example 1: A command with no parameters

The FreeRTOS vTaskList() API function generates a table containing information on the state of each
task. The table contains a line of text for each task. The command implemented in Example 1 outputs
this table. Example 1 demonstrates the simple case where the entire table is output at once. The comments
in the code provide more explanation.

```c
/* This function implements the behaviour of a command, so must have the correct
   prototype. */
static BaseType_t prvTaskStatsCommand( char *pcWriteBuffer,
                                       size_t xWriteBufferLen,
                                       const char *pcCommandString )
{
    /* For simplicity, this function assumes the output buffer is large enough
       to hold all the text generated by executing the vTaskList() API function,
       so the xWriteBufferLen parameter is not used. */
    ( void ) xWriteBufferLen;

    /* pcWriteBuffer is used directly as the vTaskList() parameter, so the table
       generated by executing vTaskList() is written directly into the output
       buffer. */
    vTaskList( pcWriteBuffer + strlen( pcHeader ) );

    /* The entire table was written directly to the output buffer. Execution
       of this command is complete, so return pdFALSE. */
    return pdFALSE;
}
```
*Example 1: Outputting multiple lines at once*


### Example 2: Returning multiple lines one line at a time

Every command registered with FreeRTOS-Plus-CLI has its own help string. The help string is one line
of text that demonstrates how the command is used. FreeRTOS-Plus-CLI includes a "help" command that
returns all the help strings, providing the user with a list of available commands along with instructions
on how each command is used. Example 2 shows the implementation of the help command. Unlike example 1,
where all the output was generated in one go, example 2 generates a single line at a time. Note this
function is **not** re-entrant.

```c
/* This function implements the behaviour of a command, so must have the correct
   prototype. */
static BaseType_t prvHelpCommand( char *pcWriteBuffer,
                                  size_t xWriteBufferLen,
                                  const char *pcCommandString )
{
/* Executing the "help" command will generate multiple lines of text, but this
   function will only output a single line at a time. Therefore, this function is
   called multiple times to complete the processing of a single "help" command. That
   means it has to remember which help strings it has already output, and which
   still remain to be output. The static pxCommand variable is used to point to the
   next help string that needs outputting. */
static const xCommandLineInputListItem *pxCommand = NULL;
signed BaseType_t xReturn;

    if( pxCommand == NULL )
    {
        /* pxCommand is NULL in between executions of the "help" command, so if
           it is NULL on entry to this function it is the start of a new "help" command
           and the first help string is returned. The following line points pxCommand
           to the first command registered with FreeRTOS-Plus-CLI. */
        pxCommand = &xRegisteredCommands;
    }

    /* Output the help string for the command pointed to by pxCommand, taking
       care not to overflow the output buffer. */
    strncpy( pcWriteBuffer,
             pxCommand->pxCommandLineDefinition->pcHelpString,
             xWriteBufferLen );

    /* Move onto the next command in the list, ready to output the help string
       for that command the next time this function is called. */
    pxCommand = pxCommand->pxNext;

    if( pxCommand == NULL )
    {
        /* If the next command in the list is NULL, then there are no more
           commands to process, and pdFALSE can be returned. */
        xReturn = pdFALSE;
    }
    else
    {
        /* If the next command in the list is not NULL, then there are more
           commands to process and therefore more lines of output to be generated.
           In this case pdTRUE is returned. */
        xReturn = pdTRUE;
    }

    return xReturn;
}
```
*Example 2: Generating multiple lines of output, one line at a time*


### Example 3: A command with a fixed number of parameters

Some commands take parameters. For example, a file system "copy" command needs the name of the source
file and the name of the destination file. Example 3 is a framework for a copy command and is provided
to demonstrate how command parameters are accessed and used.

Note that, if this command is declared to take two parameters when it is registered, FreeRTOS-Plus-CLI
will not even call the command unless exactly two parameters are supplied.

```c
/* This function implements the behaviour of a command, so must have the correct
   prototype. */
static BaseType_t prvCopyCommand( char *pcWriteBuffer,
                                  size_t xWriteBufferLen,
                                  const char *pcCommandString )
{
char *pcParameter1, *pcParameter2;
BaseType_t xParameter1StringLength, xParameter2StringLength, xResult;

    /* Obtain the name of the source file, and the length of its name, from
       the command string. The name of the source file is the first parameter. */
    pcParameter1 = [FreeRTOS\_CLIGetParameter](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/03-Command-parameters)
                        (
                          /* The command string itself. */
                          pcCommandString,
                          /* Return the first parameter. */
                          1,
                          /* Store the parameter string length. */
                          &xParameter1StringLength
                        );

    /* Obtain the name of the destination file, and the length of its name. */
    pcParameter2 = FreeRTOS_CLIGetParameter( pcCommandString,
                                             2,
                                             &xParameter2StringLength );

    /* Terminate both file names. */
    pcParameter1[ xParameter1StringLength ] = 0x00;
    pcParameter2[ xParameter2StringLength ] = 0x00;

    /* Perform the copy operation itself. */
    xResult = prvCopyFile( pcParameter1, pcParameter2 );

    if( xResult == pdPASS )
    {
        /* The copy was successful. There is nothing to output. */
        *pcWriteBuffer = NULL;
    }
    else
    {
        /* The copy was not successful. Inform the users. */
        snprintf( pcWriteBuffer, xWriteBufferLen, "Error during copyrnrn" );
    }

    /* There is only a single line of output produced in all cases. pdFALSE is
       returned because there is no more output to be generated. */
    return pdFALSE;
}
```
*Example 3: Accessing and using the command parameters*


### Example 4: A command with a variable number of parameters

Example 4 demonstrates how to create and implement a command that accepts a variable number of parameters.
FreeRTOS-Plus-CLI will not check the number of supplied parameters, and the implementation of the command
simply echos parameter back, one at a time. For example, if the assigned command string was "echo\_parameters",
if the user enters:

`echo_parameters one two three four`

Then the generated out will be:

The parameters were:

1: one

2: two

3: three

4: four

```c
static BaseType_t prvParameterEchoCommand( char *pcWriteBuffer,
                                           size_t xWriteBufferLen,
                                           const char *pcCommandString )
{
char *pcParameter;
BaseType_t lParameterStringLength, xReturn;

/* Note that the use of the static parameter means this function is not reentrant. */
static BaseType_t lParameterNumber = 0;

    if( lParameterNumber == 0 )
    {
        /* lParameterNumber is 0, so this is the first time the function has been
           called since the command was entered. Return the string "The parameters
           were:" before returning any parameter strings. */
        sprintf( pcWriteBuffer, "The parameters were:rn" );

        /* Next time the function is called the first parameter will be echoed
           back. */
        lParameterNumber = 1L;

        /* There is more data to be returned as no parameters have been echoed
           back yet, so set xReturn to pdPASS so the function will be called again. */
        xReturn = pdPASS;
    }
    else
    {
        /* lParameter is not 0, so holds the number of the parameter that should
           be returned. Obtain the complete parameter string. */
        pcParameter = ( char * ) FreeRTOS_CLIGetParameter
                                    (
                                        /* The command string itself. */
                                        pcCommandString,
                                        /* Return the next parameter. */
                                        lParameterNumber,
                                        /* Store the parameter string length. */
                                        &lParameterStringLength
                                    );

        if( pcParameter != NULL )
        {
            /* There was another parameter to return. Copy it into pcWriteBuffer.
               in the format "[number]: [Parameter String". */
            memset( pcWriteBuffer, 0x00, xWriteBufferLen );
            sprintf( pcWriteBuffer, "%d: ", lParameterNumber );
            strncat( pcWriteBuffer, pcParameter, lParameterStringLength );
            strncat( pcWriteBuffer, "rn", strlen( "rn" ) );

            /* There might be more parameters to return after this one, so again
               set xReturn to pdTRUE. */
            xReturn = pdTRUE;
            lParameterNumber++;
        }
        else
        {
            /* No more parameters were found. Make sure the write buffer does
               not contain a valid string to prevent junk being printed out. */
            pcWriteBuffer[ 0 ] = 0x00;

            /* There is no more data to return, so this time set xReturn to
               pdFALSE. */
            xReturn = pdFALSE;

            /* Start over the next time this command is executed. */
            lParameterNumber = 0;
        }
    }

    return xReturn;
}
```
*Example 4: Accessing a variable number of parameters*
