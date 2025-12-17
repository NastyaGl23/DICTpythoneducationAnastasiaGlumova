import random

def display_word(word, guessed_letters):
    display = ''
    for letter in word:
        if letter in guessed_letters:
            display += letter
        else:
            display += '-'
    return display

def hangman_game():
    words = ['python', 'java', 'javascript', 'php']
    word = random.choice(words)
    guessed_letters = set()
    incorrect_letters = set()
    attempts_left = 8

    # Отображаем первые 3 буквы
    display = word[:3] + '-' * (len(word) - 3)
    print(display)

    while attempts_left > 0:
        guess = input("Input a letter: > ")

        # Проверка ввода
        if len(guess) != 1:
            print("You should input a single letter")
            continue
        if not guess.islower() or not guess.isalpha():
            print("Please enter a lowercase English letter")
            continue
        if guess in guessed_letters or guess in incorrect_letters:
            print("You've already guessed this letter")
            continue

        if guess in word:
            guessed_letters.add(guess)
            new_display = display_word(word, guessed_letters)
            if new_display == display:
                print("No improvements")
            else:
                display = new_display
            print(display)
            if display == word:
                print(f"You guessed the word {word}!")
                print("You survived!")
                return
        else:
            incorrect_letters.add(guess)
            attempts_left -= 1
            print("That letter doesn't appear in the word")
            print(display)

    print("You lost!")

def main():
    print("HANGMAN")
    while True:
        choice = input('Type "play" to play the game, "exit" to quit: > ').strip()
        if choice == "play":
            print("----------")
            hangman_game()
        elif choice == "exit":
            break
        else:
            continue

if __name__ == "__main__":
    main()
