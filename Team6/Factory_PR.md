# 2025_AIoT_Team5_Factory_PR

## Source
將機器還原到原廠設置
### change working directory
```bash
cd ~/SageMaker
cd esp
```

### clone example source
```bash
git clone --recursive https://github.com/espressif/esp-dev-kits.git
```

#### 1) 切換至指定的 ESP-IDF 版本

本補丁係針對 **ESP-IDF `release/v5.5` 分支**中的特定提交版本
**`98cd765953dfe0e7bb1c5df8367e1b54bd966cce`** 所設計。

```bash
cd ~/SageMaker/esp/esp-idf
git checkout release/v5.5
```

> 若你尚未安裝 / 啟用 ESP-IDF，請先完成 `./install.sh all` 與 `source ./export.sh`。

---

#### 2) 將補丁檔複製至 ESP-IDF 根目錄

補丁檔位於 Factory Demo 範例資料夾下（esp-dev-kits repo 內）。請將補丁複製到 ESP-IDF 根目錄：

```bash
cp ~/SageMaker/esp/esp-dev-kits/examples/esp32-p4-eye/factory_demo/0004-fix-spi-default-clock-source.patch \
	~/SageMaker/esp/esp-idf/

cp ~/SageMaker/esp/esp-dev-kits/examples/esp32-p4-eye/factory_demo/0004-fix-sdmmc-aligned-write-buffer.patch \
	~/SageMaker/esp/esp-idf/
```

---

#### 3) 套用補丁

在 ESP-IDF 根目錄執行：

```bash
cd ~/SageMaker/esp/esp-idf
git apply 0004-fix-spi-default-clock-source.patch
git apply 0004-fix-sdmmc-aligned-write-buffer.patch
```

若套用成功，系統將修正 SPI 預設時鐘來源在高像素時鐘條件下可能引發的時序問題，提升整體系統穩定性。

---

## Build

切換到 Factory Demo 專案目錄後進行 build：

```bash
cd ~/SageMaker/esp/esp-dev-kits/examples/esp32-p4-eye/factory_demo
idf.py set-target esp32p4
idf.py menuconfig
idf.py fullclean
idf.py build
```

#### menuconfig 必改設定（ESP32-P4-EYE）
在 `idf.py menuconfig` 內，請確認以下路徑並把最小版本調成 `0.0`：

* `Component config -> Hardware settings -> Chip revision -> Minimum supported revision = 0.0`

> 說明：若未調整，可能會因晶片版本門檻導致無法正常執行。

`idf.py build` 會產生很長的 log。

> 建議：build 結束後，請在 log 末段找到 Espressif 建議的燒錄指令（含 offset），後續燒錄以該指令為準。

---

## 下載燒錄（MacOS 範例）
新增一個Factory_Demo的資料夾

- `mkdir Factory_Demo`

把 AWS 上 build 產物下載到 Factory_Demo 資料夾：

- `build/bootloader/bootloader.bin`
- `build/partition_table/partition-table.bin`
- `build/factory_demo.bin`

MacOS 範例（`--no-stub` 可以避免卡住；`-p /dev/cu.usbmodem1101` 請依你的環境調整）：

再資料夾底下執行
```bash
python3 -m esptool -p /dev/cu.usbmodem101 --chip esp32p4 -b 115200  --no-stub --before default_reset --after hard_reset write_flash --flash_mode dio --flash_size 16MB --flash_freq 40m 0x2000 bootloader.bin 0x8000 partition-table.bin 0x10000 factory_demo.bin

