#!/usr/bin/env python3
"""把 data/*.json 檢查後合併成 docs/data.js（網站讀這個檔）。

用法：cd ~/work/home-appliances && python3 build.py
"""
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CATS = ["居家安全", "廚房", "衛浴", "洗衣晾衣", "空調", "照明", "網路與通訊", "家具"]
REQUIRED = ["id", "category", "icon", "name", "brand", "model", "summary"]
LISTS = ["keywords", "quick_card", "manuals", "videos", "specs", "tutorials",
         "troubleshooting", "error_codes", "maintenance", "safety", "sources", "open_questions"]


def check(d, fname):
    problems = []
    for k in REQUIRED:
        if not d.get(k):
            problems.append(f"缺少 {k}")
    if d.get("id") and d["id"] != fname:
        problems.append(f"id「{d['id']}」和檔名不同")
    if d.get("category") not in CATS:
        problems.append(f"類別「{d.get('category')}」不在清單內")
    for k in LISTS:
        v = d.get(k)
        if v is None:
            d[k] = []
        elif not isinstance(v, list):
            problems.append(f"{k} 應該是清單")
    for k in ("manuals", "videos", "sources"):
        for x in d.get(k) or []:
            u = (x or {}).get("url")
            if u and not str(u).startswith(("http://", "https://")):
                problems.append(f"{k} 網址格式不對：{u}")
    for t in d.get("tutorials") or []:
        if not t.get("title") or not t.get("steps"):
            problems.append(f"教學缺標題或步驟：{t.get('title')}")
    d.setdefault("support", {})
    return problems


def main():
    items, bad = [], False
    for p in sorted((ROOT / "data").glob("*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"✗ {p.name}: JSON 格式錯誤 {e}")
            bad = True
            continue
        probs = check(d, p.stem)
        if probs:
            bad = True
            print(f"✗ {p.name}: " + "；".join(probs))
        d.pop("local_notes", None)
        # 本機 PDF 路徑不公開
        for m in d.get("manuals") or []:
            m.pop("local_file", None)
        items.append(d)
        print(f"✓ {d.get('icon', '')} {d.get('name')}：教學 {len(d['tutorials'])}、故障 {len(d['troubleshooting'])}、"
              f"代碼 {len(d['error_codes'])}、保養 {len(d['maintenance'])}、待確認 {len(d['open_questions'])}")

    order = {c: i for i, c in enumerate(CATS)}
    items.sort(key=lambda d: (order.get(d.get("category"), 99), d.get("name", "")))
    now = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M")
    js = ("window.BUILD_INFO = " + json.dumps({"date": now, "count": len(items)}, ensure_ascii=False) + ";\n"
          "window.APPLIANCES = " + json.dumps(items, ensure_ascii=False, indent=1) + ";\n")
    (ROOT / "docs" / "data.js").write_text(js, encoding="utf-8")
    print(f"\n共 {len(items)} 樣家電 → docs/data.js（{len(js.encode()) // 1024} KB）")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
