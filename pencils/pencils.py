import random

def request_pencil_count():
    while True:
        entry = input("How many pencils would you like to use:\n> ")
        if not entry.isdigit():
            print("The number of pencils should be numeric")
            continue

        total_amount = int(entry)
        if total_amount == 0:
            print("The number of pencils should be positive")
            continue

        return total_amount


def determine_starter(user, computer):
    while True:
        selection = input(f"Who will be the first ({user}, {computer})?\nYou are {user}, and {computer} is the bot.\n> ").strip()
        if selection not in [user, computer]:
            print(f"Choose between '{user}' and '{computer}'")
            continue
        return selection


def calculate_ai_step(remaining):
    # Математически выигрышная позиция: (4n + 1)
    optimal_take = (remaining - 1) % 4
    if optimal_take == 0:
        # Если бот в слабой позиции, берем минимум или рандом
        return 1 if remaining == 1 else random.randint(1, min(3, remaining))
    return optimal_take


def start_session():
    user_id = "John"
    bot_id = "Jack"

    stock = request_pencil_count()
    active_player = determine_starter(user_id, bot_id)

    while stock > 0:
        print("|" * stock)
        print(f"{active_player}'s turn!")

        if active_player == user_id:
            raw_move = input("> ")

            if raw_move not in ['1', '2', '3']:
                print("Possible values: '1', '2' or '3'")
                continue

            taken = int(raw_move)
            if taken > stock:
                print("Too many pencils were taken")
                continue
        else:
            # Логика хода компьютера
            taken = calculate_ai_step(stock)
            print(taken)

        stock -= taken

        if stock == 0:
            # В этой версии игры проигрывает тот, кто забрал последний предмет
            victor = bot_id if active_player == user_id else user_id
            print(f"{victor} won!")
            break

        # Передача хода
        active_player = bot_id if active_player == user_id else user_id

if __name__ == "__main__":
    start_session()