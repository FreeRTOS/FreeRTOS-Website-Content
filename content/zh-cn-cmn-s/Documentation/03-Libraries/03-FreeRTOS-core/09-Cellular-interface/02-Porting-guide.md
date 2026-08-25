---
title: 将蜂窝接口库移植到另一个调制解调器
created: 2018-09-20 00:00:00.0 UTC
categories:
- 内核
relatedLinks:
- title: 为什么使用 FreeRTOS
  link: /Why-FreeRTOS/Why-FreeRTOS/
---

FreeRTOS 现支持 TCP 卸载蜂窝抽象层的 AT 命令。为了增加 
对新蜂窝调制解调器的支持，开发人员可以使用 
已经实现 3GPP 标准 AT 命令的[通用组件](https://github.com/FreeRTOS/FreeRTOS-Cellular-Interface/tree/main/source) 
。 

要移植[通用组件](Documentation/api-ref/cellular/cellular_porting_module_guide.md)，请执行以下操作：

1. 实现 
   [cellular_common_portable.h](https://github.com/FreeRTOS/FreeRTOS-Cellular-Interface/blob/main/source/include/common/cellular_common_portable.h) 中定义的蜂窝调制解调器移植接口（[文档](Documentation/api-ref/cellular/cellular__common__portable_8h.md)）。

2. 实现使用供应商特定（非 3GPP）AT 命令的蜂窝接口库 API 的子集 
   。要实现的 API 是在此表中**未用**“o”标记的 API 
   [](Documentation/api-ref/cellular/cellular_common__a_p_is.md)。

3. 实现处理供应商特定（非 3GPP） 
   非请求结果码 (URC) 的蜂窝接口库回调函数。要实现的 URC 处理程序是在此表中**未用**“o”标记的 API 
   [](Documentation/api-ref/cellular/cellular_common__u_r_c_handlers.md)。

[蜂窝通用应用程序接口文件](Documentation/api-ref/cellular/cellular_porting_module_guide.md)提供了 
每个步骤所需的详细信息。我们建议您先克隆一个现有调制解调器的实现， 
然后在您的调制解调器供应商特定（非 3GPP）AT 命令不同的地方进行修改 
。

当前示例实现： 

* [Quectel BG96](https://github.com/FreeRTOS/FreeRTOS-Cellular-Interface-Reference-Quectel-BG96)
* [Sierra Wireless HL7802](https://github.com/FreeRTOS/FreeRTOS-Cellular-Interface-Reference-Sierra-Wireless-HL7802)
* [u-blox Sara-R4](https://github.com/FreeRTOS/FreeRTOS-Cellular-Interface-Reference-ublox-SARA-R4)

