---
title: 使用参与者模型的 FreeRTOS-Plus-POSIX 展示
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


[[FreeRTOS-Plus-POSIX 概览](/Documentation/03-Libraries/05-FreeRTOS-labs/03-FreeRTOS-plus-POSIX/00-FreeRTOS-Plus-POSIX)]


## 概览

实时应用程序开发的一大常见痛点是，
开发者往往需要经过艰难学习才能掌握特定平台的用法。虽然 FreeRTOS 已解决面向硬件的交互问题，
例如 FreeRTOS 应用程序可以轻松从受支持的平台移植到另一平台，
但开发者仍然需要先学习所有 FreeRTOS 接口。FreeRTOS-Plus-POSIX 可大大简化这一问题，
应用 POSIX 的现有应用程序可方便地移植到搭载的 AWS IoT。

为了展示如何轻松完成移植，
本演示将介绍在 Linux box 上开发，然后移植到 FreeRTOS 的全过程。本演示还包含一个简单的
[参与者模型](https://en.wikipedia.org/wiki/Actor_model)可行实现，您可以在自己的应用程序中加以采用。


## 演示具体内容

本演示创建了两类参与者：Master 和 Worker。Master 发送不同类型的消息，
通知 Worker 工作内容。收到消息后，Worker 便开始执行
与该消息类型相关联的预定义例程。Master 完成工作分配后，便会通知 Worker
“一切妥当”，所有参与者便会终止行动。

![](/media/2018/posix-demo-actor.png)

在该演示中

+ 参与者实际上是使用 pthread_create() 创建的线程。

+ 消息通过使用 mq_open() 创建的队列传递，
  通过 mq_send()、mq_timedsend()、mq_timedreceive() 发送/接收。


## 在 Linux 上编写、编译和运行代码。

只需展示您的代码——下载 [posix_demo.c](https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Labs/main/FreeRTOS-Labs/Demo/FreeRTOS_Plus_POSIX_with_actor_Windows_Simulator/posix_demo.c)

库依赖项

```c
/* Headers used in this demo, which are also defined in FreeRTOS-Plus-POSIX */
#include <pthread.h>
#include <mqueue.h>
#include <time.h>
#include <fcntl.h>
#include <errno.h>

/* Headers used in this demo, which are not defined by FreeRTOS-Plus-POSIX but defined by platform. */
#include <stdbool.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>

```

若要编译，请打开命令行窗口，然后使用 cd 命令进入存放所下载 posix_demo.c 的文件夹。

使用下列命令行编译

```c
gcc -Wall posix_demo.c -lpthread -lrt -o posix_demo

```

运行

```c
./posix_demo

```

命令行输出

![](/media/2018/linux_compile_snapshot.png)


## 移植到 FreeRTOS（Windows 模拟器）

只需展示您的代码——克隆 [`aws/amazon-freertos-staging`](https://github.com/aws/amazon-freertos)，
同一应用程序的源代码位于 `./demos/common/posix/aws_posix_demo.c` 下

更新库依赖项，将其移植到 FreeRTOS-Plus-POSIX

```c
/* Demo includes -- this is to run demo with aws_demo_runner.c. */
#include "aws_posix_demo.h"

/* FreeRTOS-Plus-POSIX */
#include "FreeRTOS_POSIX/pthread.h"
#include "FreeRTOS_POSIX/mqueue.h"
#include "FreeRTOS_POSIX/time.h"
#include "FreeRTOS_POSIX/fcntl.h"
#include "FreeRTOS_POSIX/errno.h"

/* FreeRTOS includes. */
#include "FreeRTOS.h"

/* System headers */
#include <stdbool.h>

```

除了上述标头更改外，`printf()` 也更改为 `configPRINTF(()) to print to serial port.`

另有两项与移植无关的更改

+ 在 Windows 模拟器上启动 POSIX 演示之前，configASSERT(()) 会检查配置情况。
+ Linux 版演示中的 `int main( void )` 函数签名更改为 `void vStartPOSIXDemo( void )`。
  Windows 模拟器已定义主入口点，用于调度演示任务。

要编译和运行，请执行如下操作：

将 `aws_demos.sln` 解决方案加载到 Visual Studio (`aws_demos.sln` 位于 `./demo/pc/windows/visual_studio/`下)。
通常情况下，设置 Windows 模拟器时，可参考存储库 `README.md` 。本演示假设您
已完成设置。`aws_demo.sln` 中提供了各种演示用例。默认情况下，不启用 POSIX 演示。
若要切换到 POSIX 演示，请转到 `aws_demo_runner.c`，并取消下列命令行的注释：

```c
/* some code ... */
extern void vStartMQTTEchoDemo( void );
/* some code ... */
vStartMQTTEchoDemo();

```

然后按照 `README.md` 中记录的首个演示的方式构建和运行。

命令行输出（如果在开发板上运行，则为串行端口输出。）

 ![](/media/2018/windows_compile_snapshot.png)


## 小结

本演示展示了如何将现有的 POSIX 兼容应用程序轻松移植到 FreeRTOS。虽然
本演示仅以在 Windows 模拟器上执行此操作为例，
但移植到其他平台的方法大同小异。对于 POSIX 接口子集，平台可能有自己的实现方式。在这种情况下，
可以选择性启用 FreeRTOS-Plus-POSIX 功能。请参阅 `FreeRTOS_POSIX_portable_default.h`（
默认值）和 `./lib/..` 目录下的 `FreeRTOS_POSIX_portable.h`（用于覆盖）。
