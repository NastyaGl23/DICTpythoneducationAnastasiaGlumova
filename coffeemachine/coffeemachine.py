class CoffeeApp:
    """
    Класс, имитирующий работу кофемашины.
    Управляется через состояние (current_mode).
    """

    def __init__(self):
        # Инициализация ресурсов под новыми именами
        self.ml_water = 400
        self.ml_milk = 540
        self.gr_beans = 120
        self.disposable_cups = 9
        self.cash_box = 550
        # Текущий статус устройства
        self.current_mode = "action"

    def _convert_to_integer(self, raw_text):
        """Вспомогательный метод: пробует превратить текст в число."""
        try:
            return int(raw_text)
        except ValueError:
            print(" Пожалуйста, введите корректное число!")
            return None

    def process_command(self, user_entry):
        """
        Главный распределитель команд.
        В зависимости от текущего режима вызывает нужный метод.
        """
        if self.current_mode == "action":
            self.main_menu_logic(user_entry)
        elif self.current_mode == "buy":
            self.make_purchase(user_entry)
        elif self.current_mode.startswith("fill"):
            self.add_supplies(user_entry)

    def main_menu_logic(self, cmd):
        """Обрабатывает основные команды главного меню."""
        if cmd == "buy":
            self.current_mode = "buy"
            print("Что хотите купить? 1 - эспрессо, 2 - латте, 3 - капучино, back – назад:")

        elif cmd == "fill":
            self.current_mode = "fill_water"
            print("Сколько мл воды вы хотите добавить:")

        elif cmd == "take":
            print(f"Я выдала вам ${self.cash_box}")
            self.cash_box = 0

        elif cmd == "remaining":
            self.show_inventory()

        elif cmd == "exit":
            self.current_mode = "exit"

        else:
            print(" Неизвестная команда. Выберите: buy, fill, take, remaining, exit.")

    def make_purchase(self, item_id):
        """Логика покупки и приготовления кофе."""
        if item_id == "back":
            self.current_mode = "action"
            return

        # Таблица ингредиентов
        menu_items = {
            "1": {"w": 250, "m": 0, "b": 16, "price": 4},   # Эспрессо
            "2": {"w": 350, "m": 75, "b": 20, "price": 7},  # Латте
            "3": {"w": 200, "m": 100, "b": 12, "price": 6}, # Капучино
        }

        selection = menu_items.get(item_id)
        if not selection:
            print(" Нет такого варианта.")
            self.current_mode = "action"
            return

        # Проверка запасов
        if self.ml_water < selection["w"]:
            print("Извините, не хватает воды!")
        elif self.ml_milk < selection["m"]:
            print("Извините, не хватает молока!")
        elif self.gr_beans < selection["b"]:
            print("Извините, не хватает зерен!")
        elif self.disposable_cups < 1:
            print("Извините, закончились стаканчики!")
        else:
            # Обновление ресурсов
            self.ml_water -= selection["w"]
            self.ml_milk -= selection["m"]
            self.gr_beans -= selection["b"]
            self.disposable_cups -= 1
            self.cash_box += selection["price"]
            print("Ресурсов достаточно, готовлю ваш кофе!")

        self.current_mode = "action"

    def add_supplies(self, volume):
        """Пошаговое пополнение запасов."""
        num_value = self._convert_to_integer(volume)
        if num_value is None:
            return

        if self.current_mode == "fill_water":
            self.ml_water += num_value
            self.current_mode = "fill_milk"
            print("Сколько мл молока добавить:")

        elif self.current_mode == "fill_milk":
            self.ml_milk += num_value
            self.current_mode = "fill_beans"
            print("Сколько грамм зерен добавить:")

        elif self.current_mode == "fill_beans":
            self.gr_beans += num_value
            self.current_mode = "fill_cups"
            print("Сколько стаканчиков добавить:")

        elif self.current_mode == "fill_cups":
            self.disposable_cups += num_value
            self.current_mode = "action"

    def show_inventory(self):
        """Вывод текущих запасов машины."""
        print("\nСостояние кофемашины:")
        print(f"{self.ml_water} мл воды")
        print(f"{self.ml_milk} мл молока")
        print(f"{self.gr_beans} г кофейных зерен")
        print(f"{self.disposable_cups} одноразовых стаканчиков")
        print(f"${self.cash_box} денег внутри\n")


# --- Запуск программы ---
device = CoffeeApp()

while device.current_mode != "exit":
    if device.current_mode == "action":
        print("Выберите действие (buy, fill, take, remaining, exit):")

    user_input_data = input("> ")
    device.process_command(user_input_data)