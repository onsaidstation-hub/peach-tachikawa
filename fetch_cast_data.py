"""
raku-ichi.net から PEACH キャスト44名のデータを取得して JSON 保存
"""
import urllib.request
import json
import time
import re
import os

OUTPUT = r'E:\ドキュメント\onsaid\Claude\salvage\peach-tachikawa\cast_data.json'

TARGETS = [
    (25360, "なな"),
    (25361, "うた"),
    (25362, "ゆき"),
    (25363, "ひびき"),
    (25365, "ひな"),
    (25366, "きら"),
    (25369, "さと"),
    (25371, "まなか"),
    (25375, "うみ"),
    (25376, "もも"),
    (25389, "ここ"),
    (25503, "もか"),
    (25504, "あやね"),
    (25546, "ひなた"),
    (25569, "さな"),
    (25572, "すず"),
    (25604, "ももか"),
    (25622, "もえ"),
    (25836, "こころ"),
    (25848, "ゆう"),
    (26160, "りか"),
    (26161, "もな"),
    (26162, "ゆあ"),
    (26164, "さや"),
    (26165, "るな"),
    (26167, "まひろ"),
    (26416, "るい"),
    (26496, "あかり"),
    (26867, "みこ"),
    (26883, "めあ"),
    (26951, "ほのか"),
    (27124, "りん"),
    (27144, "かなの"),
    (27145, "まりな"),
    (27537, "うい"),
    (27579, "さあや"),
    (27608, "ゆい"),
    (27754, "あみ"),
    (27880, "なお"),
    (28077, "れいな"),
    (28130, "みお"),
    (28217, "すい"),
    (28528, "みか"),
    (28544, "まき"),
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'ja,en;q=0.9',
}


def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as res:
        return res.read().decode('utf-8', errors='replace')


def strip_tags(html):
    return re.sub(r'<[^>]+>', '', html).strip()


def parse(html, detail_id, hint_name):
    result = {'id': detail_id, 'hint_name': hint_name}

    # 名前・年齢: <p class="therapist_name pdb5 pdl5">ももか(23)</p>
    m = re.search(r'<p class="therapist_name[^"]*">\s*(.+?)\((\d+)\)\s*</p>', html)
    if m:
        result['name'] = m.group(1).strip()
        result['age'] = int(m.group(2))
    else:
        result['name'] = hint_name
        result['age'] = None

    # 画像URL: <img src="/img/uploads/staff/...">
    m = re.search(r'<img src="(/img/uploads/staff/[^"]+)"', html)
    result['image_url'] = m.group(1) if m else None

    # プロフィール本文: <div class="staff-introduction"><p>...</p></div>
    m = re.search(r'<div class="staff-introduction">(.*?)</div>', html, re.S)
    if m:
        inner = m.group(1)
        # <br> を改行に変換してからタグ除去
        inner = re.sub(r'<br\s*/?>', '\n', inner, flags=re.I)
        result['introduction'] = strip_tags(inner).strip()
    else:
        result['introduction'] = None

    # トレイト: <p class="trait ...">テキスト</p>
    traits = re.findall(r'<p class="trait[^"]*">\s*(.+?)\s*</p>', html)
    result['traits'] = traits

    return result


results = []
total = len(TARGETS)

for i, (detail_id, hint_name) in enumerate(TARGETS, 1):
    url = f'https://raku-ichi.net/kantou/therapist/detail/{detail_id}'
    print(f'[{i:02d}/{total}] {hint_name} ({detail_id}) ... ', end='', flush=True)
    try:
        html = fetch(url)
        data = parse(html, detail_id, hint_name)
        data['url'] = url
        data['error'] = False
        results.append(data)
        print(f'OK  name={data["name"]} age={data["age"]} traits={data["traits"]}')
    except Exception as e:
        results.append({
            'id': detail_id,
            'hint_name': hint_name,
            'url': url,
            'error': True,
            'error_message': str(e),
        })
        print(f'ERROR: {e}')

    if i < total:
        time.sleep(1.2)

with open(OUTPUT, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

ok = sum(1 for r in results if not r.get('error'))
err = sum(1 for r in results if r.get('error'))
print(f'\n完了: 成功={ok} / エラー={err} / 合計={total}')
print(f'保存先: {OUTPUT}')
