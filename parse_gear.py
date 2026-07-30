import re, json

with open('/sessions/dazzling-laughing-rubin/mnt/outputs/gear_raw.txt', encoding='utf-8') as f:
    text = f.read()

name_jp_to_en = {
    "スミス":"Smith", "ユージーン":"Eugene", "チャーリー":"Charlie", "クラリス":"Cloris",
    "セルゲイ":"Sergey", "ジーナ":"Gina", "バシティ":"Bahiti", "ソユン":"Seo-yoon",
    "ジャセル":"Jasser", "パトリック":"Patrick", "リンセツ":"Ling Xue", "ルム・ボーガン":"Lumak Bokan",
    "ジェシー":"Jessie", "ジェロニモ":"Jeronimo", "ナタリア":"Natalia", "ジャスミン":"Molly",
    "ジンマン":"Zinman", "フリント":"Flint", "フレンダー":"Philly", "フレンダ―":"Philly", "アロンゾ":"Alonso",
    "ローガン":"Logan", "ミア":"Mia", "グレッグ":"Greg", "アクモス":"Ahmose", "レイナ":"Reina",
    "リオン":"Lynn", "ヘクトー":"Hector", "ノラ":"Norah", "グエン":"Gwen", "無名":"Wu Ming",
    "レネ":"Renee", "ウェイン":"Wayne", "エディス":"Edith", "ゴードン":"Gordon",
    "ブラッドリー":"Bradley", "ガト":"Gatot", "ヘンドリック":"Hendrik", "ソニヤ":"Sonya",
    "マグヌス":"Magnus", "フレッド":"Fred", "シュラ":"Xura", "ブランシュ":"Blanchette",
    "グレゴリー":"Gregory", "フレイヤ":"Freya", "エリオノーラ":"Eleonora", "ロイド":"Lloyd",
    "ルーファス":"Rufus", "ヘルヴィル":"Hervor", "カロール":"Karol", "ライジーア":"Ligeia",
    "ギーゼラ":"Gisela", "フローラ":"Flora", "ウルカヌス":"Vulcanus", "エリーフ":"Elif",
    "ドミニク":"Dominic", "カーラ":"Cara"
}

list_section = text.split('英雄専用装備のスキル')[0]
blocks = [b.strip() for b in list_section.split('\n\n') if b.strip()]
hero_gear = {}
for b in blocks[1:]:  # skip header block "英雄専用装備一覧\n英雄 専用装備"
    lines = b.split('\n')
    if len(lines) == 2:
        hero, gear = lines
        hero = hero.strip()
        gear = gear.strip()
        if hero in name_jp_to_en:
            hero_gear[name_jp_to_en[hero]] = gear
        else:
            print('unmatched hero in list:', repr(hero))

print('hero_gear count:', len(hero_gear))

explo_section = text.split('探検スキル')[1].split('遠征スキル')[0]
exped_section = text.split('遠征スキル')[1]

def parse_skill_section(section):
    blocks = [b.strip() for b in section.split('\n\n') if b.strip()]
    result = {}
    i = 0
    # blocks pattern after header: gear_name_block, "HeroName専用\nSkillName Effect"
    # but gear name itself might be its own block (no blank line inside), and the next block has hero+skill
    for b in blocks[1:]:
        lines = b.split('\n')
        if len(lines) == 1:
            # just gear name alone (leftover), skip - will be combined logic below
            continue
    # simpler: iterate with regex over whole section
    pattern = re.compile(r'([^\n]+)\n\n([^\n]+)専用\n(\S+)\s+(.+?)(?=\n\n[^\n]+\n\n[^\n]+専用|\Z)', re.S)
    for m in pattern.finditer(section):
        gear_name, hero_jp, skill_name, effect = m.groups()
        gear_name = gear_name.strip()
        hero_jp = hero_jp.strip()
        effect = effect.strip().replace('\n', '')
        if hero_jp in name_jp_to_en:
            en = name_jp_to_en[hero_jp]
            result[en] = {"name": skill_name.strip(), "desc": effect, "gear_name": gear_name}
        else:
            print('unmatched hero in skill section:', repr(hero_jp))
    return result

explo_gear_skills = parse_skill_section(explo_section)
exped_gear_skills = parse_skill_section(exped_section)

print('explo_gear_skills count:', len(explo_gear_skills))
print('exped_gear_skills count:', len(exped_gear_skills))

missing_explo = set(hero_gear.keys()) - set(explo_gear_skills.keys())
missing_exped = set(hero_gear.keys()) - set(exped_gear_skills.keys())
print('missing explo:', missing_explo)
print('missing exped:', missing_exped)

out = {}
for en, gear_name in hero_gear.items():
    out[en] = {
        "gear_name": gear_name,
        "exploration_gear_skill": explo_gear_skills.get(en),
        "expedition_gear_skill": exped_gear_skills.get(en),
    }

with open('/sessions/dazzling-laughing-rubin/mnt/outputs/gear_jp.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print('total heroes with gear:', len(out))
print(json.dumps(out.get('Jeronimo'), ensure_ascii=False, indent=2))
