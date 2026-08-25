---
title: "FreeRTOS_CLIRegisterCommand()"
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

FreeRTOS_CLI.h


```c
BaseType_t FreeRTOS_CLIRegisterCommand( CLI_Command_Definition_t *pxCommandToRegister )

```

FreeRTOS-Plus-CLI 是一个可扩展的框架，
应用程序写入器可以通过该框架定义并注册自己的命令行输入命令。实现用户自定义命令行为的函数必须使用一个特定的接口，
如
 [单独页面的描述所示](/Documentation/03-Libraries/02-FreeRTOS-plus/03-FreeRTOS-plus-CLI/02-Implementing-a-command)。

本页介绍了 `FreeRTOS_CLIRegisterCommand()`，
它是用于向 FreeRTOS-Plus-CLI 注册命令的 API 函数。注册命令的方法是将实现命令行为的函数与文本字符串关联起来，
并将关联情况告知 FreeRTOS-Plus-CLI。然后，FreeRTOS-Plus-CLI
将在每次输入命令文本字符串时自动运行该函数。阅读此页面后
即可了解。

**注意**：代码中出现的 `FreeRTOS_CLIRegisterCommand()` 原型
是一个指向 `CLI_Command_Definition_t` 类型常量结构体的常量指针。此处删除了常量限定符，
以使原型更易于阅读。


### 参数：

* `pxCommandToRegister`

   正在注册的命令，由 `CLI_Command_Definition_t` 类型的结构体定义。该
   结构体如此表下方所示。


### 返回：

* 如果命令成功注册，则返回 `pdPASS`。

* 返回 `pdFAIL`，如果由于没有足够的
  [FreeRTOS 堆](/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/01-Memory-management)
  可用于创建新列表项而导致命令无法注册。


### CLI_Command_Definition_t

命令由 `CLI_Command_Definition_t` 类型的结构体定义，
结构体如下所示。代码中的注释描述了
结构体成员。

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
*`CLI_Command_Definition_t` 结构体*


### 示例

一种 FreeRTOS-Plus-CLI 特色演示实现了文件系统
"del" 命令。命令定义如下。

```c
static const CLI_Command_Definition_t xDelCommand =
{
    "del",
    "del <filename>: Deletes <filename> from the diskrn",
    prvDelCommand,
    1
};
```
*文件系统 del 命令的定义*


注册此命令后：

* 每次用户键入 “del” 时都会执行 prvDelCommand()。

* 输出 "del &lt;filename&gt;: Deletes &lt;filename&gt; from the diskrn"
  来描述用户键入 “help” 时的 del 命令。

* del 命令需要一个参数（被删除文件的名称
  )。如果输入参数的数量不是 1，FreeRTOS-Plus-CLI 将输出错误字符串，而不是执行
  prvDelCommand()。

然后使用以下函数调用向 FreeRTOS-Plus-CLI 注册 del 命令：

```c
FreeRTOS_CLIRegisterCommand( &xDelCommand );
```
*使用 FreeRTOS-Plus-CLI 注册 `xDelCommand` 结构体*
