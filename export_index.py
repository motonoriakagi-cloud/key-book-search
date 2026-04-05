"""
index.db から iPhone Claude 用の検索JSONを生成するスクリプト
使用方法: python3 export_index.py

出力: index/ フォルダに書籍ごとのJSONファイル
  - index/乳房Key.json, index/胸部Key.json ... (各150〜300KB)
  - iPhone Claudeがリポジトリ経由で疾患名を検索できる
"""

import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).parent / "index.db"
OUT_DIR = Path(__file__).parent / "index"
TEXT_LIMIT = 200  # 1ページあたりの最大文字数


def export():
    if not DB_PATH.exists():
        print("index.db が見つかりません。先に build_index.py を実行してください。")
        return

    OUT_DIR.mkdir(exist_ok=True)

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT DISTINCT book FROM pages ORDER BY book")
    books = [row[0] for row in cur.fetchall()]

    total_pages = 0
    for book in books:
        cur.execute(
            "SELECT page, text FROM pages WHERE book = ? ORDER BY page", (book,)
        )
        rows = cur.fetchall()

        entries = []
        for page, text in rows:
            cleaned = " ".join(text.split())
            entries.append({"p": page, "t": cleaned[:TEXT_LIMIT]})

        out_path = OUT_DIR / f"{book}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump({"book": book, "pages": entries}, f, ensure_ascii=False, separators=(",", ":"))

        size_kb = out_path.stat().st_size / 1024
        print(f"  {book}: {len(entries)}ページ ({size_kb:.0f} KB)")
        total_pages += len(entries)

    con.close()
    print(f"\n完了: {total_pages} ページ → {OUT_DIR}/ ({len(books)} ファイル)")


if __name__ == "__main__":
    export()
