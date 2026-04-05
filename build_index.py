"""
PDFテキストをSQLite FTS5インデックスに構築するスクリプト
使用方法: python3 build_index.py
"""

import sqlite3
import sys
from pathlib import Path
import fitz  # PyMuPDF

DB_PATH = Path(__file__).parent / "index.db"
PDF_DIR = Path(__file__).parent

BOOKS = [
    ("乳房key.pdf",       "乳房Key"),
    ("小児Key.pdf",       "小児Key"),
    ("心臓血管Key.pdf",   "心臓血管Key"),
    ("救急Key.pdf",       "救急Key"),
    ("歯科Key.pdf",       "歯科Key"),
    ("泌尿器Key.pdf",     "泌尿器Key"),
    ("消化管Key.pdf",     "消化管Key"),
    ("産婦人科Key.pdf",   "産婦人科Key"),
    ("肝胆膵key.pdf",     "肝胆膵Key"),
    ("胸部Key.pdf",       "胸部Key"),
    ("胸部勘ドコロNEO.pdf","胸部勘ドコロNEO"),
    ("脊椎脊髄疾患.pdf",  "脊椎脊髄疾患"),
    ("脳MRIKey.pdf",      "脳MRI Key"),
    ("脳MRI正常解剖.pdf", "脳MRI正常解剖"),
    ("頭部勘ドコロ.pdf",  "頭部勘ドコロ"),
    ("頭頸部Key.pdf",     "頭頸部Key"),
    ("骨軟部Key.pdf",     "骨軟部Key"),
    ("骨軟部勘ドコロ.pdf","骨軟部勘ドコロ"),
]


def build(db_path: Path, pdf_dir: Path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS pages;
        DROP TABLE IF EXISTS pages_fts;
        CREATE TABLE pages (
            id      INTEGER PRIMARY KEY,
            book    TEXT NOT NULL,
            page    INTEGER NOT NULL,
            text    TEXT NOT NULL
        );
        CREATE VIRTUAL TABLE pages_fts USING fts5(
            book UNINDEXED,
            page UNINDEXED,
            text,
            content='pages',
            content_rowid='id',
            tokenize='trigram'
        );
    """)

    total_pages = 0
    for filename, title in BOOKS:
        pdf_path = pdf_dir / filename
        if not pdf_path.exists():
            print(f"  [skip] {filename} — ファイルが見つかりません")
            continue

        print(f"  処理中: {title} ...", end="", flush=True)
        doc = fitz.open(pdf_path)
        rows = []
        for i, page in enumerate(doc, start=1):
            text = page.get_text("text")
            if text.strip():
                rows.append((title, i, text))

        cur.executemany(
            "INSERT INTO pages (book, page, text) VALUES (?, ?, ?)", rows
        )
        cur.execute(
            "INSERT INTO pages_fts (rowid, book, page, text) "
            "SELECT id, book, page, text FROM pages WHERE book = ?",
            (title,),
        )
        doc.close()
        total_pages += len(rows)
        print(f" {len(rows)}ページ")

    con.commit()
    con.close()
    print(f"\n完了: {total_pages} ページをインデックスしました → {db_path}")


if __name__ == "__main__":
    print(f"インデックス構築開始: {DB_PATH}\n")
    build(DB_PATH, PDF_DIR)
