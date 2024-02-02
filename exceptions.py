class BoardException(Exception):
    pass


# Ошибка выхода за пределы поля
class BoardOutException(BoardException):
    def __init__(self, x, y):
        super().__init__(f"Incorrect coordinates: ({x}, {y})")


''' Ошибка перекрытия ячеек
Возникает, когда игрок пытается выбрать уже открытую ячейку
Или заполнить ячейку, которая уже содержит часть корабля'''
class OverlapException(BoardException):
    # добавляем отдельную переменную для сообщения, поскольку
    # это исключение может возникнуть и при постановке корабля и при выстреле
    def __init__(self, message, dot):
        super().__init__(message, f"You have already selected this cell: {dot}")


# Ошибка близкого размещения кораблей
class CountourException(BoardException):
    def __init__(self, dot):
        super().__init__(f"Cannot place a ship adjacent to another ship at {dot}")


# Ошибка неверного направления
class DirectionException(BoardException):
    def __init__(self, direction):
        super().__init__(f"Incorrect direction: {direction}")
