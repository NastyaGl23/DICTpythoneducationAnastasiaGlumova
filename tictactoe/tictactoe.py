def print_board(board):
    print("---------")
    for row in board:
        print("|", " ".join(row), "|")
    print("---------")


def check_winner(board, symbol):
    # строки и столбцы
    for i in range(3):
        if all(board[i][j] == symbol for j in range(3)):
            return True
        if all(board[j][i] == symbol for j in range(3)):
            return True

    # диагонали
    if all(board[i][i] == symbol for i in range(3)):
        return True
    if all(board[i][2 - i] == symbol for i in range(3)):
        return True

    return False


def game_state(board):
    x_count = sum(row.count("X") for row in board)
    o_count = sum(row.count("O") for row in board)

    x_wins = check_winner(board, "X")
    o_wins = check_winner(board, "O")

    if abs(x_count - o_count) >= 2:
        return "Impossible"
    if x_wins and o_wins:
        return "Impossible"
    if x_wins:
        return "X wins"
    if o_wins:
        return "O wins"

    if any("_" in row for row in board):
        return "Game not finished"

    return "Draw"


def get_coordinates(board):
    while True:
        coords = input("Enter the coordinates: ").split()

        if len(coords) != 2:
            print("You should enter numbers!")
            continue

        if not coords[0].isdigit() or not coords[1].isdigit():
            print("You should enter numbers!")
            continue

        x, y = int(coords[0]), int(coords[1])

        if x < 1 or x > 3 or y < 1 or y > 3:
            print("Coordinates should be from 1 to 3!")
            continue

        row = 3 - y
        col = x - 1

        if board[row][col] != "_":
            print("This cell is occupied! Choose another one!")
            continue

        return row, col


# ---------- ГРА ----------
board = [["_", "_", "_"],
         ["_", "_", "_"],
         ["_", "_", "_"]]

current_player = "X"

print_board(board)

while True:
    row, col = get_coordinates(board)
    board[row][col] = current_player
    print_board(board)

    state = game_state(board)
    if state != "Game not finished":
        print(state)
        break

    # смена игрока
    current_player = "O" if current_player == "X" else "X"
