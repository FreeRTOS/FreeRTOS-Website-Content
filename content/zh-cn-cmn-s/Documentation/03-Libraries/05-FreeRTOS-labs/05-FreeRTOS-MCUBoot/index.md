---
title: MCUBoot
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---


**注意**：
FreeRTOS MCUBoot 演示是一个 [FreeRTOS Lab 项目](/Documentation/03-Libraries/05-FreeRTOS-labs/01-Introduction)，供社区成员参考
。此演示虽然功能完善，但可能并不符合我们的生产代码标准
。它可从 GitHub上的 [Lab-Project-FreeRTOS-MCUBoot](https://github.com/FreeRTOS/Lab-Project-FreeRTOS-MCUBoot) 存储库中获取
。


## 引言

MCUBoot 是可配置的安全引导加载程序，由多个行业领导者维护。它可以作为
第一或第二阶段的引导加载程序运行，支持软件映像的加密验证，
并支持下述方案：

* ECDSA-P256
* RSA-2048
* RSA-3072

默认情况下，它支持映像恢复，下载的固件映像更新会被试验性地启动一次。
初次升级引导时，如果升级映像将自身标记为已确认，则其将被保留为
主图像。如果升级映像未被确认，则后续引导将回退至
上一个被确认的映像。如果任一插槽中都没有可用的有效映像，则作为一种安全
预防措施，设备会将自己变砖。MCUBoot 开发者
在 GitHub 上的[文档](https://github.com/mcu-tools/mcuboot/tree/main/docs)存储库中提供了内容更加详实的文档。

当设备进入串行启动恢复模式时，MCUBoot 还为 [MCUMGR](https://github.com/apache/mynewt-mcumgr-cli) 提供子集支持
。
如被启用，可通过用户输入（如按住按钮）在启动期间触发串行模式。MCUMGR
接口使用户能够从板上检索映像诊断，查询复位，上传/修改映像等
。
