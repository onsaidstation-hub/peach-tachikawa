"""
1. images_staff_raku/*.jpg を ASCII名にリネーム
2. cast/*/index.html の img パスを更新
"""
import os
import re

BASE = r'E:\ドキュメント\onsaid\Claude\salvage\peach-tachikawa'
IMG_DIR = os.path.join(BASE, 'images_staff_raku')
CAST_DIR = os.path.join(BASE, 'cast')

NAME_MAP = {
    'なな': 'nana',
    'うた': 'uta',
    'ゆき': 'yuki',
    'ひびき': 'hibiki',
    'ひな': 'hina',
    'きら': 'kira',
    'さと': 'sato',
    'まなか': 'manaka',
    'うみ': 'umi',
    'もも': 'momo',
    'ここ': 'koko',
    'もか': 'moka',
    'あやね': 'ayane',
    'ひなた': 'hinata',
    'さな': 'sana',
    'すず': 'suzu',
    'ももか': 'momoka',
    'もえ': 'moe',
    'こころ': 'kokoro',
    'ゆう': 'yuu',
    'りか': 'rika',
    'もな': 'mona',
    'ゆあ': 'yua',
    'さや': 'saya',
    'るな': 'runa',
    'まひろ': 'mahiro',
    'るい': 'rui',
    'あかり': 'akari',
    'みこ': 'miko',
    'めあ': 'mea',
    'ほのか': 'honoka',
    'りん': 'rin',
    'かなの': 'kanano',
    'まりな': 'marina',
    'さあや': 'saaya',
    'ゆい': 'yui',
    'あみ': 'ami',
    'なお': 'nao',
    'れいな': 'reina',
    'みお': 'mio',
    'すい': 'sui',
    'みか': 'mika',
    'まき': 'maki',
}

# ---------------------------------------------------------------
# STEP 1: images_staff_raku/*.jpg をリネーム
# ---------------------------------------------------------------
renamed = {}  # 日本語stem → ASCII stem
skipped = []

for fname in os.listdir(IMG_DIR):
    if not fname.lower().endswith('.jpg'):
        continue
    stem = os.path.splitext(fname)[0]
    if stem in NAME_MAP:
        new_fname = NAME_MAP[stem] + '.jpg'
        src = os.path.join(IMG_DIR, fname)
        dst = os.path.join(IMG_DIR, new_fname)
        os.rename(src, dst)
        renamed[stem] = NAME_MAP[stem]
        print(f'  renamed: {fname} → {new_fname}')
    else:
        skipped.append(fname)
        print(f'  SKIP (no mapping): {fname}')

print(f'\nSTEP 1 完了: {len(renamed)}件リネーム / {len(skipped)}件スキップ')

# ---------------------------------------------------------------
# STEP 2: cast/*/index.html の img パスを更新
# ---------------------------------------------------------------
updated_files = 0
updated_total = 0

for cast_name in os.listdir(CAST_DIR):
    cast_path = os.path.join(CAST_DIR, cast_name)
    html_path = os.path.join(cast_path, 'index.html')
    if not os.path.isfile(html_path):
        continue

    with open(html_path, encoding='utf-8') as f:
        content = f.read()

    new_content = content
    for jp, en in NAME_MAP.items():
        old_img = f'../../images_staff_raku/{jp}.jpg'
        new_img = f'../../images_staff_raku/{en}.jpg'
        if old_img in new_content:
            new_content = new_content.replace(old_img, new_img)
            updated_total += 1

    if new_content != content:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        updated_files += 1
        print(f'  updated: cast/{cast_name}/index.html')

print(f'\nSTEP 2 完了: {updated_files}ファイル更新 ({updated_total}箇所置換)')

# ---------------------------------------------------------------
# STEP 3: cast/index.html（一覧）の img パスも更新
# ---------------------------------------------------------------
index_path = os.path.join(CAST_DIR, 'index.html')
with open(index_path, encoding='utf-8') as f:
    content = f.read()

new_content = content
count = 0
for jp, en in NAME_MAP.items():
    old_img = f'../images_staff_raku/{jp}.jpg'
    new_img = f'../images_staff_raku/{en}.jpg'
    if old_img in new_content:
        new_content = new_content.replace(old_img, new_img)
        count += 1

if new_content != content:
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'\nSTEP 3 完了: cast/index.html {count}箇所更新')
else:
    print(f'\nSTEP 3: cast/index.html 変更なし')

print('\n全処理完了')
