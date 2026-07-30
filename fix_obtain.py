import re, json

obtain_correct = {
"Molly": "共通の欠片交換・ジャスミンパック・英雄募集・生存者の試練・灯台情報・7日間ログイン・英雄殿堂",
"Jeronimo": "VIPパック購入・最強領主",
"Natalia": "初回チャージ・VIPパック購入",
"Zinman": "ラッキールーレット・デイリー割引・英雄殿堂・英雄集結",
"Bahiti": "ミッションクリア・英雄募集・灯台情報・共通の欠片交換",
"Lumak Bokan": "共通の欠片交換・故郷と遠方・英雄募集",
"Jasser": "共通の欠片交換・故郷と遠方・英雄募集",
"Seo-yoon": "共通の欠片交換・故郷と遠方・英雄募集",
"Gina": "「ジーナの復讐」イベント・共通の欠片交換",
"Jessie": "英雄募集・灯台情報・生存者の試練・共通の欠片交換",
"Patrick": "英雄募集・灯台情報・共通の欠片交換",
"Sergey": "ミッションクリア・英雄募集・灯台情報・共通の欠片交換",
"Smith": "英雄募集・灯台情報・探検戦闘・共通の欠片交換",
"Cloris": "英雄募集・灯台情報・探検戦闘・共通の欠片交換",
"Charlie": "英雄募集・灯台情報・探検戦闘・共通の欠片交換",
"Eugene": "英雄募集・灯台情報・探検戦闘・共通の欠片交換",
"Philly": "デイリー割引・最強領主・英雄集結・氷原支配者・最強王国",
"Alonso": "英雄殿堂",
"Flint": "ラッキールーレット・共通の欠片交換・英雄殿堂",
"Logan": "英雄殿堂",
"Mia": "ラッキールーレット",
"Greg": "デイリー割引・最強領主・英雄集結",
"Reina": "英雄殿堂",
"Lynn": "ラッキールーレット",
"Ahmose": "デイリー割引・最強領主・英雄集結",
"Hector": "ラッキールーレット",
"Norah": "デイリー割引・最強領主・英雄集結",
"Gwen": "英雄殿堂",
"Wu Ming": "英雄殿堂",
"Renee": "ラッキールーレット",
"Wayne": "デイリー割引・最強領主・英雄集結",
"Gordon": "英雄殿堂・兵器工場ショップ",
"Edith": "最強領主・氷原支配者・最強王国・デイリー割引・英雄集結・兵器工場ショップ",
"Bradley": "ラッキールーレット・兵器工場ショップ",
"Gatot": "共通の欠片交換・ラッキールーレット・兵器工場ショップ",
"Sonya": "共通の欠片交換・最強領主・氷原支配者・最強王国・デイリー割引・英雄集結・兵器工場ショップ",
"Hendrik": "英雄殿堂・兵器工場ショップ",
"Ling Xue": "英雄募集",
"Xura": "最強領主・氷原支配者・最強王国・デイリー割引",
"Fred": "ラッキールーレット",
"Magnus": "英雄殿堂",
"Gregory": "最強領主・氷原支配者・最強王国・デイリー割引・英雄集結・兵器工場ショップ",
"Freya": "英雄殿堂・兵器工場ショップ",
"Blanchette": "ラッキールーレット・兵器工場ショップ",
"Eleonora": "ラッキールーレット・兵器工場ショップ",
"Lloyd": "最強領主・氷原支配者・最強王国・デイリー割引・英雄集結・兵器工場ショップ",
"Rufus": "英雄殿堂・兵器工場ショップ",
"Hervor": "英雄殿堂・兵器工場ショップ",
"Karol": "ラッキールーレット・兵器工場ショップ",
"Ligeia": "最強領主・氷原支配者・最強王国・デイリー割引・英雄集結・兵器工場ショップ",
"Gisela": "最強領主・氷原支配者・最強王国・デイリー割引・英雄集結・兵器工場ショップ",
"Flora": "兵器工場ショップ",
"Vulcanus": "ラッキールーレット・兵器工場ショップ",
"Elif": "ラッキールーレット・兵器工場ショップ",
"Dominic": "最強領主・氷原支配者・最強王国・デイリー割引・英雄集結・兵器工場ショップ",
"Cara": "兵器工場ショップ",
}

with open('/sessions/dazzling-laughing-rubin/mnt/outputs/wos_hero_database.html', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'<script id="hero-data" type="application/json">(.*?)</script>', html, re.S)
data = json.loads(m.group(1))

missing = []
for h in data['heroes']:
    en = h.get('name_en')
    if en in obtain_correct:
        h['how_to_obtain'] = obtain_correct[en]
    else:
        missing.append(en)

print('missing (not corrected, kept old value):', missing)

new_json = json.dumps(data, ensure_ascii=False, indent=2)
new_block = '<script id="hero-data" type="application/json">\n' + new_json + '\n</script>'
html2 = html[:m.start()] + new_block + html[m.end():]

with open('/sessions/dazzling-laughing-rubin/mnt/outputs/wos_hero_database.html', 'w', encoding='utf-8') as f:
    f.write(html2)

print('done, heroes:', len(data['heroes']))
