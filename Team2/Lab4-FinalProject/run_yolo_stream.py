import cv2
import numpy as np
import urllib.request

# ==========================================
# ESP32-CAM，內網IP(請確認 IP 正確)
URL = "http://172.20.10.9:81/stream" 
# ==========================================

def run_stable_yolo_stream():
    from ultralytics import YOLO
    
    print("1. 載入模型中...")
    model = YOLO('best.pt')

    print(f"2. 連線至 {URL} ...")
    try:
        stream = urllib.request.urlopen(URL, timeout=10)
    except Exception as e:
        print(f"連線失敗: {e}")
        return

    print("連線成功! (按 'q' 離開)")
    
    bytes_buffer = b''
    
    while True:
        try:
            # 讀取數據
            bytes_buffer += stream.read(4096)
            
            # 尋找 JPEG 開頭 (FF D8)
            a = bytes_buffer.find(b'\xff\xd8')
            
            # 尋找 JPEG 結尾 (FF D9)
            b = bytes_buffer.find(b'\xff\xd9')
            
            # === 關鍵修正邏輯 ===
            if a != -1 and b != -1:
                # 情況 1: 正常的順序 (開頭在結尾前面)
                if a < b:
                    jpg = bytes_buffer[a:b+2]
                    # 處理完這張，將緩衝區移到這張圖之後
                    bytes_buffer = bytes_buffer[b+2:]
                    
                    if len(jpg) > 0:
                        # 解碼
                        img_array = np.frombuffer(jpg, dtype=np.uint8)
                        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                        
                        # 只有當 frame 成功解碼才進行 YOLO
                        if frame is not None:
                            results = model(frame, conf=0.5, verbose=False)
                            annotated_frame = results[0].plot()
                            cv2.imshow("YOLO-Highway", annotated_frame)
                
                # 情況 2: 順序錯亂 (找到了結尾 b，但它在開頭 a 之前)
                # 這代表 b 是「上一張圖」的殘留結尾，a 是「新圖」的開頭
                else:
                    # 我們直接丟棄 a 之前的資料，保留新的開頭，等待下一次讀取找到新的結尾
                    bytes_buffer = bytes_buffer[a:]
                    
            # 避免緩衝區無限膨脹 (如果一直找不到結尾)
            if len(bytes_buffer) > 100000:
                bytes_buffer = b''
                print("清除緩衝區堆積...")

            if cv2.waitKey(1) == ord('q'):
                break
                
        except Exception as e:
            print(f"發生錯誤 (自動忽略): {e}")
            # 不 break，繼續嘗試讀取下一幀
            continue

    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_stable_yolo_stream()