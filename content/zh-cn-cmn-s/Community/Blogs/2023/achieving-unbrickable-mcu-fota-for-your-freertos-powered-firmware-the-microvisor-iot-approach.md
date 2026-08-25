---
title: "为基于 FreeRTOS 的固件实现防砖化 MCU FOTA：Microvisor IoT 方法"
date: 2023 年 5 月 18 日
feature: blog
authors:
  - tony_smithtwilio-com
---
FreeRTOS 为嵌入式应用程序提供了一系列功能，使其变得更加灵活，并使开发人员更具创造力。 
但是，对于物联网 (IoT) 应用程序有一个关键要求，特别是需要大量的额外开发工作才能确保其真正安全，
并消除应用程序崩溃导致设备停止工作的风险：即不会导致设备砖化的 over-the-air (OTA) 更新。 


如果硬件就在您面前的桌子上，更新一台设备可能不会成为问题，但如果您的设备群是远程部署的，那更新设备将成为一个大问题。 
幸运的是，我们有一个与 FreeRTOS 配合得天衣无缝的解决方案： 
[Twilio Microvisor](https://www.twilio.com/iot/microvisor-iot-platform)。


基于 Microvisor 的 IoT 连接方法
-------------------------------------------------


什么是 Microvisor？可以把它看作是嵌入式系统的管理程序，或者说是“微管理程序”，并在考虑 IoT 物联网用例的基础上设计了一些附加功能 
。Microvisor 并不是在 FreeRTOS 之上运行，而是直接与其并行存在，因此不会干扰操作系统或托管应用程序 
的功能。同样，Microvisor 并不依赖 FreeRTOS 来运行。


[\![](../../fr-content-src/uploads/2023/05/microvisor-zone.png)](../../fr-content-src/uploads/2023/05/microvisor-zone.png)  

Microvisor 依赖于 [Arm 的 TrustZone 技术](https://www.arm.com/technologies/trustzone-for-cortex-a) 
将主机微控制器（如我们支持的首款微控制器——STMicroelectronics 的 STM32U585 MCU）划分为一个“安全”的特权内核空间和 
一个“不安全”的用户空间。Microvisor 在前者中运行，而您的应用程序则在后者中运行。不安全听起来有些贬义， 
但它只是意味着应用程序无法访问 TrustZone 安全环境中的资源。这确保了 Microvisor 可以自由管理关键的系统功能并监视重要的攻击面： 
主互联网连接、系统时钟、中断管理等。


激活后，TrustZone 只能在安全环境中启动代码。就 Microvisor 而言，这是一个预启动存根， 
在启动前会验证已安装 Microvisor 代码的 X.509 凭证。Microvisor 本身会检查本地暂存的应用程序更新，并在安装前验证其签名。一旦 
安装了任何更新，Microvisor 就会配置不安全环境并启动应用程序。


当然， “应用程序”是指 FreeRTOS 和托管应用程序。两者在非安全区内一起运行，就像在裸机上运行一样。在 
Microvisor 下，FreeRTOS 无需任何特殊配置，您只需对任何给定的应用程序和 MCU 组合进行配置即可。您可以编写 ISR， 
并使用 FreeRTOS 的任务、信号量、队列和通知，而无需进行任何更改。


Microvisor 可通过 WiFi、蜂窝网络或以太网（或您的产品所配备的这些连接类型中的任意一种）与 Twilio Cloud 保持主连接 
。您可以将应用程序的新版本上传到 Twilio Cloud，然后远程部署到一台或多台设备上。您可以通过 
[Twilio 网络控制台](https://console.twilio.com/)或 
我们的 [CLI 工具](https://www.twilio.com/docs/iot/microvisor/how-to-install-the-microvisor-sdk)来完成这个操作


假设您已经完成了上述操作，并为应用程序进行了一次更新。云会向每个目标设备上安装的 Microvisor 发出信号。给定的 Microvisor 
实例会检索更新的清单，并使用它分块下载代码和相关数据，而这些块被称为“层”。这样，即使通信中断， 
也不会迫使 Microvisor 在每次出错时重新获取整个更新。相反，它会逐层组装更新。在验证完整的更新 
并将其写入闪存中的暂存区域后，Microvisor 会关闭非安全环境，安装新的应用程序并启动它。


Microvisor 的 TrustZone 安全环境确保应用程序崩溃不会导致其崩溃。事实上，它可以监控应用程序的状态， 
以便跟踪崩溃情况，保存堆栈轨迹供未来报告使用，并重新启动应用程序。这确保固件 OTA 更新基本上是“不会变砖的”。在您部署修复之前， 
应用程序可能在每次重新启动时都会崩溃，但 Microvisor 仍然保持运行、连接和可访问状态。


该功能是“免费”的，应用程序无需做任何操作即可激活。Microvisor 始终在保护您的设备。


使用 Microvisor 开发和调试应用程序
---------------------------------------------------------


那么，如何在 Microvisor 管理的环境中开发应用程序呢？答案很简单，您根本不需要做太多。您的 
应用程序可以在无需进行任何特殊编码的情况下运行。将现有应用程序移植到 Microvisor 中可能需要进行一些微调， 
主要是关于时钟配置的部分，Microvisor 会替您完成这一操作。然而，新的应用程序可以完全专注于业务逻辑。


与 Microvisor 同时运行的每个应用程序都可以完全访问主机设备的所有硬件资源， 
但设备的主要面向云的网络接口和少量微控制器外设除外，Microvisor 需要这些外设来实现系统级功能。如果您希望使用其他接口， 
比如其他无线技术，您可以这样做，但您的应用程序需要集成驱动程序和安全措施。如果您只需要访问自己的服务器， 
您只需使用 Microvisor 维护的链接作为隧道来托管自己的 HTTP 和/或 MQTT 请求，Microvisor 提供了相应的 API， 
我们将在后面看到。


Microvisor 和应用程序共享对 MCU GPIO 和外设的访问，但 Microvisor 保留了少量 GPIO 寄存器。 
应用程序访问这些资源的任何尝试都会导致异常，因此您可以在开发过程中发现冲突并进行补救。您可以 
在 
[Microvisor 硬件设计指南](https://www.twilio.com/docs/iot/microvisor/design-iot-devices-with-microvisor#stm32u585-reserved-peripherals)中查看由 Microvisor 保留的 STM32U585 外设和引脚的列表。


应用程序可以使用任何其他外设，在 STM32U585 上就有很多选择。它可以通过 
[STM32U585 数据表](https://www.st.com/resource/en/datasheet/stm32u585ai.pdf)中详细说明的内存位置访问这些资源， 
也可以通过调用硬件抽象层 (HAL) 库提供的便利函数来访问这些资源。


MCU 存储和内存进行了分区。STM32U585 包含 2MB 的内部闪存。Microvisor 占用上面的 1MB 并将剩余的 1MB 分配给应用程序， 
将其映射到非安全环境地址范围 0x08000000-080FFFF， 
因此应用程序可以访问与在普通 STM32U5 上运行时相同的闪存地址（除去上面的 1MB）。


Microvisor 拥有 MCU 的 BKPSRAM (2KB) 和 SRAM3 的上半部分 (256KB)。SRAM3 的下半部分 (256KB) 以及 SRAM1 的所有剩余 SRAMRAM 组（共 272KB）， 
共计 528KB 可供应用程序使用。


这意味着应用程序有大量内存、存储空间、中断和各种外设可供使用。根据应用程序的性质， 
您可能会满足于使用这些资源而忽略 Microvisor：您可以让 Microvisor 专注于应用程序更新 
和后台远程调试。是的，Microvisor 提供了用于 GDB 调试会话的通道——包括完整的代码步进、变量检查和设置、回溯、断点 
以及寄存器窥视。我们的 CLI 工具包括一个定制的本地 GDB 服务器，通过 Twilio Cloud 将消息传递给设备。


通过系统调用与 Microvisor 进行交互
------------------------------------------------


然而更有可能的情况是，您希望与 Microvisor 进行交互。您可以通过使用其[系统调用](https://www.twilio.com/docs/iot/microvisor/syscalls)和[通知机制](https://www.twilio.com/docs/iot/microvisor/microvisor-notifications)与其进行交互。系统调用允许您的应用程序请求 Microvisor 代表您执行某些操作：


* [网络管理](https://www.twilio.com/docs/iot/microvisor/syscalls/network)。
* [HTTP](https://www.twilio.com/docs/iot/microvisor/syscalls/http) 和 
 [MQTT](https://www.twilio.com/docs/iot/microvisor/syscalls/mqtt) 通讯。
* [通知设置](https://www.twilio.com/docs/iot/microvisor/syscalls/notifications)。
* [低延迟中断配置](https://www.twilio.com/docs/iot/microvisor/syscalls/interrupts)。
* [时间检查](https://www.twilio.com/docs/iot/microvisor/syscalls/time)。
* [设备管理](https://www.twilio.com/docs/iot/microvisor/syscalls/device)。
* [应用程序日志记录](https://www.twilio.com/docs/iot/microvisor/syscalls/application-logging)。


[\![](../../fr-content-src/uploads/2023/05/microvisor-notifications.png)](../../fr-content-src/uploads/2023/05/microvisor-notifications.png)  

点击放大


所有系统调用都会返回一个状态代码，说明请求是否被接受或拒绝（以及原因）。数据通过写入内存位置 
或应用程序提供的缓冲区返回给应用程序。对于高度异步的操作，例如通过 Twilio Cloud 中继的 HTTP 请求， 
当返回的数据可用时，您的应用程序会收到通知。


通知系统将操作绑定到由应用程序提供和设置大小的通知缓冲区上。通知的大小固定（16 字节）， 
并通过写指针添加到缓冲区；缓冲区是循环的。之后会触发一个中断。应用程序的通知 ISR 
可以解析最新信息并采取相应行动。


例如，要发出 HTTP 请求，您必须调用：



```c
enum MvStatus status = mvSendHttpRequest(http_channel_handle, &request_config);  
```

`http_channel_handle` 是一个 32 位无符号整数，用于标识先前建立的 HTTP 数据传输通道； 
应用程序还将建立一个网络“连接”（将其看作是利用 Microvisor 的主要互联网连接的许可）来托管该通道。 `request_config`
是由 [Microvisor 定义的结构体](https://www.twilio.com/docs/iot/microvisor/syscalls/http#mvsendhttprequest)， 
用于指定您想要发起的 HTTP 请求。


如果 Microvisor 接受请求，状态值将为零 (`MV_STATUS_OKAY`)。任何其他值都表示错误：例如， 
请求配置中包含的指针无效，或提供的句柄引用了 MQTT 通道，或通道已经关闭。


即使在这个阶段成功也并不意味着请求已发出并收到响应。在请求转发到 Twilio Cloud 并发出请求之前， 
无法识别错误的请求 URL。此类故障会报告给 Microvisor， 
Microvisor 会通过已设置并绑定到所使用的 HTTP 数据通道的通知中心通知应用程序。从目标服务器接收到的响应也通过相同的方式进行通知。


顺便一提，设备与云的连接采用 TLS 1.2 进行全面托管和保护。它定期接受渗透测试。该通道由 Microvisor 维护， 
用于 OTA 更新、HTTP 和 MQTT 通信、应用程序日志记录和远程调试。


当应用程序创建通知中心时，会为其分配一个中断；当 Microvisor 写入新通知时，就会触发该中断。该 
ISR 会确定当前通知的类型是否为 `MV_EVENTTYPE_CHANNELDATAREADABLE`，并设置一个标志 `received_request`：


```c
void TIM8_BRK_IRQHandler(void) {  
    // Check for a suitable event -- readable data in the channel – by  
    // reading in the latest notification  
    bool got_notification = false;  

    volatile struct MvNotification notification = http_notification_center[current_notification_index];  

    if (notification.event_type == MV_EVENTTYPE_CHANNELDATAREADABLE) {  
        // Flag we need to access received data and to close the HTTP channel  
  
        // when we're back in the main loop. This lets us exit the ISR quickly.  

        // We should not make Microvisor System Calls in the ISR.  
        received_request = true;  
        got_notification = true;  
    }

    if (notification.event_type == MV_EVENTTYPE_CHANNELNOTCONNECTED) {  

        // The HTTP channel signaled its unexpected closure  
        channel_was_closed = true;  
        got_notification = true;  
    }  

    if (got_notification) {  
        // Point to the next record to be written  

        current_notification_index = (current_notification_index + 1) % HTTP_NT_BUFFER_SIZE_R;  
        // Clear the current notifications event  
        // See https://www.twilio.com/docs/iot/microvisor/microvisor-notifications#buffer-overruns  
        notification.event_type = 0;  
    }  

}  


```

FreeRTOS 工作任务会检查该标志，如果该标志被设置，则会使用另一个系统调用请求 Microvisor 提供响应数据。应用程序将提供 
一个用于写入响应的缓冲区和通道 ID：



```c
status = mvReadHttpResponseData(http_channel_handle, &response_buffer);  
```

如果 `&response_buffer` 无效、句柄错误（为 `NULL` 或错误类型）或响应过大无法放入缓冲区，该调用将失败 
。如果响应被写入，它将以定义结构体的形式出现，应用程序可以从中访问响应元数据：HTTP 状态代码、 
包含的标头的数量等。通过单独的 Microvisor 系统调用，可以获取响应体本身和标头值。


Microvisor SDK 提供系统调用绑定、基于 Microvisor 的 ST STM32U585 HAL 版本以及自定义链接器脚本， 
用于处理文本、初始化数据和未初始化数据扇区地址的设置。


如何开始使用 Twilio Microvisor 和 FreeRTOS
--------------------------------------------------------


**如需了解有关 Twilio Microvisor 的更多信息并访问我们的开发板，请访问 [www.microvisor.com](https://www.twilio.com/iot/microvisor-iot-platform)。**


为了解 Microvisor 和基于 FreeRTOS 的应用程序是如何协同工作的，[我们制作了一个演示](https://github.com/twilio/twilio-microvisor-freertos)。这是一个经典的 "Hello, World" 应用程序，它建立了一对 FreeRTOS 任务： 
一个周期性地使连接的 LED 闪烁，另一个执行一些基本的日志记录工作。


该演示将 FreeRTOS 作为 git 子模块引入，并包含了一份预定义的 `FreeRTOSConfig.h` 文件。Microvisor SDK 和 HAL 
也是以相同的方式引入的。需要观察的关键文件是 `main.c`，它负责设置 FreeRTOS 任务并启动调度器。状态信息通过 
Microvisor 的应用程序日志记录系统调用发出。您可以在此基础上开发自己的 Microvisor 托管应用程序。


进一步的 [Microvisor 示例应用程序](https://www.twilio.com/docs/iot/microvisor/sample-code) 
展示了如何处理 HTTP 和 MQTT 请求，以及与连接设备（包括显示器和传感器）进行交互。
