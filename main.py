class BoardException(Exception):
    pass


# Ошибка выхода за пределы поля
class BoardOutException(BoardException):
    def __init__(self, x, y):
        # self.coordinate = (x, y)
        super().__init__(f"Incorrect coordinates: ({x}, {y}).")


# Ошибка перекрытия ячеек
# Возникает, когда игрок пытается выбрать уже открытую ячейку
# Или заполнить ячейку, которая уже содержит часть коробля
class OverlapException(BoardException):
    # добавляем отдельную переменную для сообщения, поскольку
    # это исключение может возникнуть и при постановке корабля и при выстреле
    def __init__(self, message, dot):
        super().__init__(message, f"You have already selected this cell: {dot}.")

class CountourException(BoardException):
    def __init__(self, dot):
        super().__init__(f"Cannot place a ship adjacent to another ship at {dot}.")


# Ошибка неверного размера корабля
class InvalidShipSizeException(BoardException):
    def __init__(self, length):
        self.length = length
        super().__init__(f"Incorrect ship length: {self.length}.")


# Класс точек на поле
# Перегруженный метод __eq__ проверяет совпедение точек
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

    # Перегружаем метод, чтобы при исключениях выводить не ячейку памяти
    # а координаты
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
        # количество жизней изначально равно длине корабля
        self.health = length

    def dots(self):
        ship_dots = []
        x, y = self.prow.x, self.prow.y

        # вычисляем значения остальных точек корабля
        for _ in range(self.length):
            ship_dots.append(Dot(x, y))
            # Заменить horizontal на h и v ?
            if self.direction == 'horizontal':
                x += 1
            else:
                y += 1
        return ship_dots

    # перерасчет количества жизней корабля
    def shoot_at(self, dot):
        if dot in self.dots():
            self.health -= 1
            return True # или возвратить жизни?




# Описание игрового поля
class Board:
    def __init__(self):
        # объявляем все клетки поля с помощью генератора списков
        self.board = [(i, j) for i in range (1, 7) for j in range (1, 7)]
        self.ships = []
        self.hid = True
        self.live_ships = 0
        # создаем кортеж областей, который не будет содержать повторяющихся элементов
        self.contour_points = set()

    def add_ship(self, ship):
        self.ship = ship.dots()

        # Проверка размера корабля
        if not 0 < ship.length <= 3:
            raise InvalidShipSizeException(ship.length)

        # Проверка, что корабль не выходит за границы доски
        for dot in self.ship:
            # print(point.x, point.y)
            if dot.x < 1 or dot.x > 6 or dot.y < 1 or dot.y > 6:
                raise BoardOutException(dot.x, dot.y)

        # Проверка, что корабль не пересекался с другими кораблями
        # и не стоит вплотную с другими
        for existing_ship in self.ships:
            existing_ship_dots = existing_ship.dots()
            for dot in self.ship:
                if dot in existing_ship_dots:
                    print(dot)
                    raise OverlapException(f"Cannot add ship. Overlap detected.", dot)
                elif dot in self.contour_points:
                    raise CountourException(dot)


        # Добавление корабля в счетчик кораблей и на доску
        self.live_ships += 1
        self.ships.append(ship)
        # Добавление области вокруг него
        self.contour(ship)

    def out(self, dot):
        # Если точка выходит за пределы поля, метод возвращает True
        return not (0 < dot.x <= 6 and 0 < dot.y <= 6)

    def contour(self, ship):
        # создаем массив соседних точек
        contour_offsets = [(-1, -1), (-1, 0), (-1, 1),
                           (0, -1),           (0, 1),
                           (1, -1),  (1, 0),  (1, 1)]

        for dot in ship.dots():
            for dx, dy in contour_offsets:
                adj_dot = Dot(dot.x + dx, dot.y + dy)
                # добавляем только точки, расположенные внутри доски
                if 0 < adj_dot.x <= 6 and 0 < adj_dot.y <= 6:
                    # добавляем элемент во множество.
                    # если он уже есть в нем, то ничего не добавляется
                    self.contour_points.add(adj_dot)

    def shot(self, dot):
        # Проверка был ли сделан выстрел внутри поля
        if self.out(dot):
            raise BoardOutException(dot.x, dot.y)

        for ship in self.ships:
            if dot in ship:
                print("Hit!")
                ship.remove(dot)
                # Проверка разрушился ли корабль полностью
                if not ship:
                    print("Ship destroyed!")
                    self.ships.remove(ship)
                    self.live_ships -= 1
                return True
        # В случае промаха функция не будет возвращать True и продолжит работу
        # Поэтому дополнительная проверка не нужна
        print("Miss!")
        return False






ship = Ship(3, Dot(3,4), 'horizontal')
ship1 = Ship(1, Dot(1, 1), 'horizontal')
#ship2 = Ship(3, Dot(1, 1), 'horizontal')
# This ship will overlap with ship1
ship3 = Ship(2, Dot(2, 1), 'horizontal')

board = Board()
board.add_ship(ship)
board.add_ship(ship1)
#board.add_ship(ship2)  # No exception, no overlap
board.add_ship(ship3)
# def print board():
# print("  | 1 | 2 | 3| 4 | 5| 6 |")
# print(f"1 | {X[11]}" | {X[12]} | {X[13]} | {X[14]} | {X[15]} | {X[16]} |)
# print(f"2 | {X[21]}" | {X[22]} | {X[23]} | {X[24]} | {X[25]} | {X[26]} |)
# print(f"3 | {X[31]}" | {X[32]} | {X[33]} | {X[34]} | {X[35]} | {X[36]} |)
# print(f"4 | {X[41]}" | {X[42]} | {X[43]} | {X[44]} | {X[45]} | {X[46]} |)
# print(f"5 | {X[51]}" | {X[52]} | {X[53]} | {X[54]} | {X[55]} | {X[56]} |)
# print(f"6 | {X[61]}" | {X[62]} | {X[63]} | {X[64]} | {X[65]} | {X[66]} |)
