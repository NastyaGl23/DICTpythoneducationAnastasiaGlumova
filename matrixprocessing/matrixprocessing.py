class MatrixEntity:
    def __init__(self, table):
        self.storage = table
        self.v_size = len(table)
        self.h_size = len(table[0]) if self.v_size > 0 else 0

    def display_content(self):
        """Печать матрицы с форматированием :g для чистоты вывода"""
        for line in self.storage:
            print(' '.join(f"{round(val, 2):g}" for val in line))

    def sum_with(self, other_entity):
        """Поэлементное сложение матриц"""
        if self.v_size != other_entity.v_size or self.h_size != other_entity.h_size:
            print("Размерности объектов не совпадают.")
            return None

        total = [[self.storage[i][j] + other_entity.storage[i][j] for j in range(self.h_size)]
                 for i in range(self.v_size)]
        return MatrixEntity(total)

    def scalar_product(self, factor):
        """Умножение на произвольное число"""
        scaled = [[point * factor for point in line] for line in self.storage]
        return MatrixEntity(scaled)

    def cross_product(self, second_mtx):
        """Матричное умножение (строка на столбец)"""
        if self.h_size != second_mtx.v_size:
            print("Умножение невозможно: несовпадение сторон.")
            return None

        result_grid = [[sum(self.storage[i][k] * second_mtx.storage[k][j] for k in range(self.h_size))
                        for j in range(second_mtx.h_size)] for i in range(self.v_size)]
        return MatrixEntity(result_grid)

    def flip(self, axis=1):
        """Отражение и транспонирование матрицы"""
        if axis == 1:  # Главная ось
            final = [[self.storage[j][i] for j in range(self.v_size)] for i in range(self.h_size)]
        elif axis == 2:  # Вторичная ось
            final = [[self.storage[self.v_size - 1 - j][self.h_size - 1 - i] for j in range(self.v_size)]
                     for i in range(self.h_size)]
        elif axis == 3:  # Зеркало по вертикали
            final = [row[::-1] for row in self.storage]
        elif axis == 4:  # Зеркало по горизонтали
            final = self.storage[::-1]
        else:
            return None
        return MatrixEntity(final)

    def get_determinant(self):
        """Публичный интерфейс для получения определителя"""
        if self.v_size != self.h_size:
            print("Требуется только квадратная структура.")
            return None
        return self._compute_det(self.storage)

    def _compute_det(self, current_grid):
        """Внутренний рекурсивный поиск детерминанта"""
        limit = len(current_grid)
        if limit == 1:
            return current_grid[0][0]
        if limit == 2:
            return current_grid[0][0] * current_grid[1][1] - current_grid[0][1] * current_grid[1][0]

        determinant = 0
        for col in range(limit):
            # Извлечение минора путем срезов
            sub_part = [row[:col] + row[col + 1:] for row in current_grid[1:]]
            determinant += ((-1) ** col) * current_grid[0][col] * self._compute_det(sub_part)
        return determinant

    def get_inverse(self):
        """Генерация обратной матрицы"""
        det = self.get_determinant()
        if not det:
            print("Матрица необратима (определитель = 0).")
            return None

        dim = self.v_size
        # Формирование матрицы дополнений
        complements = []
        for r in range(dim):
            row_vals = []
            for c in range(dim):
                minor_mtx = [line[:c] + line[c + 1:] for idx, line in enumerate(self.storage) if idx != r]
                row_vals.append(((-1) ** (r + c)) * self._compute_det(minor_mtx))
            complements.append(row_vals)

        # Создание инвертированной сетки (транспонирование + деление)
        inv_data = [[complements[j][i] / det for j in range(dim)] for i in range(dim)]
        return MatrixEntity(inv_data)


def input_matrix_flow():
    """Сценарий ручного ввода матрицы"""
    while True:
        try:
            raw_size = input("Укажите габариты (Строки Столбцы): ").split()
            h, w = int(raw_size[0]), int(raw_size[1])
            break
        except (ValueError, IndexError):
            print("Ошибка: введите два целых значения через пробел.")

    payload = []
    print(f"Введите значения для сетки {h}x{w}:")
    for i in range(h):
        while True:
            row_data = input(f"Строка {i + 1} > ").split()
            if len(row_data) != w:
                print(f"Должно быть ровно {w} элементов.")
                continue
            try:
                payload.append([float(x) for x in row_data])
                break
            except ValueError:
                print("Допускаются только числа.")
    return MatrixEntity(payload)


def run_app():
    """Точка входа и управление меню"""
    while True:
        print("\n=== КОНСОЛЬНЫЙ ВЫЧИСЛИТЕЛЬ ===")
        print("1. Сложение\n2. Скалярное умножение\n3. Матричное произведение")
        print("4. Трансформация\n5. Определитель\n6. Инвертирование\n0. Выйти")

        op = input("Выбор операции: ")

        if op == '1':
            m1, m2 = input_matrix_flow(), input_matrix_flow()
            res = m1.sum_with(m2)
            if res: res.display_content()

        elif op == '2':
            m = input_matrix_flow()
            try:
                val = float(input("Число: "))
                m.scalar_product(val).display_content()
            except ValueError:
                print("Некорректный ввод числа.")

        elif op == '3':
            m1, m2 = input_matrix_flow(), input_matrix_flow()
            res = m1.cross_product(m2)
            if res: res.display_content()

        elif op == '4':
            print("Оси: 1-Гл, 2-Поб, 3-Верт, 4-Гор")
            mode_id = input("ID типа: ")
            if mode_id in '1234':
                input_matrix_flow().flip(int(mode_id)).display_content()

        elif op == '5':
            d_val = input_matrix_flow().get_determinant()
            if d_val is not None: print(f"Детерминант: {d_val}")

        elif op == '6':
            res = input_matrix_flow().get_inverse()
            if res: res.display_content()

        elif op == '0':
            print("Выход из системы...")
            break


if __name__ == "__main__":
    run_app()