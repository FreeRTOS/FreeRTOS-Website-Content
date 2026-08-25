---
title: MCUBoot 演示
created: 2018-09-20 00:00:00.0 UTC
categories:
  - 内核
relatedLinks:
  - title: 为什么使用 FreeRTOS
    link: /Why-FreeRTOS/Why-FreeRTOS/
---

## 引言

**注意**：以下说明针对 Linux 或 Windows Subsystem for Linux (WSL) 主机。有关 WSL 安装 
和设置说明，详见[此处](https://docs.microsoft.com/windows/wsl/)。

本演示目前支持 esp32 架构。以下是针对此硬件的说明。 

演示包含如何使用 MCUBoot 启动应用程序：首先禁用引导加载程序看门狗定时器， 
打印版本号，然后自我确认以防止更新后恢复到之前版本。该应用程序继续 
定期打印 "hello world"。

该演示还详细介绍了应用程序的签名和升级过程， 
并为在其他 SoC上的实现提供了移植指南。最后，还演示了如何使用 [`mcumgr`](https://github.com/apache/mynewt-mcumgr-cli) 
从主机 PC 检索映像 
诊断、修改/上传映像以及触发其他主板功能。


## 构建和上传引导加载程序

1. 下载并进入存储库目录。

   ```c
   git clone --recurse-submodules https://github.com/FreeRTOS/Lab-Project-FreeRTOS-MCUBoot.git
   cd Lab-Project-FreeRTOS-MCUBoot
   ```

2. 为引导加载程序和应用程序应用必要的补丁。

   ```c
   git -C lib/mcuboot apply ../../patches/mcuboot.patch
   git -C lib/mcuboot/boot/espressif/hal/esp-idf/ apply ../../../../../../patches/esp-idf.patch
   ```

3. 配置 ESP-IDF 工具，然后进入引导加载程序项目目录。

   ```c
   ./lib/mcuboot/boot/espressif/hal/esp-idf/install.sh
   source lib/mcuboot/boot/espressif/hal/esp-idf/export.sh
   cd proj/espressif/esp32/bootloader
   ```

4. 连接 esp32，识别其 USB 描述符（例如 '/dev/ttyUSB0'），然后设置此 ID。

   ```c
   export ESPPORT=/dev/<USB>
   ```

5. 决定是否需要加密验证，可选方案包括：

   * ecdsa-p256
   * rsa-2048
   * rsa-3072

6. 如果需要加密映像验证，请使用以下命令生成构建文件， 
   将 `SIGNING_SCHEME` 设置为上述某个选项。

   ```c
   cmake -GNinja -DSIGNING_SCHEME=ecdsa-p256 -B build
   ```

   这将在引导加载程序项目目录中生成所选方案的私钥， 
   默认命名为 `mcuboot-private-key.pem`。该私钥将用于 
   在应用程序映像上签名。同时，cmake 目标负责将公钥 
   嵌入引导加载程序中，以验证映像。

   如果不需要加密映像验证，则可以省略上述命令中的 `SIGNING_SCHEME` 
   定义。

7. 最后，请运行以下命令，将引导加载程序上传到主板。

   ```c
   cmake --build build --target mcuboot-flash
   ```


## 构建和上传应用程序

构建并烧录引导加载程序后，请继续执行以下操作。如果您处于新的 shell 会话中， 
则可能需要重新运行上述配置 IDF 工具链的步骤并设置 `ESPPORT`。

1. 进入应用程序项目目录。

   ```c
   cd proj/espressif/esp32/app
   ```

2. 同样，在为应用程序生成构建文件时，必须设置 `SIGNING_SCHEME` 
   以匹配为引导加载程序选择的方案。此外，必须设置 `KEY_PATH` 
   以指向引导加载程序项目生成的私钥。如果在引导加载程序中不进行加密映像验证， 
   则必须省略下方 `SIGNING_SCHEME` 和 
   `KEY_PATH` 定义。最后，要设置应用程序版本，可以在下方命令中添加 
   `-DAPP_VERSION=X.Y.Z`。 

   ```c
   cmake -DSIGNING_SCHEME=ecdsa-p256 -DKEY_PATH=../bootloader/mcuboot-private-key.pem -GNinja -B build
   ```

3. 构建应用程序。

   ```c
   cmake --build build --target app
   ```

4. 可以通过两种方式上传映像：直接烧录到主映像插槽， 
   或烧录到辅助映像插槽。如果辅助映像的版本比主映像高， 
   则在后续启动时会提示升级。如果主映像插槽中没有映像， 
   则直接将映像上传至此处：

   ```c
   cmake --build build --target mcuboot-app-flash
   ```

   排队升级时，如果辅助映像的版本比主映像高， 
   两者将被交换，更新映像将暂时启动。
   如果更新映像未自我*确认*，则在后续启动时会还原。因此，应用程序需要调用 
   `boot_set_confirmed`，以确保自己作为主映像持久存在。未执行此操作的更新映像 
   将被还原。要升级映像，请执行以下命令：

   ```c
   cmake --build build --target mcuboot-app-upgrade
   ```

5. 最后，查看设备的输出。

   ```c
   idf.py monitor
   ```


## 调试应用程序

1. 分别在两个 shell 会话中使用以下命令配置 ESP-IDF 工具：

   ```c
   ./lib/mcuboot/boot/espressif/hal/esp-idf/install.sh
   source lib/mcuboot/boot/espressif/hal/esp-idf/export.sh
   ```

2. 在一个终端中，进入应用程序目录并启动 OpenOCD 服务器。

   ```c
   cd proj/espressif/esp32/app
   idf.py openocd
   ```

3. 在另一个终端中，进入应用程序目录并启动 GDB 会话。

   ```c
   cd proj/espressif/esp32/app
   idf.py gdb
   ```


## 串行启动模式和 MCUMGR 接口

串行启动模式默认启用，如需禁用，可将 `MCUBOOT_SERIAL` 
（位于 `lib/mcuboot/boot/freertos` 中的 `mcuboot_config.h` 文件）设置为 0。 
启动期间会检查串行启动引脚，如果激活，则进入串行启动模式。 
本演示中，串行启动引脚配置为 `GPIO 5`，并且处于高电平有效状态。将串行启动引脚 
连接到 VCC 将触发串行模式，连接到 GND 则跳过该模式。串行模式运行后， 
即可将主板与 `mcumgr` 连接。有关 
`mcumgr` 的安装说明，详见[此处](https://github.com/apache/mynewt-mcumgr-cli)。

MCUMGR 将通过 UART 引脚与主板通信，在本演示中，UART 引脚设置为 `GPIO 27 (RX)` 
和 `GPIO 26 (TX)`。您可以使用 USB-to-UART 连接线，如[此处所示](https://www.adafruit.com/product/954)。

为 `mcumgr` 定义连接，设置与连接到设备的 USB-to-UART 
相对应的 USB 描述符。

```c
mcumgr conn add esp type="serial" connstring="dev=/dev/<USB>,baud=115200,mtu=256"
```

将串行启动引脚连接到 VCC，然后重置主板以进入串行启动恢复模式。主板 
将记录其已进入串行启动模式。您可以继续使用 `mcumgr` 接口。

要列出设备上的映像，请运行以下命令：

```c
mcumgr -c esp image list
```

要上传映像，请运行以下命令：

```c
mcumgr -c esp image upload /path/to/mcuboot-image.bin
```

这需要已签名/格式化的 MCUBoot 映像。构建应用程序后， 
可在其构建目录中找到，如 `build/mcuboot-app.bin`。 

要重置主板，请运行以下命令：

```c
mcumgr -c esp reset
```
