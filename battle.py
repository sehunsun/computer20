import random
from data import hero, party, fusion_table

def roll_d20():
    return random.randint(1, 20)

def hero_attack(monster):
    monster = monster.copy()
    print(f"\n👹 遭遇怪物：{monster['name']} HP:{monster['hp']}")
    while monster["hp"] > 0 and hero["hp"] > 0:
        roll = roll_d20()
        total = roll + hero.get("attack_bonus",0)
        print(f"🎲 擲骰：{roll} + {hero.get('attack_bonus',0)} = {total} vs AC {monster.get('ac',10)}")
        if roll == 1:
            print("❌ 攻擊失敗")
        elif roll == 20 or total >= monster.get("ac",10):
            dmg = hero.get("base_damage",10)
            if roll == 20:
                dmg *= 2
                print("✨ 暴擊！")
            monster["hp"] -= dmg
            print(f"🔥 你造成 {dmg} 傷害 | 怪物 HP:{monster['hp']}")
            if roll == 20 and monster.get("is_dragon") and monster not in party:
                party.append(monster.copy())
                print(f"🤝 {monster['name']} 加入隊伍")
        else:
            print("❌ 未命中")

        if monster["hp"] <= 0:
            print(f"🏆 擊敗 {monster['name']}！")
            break

        if party:
            print("\n🛡️ 隊伍發動攻擊！")
            elements_used = set()
            for ally in party:
                dmg = ally.get("base_attack",5)
                elem = ally.get("element")
                monster["hp"] -= dmg
                print(f"{ally['name']} 攻擊造成 {dmg} 傷害 | 怪物 HP:{monster['hp']}")
                if elem: elements_used.add(elem)
            for combo, skill in fusion_table.items():
                if combo.issubset(elements_used):
                    monster["hp"] -= skill['bonus']
                    print(f"💥 融合技 {skill['name']} 對 {monster['name']} 造成額外 {skill['bonus']} 點傷害")

        if monster["hp"] > 0:
            monster_attack = random.randint(1, monster.get("base_attack",5))
            hero["hp"] -= monster_attack
            print(f"👹 {monster['name']} 反擊，對你造成 {monster_attack} 點傷害 | HP:{hero['hp']}")
        if hero["hp"] <= 0:
            print("💀 你死亡了！遊戲結束")
            return False
    return True
