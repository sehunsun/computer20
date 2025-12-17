import random
from collections import deque
import heapq

print("🐉 歡迎來到《迷你龍與地下城》 🐉\n")
print("你是一名冒險者，從新手村踏上旅程...")

# =========================
# 玩家資料
# =========================
hero = {
    "name": "勇者",
    "hp": 50,
    "max_hp": 50,
    "attack_bonus": 5,
    "base_damage": 10,
    "brave_power": True,  # 天生勇者之力
    "strength": 10,
    "agility": 10,
    "intelligence": 10
}

party = []  # 隊伍（龍可加入）
time_of_day = "Morning"  # 初始時間

# =========================
# 裝備資料
# =========================
items = [
    {"name": "Beginner's Sword", "attack": 8, "rarity": 1},
    {"name": "Knight's Steel Sword", "attack": 18, "rarity": 3},
    {"name": "Hero's Holy Sword", "attack": 30, "rarity": 5},
    {"name": "Dragon Slayer Blade", "attack": 50, "rarity": 6},
    {"name": "Wooden Shield", "attack": 2, "rarity": 1},
    {"name": "Knight's Shield", "attack": 5, "rarity": 3},
    {"name": "Armor of Light", "attack": 4, "rarity": 4}
]

# =========================
# 怪物與龍族資料
# =========================
monsters = [
    {"name": "Slime", "element":"None", "weakness": "Fire", "danger": 1, "ac": 8, "hp": 10, "base_attack": 5},
    {"name": "Goblin", "element":"None", "weakness": "Ice", "danger": 2, "ac": 11, "hp": 15, "base_attack": 6},
    {"name": "Skeleton", "element":"None", "weakness": "Light", "danger": 3, "ac": 13, "hp": 20, "base_attack": 7},
    {"name": "Orc", "element":"None", "weakness": "Lightning", "danger": 4, "ac": 14, "hp": 25, "base_attack": 8},
    {"name": "Dark Mage", "element":"None", "weakness": "Light", "danger": 5, "ac": 15, "hp": 30, "base_attack": 9},
    {"name": "Minotaur", "element":"None", "weakness": "Ice", "danger": 6, "ac": 16, "hp": 35, "base_attack": 10},
    {"name": "Lich", "element":"None", "weakness": "Holy", "danger": 7, "ac": 17, "hp": 40, "base_attack": 12},

    # 龍族
    {"name": "Fire Dragon", "element":"Fire", "weakness": "Ice", "danger": 9, "ac": 18, "hp": 50, "base_attack": 12},
    {"name": "Ice Dragon", "element":"Ice", "weakness": "Fire", "danger": 9, "ac": 18, "hp": 50, "base_attack": 12},
    {"name": "Wind Dragon", "element":"Wind", "weakness": None, "danger": 8, "ac": 17, "hp": 45, "base_attack": 10},
    {"name": "Earth Dragon", "element":"Earth", "weakness": None, "danger": 8, "ac": 17, "hp": 45, "base_attack": 10},
    {"name": "Wood Dragon", "element":"Wood", "weakness": "Wood", "danger": 9, "ac": 18, "hp": 50, "base_attack": 11},
    {"name": "Thunder Dragon", "element":"Thunder", "weakness": "Earth", "danger": 10, "ac": 19, "hp": 55, "base_attack": 13},
    {"name": "Water Dragon", "element":"Water", "weakness": None, "danger": 8, "ac": 17, "hp": 45, "base_attack": 10},
    {"name": "Ancient Dragon", "element":"Ancient", "weakness": "Brave Power", "danger": 12, "ac": 25, "hp": 80, "base_attack": 18},
    {"name": "Light Dragon", "element":"Light", "weakness": "Dark", "danger": 10, "ac": 20, "hp": 60, "base_attack": 14},
    {"name": "Dark Dragon", "element":"Dark", "weakness": "Light", "danger": 10, "ac": 20, "hp": 60, "base_attack": 14},

    # 魔王
    {"name": "Demon Lord", "element":"None", "weakness": "Holy", "danger": 12, "ac": 22, "hp": 80, "base_attack": 15}
]

# =========================
# 地圖
# =========================
game_map = {
    "Novice Village": [("Forest", 2), ("Town", 1)],
    "Forest": [("Novice Village", 2), ("Cave", 4), ("Town", 3)],
    "Cave": [("Forest", 4), ("Dungeon", 6)],
    "Town": [("Novice Village", 1), ("Forest", 3)],
    "Dungeon": [("Cave", 6), ("Dragon City", 8)],
    "Dragon City": [("Dungeon", 8)]
}

current_location = "Novice Village"

# =========================
# 融合技能表
# =========================
fusion_table = {
    frozenset(["Ice", "Fire"]): {"name": "冰火五重天", "bonus": 30},
    frozenset(["Fire", "Water"]): {"name": "氣爆", "bonus": 25},
    frozenset(["Earth", "Wind"]): {"name": "Sandstorm", "bonus": 15},
    frozenset(["Fire", "Wind"]): {"name": "Flaming Tornado", "bonus": 20},
    frozenset(["Water", "Ice"]): {"name": "Hailstorm", "bonus": 10},
    frozenset(["Fire", "Thunder"]): {"name": "Lava Lightning", "bonus": 20},
    frozenset(["Water", "Thunder"]): {"name": "Thunderstorm", "bonus": 15},
    frozenset(["Earth", "Fire"]): {"name": "Lava Flow", "bonus": 15},
    frozenset(["Ice", "Wind"]): {"name": "Blizzard", "bonus": 15},
    frozenset(["Light", "Dark"]): {"name": "Eclipse", "bonus": 25}
}

# =========================
# D20 擲骰
# =========================
def roll_d20():
    return random.randint(1, 20)

def attack_roll(hero, monster):
    roll = roll_d20()
    total = roll + hero["attack_bonus"]
    print(f"\n🎲 擲骰：{roll} + {hero['attack_bonus']} = {total} vs AC {monster['ac']}")
    if roll == 20:
        print("✨ 暴擊命中！")
        return True, True, roll
    if roll == 1:
        print("💥 攻擊失敗！")
        return False, False, roll
    return total >= monster['ac'], False, roll

def calculate_damage(hero, critical, monster):
    dmg = hero['base_damage']
    if critical:
        dmg *= 2
    if hero.get("brave_power") and monster['name'] == "Ancient Dragon":
        dmg += 10
    return dmg

# =========================
# 隊伍攻擊
# =========================
def party_attack(monster, attack_type="normal"):
    if not party:
        return
    print("\n🛡️ 你的隊伍發動攻擊！")
    elements_used = set()
    for ally in party:
        if attack_type == "normal":
            dmg = ally['base_attack']
            print(f"{ally['name']} 攻擊造成 {dmg} 點傷害 | {monster['name']} HP:{monster['hp']}")
            monster['hp'] -= dmg
        elif attack_type == "element":
            elem = ally['element']
            dmg = ally['base_attack']//2
            print(f"{ally['name']} 使用屬性 {elem} 攻擊造成 {dmg} 點傷害 | {monster['name']} HP:{monster['hp']}")
            monster['hp'] -= dmg
            elements_used.add(elem)
    # 檢查融合技
    for combo, skill in fusion_table.items():
        if combo.issubset(elements_used):
            monster['hp'] -= skill['bonus']
            print(f"💥 融合技 {skill['name']} 對 {monster['name']} 造成額外 {skill['bonus']} 點傷害")

# =========================
# 訓練/療傷系統
# =========================
def training_cmd():
    print("\n🌞 商人提供早晨訓練服務！")
    roll = roll_d20()
    if roll == 1:
        print("❌ 訓練失敗")
    elif roll == 20:
        for stat in ['strength','agility','intelligence']:
            hero[stat] += 10
        print("🎉 訓練大成功！所有屬性 +10")
    else:
        for stat in ['strength','agility','intelligence']:
            hero[stat] += 0.5*roll
        print(f"⚡ 訓練完成！所有屬性 +{0.5*roll}")

def healing_cmd():
    print("\n🌙 商人提供晚間療傷服務！")
    roll = roll_d20()
    if roll == 1:
        print("❌ 療傷失敗")
    elif roll == 20:
        hero['hp'] = hero['max_hp']
        print("💖 療傷大成功！HP 回滿")
    else:
        heal = hero['max_hp'] * (roll*5/100)
        hero['hp'] = min(hero['hp']+heal, hero['max_hp'])
        print(f"💖 回復 HP {heal:.1f} 點，目前 HP:{hero['hp']}")

# =========================
# 移動
# =========================
def move_cmd():
    global current_location, time_of_day
    print("\n你可以移動到：")
    options = game_map[current_location]
    for i, (loc, _) in enumerate(options):
        print(f"{i+1}. {loc}")
    choice = input("輸入編號移動: ")
    try:
        idx = int(choice)-1
        if 0 <= idx < len(options):
            dest = options[idx][0]
            # 洞穴進入判定
            if dest == "Cave" and current_location == "Forest":
                roll = roll_d20()
                print(f"🎲 擲骰判定進入洞穴：{roll}")
                if roll not in [7, 15, 20]:
                    print("❌ 擲骰失敗，無法進入洞穴")
                    return
            current_location = dest
            print(f"\n🚶 你來到 {current_location}")
            # 安全區：新手村/城市
            if current_location in ["Novice Village", "Town"]:
                if time_of_day == "Morning":
                    training_cmd()
                else:
                    healing_cmd()
            # 切換時間
            time_of_day = "Evening" if time_of_day == "Morning" else "Morning"
        else:
            print("❌ 無效選擇")
    except:
        print("❌ 輸入錯誤")

# =========================
# 背包
# =========================
def show_inventory():
    print("\n🎒 背包（依攻擊力排序）：")
    for i in sorted(items, key=lambda x: x['attack'], reverse=True):
        print(f"- {i['name']} | ATK:{i['attack']} | 稀有度:{i['rarity']}")

def bag_cmd():
    show_inventory()

# =========================
# 怪物生成
# =========================
def encounter_monster():
    if current_location in ["Novice Village", "Town"]:
        return None
    if current_location == "Cave":
        return random.choice([search_monster("Slime"), search_monster("Goblin")])
    if current_location == "Dungeon":
        return random.choice([search_monster("Fire Dragon"), search_monster("Ice Dragon"),
                              search_monster("Wind Dragon"), search_monster("Earth Dragon")])
    if current_location == "Dragon City":
        return random.choice([search_monster("Fire Dragon"), search_monster("Ice Dragon"),
                              search_monster("Ancient Dragon"), search_monster("Light Dragon"),
                              search_monster("Dark Dragon"), search_monster("Water Dragon")])
    return None

# =========================
# 怪物搜尋
# =========================
def search_monster(name):
    for m in monsters:
        if m["name"].lower() == name.lower():
            return m
    return None

# =========================
# 攻擊指令
# =========================
def attack_cmd():
    monster = encounter_monster()
    if not monster:
        print("🏞️ 這裡沒有怪物可以攻擊")
        return
    print(f"\n👹 遇到怪物：{monster['name']} HP:{monster['hp']}")
    while monster['hp'] > 0 and hero['hp'] > 0:
        defeated = attack_roll_hero(monster)
        if defeated:
            break
        # 隊伍攻擊
        party_attack(monster, attack_type="normal")
        if monster['hp'] <= 0:
            print(f"🏆 {monster['name']} 被隊伍擊敗！")
            break
        # 怪物回擊
        damage = random.randint(1, monster['base_attack'])
        hero['hp'] -= damage
        print(f"👹 {monster['name']} 攻擊你 {damage} 點 | HP:{hero['hp']}")
        if hero['hp'] <= 0:
            print("💀 你死亡了！遊戲結束。")
            return

def attack_roll_hero(monster):
    hit, critical, roll = attack_roll(hero, monster)
    if hit:
        dmg = calculate_damage(hero, critical, monster)
        monster['hp'] -= dmg
        print(f"🔥 你造成 {dmg} 點傷害！怪物剩餘 HP: {monster['hp']}")

        # 擲20且為龍 → 加入隊伍
        dragon_names = ["Fire Dragon","Ice Dragon","Ancient Dragon","Light Dragon","Dark Dragon",
                        "Wind Dragon","Earth Dragon","Thunder Dragon","Wood Dragon","Water Dragon"]
        if roll == 20 and monster['name'] in dragon_names:
            if monster not in party:
                party.append(monster.copy())
                print(f"🤝 {monster['name']} 加入你的隊伍！")

        if monster['hp'] <= 0:
            print(f"🏆 你擊敗了 {monster['name']}！")
            return True
    else:
        print("❌ 攻擊未命中！")
    return False

# =========================
# 指令表
# =========================
command_table = {
    "move": move_cmd,
    "attack": attack_cmd,
    "bag": bag_cmd
}

# =========================
# 遊戲主迴圈
# =========================
def game_loop():
    while True:
        print(f"\n📍 你現在在 {current_location} | HP:{hero['hp']} | 時間:{time_of_day}")
        print(f"🛡️ 隊伍成員: {[d['name'] for d in party]}")
        cmd = input("輸入指令(move/attack/bag/exit): ").lower()
        if cmd == "exit":
            print("🏁 遊戲結束，勇者回家休息。")
            break
        elif cmd in command_table:
            command_table[cmd]()
        else:
            print("❌ 無效指令")

game_loop()
