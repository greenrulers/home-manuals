# 我家家電說明書

家中 14 樣家電的操作教學、故障排除、錯誤代碼、清潔保養與客服資訊。內容整理自各品牌官方說明書與官網，每則都附來源。

- 網站：`docs/`（`index.html` 手寫；`data.js` 由 `build.py` 產生）
- 資料庫：`data/<id>.json`，每樣家電一個檔，欄位規範見 `SPEC.md`
- 更新方式：改 `data/*.json` → `python3 build.py` → commit & push

官方說明書 PDF 請到各家電頁面的「官方說明書與影片」連結下載。
