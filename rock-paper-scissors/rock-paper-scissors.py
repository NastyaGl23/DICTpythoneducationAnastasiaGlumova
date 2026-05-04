import random


class ExtendedRPSGame:
    STANDARD_LIST = ["rock", "paper", "scissors"]

    # Состояния приложения
    MODE_PREPARE = 0
    MODE_GAMEPLAY = 1
    MODE_FINISH = 2

    def __init__(self, data_file: str = "rating.txt"):
        self.points_log = data_file
        self.user_id = ""
        self.total_points = 0
        self.options = self.STANDARD_LIST.copy()
        self.current_mode = self.MODE_PREPARE

    def _fetch_rating(self) -> None:
        """Получение очков игрока из текстового файла базы."""
        try:
            with open(self.points_log, "r", encoding="utf-8") as file:
                for line in file:
                    user, val = line.strip().split()
                    if user == self.user_id:
                        self.total_points = int(val)
                        return
        except (FileNotFoundError, ValueError):
            pass
        self.total_points = 0

    def initialize(self) -> None:
        self.user_id = input("Введите имя пользователя:\n> ").strip()
        print(f"Добро пожаловать, {self.user_id}!")
        self._fetch_rating()
        self.print_manual()

    def print_manual(self):
        print("Команды управления:")
        print("!start  — переход к игре")
        print("!rating — посмотреть очки")
        print("!exit   — выход из приложения")
        print("Чтобы изменить список фигур, введите их через запятую (минимум 3 варианта) до начала игры.")

    def update_game_elements(self, raw_data: str) -> None:
        clean_input = raw_data.strip()

        # Если строка пустая — ставим дефолт
        if not clean_input:
            self.options = self.STANDARD_LIST.copy()
            print("Используются стандартные параметры.")
            return

        # Разбиваем и чистим список
        parsed_options = [item.strip() for item in clean_input.split(",") if item.strip()]

        # ПРОВЕРКА: Нужно минимум 3 элемента для корректной логики
        if len(parsed_options) < 3:
            print("Ошибка: для игры нужно минимум 3 различных символа!")
            print(f"Оставлен текущий набор: {', '.join(self.options)}")
        else:
            self.options = parsed_options
            print(f"Параметры обновлены. Текущий набор: {', '.join(self.options)}")

    def _is_cpu_winner(self, player_move: str, robot_move: str) -> bool:
        """Реализация круговой логики: бьет ли компьютерный выбор выбор игрока."""
        position = self.options.index(player_move)
        # Перестраиваем список так, чтобы выбор пользователя был в начале
        reordered = self.options[position + 1:] + self.options[:position]
        # Половина элементов после выбора игрока считаются выигрышными для ПК
        boundary = len(reordered) // 2
        return robot_move in reordered[:boundary]

    def execute_round(self, player_choice: str) -> None:
        bot_choice = random.choice(self.options)

        if bot_choice == player_choice:
            print(f"Результат: ничья ({bot_choice})")
            self.total_points += 50
        elif self._is_cpu_winner(player_choice, bot_choice):
            print(f"Поражение. Компьютер выбрал {bot_choice}")
        else:
            print(f"Победа! Вы обыграли {bot_choice}")
            self.total_points += 100

    def _process_event(self, raw_input: str):
        if raw_input == "!exit":
            print("Завершение программы. Всего доброго!")
            self.current_mode = self.MODE_FINISH
            return

        if raw_input == "!rating":
            print(f"Ваш текущий счет: {self.total_points}")
            return

        if self.current_mode == self.MODE_PREPARE:
            if raw_input == "!help":
                self.print_manual()
            elif raw_input == "!start":
                print("Бой начался! Вводите выбранную фигуру.")
                self.current_mode = self.MODE_GAMEPLAY
            else:
                self.update_game_elements(raw_input)

        elif self.current_mode == self.MODE_GAMEPLAY:
            if raw_input in self.options:
                self.execute_round(raw_input)
            else:
                print(f"Неизвестный вариант. Доступны: {', '.join(self.options)} или !exit.")

    def start_main_loop(self):
        self.initialize()

        while self.current_mode != self.MODE_FINISH:
            user_msg = input("> ").strip()
            if not user_msg:
                continue
            self._process_event(user_msg)


if __name__ == "__main__":
    session = ExtendedRPSGame()
    session.start_main_loop()