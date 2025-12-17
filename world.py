import random
from data import game_map, hero, monsters

def move_location(hero):
    current = hero['location']
    print(f"\n📍 你目前在 {current}，可以前往：")
    options = game_map.get(current, [])
    for i, loc in enumerate(options):
        print(f"{i+1}. {loc}")
    choice = input("輸入編號移動: ")
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(options):
            dest = options[idx]
            # 洞穴進入判定
            if dest == "Cave" and current == "Forest":
                roll = random.randint(1, 20)
                print(f"🎲 擲骰判定進入洞穴：{roll}")
                if roll not in [7, 15, 20]:
                    print("❌ 擲骰失敗，無法進入洞穴")
                    return
            hero['location'] = dest
            print(f"🚶 你移動到 {dest}")
            # 切換時間
            hero['time'] = "Evening" if hero['time'] == "Morning" else "Morning"
        else:
            print("❌ 無效編號")
    except ValueError:
        print("❌ 輸入錯誤")

def encounter_monster(location):
    if location in ["Novice Village", "Town"]:
        return None
    if location == "Cave":
        return random.choice([m for m in monsters if m["name"] in ["Slime", "Goblin"]])
    if location == "Dungeon":
        return random.choice([m for m in monsters if "Dragon" in m["name"] and m["name"] not in ["Ancient Dragon","Light Dragon","Dark Dragon"]])
    if location == "Dragon City":
        return random.choice([m for m in monsters if m["name"] in ["Fire Dragon","Ice Dragon","Ancient Dragon","Light Dragon","Dark Dragon","Water Dragon"]])
    return None
