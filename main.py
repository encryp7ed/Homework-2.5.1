class BoardException(Exception):
    pass


# Ошибка выхода за пределы поля
class BoardOutException(BoardException):
    def __init__(self, x, y):
        # self.coordinate = (x, y)
        super().__init__(f"Incorrect coordinates: ({x}, {y})")


# Ошибка перекрытия ячеек
# Возникает, когда игрок пытается выбрать уже открытую ячейку
# Или заполнить ячейку, которая уже содержит часть коробля
class InvalidMoveException(BoardException):
    def __init__(self, x, y):
        self.coordinate = (x, y)
        super().__init__(f"You have already selected this cell: {self.coordinate}")


# Ошибка неверного размера корабля
class InvalidShipSizeException(BoardException):
    def __init__(self, length):
        self.length = length
        super().__init__(f"Incorrect ship length: {self.length}")


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

    def add_ship(self, ship):
        self.ship_size = ship.dots()

        # Проверка, что корабль не выходит за границы доски
        for point in self.ship_size:
            # print(point.x, point.y)
            if point.x < 1 or point.x > 6 or point.y < 1 or point.y > 6:
                raise BoardOutException

        # Проверка, что корабль не пересекался с другими кораблями


        # Добавление корабля на доску
        self.live_ships += 1

    def out(self, dot):
        # Если точка выходит за пределы поля, метод возвращает True
        return not (0 < dot.x <= 6 and 0 < dot.y <= 6)

    def shot(self, dot):
        if self.out(dot):
            raise BoardOutException
        # else:






ship = Ship(3, Dot(3,4), 'horizontal')
board = Board()
board.add_ship(ship)
# def print board():
# print("  | 1 | 2 | 3| 4 | 5| 6 |")
# print(f"1 | {X[11]}" | {X[12]} | {X[13]} | {X[14]} | {X[15]} | {X[16]} |)
# print(f"2 | {X[21]}" | {X[22]} | {X[23]} | {X[24]} | {X[25]} | {X[26]} |)
# print(f"3 | {X[31]}" | {X[32]} | {X[33]} | {X[34]} | {X[35]} | {X[36]} |)
# print(f"4 | {X[41]}" | {X[42]} | {X[43]} | {X[44]} | {X[45]} | {X[46]} |)
# print(f"5 | {X[51]}" | {X[52]} | {X[53]} | {X[54]} | {X[55]} | {X[56]} |)
# print(f"6 | {X[61]}" | {X[62]} | {X[63]} | {X[64]} | {X[65]} | {X[66]} |)
