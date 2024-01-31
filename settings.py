from exceptions import BoardOutException, CountourException, OverlapException, InvalidShipSizeException


# Класс точек на поле
# Перегруженный метод __eq__ проверяет совпадение точек
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.coordinate = (x, y)

    def __eq__(self, other):
        if isinstance(other, Dot):
            return self.coordinate == other.coordinate
        else:
            return False

    # Перегружаем метод, чтобы при исключениях выводить не ячейку памяти, а координаты
    def __str__(self):
        return f"{self.coordinate}"

    # Поскольку перегружая метод __str__ python помечает объекты как нехэшируемые
    # Нам нужно реализовать __hash__ для отслеживания контуров
    def __hash__(self):
        return hash((self.x, self.y))


#  Описание корабля на поле
class Ship:
    def __init__(self, length, prow, direction):
        self.length = length
        self.prow = prow
        self.direction = direction
        self.health = length  # количество жизней изначально равно длине корабля

    def dots(self):
        ship_dots = []
        x, y = self.prow.x, self.prow.y

        # вычисляем значения остальных точек корабля
        for _ in range(self.length):
            ship_dots.append(Dot(x, y))
            # Заменить horizontal на h и v ?
            if self.direction == 'h':
                x += 1
            else:
                y += 1
        return ship_dots


# Описание игрового поля
class Board:
    def __init__(self):
        self.ships = []  # список кораблей на доске
        self.hits = []  # список точек попаданий
        self.misses = []  # список точек промахов
        self.live_ships = 0
        self.hid = False  # агрумент видимости доски
        # создаем кортеж областей, который не будет содержать повторяющихся элементов
        self.contour_points = set()

    def add_ship(self, ship):
        self.ship = ship.dots()

        # Проверка размера корабля
        if not 0 < ship.length <= 3:
            raise InvalidShipSizeException(ship.length)

        # Проверка, что корабль не выходит за границы доски
        for dot in self.ship:
            if dot.x < 1 or dot.x > 6 or dot.y < 1 or dot.y > 6:
                raise BoardOutException(dot.x, dot.y)

        # Проверка, что корабль не пересекался с другими кораблями
        # и не стоит вплотную с другими
        for existing_ship in self.ships:
            existing_ship_dots = existing_ship.dots()
            for dot in self.ship:
                if dot in existing_ship_dots:
                    raise OverlapException("Cannot add ship. Overlap detected.", dot)
                elif dot in self.contour_points:
                    raise CountourException(dot)

        self.live_ships += 1  # Обвновление счетчика кораблей
        self.ships.append(ship)  # Добавление корабля в список кораблей игрока
        self.contour(ship)  # Добавление области вокруг корабля

    def out(self, dot):
        # Если точка выходит за пределы поля, метод возвращает True
        return not (0 < dot.x <= 6 and 0 < dot.y <= 6)

    def contour(self, ship):
        # создаем массив соседних точек
        contour_offsets = [(-1, -1), (-1, 0), (-1, 1),
                           (0, -1), (0, 1),
                           (1, -1), (1, 0), (1, 1)]

        for dot in ship.dots():
            for dx, dy in contour_offsets:
                adj_dot = Dot(dot.x + dx, dot.y + dy)
                # добавляем только точки, расположенные внутри доски
                if 0 < adj_dot.x <= 6 and 0 < adj_dot.y <= 6:
                    # добавляем элемент во множество, если он уже есть в нем, то ничего не добавляется
                    self.contour_points.add(adj_dot)

    def shot(self, dot):
        # Проверка был ли сделан выстрел внутри поля
        if self.out(dot):
            raise BoardOutException(dot.x, dot.y)

        for ship in self.ships:
            if dot in ship.dots():
                print("Hit!")
                ship.health -= 1  # Перерасчет оставшихся жизней корабля
                self.hits.append(dot)  # Добавление попадания в список
                if ship.health == 0:  # Проверка разрушился ли корабль полностью
                    self.live_ships -= 1  # Обновление счетчика кораблей
                return True
        # В случае промаха функция не будет возвращать True и продолжит работу
        # Поэтому дополнительная проверка не нужна
        print("Miss!")
        self.misses.append(dot)  # Добавление промаха в список
        return False

    def print_board(self, hid=False):  # Печать доски игрока, при выставлении hid=True печать доски врага
        # Печать верхней строки поля с обозначением столбцов
        board_str = '  | '
        for col in range(1, 7):
            board_str += str(col) + ' | '
        board_str += '\n'
        # print("   | " + " | ".join(str(col) for col in range(1, 7)) + " |")

        # Печать поля с кораблями
        for row in range(1, 7):
            board_str += str(row) + ' | '

            for col in range(1, 7):
                dot = Dot(col, row)
                # Проверка был ли сделан выстрел в корабль
                if dot in self.hits:
                    board_str += 'X | '
                # Печать промаха
                elif dot in self.misses:
                    board_str += 'T | '
                # Печать вражеской доски
                elif any(dot in ship.dots() for ship in self.ships) and hid:
                    board_str += 'O | '
                # Печать доски игрока
                elif any(dot in ship.dots() for ship in self.ships) and not hid:
                    board_str += '■ | '
                # Печать оставшихся клеток
                else:
                    board_str += 'O | '

            board_str += '\n'

        return board_str

    def reset_board(self):  # Сброс всех данных доски для новой игры
        self.ships = []
        self.hits = []
        self.live_ships = 0
        self.contour_points = set()
