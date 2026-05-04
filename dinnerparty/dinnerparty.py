import random

# ---------- Stage 1: input friends ----------
print("Enter the number of friends joining (including you):")
try:
    count = int(input())
except ValueError:
    print("No one is joining for the party")
    exit()

if count <= 0:
    print("No one is joining for the party")
    exit()

print("Enter the name of every friend (including you), each on a new line:")

friends = {}
for _ in range(count):
    name = input()
    friends[name] = 0

# ---------- Stage 2: split the bill ----------
print("Enter the total amount:")
total_amount = float(input())

split_amount = round(total_amount / count, 2)

for friend in friends:
    friends[friend] = split_amount

# ---------- Stage 3: lucky one ----------
print('Do you want to use the "Who is lucky?" feature? Write Yes/No:')
answer = input()

lucky_friend = None

if answer == "Yes":
    lucky_friend = random.choice(list(friends.keys()))
    print(f"{lucky_friend} is the lucky one!")
else:
    print("No one is going to be lucky")

# ---------- Stage 4: recalculate if lucky ----------
if lucky_friend:
    new_split = round(total_amount / (count - 1), 2)
    for friend in friends:
        if friend == lucky_friend:
            friends[friend] = 0
        else:
            friends[friend] = new_split

print(friends)
