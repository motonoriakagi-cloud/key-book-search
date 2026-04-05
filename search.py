"""
PDFインデックスを検索するスクリプト
使用方法: python3 search.py <キーワード> [オプション]

例:
  python3 search.py 気胸
  python3 search.py 乳癌 --book 乳房Key
  python3 search.py 骨折 --limit 20
"""

import sqlite3
import argparse
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent / "index.db"


def make_snippet(text: str, keyword: str, context: int = 80) -> str:
    """テキスト中からキーワード周辺を抜き出す"""
    pos = text.find(keyword)
    if pos == -1:
        return ""
    start = max(0, pos - context)
    end = min(len(text), pos + len(keyword) + context)
    snippet = text[start:end]
    snippet = " ".join(snippet.split())  # 改行・連続スペースを整理
    # キーワードをマーク
    snippet = snippet.replace(keyword, f">>>{keyword}<<<")
    if start > 0:
        snippet = "..." + snippet
    if end < len(text):
        snippet = snippet + "..."
    return snippet


def search(keyword: str, book, limit: int):
    if not DB_PATH.exists():
        print("インデックスが見つかりません。先に build_index.py を実行してください。")
        sys.exit(1)

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    # FTS5 trigram は3文字以上が必要。常に pages テーブルへ LIKE 検索を使用。
    if book:
        cur.execute(
            """
            SELECT book, page, text
            FROM pages
            WHERE text LIKE ? AND book LIKE ?
            LIMIT ?
            """,
            (f"%{keyword}%", f"%{book}%", limit),
        )
    else:
        cur.execute(
            """
            SELECT book, page, text
            FROM pages
            WHERE text LIKE ?
            LIMIT ?
            """,
            (f"%{keyword}%", limit),
        )

    rows = cur.fetchall()
    con.close()

    results = []
    for book_name, page, text in rows:
        snippet = make_snippet(text, keyword)
        results.append((book_name, page, snippet))
    return results


def main():
    parser = argparse.ArgumentParser(description="Key画像シリーズ PDF全文検索")
    parser.add_argument("keyword", help="検索キーワード")
    parser.add_argument("--book", "-b", help="書籍名でフィルタ（部分一致）", default=None)
    parser.add_argument("--limit", "-n", type=int, default=10, help="最大表示件数（デフォルト: 10）")
    args = parser.parse_args()

    print(f"\n検索: 「{args.keyword}」", end="")
    if args.book:
        print(f"  書籍フィルタ: {args.book}", end="")
    print(f"\n{'─' * 60}")

    results = search(args.keyword, args.book, args.limit)

    if not results:
        print("  ヒットなし")
        return

    prev_book = None
    for book, page, snippet in results:
        if book != prev_book:
            print(f"\n【{book}】")
            prev_book = book
        print(f"  p.{page:4d}  {snippet}")

    print(f"\n{'─' * 60}")
    print(f"{len(results)} 件ヒット（最大 {args.limit} 件表示）")


if __name__ == "__main__":
    main()
