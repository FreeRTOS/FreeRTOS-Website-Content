---
title: 确保 FreeRTOS 的内存安全第 2 部分
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



本帖由 [Nathan Chong](../author/ncchong) 于 2020 年 5 月 7 日发布

在[第 1 部分](../02/ensuring-the-memory-safety-of-freertos-part-1)中，我们讨论了 FreeRTOS 如何解决 
安全问题的一个重要来源：--- 缓冲区溢出 ---， 
解决方法是确保 TCP/IP、ARP、DHCP、DNS 和 FreeRTOS-Plus-TCP TCP/IP 堆栈中解析的 HTTPS 标头的内存安全。我们介绍了 
如何使用自动推理技术、**软件模型检测**，以及 
我们从该技术获得的保证水平如何不同于通过错误查找工具获得的水平 
。

在这篇后续文章中，我们将更详细地研究软件模型检查：让您直观认识 
它所解决的问题，以及软件模型检查工具在实践中如何解决此问题。与 
其他自动推理技术类似，软件模型检查的目标是保证 
程序符合**规范**。规范是程序必须 
始终遵守（无论如何）的属性，例如不得取消引用空指针或在写入时超出 
缓冲区末尾。为了提供这种程度的保证，我们需要一种方法， 
在每个输入上有效推理程序的每个执行路径，搜索违反规范的执行 
。

首先我们来描述一下问题的特征。下图（转载自 
 John Regehr 的演讲  ["SQLite with a fine toothed comb"](https://www.youtube.com/watch?v=LXdyD_mhbzk)。  我们强烈 
推荐这场演讲）显示了程序的*状态空间*。状态是将程序的变量赋值 
。可将状态看作程序变量的快照，如果在调试器中分析程序， 
可以检查这些变量。例如，在具有两个整数变量 `x`  
和 `y` 以及指针 `p` 的程序中，一个可能的状态是 `(x=1, y=2, p=NULL)`。状态空间指 
程序潜在的状态*可能*占用的空间。在图中，状态空间是方框中的*任意*点 
。

继续这个类比，执行程序是通过状态空间的*路径*。图中， 
可能的执行用一系列白色箭头表示，通过执行*达到*的特定状态 
用白点表示。例如，此执行可以是单位测试的运行结果， 
所述单位测试以状态 `(x=0, y=0, p=NULL)` 开始，`x` 递增四次以状态 
 `(x=4, y=0, p=NULL)` 结束。

作为程序员，我们知道有些状态是可取的，有些则不然。接下来我们说得再精确一些。 
首先，蓝色的形状代表程序的*可行状态*：程序通过某种执行可以达到的状态 
。例如，假设程序将 `x` 和 `y` 的值饱和为 `1024`。 
这种情况下，`(x=1024, y=1024, p=NULL)` 属于可行状态（即在蓝色形状内）， 
而 `(x=1024, y=102**5**, p=NULL)` 属于*不*可行状态（即在蓝色形状外）。

![](/media/2020/cmbc-ensuring-memory-pt-2-pic1.png)   
其次，我们说的*错误状态*是指违反了我们尝试验证的规范（例如内存安全性）的任何状态 
。例如，程序可能取消引用 `p`，前提是 
 `x` 和 `y` 的一些复杂条件成立时。如果 `p` 也是 `NULL`，则状态为错误状态。在下面的 
第二个图中，错误状态由红色形状的集合表示。请注意，存在 
这种错误状态并不是问题。关键在于这种状态是否也*可行*。

![](/media/2020/cmbc-ensuring-memory-pt2-pic2.png)   
通过这种设置，我们可以将*错误*描述为既是错误（红色）又是可行的（蓝色）的不理想状态 
。查找所有错误的问题可以看作是寻找位于红色形状和蓝色形状的 
交集处的所有状态，例如左下角。换句话说，证明 
*不存在*一整类错误存在的关键在于证明不存在这样的状态：即红色和蓝色 
形状*永远不会*相交。

这听起来很简单，但 (1) 很难确定任意状态是否可行， 
而且 (2) 即使是程序大小适度，状态的数量也可能是天文数字。例如， 
我们在这篇文章中一直在考虑的简单程序只有三个变量，但有 `2^32 * 2^32 * 2^32` 种 
不同的状态（如果每个整数和指针是 32 位）。 即使对专业程序员来说， 
考虑一个程序所有可能的极端情况也很困难。此外，该程序仅向我们隐含地提供 
可达到的状态。因此，需要自动验证技术来有效推理 
状态空间。

软件模型检查器如何解决这个问题？其关键思路是将程序转化为 
描述可行程序状态和规范集合的*逻辑公式*。逻辑 
公式是一种使用布尔变量和其他连接符的表达式，如逻辑和、 
逻辑或以及否定，并且可以通过给每个变量赋值（true 或 false）来评估为 true 或 false 
。转换经过精心构建，以确保公式与可行的程序状态 
之间的对应性。特别是如果公式存在解，即让公式评估 
为 true 的变量赋值，则对应的是违反规范的一种 
可行程序状态。相反，如果无解，则证明程序 
不可能达到错误状态。这种转换将寻找错误的问题简化为求解公式的问题。 
。

这个求解布尔公式的问题被称为 SAT。原则上，这是一个非常棘手的 
问题：赋值的数量呈指数增长，随着公式中每个变量的增加而翻倍。然而， 
自动推理社区已经建立了约束求解器，对实践中遇到的公式非常有效 
。这些 SAT 求解器（和 SMT 求解器，允许更丰富的表达式， 
涉及诸如整数，数组和字符串等特征）是许多自动推理工具的基础， 
包括软件模型检查器。

感谢您加入本次软件模型检查的短途旅行。我们希望本文 
能为您提供更多关于 FreeRTOS 内存安全性验证的背景信息。正如我们在第 1 部分中写道， 
我们很高兴进一步推动自动化推理技术，为我们的客户提供 
更强有力的保证，并支持有意采用这些技术来开发高质量代码的 
开发人员社区。

* John Regehr，["SQLite with a fine toothed comb"](https://www.youtube.com/watch?v=LXdyD_mhbzk)
* Sharad Malik and Lintao Zhang，["Boolean Satisfiability: From Theoretical Hardness to Practical Success"](https://cacm.acm.org/magazines/2009/8/34498-boolean-satisfiability-from-theoretical-hardness-to-practical-success/fulltext)
* Leonardo De Moura and Nikolaj Bjørner，["Satisfiability Modulo Theories: Introduction and Applications"](https://cacm.acm.org/magazines/2011/9/122785-satisfiability-modulo-theories/fulltext)


## 作者简介

![](https://secure.gravatar.com/avatar/bd7191d11f35f3d6d9b292b87dbbaaa1?s=200&d=mm&r=g)   
Nathan Chong 是 Amazon Web Services 自动推理小组首席工程师。他的 
工作重点在于确保并发系统代码的正确性，特别是在硬件-软件边界。  
[查看此作者的文章](../author/ncchong) 

FreeRTOS 论坛：获得行业领先的专家支持，并与全球同行 
合作。[查看论坛](https://forums.freertos.org/)

