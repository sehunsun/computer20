from commands import COMMANDS
from data import hero, party, load_game

def game_loop():
    while True:
        print("\n==============================")
        print(f"📍 地點：{hero['location']} | ⏰ 時間：{hero['time']}")
        print(f"❤️ HP：{hero['hp']} / {hero['max_hp']}")
        print(f"🛡️ 隊伍：{[d['name'] for d in party] if party else '無'}")
        print("==============================")

        print("""
🎮【行動選單】
1️⃣ 移動
2️⃣ 攻擊
3️⃣ 背包
4️⃣ 狀態
5️⃣ 存檔
6️⃣ 說明
0️⃣ 離開
""")

        choice = input("請選擇行動：")

        if choice == "1": COMMANDS["move"]()
        elif choice == "2": COMMANDS["attack"]()
        elif choice == "3": COMMANDS["bag"]()
        elif choice == "4": COMMANDS["status"]()
        elif choice == "5": COMMANDS["save"]()
        elif choice == "6": COMMANDS["help"]()
        elif choice == "0":
            print("🏁 遊戲結束，感謝遊玩！")
            break
        else:
            print("❌ 無效選擇")

if __name__ == "__main__":
    load_game(hero, party)
    game_loop()
