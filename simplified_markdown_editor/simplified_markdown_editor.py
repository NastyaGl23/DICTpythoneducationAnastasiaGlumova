class TextFormatter:
    def __init__(self):
        # Хранилище для финальной сборки текста
        self.output_buffer = ""
        # Список доступных опций разметки
        self.valid_tags = {
            "plain", "bold", "italic", "header", "link",
            "inline-code", "ordered-list", "unordered-list", "new-line"
        }
        # Системные инструкции
        self.terminal_cmds = {"!help", "!done", "exit"}

    def show_manual(self):
        print("Доступные форматы: " + ", ".join(self.valid_tags))
        print("Команды: !help (справка), !done (сохранить результат)")

    def _request_line_count(self):
        while True:
            try:
                count = int(input("Введите число строк: > "))
                if count > 0:
                    return count
                print("Ошибка: требуется число больше нуля.")
            except ValueError:
                print("Ошибка: некорректный ввод, нужно целое число.")

    def launch(self):
        print("Редактор Markdown активен.")
        print("Введите !help для списка команд или exit для выхода.")

        while True:
            selection = input("Тип разметки или команда:\n> ").strip().lower()

            if selection in self.terminal_cmds:
                if selection == "!help":
                    self.show_manual()
                elif selection == "!done":
                    with open("output.md", "w", encoding="utf-8") as md_file:
                        md_file.write(self.output_buffer)
                    print("Файл output.md сохранен. Работа завершена.")
                    break
                elif selection == "exit":
                    print("Завершение без сохранения.")
                    break
                continue

            if selection not in self.valid_tags:
                print("Ошибка: такой опции не существует.")
                continue

            # Блок обработки элементов разметки
            if selection == "plain":
                string = input("Введите текст: > ")
                self.output_buffer += string

            elif selection == "bold":
                string = input("Текст для жирного выделения: > ")
                self.output_buffer += f"**{string}**"

            elif selection == "italic":
                string = input("Текст для курсива: > ")
                self.output_buffer += f"*{string}*"

            elif selection == "inline-code":
                string = input("Код: > ")
                self.output_buffer += f"`{string}`"

            elif selection == "header":
                while True:
                    try:
                        level = int(input("Уровень (1-6): > "))
                        if 1 <= level <= 6:
                            break
                        print("Диапазон уровней: от 1 до 6.")
                    except ValueError:
                        print("Нужна цифра от 1 до 6.")
                string = input("Заголовок: > ")
                self.output_buffer += f"{'#' * level} {string}\n"

            elif selection == "link":
                anchor = input("Текст ссылки: > ")
                address = input("URL: > ")
                self.output_buffer += f"[{anchor}]({address})"

            elif selection == "new-line":
                if self.output_buffer.endswith("\n\n"):
                    pass
                elif self.output_buffer.endswith("\n"):
                    self.output_buffer += "\n"
                else:
                    self.output_buffer += "\n\n"

            elif selection in ("ordered-list", "unordered-list"):
                total_lines = self._request_line_count()
                if self.output_buffer and not self.output_buffer.endswith("\n"):
                    self.output_buffer += "\n"

                for i in range(1, total_lines + 1):
                    entry = input(f"Строка #{i}: > ")
                    if selection == "ordered-list":
                        self.output_buffer += f"{i}. {entry}\n"
                    else:
                        self.output_buffer += f"* {entry}\n"
                self.output_buffer += "\n"

            # Отображение текущего результата
            print("--- Предпросмотр ---")
            print(self.output_buffer)
            print("--------------------")


if __name__ == "__main__":
    editor_instance = TextFormatter()
    editor_instance.launch()