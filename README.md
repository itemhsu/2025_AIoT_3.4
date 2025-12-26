# Hour 4：Edge AI 實戰 — COCO / YOLO / esp-dl 與模型部署
（課程時間：60 分鐘）

---

## 一、本小時課程目標（Learning Objectives）

完成本小時課程後，學生應能：

- 理解 **Edge AI 與傳統 AI 在部署上的根本差異**
- 清楚分辨「模型檔案」在不同階段的型態與用途
- 看懂 **COCO / YOLO 在 ESP32-P4 上的實際程式碼**
- 理解 **esp-dl 與 espdl 模型格式的角色**
- 能說明 ONNX → espdl 的完整生成流程與指令

---

## 二、Edge AI 不是「把模型丟進來跑」

在 PC / Server 上，AI 流程通常是：

```
Dataset → Training → Model → Inference
```

在 AIoT / Edge AI 上，實際流程是：

```
Dataset
  ↓
Training (PyTorch)
  ↓
ONNX（交換格式）
  ↓
量化 / 編譯（esp-dl）
  ↓
espdl（部署格式）
  ↓
MCU Runtime
```

> **部署流程本身，就是 Edge AI 的一半難度。**

---

## 三、本專案使用的 Edge AI 技術堆疊

### 3.1 AI 模型：YOLO11n（COCO）

- 任務：Object Detection
- 資料集：COCO
- 模型特性：
  - 輕量化
  - 適合量化
  - 可在 MCU 上即時推論
  - 高精度
  <img width="626" height="360" alt="image" src="https://github.com/user-attachments/assets/781daa19-bf48-4587-802e-ae23fc30f052" />
  
---
  <img width="536" height="367" alt="image" src="https://github.com/user-attachments/assets/797ebe38-90c1-4b6b-9d50-0bc5d81d725f" />
  
---
  <img width="833" height="437" alt="image" src="https://github.com/user-attachments/assets/8cfa71f4-33cb-4cd2-87e3-c0402cbaf667" />




---

### 3.2 AI Runtime：esp-dl

- Espressif 官方 Edge AI Runtime
- 提供：
  - 模型載入
  - Preprocess / Postprocess
  - 記憶體管理

---

## 四、COCO Detect 模組程式碼導讀（核心）
- 什麼是微軟 COCO 資料集？
  - 微軟通用物件上下文資料集（COCO）是評估最先進電腦視覺模型效能的黃金標準基準資料集。 COCO 包含超過 33 萬張圖像，其中超過 20 萬張圖像已標註，涵蓋數十個物件類別。 COCO 是一個合作項目，由來自眾多知名機構（包括Google、加州理工學院和喬治亞理工學院）的電腦視覺專家共同維護。
  - COCO 資料集旨在代表我們在日常生活中經常遇到的各種事物，從自行車等交通工具到狗等動物再到人。
  - COCO 資料集包含來自 80 多個「物件」類別和 91 個通用「物品」類別的影像，這意味著該資料集可以比小規模資料集更有效地用於對通用模型進行基準測試。
  - 此外，COCO 資料集還包含：
    - 121,408 張圖片
    - 883,331 物件註釋
    - 80類數據
    - 影像中位數比例為 640 x 480
<img width="756" height="175" alt="image" src="https://github.com/user-attachments/assets/b8e5bb36-4d32-4b4d-8816-03e0f2fa2516" />

- 要實作 COCO 偵測功能的 UI 觸發，必須完成以下四個確定步驟：
  - 1. 修改模式定義 (./main/ui/ui_extra.h)
  - 在現有的枚舉中新增 AI_DETECT_COCO。根據原始碼，PEDESTRIAN 為 0，FACE 為 1。
```C
typedef enum {
    AI_DETECT_PEDESTRIAN = 0, // Pedestrian detection
    AI_DETECT_FACE,           // Face detection
    AI_DETECT_COCO,           // 確定新增：COCO 物件偵測 (數值為 2)
    AI_DETECT_MODE_MAX        // Maximum number of modes
} ai_detect_mode_t;
```
- 2. 更新 AI 處理邏輯 (./main/app/AI/app_ai_detect.cpp)
  - 您必須在後端的任務與影格處理函式中加入 COCO 的路徑。
  - 修改偵測任務：在 camera_dectect_task 函式中加入 COCO 偵測呼叫
```C
if (ui_extra_get_ai_detect_mode() == AI_DETECT_PEDESTRIAN) {
    detect_results = app_pedestrian_detect((uint16_t *)p->buffer, DETECT_WIDTH, DETECT_HEIGHT);
} else if (ui_extra_get_ai_detect_mode() == AI_DETECT_FACE) {
    detect_results = app_humanface_detect((uint16_t *)p->buffer, DETECT_WIDTH, DETECT_HEIGHT);
} else if (ui_extra_get_ai_detect_mode() == AI_DETECT_COCO) {
    // 呼叫來源中定義的 COCO 偵測函式
    detect_results = app_coco_detect((uint16_t *)p->buffer, DETECT_WIDTH, DETECT_HEIGHT);
}
```

- 修改影格處理：在 app_ai_detection_process_frame 中串聯繪圖邏輯
```C
if(ai_detect_mode == AI_DETECT_FACE) {
    ret = app_humanface_ai_detect((uint16_t*)current_ai_buffer, (uint16_t*)detect_buf, width, height);
} else if(ai_detect_mode == AI_DETECT_PEDESTRIAN) {
    ret = app_pedestrian_ai_detect((uint16_t*)current_ai_buffer, (uint16_t*)detect_buf, width, height);
} else if(ai_detect_mode == AI_DETECT_COCO) {
    // 呼叫來源中已實作的繪製函式，它會處理 YOLO 框與文字標籤
    ret = app_coco_od_detect((uint16_t*)detect_buf, width, height); 
}
```
- 3. 更新 UI 標籤顯示 (./main/ui/ui_extra.c)
  - 修改 ui_extra_update_ai_detect_mode_label 函式，讓 UI 能顯示「Mode: COCO」
```C
static void ui_extra_update_ai_detect_mode_label(void) {
    if (ai_mode_label == NULL) return;

    if (current_ai_detect_mode == AI_DETECT_PEDESTRIAN) {
        lv_label_set_text(ai_mode_label, "Mode: Pedestrian");
    } else if (current_ai_detect_mode == AI_DETECT_FACE) {
        lv_label_set_text(ai_mode_label, "Mode: Face");
    } else if (current_ai_detect_mode == AI_DETECT_COCO) {
        lv_label_set_text(ai_mode_label, "Mode: COCO"); // 新增顯示文字
    }
}
```
- 4. 實作 UI 按鈕切換邏輯 (./main/ui/ui_extra.c)
  - 目前的 UI 透過上下按鈕來切換模式。您需要修改 ui_extra_btn_up 與 ui_extra_btn_down 的 switch-case 邏輯，使其支援三個模式的循環切換
  - 向下按鈕 (Next Mode)：
```C
case UI_PAGE_AI_DETECT:
    if (current_ai_detect_mode == AI_DETECT_PEDESTRIAN) {
        ui_extra_change_ai_detect_mode(AI_DETECT_FACE);
    } else if (current_ai_detect_mode == AI_DETECT_FACE) {
        ui_extra_change_ai_detect_mode(AI_DETECT_COCO); // 切換至 COCO
    } else {
        ui_extra_change_ai_detect_mode(AI_DETECT_PEDESTRIAN); // 循環回第一個
    }
    break;
```
- 向上按鈕 (Prev Mode)：
```C
case UI_PAGE_AI_DETECT:
    if (current_ai_detect_mode == AI_DETECT_PEDESTRIAN) {
        ui_extra_change_ai_detect_mode(AI_DETECT_COCO); // 回到最後一個 (COCO)
    } else if (current_ai_detect_mode == AI_DETECT_COCO) {
        ui_extra_change_ai_detect_mode(AI_DETECT_FACE);
    } else {
        ui_extra_change_ai_detect_mode(AI_DETECT_PEDESTRIAN);
    }
    break;
```

#### 實作關鍵
- 現成功能：您的專案已經在 app_ai_detect.cpp 中初始化了 coco_od_detect 指標，並實作了完整的繪圖邏輯 app_coco_od_detect，因此只需完成上述的 UI 與邏輯串聯即可運作。
- 確定性：根據 ui_extra.h 的結構，AI_DETECT_COCO 的數值確定應為 2。
- UI 互動：使用者只要進入「AI DETECT」頁面，按下實體按鈕或點擊對應的 UI 元件，就能看到模式標籤切換至 COCO，並啟動 80 類物件的偵測



### 4.1 模組位置與檔案

**檔案位置：**
- `components/coco_detect/coco_detect.cpp`
- `components/coco_detect/coco_detect.hpp`

**角色定位：**
- 封裝 YOLO11n 模型
- 對 App 提供「簡單 API」

---

### 4.2 COCODetect 類別（封裝層）

```cpp
COCODetect::COCODetect(model_type_t model_type)
```

**說明：**
- App 只需選模型類型
- 不需知道模型檔案路徑
- 不需知道模型存放位置

> 這是「AI Service Layer」的概念。

---

### 4.3 模型載入（dl::Model）

```cpp
m_model = new dl::Model(
    path,
    model_name,
    model_location,
    0,
    dl::MEMORY_MANAGER_GREEDY,
    nullptr,
    param_copy
);
```

**關鍵說明：**
- `path`：Flash / Partition / SD
- `param_copy`：是否複製參數到 PSRAM
- 會依 ESP32-P4 記憶體條件動態決定

---

### 4.4 為什麼呼叫 minimize()

```cpp
m_model->minimize();
```

**用途：**
- 釋放初始化用 buffer
- 降低 Runtime 記憶體占用

> 在 Edge AI 中，「不用的記憶體一定要釋放」。

---

## 五、Preprocess 與 Postprocess（AI 成敗關鍵）

### 5.1 Preprocess（影像前處理）

在 `coco_detect.cpp` 中：

```cpp
m_image_preprocessor =
    new dl::image::ImagePreprocessor(
        m_model,
        {0, 0, 0},
        {255, 255, 255}
    );
```

**負責：**
- Resize
- Normalize
- Color format 調整

---

### 5.2 Postprocess（YOLO 特有）

```cpp
m_postprocessor =
    new dl::detect::yolo11PostProcessor(
        m_model,
        0.25,   // confidence threshold
        0.7,    // NMS threshold
        10,     // max boxes
        {...}
    );
```

**說明：**
- Threshold 會直接影響「準不準」
- 不只是模型權重的問題

---

## 六、模型檔案的生命週期（非常重要）

### 6.0 模型數據源
```
https://universe.roboflow.com/
```

<img width="760" height="421" alt="image" src="https://github.com/user-attachments/assets/8e951fa2-a9f0-47fc-99ca-3c4a4a4eb4f2" />


### 6.1 訓練階段模型（PyTorch）
PyTorch 是由 Facebook AI Research 在 2016 年推出的 Python 深度學習框架，以動態計算圖為核心，先征服學術界，再完成工業化，現在已是全球 AI 的基礎設施之一。

<img width="535" height="317" alt="image" src="https://github.com/user-attachments/assets/8da497ed-0699-4cbf-9dcb-151cee3d9980" />

<img width="591" height="248" alt="image" src="https://github.com/user-attachments/assets/ed6f0b0e-44b0-4d94-aeb5-66075c99c2a9" />


- 運算環境
  
  <img width="445" height="186" alt="image" src="https://github.com/user-attachments/assets/2aa94047-31a7-414a-a926-092f906cc4f8" />

- `.pt`
- 僅用於訓練 / 評估
- **不能部署到 MCU**

---

### 6.2 ONNX（中繼交換格式）

**檔案範例：**
- `yolo11n.onnx`
- `yolo11n_320.onnx`

**用途：**
- 介於 Training 與 Deployment 之間

---

### 6.3 ONNX 生成方式

**工具：**
- PyTorch
- YOLOv11
- 自訂腳本：`export_onnx.py`

**生成指令範例：**

```bash
python export_onnx.py   --weights yolo11n.pt   --imgsz 640   --output yolo11n.onnx
```

---

### 6.4 espdl（最終部署格式）

**檔案範例：**
- `coco_detect_yolo11n_s8_v1.espdl`

**特性：**
- INT8 / Mixed precision
- 記憶體佈局最佳化
- 可直接由 esp-dl 載入
<img width="578" height="245" alt="image" src="https://github.com/user-attachments/assets/d370879b-1aba-4efc-98ff-30f1e5107625" />

<img width="585" height="196" alt="image" src="https://github.com/user-attachments/assets/b9b0d098-723c-4a9a-b2de-8efa2694426a" />

<img width="455" height="194" alt="image" src="https://github.com/user-attachments/assets/f9c1cada-39e8-4b53-a99f-b1b6cee7e661" />

---

## 七、ONNX → espdl 的生成流程

### 7.1 為什麼不能直接用 ONNX？

- Float32
- 記憶體需求過大
- 不適合 MCU

---

### 7.2 espdl 生成工具

- Espressif esp-dl toolchain
- `pack_espdl_models.py`

此步驟通常在 **build 階段自動完成**。

---

## 八、效能與解析度的取捨（640 vs 320）

| 模型 | Input | 推論時間（P4） |
|----|----|----|
| YOLO11n | 640x640 | ~3 ms |
| YOLO11n | 320x320 | ~0.6 ms |

**教學重點：**
- Edge AI 永遠在 trade-off
- 不存在「又快又準又省」

---

## 九、常見錯誤與教學提醒

- 認為模型越大越好
- 忽略 Preprocess / Postprocess
- 不釋放模型初始化資源

---

## 十、課堂練習（10 分鐘）

請學生回答：

1. 為什麼 espdl 才是部署格式？
2. param_copy 對效能有什麼影響？
3. 如果 AI 很慢，應該先檢查哪一段？

---

## 十一、本小時重點整理

- Edge AI 的難點在部署
- 模型有完整生命週期
- esp-dl + espdl 是關鍵
- P4 讓 YOLO 在 MCU 上變得實用

---

## 十二、Next Hour 預告

**Hour 5：UI、事件、決策與儲存 — AIoT 的行為閉環**
