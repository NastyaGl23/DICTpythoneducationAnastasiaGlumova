import random

def play_game():
    words = ['python', 'java', 'javascript', 'php']
    secret_word = random.choice(words)
    display = ["-"] * len(secret_word)
    attempts_left = 8
    guessed_letters = set()

    while attempts_left > 0:
        print("".join(display))
        guess = input("Input a letter: > ").strip()

        # Перевірка: рівно одна літера
        if len(guess) != 1:
            print("You should input a single letter")
            continue

        # Перевірка: мала англійська літера
        if not guess.isalpha() or not guess.islower():
            print("Please enter a lowercase English letter")
            continue

        # Перевірка повторної літери
        if guess in guessed_letters:
            print("You've already guessed this letter")
            continue

        guessed_letters.add(guess)

        if guess in secret_word:
            for i, letter in enumerate(secret_word):
                if letter == guess:
                    display[i] = guess
        else:
            print("That letter doesn't appear in the word")
            attempts_left -= 1

        # Перевірка перемоги
        if "-" not in display:
            print("".join(display))
            print(f"You guessed the word {secret_word}!")
            print("You survived!")
            return

    # Якщо закінчились спроби
    print("".join(display))
    print("You lost!")

def main():
    print("HANGMAN\n")

    while True:
        choice = input('Type "play" to play the game, "exit" to quit: > ').strip().lower()
        if choice == "play":
            play_game()
        elif choice == "exit":
            break
        else:
            continue

if __name__ == "__main__":
    main()
