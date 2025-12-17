import random

# ===== Етап 1: Введення кількості друзів із захистом =====
while True:
    try:
        num_friends = int(input("Enter the number of friends joining (including you):\n> "))
        if num_friends <= 0:
            print("No one is joining for the party")
            exit()
        break
    except ValueError:
        print("Please enter a valid number!")

# ===== Введення імен друзів =====
friends = {}
print("Enter the name of every friend (including you), each on a new line:")
for _ in range(num_friends):
    name = input("> ")
    friends[name] = 0

# ===== Етап 2: Введення суми вечері з перевіркою =====
while True:
    try:
        total_amount = float(input("Enter the total amount:\n> "))
        if total_amount < 0:
            print("Amount cannot be negative!")
            continue
        break
    except ValueError:
        print("Please enter a valid number!")

# ===== Розподіл суми на всіх друзів =====
split_amount = round(total_amount / num_friends, 2)
for name in friends:
    friends[name] = split_amount

# ===== Етап 3 і 4: Вибір щасливчика =====
use_lucky = input('Do you want to use the "Who is lucky?" feature? Write Yes/No:\n> ').strip().lower()
if use_lucky == "yes":
    lucky_one = random.choice(list(friends.keys()))
    print(f"{lucky_one} is the lucky one!")
    if num_friends > 1:
        split_amount = round(total_amount / (num_friends - 1), 2)
        for name in friends:
            friends[name] = 0 if name == lucky_one else split_amount
    else:
        friends[lucky_one] = 0
else:
    print("No one is going to be lucky")

# ===== Вивід фінальної суми =====
print("\nFinal amounts to pay:")
for name, amount in friends.items():
    print(f"{name}: {amount:.2f}")


