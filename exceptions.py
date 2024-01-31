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
