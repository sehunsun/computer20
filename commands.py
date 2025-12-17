import random
from data import hero, party, items, save_game
from world import move_location, encounter_monster
from battle import hero_attack

def bag():
    print("\n🎒【背包】")
    if not items:
        print("背包是空的")
        return
    for i in sorted(items, key=lambda x:x["attack"], reverse=True):
        print(f"- {i['name']} | ATK:{i['attack']} | 稀有度:{i.get('rarity','?')}")

def attack():
    monster = encounter_monster(hero["location"])
    if not monster:
        print("🏞️ 這裡沒有怪物")
        return
    hero_attack(monster)

def move():
    move_location(hero)

def status():
    print("\n📊【勇者狀態】")
    print(f"姓名：{hero['name']}")
    print(f"位置：{hero['location']}")
    print(f"時間：{hero['time']}")
    print(f"HP：{hero['hp']} / {hero['max_hp']}")
    print(f"ATK加值：{hero['attack_bonus']}")
    print(f"基礎傷害：{hero['base_damage']}")
    print(f"STR：{hero['strength']} | AGI：{hero['agility']} | INT：{hero['intelligence']}")
    print(f"勇者之力：{'有' if hero['brave_power'] else '無'}")
    print(f"隊友：{[d['name'] for d in party] if party else '無'}")

def help_cmd():
    print("""
📖【指令說明】
move    - 移動
attack  - 攻擊怪物
bag     - 查看背包
status  - 查看狀態
save    - 存檔
help    - 指令說明
exit    - 離開遊戲
""")

COMMANDS = {
    "move": move,
    "attack": attack,
    "bag": bag,
    "status": status,
    "help": help_cmd,
    "save": lambda: save_game(hero, party)
}
