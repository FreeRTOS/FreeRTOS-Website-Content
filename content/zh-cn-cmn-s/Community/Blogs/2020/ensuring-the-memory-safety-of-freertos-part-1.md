---
title: 确保 FreeRTOS 内存安全第1 部分
date: null
feature: blog
categories:
- 长期支持
authors:
- ncchong
relatedLinks:
- title: 什么是 FreeRTOS
  link: /Why-FreeRTOS/What-is-FreeRTOS/
---

本帖由 [Nathan Chong](../author/ncchong) 于 2020 年 2 月 18 日发布

FreeRTOS 是专为资源受限设备设计的实时操作系统，包括 
物联网 (IoT) 中的各种设备。由于这些设备属于资源限制型设备，因此，无法提供 
资源更多操作系统所使用的硬件机制来使系统免受外部干扰。在 
这类小型设备上，安全取决于较简单的内存保护、具有执行优先级的硬件 
以及操作系统代码本身。

本文将介绍如何通过 
确保 FreeRTOS-Plus-TCP 库中函数**的内存安全**来处理安全问题的一个重要来源（缓冲区溢出）。 
这些函数用于解析 TCP、IP、ARP、DHCP 和 DNS 数据包。我们**使用了自动推理技术，通过该技术，我们
获得了通过错误查找工具无法获得的保证水平**。此类验证也 
适用于其他库，乃至 FreeRTOS 内核本身。共有两篇文章介绍这一主题，本文 
为第一篇。第 1 部分（本文）将此技术运用于一个 FreeRTOS  
示例从而简单介绍这项技术，而第 2 部分（后一篇文章）则更深入探讨技术的工作原理。通过这两篇文章，我们希望 
读者能够阅读、理解和重新运行我们的结果（内存安全验证） ，这些结果 
都可公开获取。


## 从发现错误改为验证错误

改进和测试软件质量的技术和工具种类繁多。这类技术包括编码 
标准、代码审查、防御性编程和动态测试。这类工具包括 
 Coverity 和 Infer 等静态分析解决方案，以及使用模糊器和 clang sanitizer 系列进行的动态测试。这些工具 
易于使用，可扩展至大型代码库，属于有效的错误检测工具。这些技术和工具 
结合使用，利于提升人们对软件质量的信心。

然而，此类工具*无法保证完全避免安全问题*。这类工具中，有些使用启发式方法来查找 
错误，有些只考虑程序的动态运行，这样便无法探索程序的所有可能行为。 
事实上，有些工具可能故意跳过已知错误实例，因为这些工具并不认为这些漏洞 
存在高风险；跳过低风险实例可避免用户看到太长串的小问题 
。

有时候，我们希望能够保证完全消除某一类软件故障。 
例如，由于---攻击者可能控制数据，进而生成旨在触发缓冲区溢出的畸形数据包， 
因而网络数据包解析器从网络中提取数据包， 
---并将数据解析为供高级软件使用的架构。攻击者不能 
通过发送畸形数据包来诱导解析器中的不必要行为，特别是在解析器使用内核 
本身的权限运行时，这一点至关重要。

_在没有安全问题的情况下实现更大信心的一个途径是使用基于数学逻辑和验证的自动
推理技术_。软件模型检查器指的是一种将 
源代码作为输入的工具，对所有可能输入的代码中所有可能的执行路径 
进行分析，查找可能违反代码断言的执行，查找 
可能出现缓冲区溢出等安全问题的执行。当模型检查器在任何执行中 
都无法找到缓冲区溢出时，模型检查器的验证相当于一个论证缓冲区溢出不可能出现的数学证明 
。

关于验证，需要牢记的重要结论是*所有验证均须做假设*。例如， 
对“如果 `a` 和 `b` 是正整数，则 `a+b` 是正整数”的验证仅能 
保证在 `a` 和 `b` 均为正时， `a+b` 为正。在软件模型检查中， 
假设通常关于被验证程序的输入。有力验证可以假设一个 
缓冲区可以是任何长度的任何内容。薄弱验证可以假设缓冲区的长度 
限制为 1000 字节。也就是说，薄弱验证不能保证缓冲区为 1001 字节时， 
会发生什么情况。使用模型检查器的诀窍在于找到允许模型检查器验证 
所需属性的一组最弱假设。我们的验证均公开可查：您 
可以看到我们目前所作假设，而且确认我们的假设是合理的。


## 内存安全

如果程序仅读取和写入允许的内存，则该程序是内存安全的。缓冲区溢出 
是内存安全违规的常见示例。程序写入超出内存中对象（如输入缓冲区）界限时， 
会发生缓冲区溢出，进而可能覆盖可信数据，例如 
函数返回指针。微软的一项研究表明，每年微软安全更新所解决的 
安全问题中，大约 70% 是由于内存安全违规所导致 
。[[Slide 10 ，软件漏洞缓解的趋势、挑战和转变，Miller](https://github.com/microsoft/MSRC-Security-Research/blob/master/presentations/2019_02_BlueHatIL/2019_01%20-%20BlueHatIL%20-%20Trends%2C%20challenge%2C%20and%20shifts%20in%20software%20vulnerability%20mitigation.pdf)]。

关于缓冲区溢出的一个有趣例子参见 
 [CVE-2019-15505](https://nvd.nist.gov/vuln/detail/CVE-2019-15505)。在这个例子中，如果攻击者 
能够为 USB 驱动程序制作字节流，就可以用任意代码覆盖 
内核，并以内核本身的权限运行该代码。_这是一个简单错误的示例，
会对软件安全性产生重大影响_。

我们的目标是验证在 FreeRTOS 内核和库中，始终不会发生内存安全违规行为。


## 软件模型检查

软件模型检查是一种用于证明内存安全等属性的自动推理技术。 
模型检查的工作原理是*通过对程序的每个
输入的执行路径进行有效推理*，搜索违反代码中的断言或违反内存安全等属性的执行 
。需注意现代软件模型检查器可以有效地应用于真实世界的 
代码库，如 FreeRTOS，这一点至关重要。由于 FreeRTOS 代码库采用 C 语言编写，因此我们应用了一个名为 
 [CBMC（C 语言边界模型检查器）的软件模型检查器](https://www.cprover.org/cbmc/)。


## HTTP 内存安全的 API 验证方法

为了帮助您了解我们如何将软件模型检查应用于 FreeRTOS，请考虑 
一个我们已验证内存安全的组件： 
HTTP 的客户端实现 [GitHub] (https://github.com/aws/amazon-freertos/tree/master/libraries/c_sdk/standard/https/src)。 
现在我们探讨 `AddHeader` 方法的内存安全性。此方法旨在将 
标头（---由标头名称和标头值组成---）添加到正在构建的 HTTP 请求的标头列表中 
。函数的签名为：

```c
IotHttpsReturnCode_t IotHttpsClient_AddHeader(
        IotHttpsRequestHandle_t reqHandle,
        const char * pName,
        uint32_t nameLen,
        const char * pValue,
        uint32_t valueLen );
```

第一个实参 `reqHandle` 是指向正在构建的请求对象的指针。句柄包含 
请求的上下文，包括响应标头。下图展示了方法调用前的 
程序堆的状态。标头是 `reqHandle->pHeaders`指向的字节缓冲区。 
 `reqHandle->pHeadersCur` 处有添加新标头名称/值对的空间。为避免缓冲区 
溢出，该方法写入时不得超出缓冲区末端（由 `reqHandle->pHeadersEnd` 指向）。 
请注意，我们的验证还处理了其他内存安全问题（例如传递 NULL 指针）。

![](/media/2020/Ensuring-Memory-Safety-1.png)   
如果名称/值对空间充足，则该方法成功，下图 
展示了程序堆的状态。

![](/media/2020/cbmc-ensuring-memory-2.png)   
我们的目标是验证这种方法的实现是内存安全的。我们尤其想验证， 
对于每个可能的输入，每次执行该方法时，该实现均不会触发 
缓冲区溢出。为了使用 CBMC 分析这个问题，我们写入了一个*验证线束*，它构造了 
调用方法的*任意*状态。请注意，线束不可执行。考虑 
输入变量 nameLen：一个 32 位无符号整数。在错误查找工具中，我们需要考虑 
每个 2^32 值（或更可能执行代表性抽样）。在验证线束中，我们保留变量 
未初始化，让 CBMC 可以考虑变量的任何值。

```c
1    void harness() {
2      IotHttpsRequestHandle_t reqHandle = allocate_IotRequestHandle();
3      if (reqHandle)
4        __CPROVER_assume(is_valid_IotRequestHandle(reqHandle));
5      uint32_t nameLen;
6      uint32_t valueLen;
7      char * pName = allocate_CString(nameLen);
8      char * pValue = allocate_CString(valueLen);
9      IotHttpsClient_AddHeader(reqHandle, pName, nameLen, pValue, valueLen);
10  }
```

第 2 行的函数 `allocate_IotRequestHandle` 返回 `NULL` 指针或指向 
分配用于保存请求对象的空间的指针。已将该空间初始化为完全不受约束的值。例如， 
标头缓冲区可以包含任何任意字符数据。此外，允许 
对象中的指针指向内存中的任意位置。

这样过于不受约束：例如，指向标头缓冲区末端的指针可能指向 
缓冲区开始之前的位置。为了避免对这些不合理情况进行推理，我们使用 
布尔函数（也称为谓词）`is_valid_IotRequestHandle` 来测试响应对象 
是否“格式正确”。例如，标头缓冲区的指针是按 
 `pHeaders <= pHeadersCur <= pHeadersEnd` 进行排序。线束在第 4 行使用 `__CPROVER_assume()`， 
假设请求对象至少具有这些特性。

第 7 行和第 8 行的函数 `allocate_CString` 封装了（确保在本文中清晰可见） 
实际线束中出现的重复行。函数返回 `NULL` 指针或指向 
给定长度 C 语言字符串（以空终止字符 `‘\0’` 终止的字节缓冲区）的指针。 
该函数将长度假设为比 32 位无符号整数的最大值 
小一，以便为空终止字符留出足够的空间。 
第 7 行和第 8 行的函数 `allocate_CString` 封装了（在本文中） 
实际线束中出现的若干重复行。函数返回 `NULL` 指针或指向给定长度 
 C 语言字符串（以空终止字符 `‘\0’` 终止的字节缓冲区）的指针。该函数将 
长度假设为比 32 位无符号整数的最大值小一， 
以便为空终止字符留出足够的空间。

```c
1  char * allocate_CString(uint32_t len) {
2     __CPROVER_assume(len < UINT32_MAX-1);
3     char * result = safeMalloc(len+1);
4     if (result) result[len] = '&bsol;0';
5     return result;
6 }
```

最后，线束调用 `IotHttpsClient_AddHeader` 方法，添加了 
任意请求句柄以及标头名称和值的任意字符串。如果 CBMC 无法发现内存 
安全违规，则这证明 HTTP API 函数对于满足线束假设的任何任意输入 
均是内存安全的。


## 结论

我们讨论了如何使用软件模型检查（一种自动推理技术）来确保  
FreeRTOS 中代码的内存安全。与错误查找工具不同，这项技术可以保证 
基于数学逻辑和验证的正确性。到目前为止，我们已将此技术应用于 TCP、 
IP、ARP、DHCP 和 FreeRTOS-Plus-TCP 库中解析的 DNS 标头，以及 HTTP 标头处理 
。

可访问 [GitHub] 上的 AWS FreeRTOS 存储库 (https://github.com/aws/amazon-freertos)  
获取我们编写的所有验证，而且所有验证正在迁移到主 FreeRTOS  
存储库（目前也在 [Github] 上，网址：https://github.com/freertos）。我们所用的全部工具 
（例如 CBMC）均已开源，其安装说明也可参见 
AWS FreeRTOS 存储库 [GitHub] (https://github.com/aws/amazon-freertos/tree/master/tools/cbmc)。

既然您已阅读本文，我们希望您能从中获得鼓舞，查看我们的验证，确保 
我们验证线束中的假设具有合理性。若您确实从中受到启发，则可以 
按照下列说明 [GitHub] (https://github.com/aws/amazon-freertos/blob/master/tools/cbmc/README)  
运行并重新验证所有验证程序。展望 
未来，我们很高兴进一步推动自动化推理技术，为我们的客户提供 
更强有力的保证，并支持有意采用这些技术来开发高质量代码的 
开发人员社区。

敬请关注本系列的第二篇文章，届时将带您深入了解软件模型检查的 
幕后工作原理。


## 致谢

感谢以下人士参与了本文中涉及的工作：Debasmita Lohar（Max  
Planck 软件系统研究所）于 2019 年以 Amazon 实习生身份编写了 FreeRTOS HTTP 库验证； 
Sarena Meas（AWS 软件开发工程师），FreeRTOS HTTP 库首席工程师； 
Mark Tuttle（AWS 首席应用科学家）。我们也感谢 Jonathan Eidelman、 
Kareem Khazem、Felipe Monteiro、Daniel Schwartz-Narbonne、Michael Tautschnig、Mark Tuttle 和 Mike 
Whalen 对在 Amazon 中使用和采用 CBMC 所作的贡献。


## 作者简介

![](https://secure.gravatar.com/avatar/bd7191d11f35f3d6d9b292b87dbbaaa1?s=200&d=mm&r=g)   
Nathan Chong 是 Amazon Web Services 自动推理小组首席工程师。他的 
工作重点在于确保并发系统代码的正确性，特别是在硬件-软件边界。  
[查看此作者的文章](../author/ncchong)

FreeRTOS 论坛：获得行业领先的专家支持，并与全球同行 
合作。[查看论坛](https://forums.freertos.org/)

