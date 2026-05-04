import random


class MathQuizMaster:
    def __init__(self):
        # Описание доступных режимов тренировки
        self.lv_descriptions = {
            1: "базовые операции (числа 2-9)",
            2: "квадраты двузначных чисел (11-29)"
        }
        self.points = 0
        self.current_tier = None

    def select_complexity(self):
        """Выбор сложности пользователем."""
        while True:
            print("Укажите желаемый уровень:")
            for idx, label in self.lv_descriptions.items():
                print(f"{idx} — {label}")

            user_pick = input("> ").strip()
            if user_pick in ("1", "2"):
                self.current_tier = int(user_pick)
                break
            print("Неверный ввод. Выберите 1 или 2.")

    def create_math_problem(self):
        """Подготовка математического примера."""
        if self.current_tier == 1:
            num1 = random.randint(2, 9)
            num2 = random.randint(2, 9)
            sign = random.choice(["+", "-", "*"])
            math_expr = f"{num1} {sign} {num2}"
            # Вычисляем эталонный ответ
            return math_expr, eval(math_expr)
        else:
            val = random.randint(11, 29)
            return str(val), val ** 2

    def capture_integer(self):
        """Безопасное получение целого числа от пользователя."""
        while True:
            try:
                return int(input("> "))
            except ValueError:
                print("Ошибка: введите целое число.")

    def export_progress(self):
        """Запись достижений в текстовый файл."""
        print("Сохранить результат сессии в файл? (yes/no)")
        is_confirmed = input("> ").lower()
        if is_confirmed in ("yes", "y", "да"):
            username = input("Введите имя для протокола: > ")
            # Сохраняем строку с результатами (дозапись в конец файла)
            with open("results.txt", "a", encoding="utf-8") as file_out:
                data_line = (f"{username}: {self.points}/5 на уровне {self.current_tier} "
                             f"({self.lv_descriptions[self.current_tier]}).\n")
                file_out.write(data_line)
            print("Результат успешно экспортирован.")

    def start_engine(self):
        """Запуск основного цикла программы."""
        while True:
            self.points = 0
            self.select_complexity()

            for _ in range(5):
                question, solution = self.create_math_problem()
                print(question)

                if self.capture_integer() == solution:
                    print("Правильно!")
                    self.points += 1
                else:
                    print("Неверно.")

            print(f"Итоговый балл: {self.points} из 5.")
            self.export_progress()

            print("\nЖелаете начать новую серию задач? (yes/no)")
            is_repeat = input("> ").lower()
            if is_repeat not in ("yes", "y", "да"):
                print("До встречи!")
                break


if __name__ == "__main__":
    app_instance = MathQuizMaster()
    app_instance.start_engine()