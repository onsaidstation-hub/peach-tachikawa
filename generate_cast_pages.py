"""
cast_data.json からキャスト一覧ページ・個別ページを生成
出力先: cast/index.html, cast/[名前]/index.html
"""
import json
import os

DATA_PATH = r'E:\ドキュメント\onsaid\Claude\salvage\peach-tachikawa\cast_data.json'
OUT_DIR   = r'E:\ドキュメント\onsaid\Claude\salvage\peach-tachikawa\cast'
IMG_DIR   = r'E:\ドキュメント\onsaid\Claude\salvage\peach-tachikawa\images_staff_raku'

with open(DATA_PATH, encoding='utf-8') as f:
    casts = json.load(f)

os.makedirs(OUT_DIR, exist_ok=True)


# ---------------------------------------------------------------
# 共通パーツ（パス深さを引数で調整）
# ---------------------------------------------------------------
def head(title, depth=1):
    """depth=1: cast/, depth=2: cast/名前/"""
    root = '../' * depth
    return f"""<!doctype html>
<html lang="ja" class="col2">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<title>{title} | 立川のメンズエステなら【PEACH（ピーチ）】</title>
<link rel="shortcut icon" type="image/x-icon" href="/images_shop/favicon.ico">
<link rel="stylesheet" href="/css/advanced.css">
<link rel="stylesheet" href="/css/base.css?1685829625">
<link rel="stylesheet" href="/css/change_white.css?1685829625">
</head>
<body class="home">
<div id="top" class="container">

<!--▼▼ ヘッダー ▼▼-->
<div class="header_wrap">
<div class="header_outer">
<header class="header header_col2">
<div class="header_inner">
<h1 class="site-title"><a href="{root}"><img src="/images_shop/logo.png" class="header_logo" alt="立川のメンズエステなら【PEACH（ピーチ）】"></a></h1>
<div class="header_cont">
<div class="show-pc">
JR立川駅北口徒歩5分・南口徒歩6分<br><span>電話番号</span> <a href=""><span class="f16em suu">***-****-****</span></a><br>
<span>営業時間</span> 11:00～早朝5:00（受付 10:00～深夜3:00）</div>
<div class="show-sp f08em">
<span>電話番号</span> <a href="">***-****-****</a><br>
<span>営業時間</span> 11:00～早朝5:00</div>
</div>
</div>
</header>
</div>
</div>
<!--▲▲ ヘッダー ▲▲-->

<!--▼▼ グローバルナビ ▼▼-->
<div class="gnav_wrap">
<div class="gnav_outer">
<nav class="gnav">
<div class="gnav_inner">
<ul class="gnav_cont">
<li><a href="{root}"><div class="show-pc"><span class="f12em eng">TOP PAGE</span><br></div>トップページ</a></li>
<li><a href="{root}schedule/"><div class="show-pc"><span class="f12em eng">SCHEDULE</span><br></div>出勤情報</a></li>
<li><a href="{root}cast/"><div class="show-pc"><span class="f12em eng">THERAPIST</span><br></div>セラピスト</a></li>
<li><a href="{root}price/"><div class="show-pc"><span class="f12em eng">PRICE</span><br></div>料金システム</a></li>
<li><a href="{root}event/"><div class="show-pc"><span class="f12em eng">EVENT</span><br></div>イベント</a></li>
<li><a href="{root}access/"><div class="show-pc"><span class="f12em eng">ACCCESS</span><br></div>アクセス</a></li>
<li><a href="{root}recruit/"><div class="show-pc"><span class="f12em eng">RECRUIT</span><br></div>求人情報</a></li>
</ul>
</div>
<div class="gnav_btn_wrap">
<div class="gnav_btn"><span class="gnav_btn_icon-open"></span><div class="gnav_btn_menu">MENU</div></div>
</div>
</nav>
</div>
</div>
<!--▲▲ グローバルナビ ▲▲-->
"""


def footer(depth=1):
    root = '../' * depth
    return f"""
<!--▼▼ footer ▼▼-->
<footer class="footer_wrap">
<div class="footer_outer">
<section class="section">
JR立川駅北口徒歩5分・南口徒歩6分<br>立川市曙町2-23<br><span>電話番号</span> <a href=""><span class="f16em suu">***-****-****</span></a><br>
<span>営業時間</span> 11:00～早朝5:00（<span>受付</span> 10:00～深夜3:00）
<ul class="footer-navi clerfix">
<li><a href="{root}">トップページ</a></li>
<li><a href="{root}schedule/">出勤情報</a></li>
<li><a href="{root}cast/">セラピスト</a></li>
<li><a href="{root}price/">料金システム</a></li>
<li><a href="{root}event/">イベント</a></li>
<li><a href="{root}access/">アクセス</a></li>
<li><a href="{root}recruit/">求人情報</a></li>
<li><a href="{root}link/">リンク</a></li>
</ul>
</section>
</div>
<div class="copyright_wrap">
<div class="copyright al-c">
© 2023 <a href="{root}">立川のメンズエステなら【PEACH（ピーチ）】</a>ver3.0</div>
</div>
</footer>
<!--▲▲ footer ▲▲-->

<div class="footer-panel_wrap">
<div class="footer-panel_outer">
<aside class="footer-panel">
<ul class="utility-menu">
<li class="utility-menu_item color_tel"><a href=""><span class="icon_tel"></span><br>電話</a></li>
<li class="utility-menu_item color_top"><a href="#top"><span class="icon_arrow_s_up"></span><br>TOPへ</a></li>
</ul>
</aside>
</div>
</div>
</div><!--container-->
<p class="page-top"><a href="#top"></a></p>
<script src="/js/utility.js" defer></script>
</body>
</html>"""


# ---------------------------------------------------------------
# 画像存在チェック
# ---------------------------------------------------------------
def img_path_for_index(name):
    """cast/index.html からの相対パス"""
    if os.path.exists(os.path.join(IMG_DIR, f'{name}.jpg')):
        return f'../images_staff_raku/{name}.jpg'
    return '../images_staff_raku/placeholder.jpg'


def img_path_for_detail(name):
    """cast/[名前]/index.html からの相対パス"""
    if os.path.exists(os.path.join(IMG_DIR, f'{name}.jpg')):
        return f'../../images_staff_raku/{name}.jpg'
    return '../../images_staff_raku/placeholder.jpg'


# ---------------------------------------------------------------
# cast/index.html（一覧）
# ---------------------------------------------------------------
items_html = ''
for c in casts:
    name = c['name']
    age  = c['age'] if c['age'] and c['age'] < 100 else '?'
    img  = img_path_for_index(name)
    items_html += f"""
<div class="col">
<div class="cast_box">
<a href="./{name}/">
<div class="cast_box_img">
<figure><img src="{img}" alt="{name}"></figure>
</div>
<div class="cast_box_info">
{name}<span class="color01"> / </span>{age}歳
</div>
</a>
</div>
</div>
"""

index_html = head('セラピスト一覧', depth=1) + f"""
<div class="main_wrap">
<div class="main_outer">
<main id="main" class="main">
<div class="main_inner">
<div class="section_wrap-wide">
<section class="section">
<h2><span class="f30rem eng color01">THERAPIST</span><br><span class="f14rem">セラピスト一覧</span></h2>
<div class="inner">
<div class="cast-top-wrap">
{items_html}
</div>
</div>
</section>
</div>
</div>
</main>
</div>
</div>
""" + footer(depth=1)

with open(os.path.join(OUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(index_html)
print('cast/index.html 生成完了')


# ---------------------------------------------------------------
# cast/[名前]/index.html（個別ページ）× 44
# ---------------------------------------------------------------
for c in casts:
    name  = c['name']
    age   = c['age'] if c['age'] and c['age'] < 100 else '?'
    img   = img_path_for_detail(name)
    intro = c.get('introduction') or ''
    traits = c.get('traits') or []

    intro_block = ''
    if intro:
        intro_html = intro.replace('\n', '<br>\n')
        intro_block = f"""
<div class="section_wrap">
<section class="section">
<h3><span class="color01">プロフィール</span></h3>
<div class="inner">
<p>{intro_html}</p>
</div>
</section>
</div>"""

    traits_block = ''
    if traits:
        trait_items = ''.join(f'<p class="cast_tag">{t}</p>' for t in traits)
        traits_block = f"""
<div class="section_wrap">
<section class="section">
<div class="inner">
{trait_items}
</div>
</section>
</div>"""

    page_html = head(name, depth=2) + f"""
<div class="main_wrap">
<div class="main_outer">
<main id="main" class="main">
<div class="main_inner">

<div class="section_wrap-wide">
<section class="section">
<div class="cast_box" style="max-width:600px; margin:0 auto;">
<div class="cast_box_img" style="text-align:center;">
<img src="{img}" alt="{name}" style="max-width:100%; height:auto;">
</div>
<div class="cast_box_info" style="padding:10px 0;">
<h2 class="f20em">{name}<span class="color01"> / </span>{age}歳</h2>
</div>
</div>
</section>
</div>

{intro_block}
{traits_block}

<div class="section_wrap">
<section class="section">
<div class="inner al-c">
<a href="../"><button class="btn_02"><span class="f12em">← セラピスト一覧に戻る</span></button></a>
</div>
</section>
</div>

</div>
</main>
</div>
</div>
""" + footer(depth=2)

    cast_dir = os.path.join(OUT_DIR, name)
    os.makedirs(cast_dir, exist_ok=True)
    with open(os.path.join(cast_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(page_html)

print(f'個別ページ {len(casts)} 件生成完了')

# ---------------------------------------------------------------
# サマリー
# ---------------------------------------------------------------
total_files = 1 + len(casts)
no_img = [c['name'] for c in casts
          if not os.path.exists(os.path.join(IMG_DIR, f"{c['name']}.jpg"))]
print(f'生成ファイル数: {total_files} (index×1 + 個別×{len(casts)})')
print(f'画像なし(placeholder使用): {len(no_img)}名 → {no_img}')
