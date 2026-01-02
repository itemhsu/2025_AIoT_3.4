# AIoT第四組PR
環境建置

開啟AWS主控台登入
URL https://049281306005.signin.aws.amazon.com/console

使用者名稱:class4@NTUT

密碼:class4@NTUT

每次開機都需要重新執行 
```
cd SageMaker
 ```
```
./install.sh all
```
```
source ./export.sh
```
### Project Building Hands on 
Creating a "Hellow world" example
* 切換到名為 esp 的目錄：
```
cd esp
```
* 遞歸克隆 esp-idf 專案的 Git 儲存庫：
```
git clone --recursive https://github.com/espressif/esp-idf.git
```
* 切換到 esp-idf 目錄：
```
cd esp-idf/
```
* 執行 install.sh 腳本，安裝開發環境：
```
./install.sh
```
* 執行 export.sh 腳本，設置環境變量：
```
source ./export.sh
```
* 返回上一級目錄：
```
cd ..
```

* 從 IDF_PATH 環境變量指定的路徑復制 hello_world 範例到當前目錄：
```
cp -r $IDF_PATH/examples/get-started/hello_world .
```
* 切換到 hello_world 目錄：
```
cd hello_world/
```

* 執行 idf.py 工具進行配置（例如設置項目參數）：
```
idf.py set-target esp32p4
idf.py menuconfig
```
<img width="513" alt="image" src="https://github.com/itemhsu/AIoT_one/assets/25599185/cd5da1d0-5404-4e36-82f2-ad104b90d7fe">
* 設定晶片版本
<img width="710" height="339" alt="image" src="https://github.com/user-attachments/assets/cacb3a47-fe93-40ff-89fa-467971a50219" />


* 使用 idf.py 工具構建項目：
```
idf.py fullclean
idf.py build
```
### Image Flashing Hands on 
要把 AWS 云上的 Amazon Linux 环境中构建的 ESP32 项目烧录到您本地的设备上，您需要通过以下几个步骤操作：
#### 執行結果（minicom）
```
rst:0xc (SW_CPU_RESET),boot:0x13 (SPI_FAST_FLASH_BOOT)
configsip: 0, SPIWP:0xee
clk_drv:0x00,q_drv:0x00,d_drv:0x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00
mode:DIO, clock div:2
load:0x3fff0030,len:7176
load:0x40078000,len:15564
ho 0 tail 12 room 4
load:0x40080400,len:4
load:0x40080404,len:3904
entry 0x40080640
I (31) boot: ESP-IDF v5.3-dev-3220-g9c99a385ad 2nd stage bootloader
I (31) boot: compile time Apr  5 2024 08:51:47
I (33) boot: Multicore bootloader
I (37) boot: chip revision: v1.0
I (41) boot.esp32: SPI Speed      : 40MHz
I (45) boot.esp32: SPI Mode       : DIO
I (50) boot.esp32: SPI Flash Size : 2MB
I (54) boot: Enabling RNG early entropy source...
I (60) boot: Partition Table:
I (63) boot: ## Label            Usage          Type ST Offset   Length
I (71) boot:  0 nvs              WiFi data        01 02 00009000 00006000
I (78) boot:  1 phy_init         RF data          01 01 0000f000 00001000
I (86) boot:  2 factory          factory app      00 00 00010000 00100000
I (93) boot: End of partition table
I (97) esp_image: segment 0: paddr=00010020 vaddr=3f400020 size=09414h ( 37908) map
I (119) esp_image: segment 1: paddr=0001943c vaddr=3ffb0000 size=02200h (  8704) load
I (122) esp_image: segment 2: paddr=0001b644 vaddr=40080000 size=049d4h ( 18900) load
I (132) esp_image: segment 3: paddr=00020020 vaddr=400d0020 size=13850h ( 79952) map
I (161) esp_image: segment 4: paddr=00033878 vaddr=400849d4 size=077ech ( 30700) load
I (179) boot: Loaded app from partition at offset 0x10000
I (179) boot: Disabling RNG early entropy source...
I (191) cpu_start: Multicore app
I (199) cpu_start: Pro cpu start user code
I (199) cpu_start: cpu freq: 160000000 Hz
I (200) app_init: Application information:
I (202) app_init: Project name:     hello_world
I (208) app_init: App version:      1
I (212) app_init: Compile time:     Apr  5 2024 08:52:04
I (218) app_init: ELF file SHA256:  bb6384479...
I (223) app_init: ESP-IDF:          v5.3-dev-3220-g9c99a385ad
I (230) efuse_init: Min chip rev:     v0.0
I (234) efuse_init: Max chip rev:     v3.99
I (239) efuse_init: Chip rev:         v1.0
I (245) heap_init: Initializing. RAM available for dynamic allocation:
I (252) heap_init: At 3FFAE6E0 len 00001920 (6 KiB): DRAM
I (258) heap_init: At 3FFB2AC8 len 0002D538 (181 KiB): DRAM
I (264) heap_init: At 3FFE0440 len 00003AE0 (14 KiB): D/IRAM
I (270) heap_init: At 3FFE4350 len 0001BCB0 (111 KiB): D/IRAM
I (277) heap_init: At 4008C1C0 len 00013E40 (79 KiB): IRAM
I (284) spi_flash: detected chip: generic
I (287) spi_flash: flash io: dio
W (291) spi_flash: Detected size(4096k) larger than the size in the binary image header(2048k). Using the.
I (305) main_task: Started on CPU0
I (315) main_task: Calling app_main()
Hello world!
This is esp32 chip with 2 CPU core(s), WiFi/BTBLE, silicon revision v1.0, 2MB external flash
Minimum free heap size: 305360 bytes
Restarting in 10 seconds...
Restarting in 9 seconds...
Restarting in 8 seconds...
Restarting in 7 seconds...
Restarting in 6 seconds...
Restarting in 5 seconds...
Restarting in 4 seconds...
Restarting in 3 seconds...
Restarting in 2 seconds...
Restarting in 1 seconds...
Restarting in 0 seconds...
Restarting now.
ets Jun  8 2016 00:22:57
```
#### hello_world_main.c
```c
/*
 * SPDX-FileCopyrightText: 2010-2022 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: CC0-1.0
 */

#include <stdio.h>
#include <inttypes.h>
#include "sdkconfig.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_chip_info.h"
#include "esp_flash.h"
#include "esp_system.h"

void app_main(void)
{
    printf("Hello world!\n");

    /* Print chip information */
    esp_chip_info_t chip_info;
    uint32_t flash_size;
    esp_chip_info(&chip_info);
    printf("This is %s chip with %d CPU core(s), %s%s%s%s, ",
           CONFIG_IDF_TARGET,
           chip_info.cores,
           (chip_info.features & CHIP_FEATURE_WIFI_BGN) ? "WiFi/" : "",
           (chip_info.features & CHIP_FEATURE_BT) ? "BT" : "",
           (chip_info.features & CHIP_FEATURE_BLE) ? "BLE" : "",
           (chip_info.features & CHIP_FEATURE_IEEE802154) ? ", 802.15.4 (Zigbee/Thread)" : "");

    unsigned major_rev = chip_info.revision / 100;
    unsigned minor_rev = chip_info.revision % 100;
    printf("silicon revision v%d.%d, ", major_rev, minor_rev);
    if(esp_flash_get_size(NULL, &flash_size) != ESP_OK) {
        printf("Get flash size failed");
        return;
    }

    printf("%" PRIu32 "MB %s flash\n", flash_size / (uint32_t)(1024 * 1024),
           (chip_info.features & CHIP_FEATURE_EMB_FLASH) ? "embedded" : "external");

    printf("Minimum free heap size: %" PRIu32 " bytes\n", esp_get_minimum_free_heap_size());

    for (int i = 10; i >= 0; i--) {
        printf("Restarting in %d seconds...\n", i);
        vTaskDelay(1000 / portTICK_PERIOD_MS);
    }
    printf("Restarting now.\n");
    fflush(stdout);
    esp_restart();
}
```
利用COM3連接clude <inttypes.h>
#include "sdkconfig.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_chip_info.h"
#include "esp_flash.h"
#include "esp_system.h"

void app_main(void)
{
    printf("Hello world!\n");

    /* Print chip information */
    esp_chip_info_t chip_info;
    uint32_t flash_size;
    esp_chip_info(&chip_info);
    printf("This is %s chip with %d CPU core(s), %s%s%s%s, ",
           CONFIG_IDF_TARGET,
           chip_info.cores,
           (chip_info.features & CHIP_FEATURE_WIFI_BGN) ? "WiFi/" : "",
           (chip_info.features & CHIP_FEATURE_BT) ? "BT" : "",
           (chip_info.features & CHIP_FEATURE_BLE) ? "BLE" : "",
           (chip_info.features & CHIP_FEATURE_IEEE802154) ? ", 802.15.4 (Zigbee/Thread)" : "");

    unsigned major_rev = chip_info.revision / 100;
    unsigned minor_rev = chip_info.revision % 100;
    printf("silicon revision v%d.%d, ", major_rev, minor_rev);
    if(esp_flash_get_size(NULL, &flash_size) != ESP_OK) {
        printf("Get flash size failed");
        return;
    }

    printf("%" PRIu32 "MB %s flash\n", flash_size / (uint32_t)(1024 * 1024),
           (chip_info.features & CHIP_FEATURE_EMB_FLASH) ? "embedded" : "external");

    printf("Minimum free heap size: %" PRIu32 " bytes\n", esp_get_minimum_free_heap_size());

    for (int i = 10; i >= 0; i--) {
        printf("Restarting in %d seconds...\n", i);
        vTaskDelay(1000 / portTICK_PERIOD_MS);
    }
    printf("Restarting now.\n");
    fflush(stdout);
    esp_restart();
}


利用COM3連接埠連接PUTTY並使用以下指令連接:
```
esptool -p COM3 --chip esp32p4 -b 115200 --no-stub --before default_reset --after hard_reset write_flash --flash_mode dio --flash_size 2MB --flash_freq 80m 0x2000 ./bootloader.bin 0x8000 ./partition-table.bin 0x10000 ./hello_world.bin"-->燒入的command
```

![messageImage_1767235739080_0](https://github.com/user-attachments/assets/ca71b2c2-787b-4e2d-b586-34da33ac5c6e)


PUTTY軟體成功跑出 Hello world
![messageImage_1767235702998_0](https://github.com/user-attachments/assets/7b53391d-06d2-4956-b215-d1c7ffd186bb)

------------------------------------------------------------------
<img width="1203" height="278" alt="image" src="https://github.com/user-attachments/assets/8d437fad-2d98-46e9-a98f-b6fda65e63f8" />
# ESP32-P4-EYE 迷你智慧相機應用示例說明

本示例係基於 **ESP32-P4-EYE 開發板** 所打造，完整展示一套功能齊全的 **迷你智慧相機應用系統**。該應用支援多種基礎與進階攝影功能，包括 **即時拍照、定時拍照、影片錄製、相簿瀏覽預覽**，並可透過 **USB 掛載方式將 SD 卡作為隨身碟存取**，方便影像資料的讀取與管理。

## 影像功能與參數調校

在影像調校方面，系統提供彈性化的影像參數設定介面，使用者可依需求調整：

- 影像解析度  
- 飽和度（Saturation）  
- 對比度（Contrast）  
- 亮度（Brightness）  
- 色度（Hue / Chroma）  

以因應不同場景與光線條件，確保最佳成像品質。

## 智慧視覺與 AI 辨識能力

在基礎影像功能之上，本應用進一步整合多項 **智慧視覺辨識功能**，包含：

- **人臉偵測（Face Detection）**
- **行人偵測（Person Detection）**
- **基於 YOLOv11 Nano 模型的即時物件偵測**

上述功能可在邊緣端即時執行，大幅提升裝置在 **智慧監控、人機互動、AIoT 應用** 等情境中的視覺分析與智慧判斷能力。

## 硬體資源與周邊整合

整體專案充分發揮 **ESP32-P4-EYE 開發板** 的硬體整合優勢，綜合運用多種關鍵周邊資源，包括：

- **MIPI-CSI 高速攝影機介面**  
  - 支援高品質影像擷取與即時串流  

- **SPI 介面 LCD 顯示模組**  
  - 即時顯示拍攝畫面、操作選單與系統狀態  

- **USB High-Speed（HS）介面**  
  - 實現高速資料傳輸與 USB Mass Storage（SD 卡掛載）功能  

- **實體按鍵與旋轉編碼器**  
  - 提供直覺且高可用性的人機操作體驗  

- **SD 卡儲存系統**  
  - 用於照片與影片資料的長期保存與管理  


### Source
change working directory
```
cd ~/SageMaker
cd esp
```
clone example source
```
git clone --recursive https://github.com/espressif/esp-dev-kits.git
```

### 應用補丁說明

當 **像素時鐘（Pixel Clock）設定為 80 MHz** 時，**SPI 介面的預設時鐘來源** 在部分情況下可能暫時無法滿足系統的時序需求，進而導致顯示或資料傳輸不穩定。為確保系統運作的可靠性，需手動套用修正補丁 **`0004-fix-spi-default-clock-source.patch`**。

請依照以下步驟完成補丁套用前的準備作業。

### 應用補丁說明

當 **像素時鐘（Pixel Clock）設定為 80 MHz** 時，**SPI 介面的預設時鐘來源** 在部分情況下可能無法滿足系統時序需求，進而導致顯示或資料傳輸不穩定。為提升系統整體穩定性，請依照以下步驟套用修正補丁 **`0004-fix-spi-default-clock-source.patch`**。

---

#### 1) 切換至指定的 ESP-IDF 版本

本補丁係針對 **ESP-IDF `release/v5.5` 分支**中的特定提交版本  
**`98cd765953dfe0e7bb1c5df8367e1b54bd966cce`** 所設計。  
為確保補丁可正確套用並生效，請先切換至對應版本：

```bash
cd ~/SageMaker/esp/esp-idf
git checkout release/v5.5
git checkout 98cd765953dfe0e7bb1c5df8367e1b54bd966cce
```

---

#### 2) 將補丁檔複製至 ESP-IDF 根目錄

請將補丁檔 **`0004-fix-spi-default-clock-source.patch`** 複製到 ESP-IDF 的根目錄，以便後續套用補丁作業，例如：

```bash
cp 0004-fix-spi-default-clock-source.patch ~/SageMaker/esp/esp-idf/
cp 0004-fix-sdmmc-aligned-write-buffer.patch ~/SageMaker/esp/esp-idf/
```

---

#### 3) 套用補丁

完成上述準備後，請在 ESP-IDF 根目錄下執行以下指令以套用補丁：

```bash
git apply 0004-fix-spi-default-clock-source.patch
git apply 0004-fix-sdmmc-aligned-write-buffer.patch
```

若套用成功，系統將修正 SPI 預設時鐘來源在高像素時鐘條件下可能引發的時序問題，提升整體系統穩定性。

### Build
```
idf.py buuild
```
會產生很長的log

###
下載燒錄. MacOS 範例,   --no-stub 可以避免卡住,  -p /dev/cu.usbmodem1101 根據你的環境調整
```bash
python3 -m esptool -p /dev/cu.usbmodem1101 --chip esp32p4 -b 115200  --no-stub --before default_reset --after hard_reset write_flash --flash_mode dio --flash_size 16MB --flash_freq 40m 0x2000 bootloader.bin 0x8000 partition-table.bin 0x10000 factory_demo.bin
```

### 快速復原
下載編好的
```
https://dl.espressif.com/AE/esp-dev-kits/p4_eye_factory_demo_100.bin
```

```
python3 -m esptool -p /dev/cu.usbmodem1101   --chip esp32p4   -b 115200 --no-stub  write_flash   0x0 p4_eye_factory_demo_100.bin
```
### 完成程式燒入
![S__74481822](https://github.com/user-attachments/assets/76013c8e-90cc-4850-8302-0e58ac900ed9)
可以判斷物體是否為行人 



