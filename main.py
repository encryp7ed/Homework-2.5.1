import random
from exceptions import BoardOutException, CountourException, OverlapException, BoardException
from settings import Dot, Board, Ship


# Описание возможностей игроков
class Player:
    def __init__(self, name):
        self.name = name
        self.board = Board()
        self.enemy_board = Board()

    def ask(self):
        pass

    def move(self):
        # Запрашиваем ход игрока, пока он не промахнется
        while True:
            try:
                target = self.ask()
                # Метод shot возвращает True или False, поэтому используем его для цикла
                result = self.enemy_board.shot(target)
                return result  # Если игрок попал по цели, цикл повторяется
            except BoardOutException as e:
                print(f'Error: {e}')
            except OverlapException as e:
                print(f'Error: {e}')


class AI(Player):
    def __init__(self):
        super().__init__('AI')  # Установка имени игрока

    def ask(self):
        # генерируем случайные координаты
        x = random.randint(1, 6)
        y = random.randint(1, 6)
        return Dot(x, y)


class User(Player):
    def __init__(self):
        super().__init__('User')

    def ask(self):
        coordinates = input('Your turn. Enter the coordinates (column row): ')
        x, y = map(int, coordinates.split())
        return Dot(x, y)


class Game:
    ship_lengths = [3, 2, 2, 1, 1, 1, 1]

    def __init__(self):
        self.user = User()
        self.user_board = self.user.board
        self.ai = AI()
        self.ai_board = self.ai.board
        # Установка вражеских досок
        self.user.enemy_board = self.ai.board
        self.ai.enemy_board = self.user.board

        self.players = [self.user, self.ai]  # Создание списка игроков

    def random_board(self, board):
        max_attempts = 10000  # Накладываем ограничение, чтобы избежать бесконечного цикла

        while True:  # Цикл для перезапуска генерации доски
            try:
                for ship_length in self.ship_lengths:
                    attempts = 0  # Счетчик попыток установить текущий корабль
                    placed = False  # Флаг, указывающий, размещен ли корабль

                    while not placed and attempts < max_attempts:
                        # Выбираем случайное направление корабля
                        direction = random.choice(['h', 'v'])

                        if direction == 'h':
                            # выбираем случайную начальную позицию для корабля
                            start_x = random.randint(1, 7 - ship_length)
                            start_y = random.randint(1, 6)

                            # Создаем корабль
                            ship = Ship(ship_length, Dot(start_x, start_y), direction)

                            try:
                                # Пытаемся добавить корабль на доску
                                board.add_ship(ship)
                            except (BoardOutException, OverlapException, CountourException):
                                attempts += 1  # Увеличиваем счетчик попыток
                            else:
                                placed = True  # Корабль успешно поставлен
                        else:  # direction == 'vertical'
                            start_x = random.randint(1, 6)
                            start_y = random.randint(1, 7 - ship_length)

                            ship = Ship(ship_length, Dot(start_x, start_y), direction)

                            try:
                                board.add_ship(ship)
                            except (BoardOutException, OverlapException, CountourException):
                                attempts += 1
                            else:
                                placed = True
                    if attempts == max_attempts:
                        raise Exception('Failed generation attempt. Try again.')
                return board
            except Exception as e:
                print(f'An error occurred: {e}')
                retry = input('Do you want to retry? (y/n): ')
                if retry.lower() != 'y':
                    raise BoardException('Board generation cancelled by user.')
                self.user_board.reset_board()
                self.ai_board.reset_board()  # Обнуление доски ИИ

    @staticmethod
    def greet():  # Сообщение правил игры и ввода
        print('Welcome to Battleship game!\n'
              'The rules of the game:\n'
              '1) Each player has the following number of ships: '
              '1 ship per 3 cells, 2 ships per 2 cells, 4 ships per one cell.\n'
              '2) The playing board is 6x6 in size.\n'
              '3) To install the ship on the board, use the following format:\n'
              'column_number row_number direction(h/v)\n'
              'directions: horizontal (h) and vertical (v)\n'
              'For Example: 4 2 h\n'
              "The ship's size is entered automatically from larger to smaller"
              '4) Each ship must be at least one cell away from the other ships.\n'
              '5) To make a shot, enter the coordinates: column number and row number.\n'
              'For Example: 5 1\n'
              '6) The letter X marks downed ships, the letter T marks misses.\n'
              '7) If you hit an enemy ship, you continue your turn.\n'
              '8) The winner is the first one who sinks all enemy ships.\n'
              )

    def loop(self):
        self.random_board(self.ai_board)  # Размещение кораблей для ИИ

        while True:
            for player in self.players:  # цикл по всем игрокам
                print(f"Player {player.name}'s move.")
                hit = True
                while hit:
                    hit = player.move()  # hit = False если игрок промахнется
                    if player.name == 'AI':  # Выводим выстрел по вражеской доске пользователем
                        # Выводим выстрелы, сделанные по доске пользователя
                        print('Your board:\n', self.user_board.print_board(hid=False))
                    else:
                        print('Enemy board:\n', self.ai_board.print_board(hid=True))

                    if player.enemy_board.live_ships == 0:  # Проверка условия победы
                        print(f'Player {player.name} won!')
                        return  # Завершение игры, если победитель найден

    def user_place_ships(self):
        print(self.user_board.print_board())  # Вывод доски перед началом игры для наглядности
        print('Place your ships on the board.')
        for ship_size in self.ship_lengths:
            while True:
                try:
                    coordinates = input(f'Enter the start coordinates for a ship of the size {ship_size} '
                                        f'and its direction (vertical/horizontal): ')
                    x, y, direction = coordinates.split()
                    direction = direction.lower()
                    ship = Ship(ship_size, Dot(int(x), int(y)), direction)  # Разделяем введенные данные по переменным
                    self.user.board.add_ship(ship)
                    print("\n", self.user_board.print_board())  # Вывод доски после постановки каждого корабля
                    break
                except (BoardOutException, OverlapException, CountourException) as e:
                    print(f'An error in the placement of the ship: {e}. Try again.')

    def start(self):
        self.greet()
        # self.user_place_ships()  # Пользователь размещает корабли
        while True:  # Цикл для повторения игры
            self.random_board(self.user_board)
            self.loop()
            play_again = input('Do you want to play again? (y/n): ')
            if play_again.lower() != 'y':
                break  # Выход из цикла, если пользователь не хочет играть снова
            self.user.board.reset_board()
            self.ai.board.reset_board()
            self.user_place_ships()  # Повторная расстановка кораблей от пользователя


new_game = Game()
new_game.start()
