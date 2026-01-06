# Emergency Vehicle Detection（YOLOv11 → ONNX → ESPDL → ESP32-P4-EYE）SOP

## 1. 目標與最終產物

本 SOP 用 Roboflow 的 Emergency Vehicle Detection 資料集完成：

- YOLOv11 訓練 200 epochs
- 匯出 ONNX
- 量化並轉成 ESPDL
- 部署到 ESP32-P4-EYE

最終會產出：

- `best.pt`：YOLOv11 最佳權重
- `results.png`：訓練曲線
- `best_split.onnx`：給 ESP 轉檔用的 ONNX
- `model.espdl`：ESP32-P4-EYE 上使用的模型檔

---

## 2. 取得資料集

### 操作
1. 開啟 Roboflow 資料集頁面  
   https://universe.roboflow.com/test-ho5i1/emergency-vehicle-detection-yx3gh/dataset/3
2. Export 選擇 YOLO 格式並下載
3. 解壓縮到本機資料夾，例如 `D:\datasets\evd`

### 產出
資料夾結構應包含：

```
D:\datasets\evd
├── data.yaml
├── train
│   ├── images
│   └── labels
├── valid
│   ├── images
│   └── labels
└── test
    ├── images
    └── labels
```

---

## 3. 建立 Windows 訓練環境

### 操作（PowerShell）
```powershell
cd D:\work
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install ultralytics onnx onnxsim
```

若 PowerShell 不允許啟用 venv，可改用 CMD：

```batch
cd /d D:\work
python -m venv .venv
.\.venv\Scripts\activate.bat
python -m pip install -U pip
pip install ultralytics onnx onnxsim
```

### 產出
- 可使用 `yolo` 指令
- 可進行訓練、推論與匯出

---

## 4. YOLOv11 訓練（200 epochs）

### 操作

**準備 YOLOv11 訓練設定**
- 使用 YOLOv11 模型
- 建議使用 ReLU 版本設定檔以降低後續在 ESP 端不支援算子的機率

**執行訓練**

```powershell
yolo detect train `
  model=yolo11n_relu.yaml `
  data=D:\datasets\evd\data.yaml `
  imgsz=320 `
  epochs=200 `
  batch=8 `
  device=0
```

**備註**：`imgsz` 請固定，後續 ONNX 與 ESPDL 都要一致。

### 產出
訓練完成後會生成類似：

```
runs\detect\train\
├── results.png
└── weights\
    ├── best.pt
    └── last.pt
```

---

## 5. PC 端推論驗證

### 操作
用 `best.pt` 對 test images 推論：

```powershell
yolo detect predict `
  model=runs\detect\train\weights\best.pt `
  source=D:\datasets\evd\test\images `
  conf=0.25 `
  save=True
```

### 產出
`runs\detect\predict\` 會輸出推論圖片與標註框結果

---

## 6. 匯出 ONNX

### 操作
使用專案內的 `export_onnx.py` 匯出 ONNX，並固定輸入尺寸與 opset。

```powershell
python export_onnx.py `
  --weights runs\detect\train\weights\best.pt `
  --imgsz 320 `
  --output best_split.onnx `
  --simplify
```

### 產出
- `best_split.onnx`

---

## 7. ONNX → ESPDL（INT8 量化與轉檔）

### 操作
使用專案既有的量化/轉檔腳本，設定要點：

- **target**：esp32p4
- **bits**：8
- **calibration images**：D:\datasets\evd\valid\images
- **input size**：320

> 量化工具與指令會依你們使用的工具鏈不同而不同。若你把目前使用的腳本名稱或指令貼上，可將此段改成可直接複製使用的版本。

### 產出
- `*.espdl` 模型檔，例如 `evd_yolo11_320_s8.espdl`

---

## 8. 部署到 ESP32-P4-EYE

### 操作
- 將 `.espdl` 放入 ESP32-P4-EYE 專案指定模型路徑
- 在程式碼中更新模型檔名與路徑，確保載入的是新模型

**編譯與燒錄**

```powershell
idf.py build
idf.py flash monitor
```

### 產出
- 裝置可載入新模型並執行推論

---

## 9. 參數固定清單

建議在整條流程維持一致：

- `imgsz=320`
- 類別數與 `data.yaml` 一致
- ONNX 匯出 opset 一致
- 量化 calibration 使用 `valid/images`
