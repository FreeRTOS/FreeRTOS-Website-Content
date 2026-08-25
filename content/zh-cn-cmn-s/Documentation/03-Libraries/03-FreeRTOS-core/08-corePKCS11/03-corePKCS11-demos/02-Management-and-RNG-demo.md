---
title: corePKCS11 管理和随机数演示
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---


* 本页内容：
    + [简介](#简介)
    + [源代码组织](#源代码组织)
    + [配置演示项目](#配置演示项目)
    + 构建演示项目
    + [功能](#功能)


## 简介

本演示是 corePKCS11 演示系列中的第一个，介绍了 PKCS #11 API 中管理 PKCS #11堆栈相关部分， 
并展示了如何使用 PKCS #11 生成随机数。如需查看 PKCS #11 标准， 
请点击[此处](http://docs.oasis-open.org/pkcs11/pkcs11-base/v2.40/os/pkcs11-base-v2.40-os.html)。 

演示及其相关网页交替使用 PKCS #11 定义的术语， 
如 PKCS #11 API、堆栈、标准等。标准中定义的术语总结如下："Cryptoki" 
是指 PKCS #11 标准中定义的加密令牌接口，即 PKCS #11 
API 或函数。Cryptoki 的实现称为“Cryptoki 库”， 
等同于术语“PKCS #11 实现”或“PKCS #11 堆栈”。

PKCS #11 规范以三个头文件的形式分发：


**pkcs11.h**   
这是主头文件，也是唯一需要添加到应用程序中的文件。需要定义一些宏， 
方可将其添加到应用程序中。这些定义位于 
"core_pkcs11.h" 中（请参阅 `<freertos>/libraries/freertos_plus/source/corepkcs11/include/core_pkcs11.h`）。 
在添加 PKCS #11 库时，请先添加 "core_pkcs11.h"，再添加 "pkcs11.h"。 

**pkcs11f.h**   
该头文件中包含函数原型。

**pkcs11t.h**   
该头文件中包含 PKCS #11 规范中定义的各种类型。

PKCS #11 演示项目使用 
[FreeRTOS Windows 移植](/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-Emulator-for-Visual-Studio-and-Eclipse-MingW)， 
因此可以在 Windows 上使用 
[社区免费版 Visual Studio](https://visualstudio.microsoft.com/vs/community/) 进行构建和评估， 
无需任何特定 MCU 硬件。

本演示中介绍的函数集分类如下：

+ 通用函数
  + 插槽和令牌管理函数
  + 会话管理函数
  + 随机数生成函数


## 源代码组织

基于 PKCS #11 的双向验证的 Visual Studio 解决方案演示名为 `pkcs11_demo.sln`， 
位于 `FreeRTOS\FreeRTOS-Plus\Demo\corePKCS11_Windows_Simulator\` 目录 
（详见 FreeRTOS 主下载内容）。

[\![](../fr-content-src/uploads/2020/10/PKCS11-Source-Code-Organization.png)](../fr-content-src/uploads/2020/10/PKCS11-Source-Code-Organization.png)   
*点击放大*


## 配置演示项目

要配置演示项目，请在 `pkcs11\_demo\_config.h` 中将 `configPKCS11\_MANAGEMENT\_AND\_RNG\_DEMO` 设置为 1。


## 构建演示项目

演示项目使用[社区免费版 Visual Studio](https://visualstudio.microsoft.com/vs/community/)。

1. 在 Visual Studio IDE 中，打开 Visual Studio 解决方案 
   文件 `FreeRTOS\FreeRTOS-Plus\Demo\corePKCS11_Windows_Simulator\pkcs11_demos.sln`。
2. 在 IDE 的 '**build**'（构建）菜单中选择 '**build solution**' （构建解决方案）。


## 功能

本演示的入口点是 **vPKCS11ManagementAndRNGDemo**。此函数概述了 
如何启动 PKCS #11 会话并用其生成随机数的基本步骤。

第一步是获取函数指针结构体，其中包含 
指向 PKCS #11 堆栈所实现函数的指针。未实现的函数始终为 NULL。这很有用， 
因为某些 PKCS #11 实现可能不会定义每个函数。演示将对未实现的函数 
进行断言。在实际应用中，考虑这种情况可能会很有用， 
这可确保库在不同的 PKCS #11 实现之间兼容。


### 获取 PKCS #11 函数列表：

```c
/* The CK_FUNCTION_LIST is a structure that contains the Cryptoki version  
 * and a function pointer to each function in the Cryptoki API. If the  
 * function pointer is NULL it is unimplemented.   
 */  
CK_FUNCTION_LIST_PTR pxFunctionList = NULL;  
  
/* We use the function list returned by C_GetFunctionList to see what functions  
 * the Cryptoki library supports. We use asserts to ensure that all the  
 * functionality needed in this demo is available.   
 */  
xResult = C_GetFunctionList( &pxFunctionList );  
configASSERT( xResult == CKR_OK );  
configASSERT( pxFunctionList != NULL );  
configASSERT( pxFunctionList->C_Initialize != NULL );  
configASSERT( pxFunctionList->C_GetSlotList != NULL );  
configASSERT( pxFunctionList->C_OpenSession != NULL );  
configASSERT( pxFunctionList->C_Login != NULL );  
configASSERT( pxFunctionList->C_GenerateRandom != NULL );  
configASSERT( pxFunctionList->C_CloseSession != NULL );  
configASSERT( pxFunctionList->C_Finalize != NULL );   

```

从 PKCS #11 实现中获取函数后，可以通过 
调用 `C_Initialize` 初始化 PKCS#11 实现。此函数不保证线程安全， 
在调用时应谨慎考虑并发问题。演示中使用的 PKCS #11 堆栈 
未实现规范中定义的线程安全机制。因此，在使用不同的 PKCS #11 堆栈时， 
可能需要重新检查调用 `C_Initialize` 的代码，以确保 
正确处理并发问题。


### 初始化 PKCS #11 堆栈：

```c
/* This Cryptoki library does not implement any initialization arguments. At the time of  
 * writing this demo, the purpose of these optional arguments is to provide  
 * function pointers for mutex operations.   
 */  
CK_C_INITIALIZE_ARGS xInitArgs = { 0 };  
  
/* C_Initialize will initialize the Cryptoki library and the hardware it  
 * abstracts.   
 */  
xResult = pxFunctionList->C_Initialize( &xInitArgs );  
configASSERT( xResult == CKR_OK );   

```

初始化后，我们会查询应用程序可以使用的插槽。PKCS #11 将插槽定义为 
“可能包含令牌的逻辑读取器”。演示中将始终使用 
`C_GetSlotList` 返回的第一个插槽，这是因为编写该演示的实现仅有一个插槽。通过插槽， 
应用程序可以指定要使用的令牌。在许多实现中，插槽与令牌的关系 
各不相同。重点是 SlotID 将指定我们希望在应用程序会话中使用的 
令牌。


### 选择插槽：

```c
/* A slot ID is an integer that defines a slot. The Cryptoki definition of  
 * a slot is "A logical reader that potentially contains a token."  
 *  
 * Essentially it is an abstraction for accessing the token. The reason for  
 * this is some tokens are a physical "card' that needs to be inserted into  
 * a slot for the device to read.  
 *  
 * A concrete example of a slot could be a USB Hardware Security Module (HSM),  
 * which generally appears as a singular slot, and abstracts it's internal "token".  
 *  
 * Some implementations have multiple slots mapped to a single token, or maps  
 * a slot per token.   
 */  
CK_SLOT_ID * pxSlotId = NULL;  
  
/* CK_ULONG is a long unsigned integer as defined by PKCS #11. */  
CK_ULONG xSlotCount = 0;  
  
/* C_GetSlotList will retrieve an array of CK_SLOT_IDs.  
 * This Cryptoki library does not implement slots, but it is important to  
 * highlight how Cryptoki can be used to interface with real hardware.  
 *  
 * By setting the first argument "tokenPresent" to true, we only retrieve  
 * slots that have a token. If the second argument "pSlotList" is NULL, the  
 * third argument "pulCount" will be modified to contain the total slots.   
 */  
xResult = pxFunctionList->C_GetSlotList( CK_TRUE,  
                                         NULL,  
                                         &xSlotCount );  
configASSERT( xResult == CKR_OK );  
  
/* Since C_GetSlotList does not allocate the memory itself for getting a list  
 * of CK_SLOT_ID, we allocate one for it to populate with the list of  
 * slot ids.   
 */  
pxSlotId = pvPortMalloc( sizeof( CK_SLOT_ID ) * ( xSlotCount ) );  
configASSERT( pxSlotId != NULL );  
  
/* Now since pSlotList is not NULL, C_GetSlotList will populate it with the  
 * available slots.   
 */  
xResult = pxFunctionList->C_GetSlotList( CK_TRUE,  
                                         pxSlotId,  
                                         &xSlotCount );  
configASSERT( xResult == CKR_OK );  

```

下一步是创建会话，将应用程序连接到由 PKCS #11 堆栈返回的 
插槽。规范将会话定义为“应用程序和令牌之间的逻辑连接”。 
源代码和 PKCS #11 规范中对此进行了进一步解释。要建立会话， 
可以调用 `C_OpenSession`，然后指定应用程序希望使用的插槽。


### 打开 PKCS #11 会话：

```c
/* A session is defined to be "The logical connection between an application  
 * and a token."  
 *  
 * The session can either be private or public, and differentiates  
 * your application from the other users of the token.   
 */  
CK_SESSION_HANDLE hSession = CK_INVALID_HANDLE;  
  
/* Since this Cryptoki library does not actually implement the concept of slots,  
 * but we will use the first available slot, so the demo code conforms to  
 * Cryptoki.  
 *  
 * C_OpenSession will establish a session between the application and  
 * the token and we can then use the returned CK_SESSION_HANDLE for  
 * cryptographic operations with the token.  
 *  
 * For legacy reasons, Cryptoki demands that the CKF_SERIAL_SESSION bit  
 * is always set.   
 */  
xResult = pxFunctionList->C_OpenSession( pxSlotId[0],  
                                         CKF_SERIAL_SESSION | CKF_RW_SESSION,  
                                         NULL, /* Application defined pointer. */  
                                         NULL, /* Callback function. */  
                                         &hSession );  
configASSERT( xResult == CKR_OK );  

```

会话现已建立，可用来生成随机数。随机数 
在加密操作中广泛使用，许多加密算法依赖随机数生成器的“随机性”， 
以确保密码不会遭到破解。


### 生成随机数缓冲区：

```c
/* CK_BYTE is a PKCS #11 type that is defined as an unsigned char. */  
CK_BYTE xRandomData[ 10 ] = { 0 };  
  
/* C_GenerateRandom generates random or pseudo random data. As arguments it  
 * takes the application session, and a pointer to a byte buffer, as well as  
 * the length of the byte buffer. Then it will fill this buffer with random  
 * bytes.   
 */  
xResult = pxFunctionList->C_GenerateRandom( hSession,  
                                            xRandomData,  
                                            sizeof( xRandomData ) );  
configASSERT( xResult == CKR_OK );  
  
for( ulIndex = 0; ulIndex < sizeof( xRandomData ); ulIndex++ )  
{  
    configPRINTF( ( "Generated random number: %x\r\n", xRandomData[ ulIndex ] ) );  
}  

```

加密操作现已完成，演示将按照以下步骤清理资源：

1. 关闭活动会话。
2. 调用 `C_Finalize` 以取消初始化 PKCS #11 堆栈。


### 清理：

```c
/* C_CloseSession closes the session that was established between the  
 * application and the token. This will clean up the resources that maintained  
 * the link between the application and the token. If the application wishes  
 * to use the token again, it will need to open a new session.   
 */  
xResult = pxFunctionList->C_CloseSession( hSession );  
configASSERT( xResult == CKR_OK );  
  
/* C_Finalize signals to the Cryptoki library that the application is done  
 * using it. It should always be the last call to the Cryptoki library.  
 * NULL should always be passed as the argument, as the parameter is currently  
 * just reserved for future revisions.  
 *  
 * Calling this function in a multi threaded environment can lead to undefined  
 * behavior if other threads are accessing the Cryptoki library.   
 */  
xResult = pxFunctionList->C_Finalize( NULL );  
configASSERT( xResult == CKR_OK );  

```

