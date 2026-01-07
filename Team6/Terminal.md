# 完成Terminal 範例 Markdown 操作手冊 PR

## 一、開發環境

- 作業系統：MacOS
- 開發框架：ESP-IDF
- 操作終端：ESP-IDF Command Prompt
- 範例專案：hello_world（ESP-IDF 內建範例）





## 二、建立專案（Project Building）

1. 開啟 **ESP-IDF CMD**
2. 切換至工作目錄

```bash
cd C:\esp
```
3.使用 Git 遞歸克隆 esp-idf 專案的 Git 儲存庫：
```bash
git clone --recursive https://github.com/espressif/esp-idf.git
```

4.複製 HelloWorld至工作目錄
```
esp-idf\examples\get-started\hello_world
```
5.進入 HelloWorld 專案目錄
```bash
cd ~\esp-idf\examples\get-started\hello_world
```


## 三、專案設定（menuconfig）

在專案根目錄執行(~\esp\2025_AIoT_1\Project_Building\hello_world)：
```bash
#設定晶片為 ESP32-P4
idf.py set-target esp32p4

idf.py menuconfig
```

建議檢查項目：

- **Serial flasher config**
  - Flash baud rate（可先維持預設）
- **Serial Monitor**
  - 預設 UART / 監看埠（依實際板子連線情況）
- 其餘維持預設即可

完成後按提示儲存並離開。

---

## 四、專案編譯（Build）

```bash
idf.py set-target esp32p4
idf.py menuconfig
idf.py fullclean
idf.py build
```

## 五、燒錄至開發板（Flash）

1. 確認 ESP32 已透過 USB 連接到 MAC
```
ls /dev/cu.*
```
2. 燒錄
```bash
idf.py -p /dev/cu.usbmodem101 flash
```
---

### 燒入 燒錄 Hello World
將這三個檔案丟入 hello_world這個資料夾下
```bash
partition-table.bin
bootloader.bin
hello_world.bin
```
進入這個資料夾(假設你把檔案放在 ~/Downloads/hello_world)
```bash
cd ~/Downloads/hello_world
```
然後執行
```bash
python3 -m esptool -p /dev/cu.usbmodem1101 --chip esp32p4 -b 115200 \
 --no-stub --before default_reset --after hard_reset write_flash --flash_mode dio \
 --flash_size 4MB --flash_freq 80m 0x2000 ./bootloader.bin 0x8000 ./partition-table.bin 0x10000 \
  ./hello_world.bin
```

## 七、序列監看（Monitor）

查看DEBUG輸出
```bash
minicom -s
```

看到類似輸出即成功：
```
Hello world!
This is esp32 chip with 2 CPU cores
ESP-IDF version: x.x.x
