---
title: 编码标准、测试和样式指南
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 半导体
description: 用于 FreeRTOS 代码的编码标准、样式和测试。
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
  - title: FreeRTOS简介
    link: /Why-FreeRTOS/What-is-FreeRTOS/
  - title: FreeRTOS 初学者指南
    link: /Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/00-Overview/
  - title: 下载 FreeRTOS
    link: /Documentation/02-Kernel/01-About-the-FreeRTOS-kernel/03-Download-freeRTOS/01-DownloadFreeRTOS/
  - title: 常见问题
    link: /Why-FreeRTOS/FAQs
---


### 编码标准 / MISRA C:2012 合规性

核心 FreeRTOS 源文件（通用于所有移植但非移植层）符合
[MISRA](http://www.misra.org.uk/) 编码标准准则。合规性使用
[Coverity](https://www.synopsys.com/software-integrity/static-analysis-tools-sast/coverity.html)
和 [coverity MISRA配置文件](https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/examples/coverity/coverity_misra.config)进行检查。
由于标准页数众多且可以从 MISRA 低价购买，因此，
我们并未复制所有规则。本
[文档](https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/MISRA.md)中列出了与 MISRA 标准存在的偏差。

FreeRTOS 使用多种不同的编译器构建，其中不乏相对高级的编译器。因此，
FreeRTOS 不使用 C99 标准引入或其之后出现的任何 C 语言
功能或语法。但使用 `stdint.h` 头文件的情况除外。
`FreeRTOS/Source/include` 目录包含一个名为 `stdint.readme` 的文件。可将该文件重命名为 `stdint.h`，
以提供构建 FreeRTOS 所需的最低 stdint 类型定义，
但前提是用户的编译器本身无此类型定义。

---


### 编码标准/MISRA C:2004 合规性（11.0.0 之前的 FreeRTOS 内核版本）

对于早于 11.0.0 版本的 FreeRTOS 内核，
使用 [pc-lint](https://pclintplus.com/) 和
[链接的 lint 配置文件进行 MISRA C:2004 合规性检查](/media/lint_configuration.zip)。

以下即为与 MISRA 标准存在的偏差：

* 两个 API 函数具有一个以上出口点。由于临界效率的原因，
  允许二者存在偏差。

* 创建任务时，源代码会操纵内存地址，以此来定位分配给已创建任务的堆栈的起始地址和结束地址
  。代码必须适用于已移植 FreeRTOS 的全部架构，
  包括具有 8、16、20、24 和 32 位总线的架构。这必然需要
  一些指示字运算。使用指示字运算时，通过编程检查算术结果的正确性
  。

* 默认情况下，跟踪宏为空，因此跟踪宏不会生成任何代码。因此，使用虚拟宏定义
  执行 MISRA 合规性检查。

* 如果认为适当（即针对深度嵌入式系统而言，
  当认为遵守该规则创建的代码不如谨慎不遵守时），MISRA 规则将逐行关闭。每次出现这种情况时，
  均使用特殊的 pc-lint MISRA 注释标记语法进行解释。

---


### 测试

本节阐述了对通用代码
（[位于 FreeRTOS/Source 目录](/Documentation/02-Kernel/06-Coding-guidelines/01-Source-code-organization/)中的代码，
由所有 FreeRTOS 内核移植构建）执行的测试，以及对可移植层代码
（位于 FreeRTOS/Source/portable 目录的子目录中的代码）执行的测试。

* **通用代码**

  标准演示/测试文件可提供“分支”测试覆盖范围，
  从而测试确保通过每个决策同时执行“true”和“false”路径。（在大多数情况下，
  这实际上实现了[ 'condition' 覆盖范围](https://en.wikipedia.org/wiki/Code_coverage)，
  原因在于内核编码样式会故意为此保留简单条件）。如果“else”路径为空，
  则会测量“branch”覆盖范围，
  方法是使用 GCOV 在每个“if”条件的“else”路径中将 mtCOVERAGE_TEST_MARKER () 宏定义为 NOP（无操作）指令。仅在测量测试覆盖范围时定义 mtCOVERAGE_TEST_MARKER ()，
  通常为不会生成任何代码的空宏。

* **移植层**

  使用“reg test”任务测试移植层代码；对于支持中断嵌套的移植，
  则使用“interrupt queue”任务进行测试。

  “reg test”任务创建多个（通常是两个）任务，即首先用已知值填充所有 CPU 寄存器，
  然后在其他测试连续执行时，不断检查每个寄存器是否保持其预期的已知值
  （浸泡测试）。每个 reg test 任务均使用唯一值。

  “interrupt queue”任务对嵌套至少三层的不同优先级的中断执行测试。宏
  用于将人为延迟插入代码中的相关点，确保达到所需的测试覆盖率。

**值得注意的是，这些测试较为彻底，致使多次发现晶片中的错误。**

---


### 内存安全验证

[FreeRTOS 核心](/Documentation/03-Libraries/03-FreeRTOS-core/01-Introduction)（以及用于 AWS IoT[(/Documentation/03-Libraries/04-AWS-libraries/01-Introduction) 的 ]FreeRTOS）
库包括[内存安全验证](/Community/Blogs/2020/ensuring-the-memory-safety-of-freertos-part-1)。
FreeRTOS 内核和 FreeRTOS-Plus-TCP 堆栈也应用相同验证，
但这两个旧库尚未完全覆盖。

---


### 安全性审查

重要更新须在发布
（由 AWS 提供的服务）前通过应用安全性 (APSEC) 审查和渗透测试 (Pentesting)。


---

### 命名惯例

RTOS 内核和演示应用程序源代码使用以下惯例:

* 变量
	+ *uint32_t* 类型变量以 *ul* 为前缀，其中“u”表示“unsigned” ，“l”表示“long”。
	+ *uint16_t* 类型变量以 *us* 为前缀，其中“u”表示“unsigned” ，“s”表示“short”。
	+ *uint8_t* 类型变量以 *uc* 为前缀，其中“u”表示“unsigned” ，“c”表示“char ”。
	+ 非 stdint 类型的变量以 *x* 为前缀。例如，BaseType_t 和 TickType_t，
	  二者分别是可移植层定义的定义类型，主要架构的自然类型或最有效类型，
	  以及用于保存 RTOS 滴答计数的类型。
	+ 非 stdint 类型的未签名变量存在附加前缀 *u*。例如，
	  UBaseType_t（未签名 BaseType_t）类型变量以 *ux* 为前缀。
	+ *size_t* 类型变量也带有 *ux* 前缀。
	+ 枚举变量以 *e* 为前缀
	+ 指针以附加 *p* 为前缀，例如，指向 uint16_t 的指针将以 *pus* 为前缀。
	+ 根据 MISRA 指南，未限定标准 *char* 类型仅可包含 ASCII 字符，
	  并以 *c* 为前缀。
	+ 根据 MISRA 指南，*char ** 类型变量仅可包含指向 ASCII 字符串的指针，
	  并以 *pc* 为前缀。

* 函数
	+ 文件作用域静态（私有）函数以 *prv* 为前缀。
	+ 根据变量定义的相关规定，API 函数以其返回类型为前缀，
	  并为 *void* 添加前缀 *v*。
	+ API 函数名称以定义 API 函数文件的名称开头。例如，在 tasks.c 中定义 vTaskDelete，
	  并且具有 void 返回类型。

* 宏
	+ 宏以定义宏的文件为前缀。前缀为小写。例如，
	  configUSE_PREEMPTION 在 FreeRTOSConfig.h 中定义。
	+ 除前缀外，所有宏均使用大写字母书写，并使用下划线来分隔单词。

---


### 数据类型

仅使用 stdint.h 类型和 RTOS 自带的 typedef，但以下情况除外：

* char

  根据 MISRA 指南，仅在未限定字符类型包含 ASCII 字符方可使用未限定字符类型。

* char \*

  根据 MISRA 指南，仅在未限定字符指针指向 ASCII 字符串时方可使用未限定字符指针
  。使用需要 char * 参数的标准库函数时，
  无需抑制良性编译器警告，此举尤其考虑到将一些编译器默认为未限定 char 类型是签名的，
  而其他编译器默认未限定 char 类型是未签名的。


针对每个移植定义四种类型。即：

* TickType_t

  + 如果 configUSE_16_BIT_TICKS 设置为非零 (true) ，则将 TickType_t 定义为未签名的 16 位类型。
  + 如果 configUSE_16_BIT_TICKS 设置为零 (false)，则将 TickType_t 定义为未签名的 32 位类型。

  请参阅 API 文档的[自定义](/Documentation/02-Kernel/03-Supported-devices/02-Customization/)章节
  获取完整信息。

  32 位架构应始终将 configUSE_16_BIT_TICKS 设置为 0。

* BaseType_t

  架构中最有效、最自然的类型。例如，在 32 位架构上，
  BaseType_t 会被定义为 32 位类型。在 16 位架构上，BaseType_t 会被定义为 16 位类型
  。如果将 BaseType_t 定义为 char，
  则须特别注意确保将签名字符用于可能为负的函数返回值来指示错误。

* UBaseType_t

  未签名的 BaseType_t。

* StackType_t

  意指架构用于存储堆栈项目的类型。通常是 16 位架构上的 16 位类型
  和 32 位架构上的 32 位类型，但也有例外情况。供
  FreeRTOS 内部使用。


---

### 样式指南

* 缩进

  使用四个空格字符进行缩进。

* 注释

  除非注释遵循并描述某个阐述，否则注释始终不会通过第 80 列。

  不使用 C + + 样式双斜杠 (//) 注释。

* 布局

  FreeRTOS 源代码布局旨在实现尽可能轻松地查看及读取。下述代码片段首先显示文件布局，
  然后显示 C 代码格式。

  ```c
  /* Library includes come first... */

  #include <stdlib.h>
  /* ...followed by FreeRTOS includes... */
  #include "FreeRTOS.h"
  /* ...followed by other includes. */
  #include "HardwareSpecifics.h"
  /* #defines come next, bracketed where possible. */
  #define A_DEFINITION	( 1 )

  /*
   * Static (file private) function prototypes appear next, with comments
   * in this style - each line starting with a '*'.
   */
  static void prvAFunction( uint32_t ulParameter );

  /* File scope variables are the last thing before the function definitions.
  Comments for variables are in this style (without each line starting with
  a '*'). */
  static BaseType_t xMyVariable;

  /* The following separator is used after the closing bracket of each function,
  with a blank line following it before the start of the next function definition. */

  /*-----------------------------------------------------------*/

  void vAFunction( void )
  {
    /* Function definition goes here - note the separator after the closing
    curly bracket. */
  }

  /*-----------------------------------------------------------*/

  static UBaseType_t prvNextFunction( void )
  {
    /* Function definition goes here. */
  }

  /*-----------------------------------------------------------*/

  ```
  *文件布局*

  ```c
  /* Function names are always written on a single line, including the return
     type. As always, there is no space before the opening parenthesis. There
     is a space after an opening parenthesis. There is a space before a closing
     parenthesis. There is a space after each comma. Parameters are given
     verbose, descriptive names (unlike this example!). The opening and closing
     curly brackets appear on their own lines, lined up underneath each other. */
  void vAnExampleFunction( long lParameter1, unsigned short usParameter2 )
  {
  /* Variable declarations are not indented. */
  uint8_t ucByte;

      /* Code is indented. Curly brackets are always on their own lines
      and lined up underneath each other. */
      for( ucByte = 0U; ucByte < fileBUFFER_LENGTH; ucByte++ )
      {
          /* Indent again. */
      }
  }

  /* For, while, do and if constructs follow a similar pattern. There is no
     space before the opening parenthesis. There is a space after an opening
     parenthesis. There is a space before a closing parenthesis. There is a
     space after each semicolon (if there are any). There are spaces before and
     after each operator. No reliance is placed on operator precedence -
     parenthesis are always used to make precedence explicit. Magic numbers,
     other than zero, are always replaced with a constant or #defined constant.
     The opening and closing curly brackets appear on their own lines. */
  for( ucByte = 0U; ucByte < fileBUFFER_LENGTH; ucByte++ )
  {
  }

  while( ucByte < fileBUFFER_LENGTH )
  {
  }

  /* There must be no reliance on operator precedence - every condition in a
     multi-condition decision must uniquely be bracketed, as must all
     sub-expressions. */
  if( ( ucByte < fileBUFFER_LENGTH ) && ( ucByte != 0U ) )
  {
      /* Example of no reliance on operator precedence! */
      ulResult = ( ( ulValue1 + ulValue2 ) - ulValue3 ) * ulValue4;
  }

  /* Conditional compilations are laid out **and indented** as per any
     other code. */
  #if( configUSE_TRACE_FACILITY == 1 )
  {
      /* Add a counter into the TCB for tracing only. */
      pxNewTCB->uxTCBNumber = uxTaskNumber;
  }
  #endif

  /* A space is placed after an opening square bracket, and before a closing
     square bracket. */
  ucBuffer[ 0 ] = 0U;
  ucBuffer[ fileBUFFER_LENGTH - 1U ] = 0U;
  ```
  *C 结构体的格式*
