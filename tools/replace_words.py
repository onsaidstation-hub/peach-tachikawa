"""
replace_words.py
cast/ および reviews/ 以下の .html ファイル内のコード語を実際の語句に置換するスクリプト

置換テーブル:
  AA → クンニ / BB → 射精  / CC → 陰茎 / DD → 洗体  / EE → 手コキ
  FF → フェラ / GG → 乳首  / HH → 舐め / II → パイパン / JJ → クリ / KK → 陰部
"""

import os
import shutil
from pathlib import Path

# ----------------------------------------------------------------
# 設定
# ----------------------------------------------------------------
BASE = Path(r'E:\ドキュメント\onsaid\Claude\salvage\peach-tachikawa')
TARGET_DIRS = [
    BASE / 'cast',
    BASE / 'reviews',
]
BACKUP_DIR = BASE / 'tools' / 'backup'

REPLACE_TABLE = {
    'AA': 'クンニ',
    'BB': '射精',
    'CC': '陰茎',
    'DD': '洗体',
    'EE': '手コキ',
    'FF': 'フェラ',
    'GG': '乳首',
    'HH': '舐め',
    'II': 'パイパン',
    'JJ': 'クリ',
    'KK': '陰部',
}

# ----------------------------------------------------------------
# STEP 1: 対象ファイルを再帰的に収集
# ----------------------------------------------------------------
print('=' * 60)
print('replace_words.py — コード語置換ツール')
print('=' * 60)

html_files = sorted(
    f for d in TARGET_DIRS for f in d.rglob('*.html')
)

if not html_files:
    print(f'\n[ERROR] HTMLファイルが見つかりませんでした: {TARGET_DIRS}')
    exit(1)

print(f'\n【対象ファイル一覧】 ({len(html_files)}件)')
for f in html_files:
    print(f'  {f.relative_to(BASE)}')

# ----------------------------------------------------------------
# STEP 2: 各コードの出現箇所数を集計
# ----------------------------------------------------------------
print('\n【コード出現数】')

# {code: {filepath: count}} の形で集計
code_totals = {code: 0 for code in REPLACE_TABLE}
file_counts  = {}   # {filepath: {code: count}}

for fpath in html_files:
    content = fpath.read_text(encoding='utf-8', errors='replace')
    per_file = {}
    for code in REPLACE_TABLE:
        n = content.count(code)
        if n:
            per_file[code] = n
            code_totals[code] += n
    if per_file:
        file_counts[fpath] = per_file

# 集計表示
has_any = False
for code, word in REPLACE_TABLE.items():
    n = code_totals[code]
    if n:
        has_any = True
        print(f'  {code} → {word} : {n}箇所')

if not has_any:
    print('  置換対象のコードは見つかりませんでした。')
    exit(0)

total_replacements = sum(code_totals.values())
print(f'\n  合計: {total_replacements}箇所 / {len(file_counts)}ファイル')

# ----------------------------------------------------------------
# STEP 3: 確認プロンプト
# ----------------------------------------------------------------
print()
answer = input('置換を実行しますか？ (y/n): ').strip().lower()

if answer != 'y':
    print('キャンセルしました。')
    exit(0)

# ----------------------------------------------------------------
# STEP 4: バックアップ → 置換実行
# ----------------------------------------------------------------
print(f'\n[1/2] バックアップ中 → {BACKUP_DIR}')
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

for fpath in html_files:
    # BASE からの相対パスをそのまま backup/ 以下に再現
    rel = fpath.relative_to(BASE)
    dest = BACKUP_DIR / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(fpath, dest)

print(f'  {len(html_files)}ファイルをバックアップしました。')

print('\n[2/2] 置換実行中...')

replaced_files = 0
replaced_total = 0

for fpath in html_files:
    if fpath not in file_counts:
        continue  # 置換対象なし

    content = fpath.read_text(encoding='utf-8', errors='replace')
    new_content = content
    file_replaced = 0

    for code, word in REPLACE_TABLE.items():
        n = new_content.count(code)
        if n:
            new_content = new_content.replace(code, word)
            file_replaced += n

    if file_replaced:
        fpath.write_text(new_content, encoding='utf-8')
        replaced_files += 1
        replaced_total += file_replaced
        rel = fpath.relative_to(BASE)
        print(f'  更新: {rel}  ({file_replaced}箇所)')

# ----------------------------------------------------------------
# STEP 5: 完了報告
# ----------------------------------------------------------------
print(f'\n完了: {replaced_files}件のファイル・{replaced_total}箇所を置換しました。')
print(f'バックアップ保存先: {BACKUP_DIR}')
