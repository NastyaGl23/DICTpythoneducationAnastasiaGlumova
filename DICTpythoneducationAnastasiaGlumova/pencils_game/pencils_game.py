# pencils_game.py
import random

# --- Етап 1. Запит кількості олівців ---
while True:
    pencils = input("How many pencils would you like to use:\n> ")
    if not pencils.isdigit():
        print("The number of pencils should be numeric")
        continue
    pencils = int(pencils)
    if pencils == 0:
        print("The number of pencils should be positive")
        continue
    break

# --- Етап 1. Запит, хто буде першим ---
players = ["John", "Jack"]
while True:
    first_player = input(f"Who will be the first ({players[0]}, {players[1]}):\n> ")
    if first_player in players:
        break
    else:
        print(f"Choose between '{players[0]}' and '{players[1]}'")

# --- Встановлюємо початкові дані ---
current_player = first_player
print("|" * pencils)

# --- Функція для зміни гравця ---
def switch_player(name):
    return players[1] if name == players[0] else players[0]

# --- Основний ігровий цикл ---
while pencils > 0:
    print(f"{current_player}'s turn:")

    # Якщо грає бот (Jack)
    if current_player == "Jack":
        # --- Етап 4: стратегія ---
        if pencils % 4 == 0:
            take = 3
        elif pencils % 4 == 3:
            take = 2
        elif pencils % 4 == 2:
            take = 1
        else:
            # Програшна позиція — бот бере випадкову кількість
            take = random.randint(1, 3)
        print(take)
    else:
        # --- Хід гравця (перевірка вводу) ---
        while True:
            take = input("> ")
            if not take.isdigit() or take not in ['1', '2', '3']:
                print("Possible values: '1', '2' or '3'")
                continue
            take = int(take)
            if take > pencils:
                print("Too many pencils were taken")
                continue
            break

    # --- Виконання ходу ---
    pencils -= take

    # Якщо олівці закінчились — гра завершена
    if pencils == 0:
        winner = switch_player(current_player)
        print(f"{winner} won!")
        break

    # Вивести стан столу
    print("|" * pencils)

    # Змінити гравця
    current_player = switch_player(current_player)
