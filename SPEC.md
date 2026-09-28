# 家電說明書資料庫：資料格式與撰寫規範

專案根目錄：`~/work/home-appliances/`
- `data/<id>.json`：每個家電一個檔（這就是「資料庫」）
- `manuals/<id>/`：下載的官方說明書 PDF（只留本機，不公開上網）
- `docs/`：網站（index.html 手寫；data.js 由 build.py 產生）

## JSON 欄位（全部必填；沒有資料就給空陣列 [] 或 null）

```json
{
  "id": "英數小寫加連字號，例如 toto-g5",
  "category": "只能用其中一個：網路與通訊 / 廚房 / 衛浴 / 洗衣晾衣 / 空調 / 照明 / 居家安全 / 家具",
  "icon": "一個 emoji",
  "name": "中文俗稱，例如「TOTO 全自動馬桶 G5」",
  "brand": "品牌",
  "model": "型號（說明書涵蓋多型號就全列，用 / 分隔）",
  "model_note": "型號補充；例如說明書涵蓋多個容量，家裡實際是哪台要看機身銘牌在哪裡",
  "summary": "一兩句話：這是什麼、主要特色",
  "keywords": ["搜尋用關鍵字：俗稱、功能名、常見問題字眼，10–20 個"],
  "quick_card": ["最常用的 3–6 件事，一行一件，例如：「開機：按「電源」鍵」"],
  "manuals": [{"title": "", "url": "官方網址", "type": "官方PDF|官方網頁|官方影片|第三方", "lang": "zh-TW|en", "local_file": "manuals/<id>/xxx.pdf 或 null"}],
  "videos": [{"title": "", "url": ""}],
  "specs": [{"label": "", "value": ""}],
  "tutorials": [{"title": "怎麼…（用使用者會搜尋的問句當標題）", "when": "什麼情況會用到", "steps": ["步驟一", "步驟二"], "tips": ["注意事項"], "source": "說明書 p.xx 或網址"}],
  "troubleshooting": [{"symptom": "", "cause": "", "fix": "", "source": ""}],
  "error_codes": [{"code": "", "meaning": "", "action": ""}],
  "maintenance": [{"task": "", "frequency": "", "how": "", "source": ""}],
  "safety": ["重要安全注意事項，5–10 條"],
  "support": {"company": "", "phone": "", "website": "", "service_hours": "", "warranty": "", "register_url": ""},
  "sources": [{"title": "", "url": ""}],
  "open_questions": ["需要使用者確認、或請使用者補拍紙本說明書哪幾頁的事項"]
}
```

## 撰寫規則（一定要遵守）

1. **繁體中文、台灣用語、極度白話**。讀者對機械不熟，要能一邊看手機一邊操作。步驟一步一動作，例如「按住「電源」鍵 3 秒 → 螢幕亮起」。按鍵、選單名稱照說明書原文，用「」框起來。
2. **每一項內容都要有來源**：官方說明書 > 官網 FAQ / 支援頁 > 官方影片 > 可信第三方。`source` 欄寫頁碼或網址。
3. **絕對不可憑印象編造**按鍵名稱、錯誤代碼、數字、電話。查不到就寫進 `open_questions`，不要猜。說明書涵蓋多型號、或與家裡實機可能不同時，要註明。
4. `tutorials` 至少 8 則，涵蓋：第一次使用／基本操作、最常用功能、進階或省電功能、清潔保養、停電或異常時怎麼辦。`troubleshooting` 盡量完整抄錄說明書的故障排除表（改寫成白話）。`error_codes` 有就完整列出。
5. 下載官方 PDF 放到 `manuals/<id>/`（檔名英數），用 Read 工具讀 PDF（pages 參數每次最多 20 頁）。下載失敗就只記網址。
6. **不要登入任何網站、不要輸入帳密、不要送出任何表單**。不要寫入任何使用者個資（姓名、地址、Wi-Fi 密碼等）。
7. 寫完用 `python3 -c "import json;json.load(open('data/<id>.json'))"` 驗證格式。
8. 完成後回報（300 字內）：找到哪些官方說明書（網址）、哪些找不到、`open_questions` 重點。
