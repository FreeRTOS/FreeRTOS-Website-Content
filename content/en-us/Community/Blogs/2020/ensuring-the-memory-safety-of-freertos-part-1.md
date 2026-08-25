---
title: Ensuring the Memory Safety of FreeRTOS Part 1
description:
date:
feature: blog
categories:
  - Long term support
authors:
  - ncchong
relatedLinks:
  - title: What is FreeRTOS
    link: /Why-FreeRTOS/What-is-FreeRTOS/
---

by [Nathan Chong](../author/ncchong) on 18 Feb 2020

FreeRTOS is a real-time operating system designed for resource-constrained devices, including devices in 
the Internet of Things (IoT). Because these devices are resource-constrained, they do not provide all the 
hardware mechanisms richer operating systems utilize to protect the system from external adversaries. On 
such small devices, security depends on simpler memory protection and execution privilege level hardware, 
and on the operating system code itself.

In this article, we want to tell you about how we are dealing with an important source of security 
issues (buffer overflow) by **ensuring the memory safety** of functions in the FreeRTOS-Plus-TCP library 
that parse TCP, IP, ARP, DHCP, and DNS packets. Our work **uses an automated reasoning technique that 
gives a level of assurance we could not obtain through bug-finding tools**. The same proofs are being 
extended to additional libraries, and to the FreeRTOS kernel itself. This article is the first of two 
on this topic. Part 1 (this article) gives an overview of the technique by applying it to a FreeRTOS 
example and Part 2 (to follow) dives deeper into how the technique works. After reading both, we hope 
you will be equipped to read, understand, and re-run our results (proofs of memory safety), all of which 
are publicly available.


## Moving from Bug-finding to Proof

There are many techniques and tools for improving and testing software quality. Techniques include coding 
standards, code reviews, defensive programming and dynamic testing. Tools include static analyzers such as 
Coverity and Infer as well as dynamic testing with fuzzers and the clang sanitizer family. These tools are 
easy-to-use, scale to large code-bases, and are effective bug-finders. Used together, these techniques and 
tools can give high confidence in the quality of software.

Such tools, however, *cannot guarantee the absence of security issues*. They either use heuristics for finding 
bugs or only consider dynamic runs of the program, which cannot explore all possible behaviors of a program. 
Some tools may, in fact, intentionally skip over known instances of bugs that the tool does not consider 
to be high-risk; skipping low-risk instances avoids the user from being overwhelmed with long lists of minor 
issues.

There are times when we would like a guarantee that a class of software bugs has been completely eliminated. 
An example is a parser of network packets that takes packets off the network---data potentially under the 
control of an adversary with the ability to generate malformed packets intended to trigger a buffer 
overflow---and parses the data into structures consumed by higher-level software. It is critical that an 
adversary is not able to induce unwanted behavior in the parser by sending malformed packets, especially 
if the parser is running with the privileges of the kernel itself.

_One route to achieving greater confidence in the absence of security issues is through the use of automated 
reasoning techniques, based on mathematical logic and proof_. A software model checker is a tool that takes 
source code as input and, in effect, reasons about all possible execution paths through the code on all 
possible inputs looking for executions in which an assertion in the code could be violated, and looking for 
executions in which a security issue like buffer overflow might occur. When a model checker fails to find 
buffer overflow in any execution, the model checker’s certification amounts to a mathematical proof that 
buffer overflow cannot occur.

An important takeaway to keep in mind with proofs is that *all proofs make assumptions*. For example, a 
proof of the statement “if `a` and `b` are positive integers then `a+b` is a positive integer” only 
guarantees that `a+b` is positive if both `a` and `b` are positive. With software model checking, the 
assumptions are typically about the inputs to the program being proved. A strong proof may assume a 
buffer can be of any length with any contents. A weaker proof may assume that the length of the buffer 
is limited to 1000 bytes. That is, the weaker proof does not make any guarantees about what can happen 
if the buffer is 1001 bytes long. The art of using a model checker is finding the weakest set of assumptions 
that allows the model checker to prove the desired property. Our proofs are publicly available: you 
can see the assumptions we are making, and assure yourself that our assumptions are reasonable.


## Memory Safety

A program is memory safe if it only reads and writes to memory that it is allowed to. A common example 
of a memory safety violation is buffer overflow. A buffer overflow occurs when a program writes beyond 
the bounds of an object in memory, such as an input buffer, potentially overwriting trusted data, such 
as the function return pointer. A Microsoft study indicates that approximately 70% of security issues 
addressed by Microsoft security updates each year are due to memory safety 
violations. [[Slide 10, Trends, challenge, and shifts in software vulnerability mitigation, Miller](https://github.com/microsoft/MSRC-Security-Research/blob/master/presentations/2019_02_BlueHatIL/2019_01%20-%20BlueHatIL%20-%20Trends%2C%20challenge%2C%20and%20shifts%20in%20software%20vulnerability%20mitigation.pdf)]

An interesting example of buffer overflow is described 
in [CVE-2019-15505](https://nvd.nist.gov/vuln/detail/CVE-2019-15505). In this example, an adversary with 
the ability to craft the stream of bytes for the USB driver could overwrite the kernel with arbitrary 
code, and run that code with the privileges of the kernel itself. _This is an example of a simple error 
with significant consequences for software security_.

Our goal is to prove that memory safety violations can never happen in the FreeRTOS kernel and libraries.


## Software Model Checking

Software model checking is an automated reasoning technique for proving properties like memory safety. 
Model checking works by *effectively reasoning about every execution path through a program on every 
input*, searching for executions that violate an assertion in the code or violate a property like memory 
safety. It is important to note that modern software model checkers can be applied effectively to real-world 
code-bases such as FreeRTOS. Because the FreeRTOS code-base is written in C, we have applied a software 
model checker called [CBMC (C Bounded Model Checker)](https://www.cprover.org/cbmc/).


## Proving an API Method of HTTP Memory Safe

To help you understand how we have applied software model checking to FreeRTOS consider one component 
that we have proved memory safe: the client-side implementation of 
HTTP [[GitHub]](https://github.com/aws/amazon-freertos/tree/master/libraries/c_sdk/standard/https/src). 
Let us discuss the memory safety of the `AddHeader` method. The purpose of this method is to add a 
header---consisting of a header name and a header value---to the list of headers of an HTTP request 
under construction. The signature of the function is:

```c
IotHttpsReturnCode_t IotHttpsClient_AddHeader(
        IotHttpsRequestHandle_t reqHandle,
        const char * pName,
        uint32_t nameLen,
        const char * pValue,
        uint32_t valueLen );
```

The first argument `reqHandle` is a pointer to a request object under construction. The handle contains 
the context for the request, including the response header. The following figure shows the state of the 
program heap before the method call. The header is a buffer of bytes pointed-to by `reqHandle->pHeaders`. 
There is space for appending new header name/value pairs at `reqHandle->pHeadersCur`. To avoid buffer 
overflow the method must not write past the end of the buffer (pointed-to by `reqHandle->pHeadersEnd`). 
Note there are other memory safety issues (such as passing NULL pointers) that are also handled by our proof.

![](/media/2020/Ensuring-Memory-Safety-1.png)   
If there is sufficient space for the name/value pair then the method is successful and the following figure 
shows the state of the program heap.

![](/media/2020/cbmc-ensuring-memory-2.png)   
Our goal is to prove that the implementation of this method is memory safe. In particular, we want to 
prove that for every execution of the method on every possible input, the implementation never triggers 
a buffer overflow. To analyze this problem with CBMC, we write a *proof harness* that constructs 
an *arbitrary* state that the method is called-on. Note that the harness is not executable. Consider 
the input variable nameLen: a 32-bit unsigned integer. In a bug-finding tool, we would need to consider 
each 2^32 value (or more-likely do a representative sampling). In the proof harness, we leave the variable 
uninitialized - this lets CBMC consider any value for the variable.

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

The function `allocate_IotRequestHandle` on line 2 returns either a `NULL` pointer or a pointer to space 
allocated to hold a request object. This space is initialized to a completely unconstrained value. For 
example, the header buffer can contain any arbitrary character data. In addition, the pointers in the 
object are allowed to point-to arbitrary locations in memory.

This is too unconstrained: for example, the pointer to the end of the header buffer might point-to a 
location before the start of the buffer. To avoid reasoning about these unreasonable cases we use the 
Boolean function (also called a predicate) `is_valid_IotRequestHandle` to test that the response object 
is “well-formed”. For example, that the pointers for the header buffer are 
ordered `pHeaders <= pHeadersCur <= pHeadersEnd`. The harness assumes using `__CPROVER_assume()` on 
line 4 that the request object has at-least these characteristics.

The function `allocate_CString` on lines 7 and 8 encapsulates (for clarity in this article) repeated 
lines appearing in the actual harness. The function returns either a `NULL` pointer or a pointer to 
a C string (a byte buffer terminated with a null termination `‘\0’` character) of the given length. 
The function adds an assumption to the length to being at most one less than the maximum value of a 
32-bit unsigned integer in order to leave enough space for the null termination character. The 
function `allocate_CString` on lines 7 and 8 encapsulates for this article a few repeated lines appearing 
in the actual harness. The function returns either a `NULL` pointer or a pointer to a C string (a byte 
buffer terminated with a null termination `‘\0’` character) of the given length. The function adds an 
assumption to the length to being at most one less than the maximum value of a 32-bit unsigned integer 
in order to leave enough space for the null termination character.

```c
1  char * allocate_CString(uint32_t len) {
2     __CPROVER_assume(len < UINT32_MAX-1);
3     char * result = safeMalloc(len+1);
4     if (result) result[len] = '\0';
5     return result;
6 }
```

Finally, the harness invokes the `IotHttpsClient_AddHeader` method with the arbitrary request handle 
and the arbitrary strings for the name and value of the header being added. If CBMC cannot find a memory 
safety violation then this is a proof that the HTTP API function is memory safe for any arbitrary input 
that satisfies the assumptions of the harness.


## Conclusion

We have discussed how we are using software model checking, an automated reasoning technique, to ensure 
the memory safety of code in FreeRTOS. Unlike bug-finding tools, this technique can give guarantees of 
correctness based on mathematical logic and proof. So far, we have applied this technique to the TCP, 
IP, ARP, DHCP, and DNS headers parsing in the FreeRTOS-Plus-TCP library, as well as to HTTP header 
processing.

All proofs we have written are available in the AWS FreeRTOS repository 
on [[GitHub]](https://github.com/aws/amazon-freertos), and are being migrated into the main FreeRTOS 
repository, which is now also in [[Github]](https://github.com/freertos) . All of the tools we have 
used, such as CBMC, are available in the open source, and instructions for installing them are also 
available in the AWS FreeRTOS repository [[GitHub]](https://github.com/aws/amazon-freertos/tree/master/tools/cbmc).

Now that you've read this article, we hope you will be encouraged to examine our proofs and assure yourself 
that the assumptions in our proof harnesses are reasonable. If you are truly inspired then you can run 
and re-validate the proofs by following the 
instructions [[GitHub]](https://github.com/aws/amazon-freertos/blob/master/tools/cbmc/README). Looking 
forward, we are excited about pushing automated reasoning techniques even further to provide even stronger 
assurances to our customers and supporting a community of developers interested in adopting these techniques 
to develop high-quality code themselves.

Stay tuned for the second article in this series that will dive deeper into how software model checking 
works under the hood.


## Acknowledgments

We are grateful to the following individuals whose work is covered in this article: Debasmita Lohar (Max 
Planck Institute for Software Systems) who wrote the FreeRTOS HTTP library proofs as an intern with Amazon 
in 2019, Sarena Meas (Software Development Engineer, AWS) lead engineer of the FreeRTOS HTTP library, 
and Mark Tuttle (Principal Applied Scientist, AWS). We also acknowledge and thank Jonathan Eidelman, 
Kareem Khazem, Felipe Monteiro, Daniel Schwartz-Narbonne, Michael Tautschnig, Mark Tuttle, and Mike 
Whalen for their contributions to the use and adoption of CBMC in Amazon.


## About the author

![](https://secure.gravatar.com/avatar/bd7191d11f35f3d6d9b292b87dbbaaa1?s=200&d=mm&r=g)   
Nathan Chong is a Principal Engineer with the Automated Reasoning Group at Amazon Web Services. His 
work focuses on the correctness of concurrent systems code, particularly at the hardware-software boundary.   
[View articles by this author](../author/ncchong)

FreeRTOS forums: Get industry-leading support from experts and collaborate with peers around the 
globe. [View Forums](https://forums.freertos.org/)
