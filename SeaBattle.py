from random import randint

class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Выстрел за пределы доски, повторите выстрел."

class BoardUsedException(BoardException):
    def __str__(self):
        return "Повторный выстрел в эту точку, повторите выстрел."

class BoardWrongShipException(BoardException):
    pass

class Point:
    def __init__(self, x, y) -> None: # конструктор инициализирующий класс
        self.x = x
        self.y = y

    def __eq__(self, object): # Для сравнения экземпляров класса
        return self.x == object.x and self.y == object.y

    def __repr__(self):
        return f"({self.x}, {self.y})"

class Ship:  # описание корабля принимающим в себя набор точек (координат) на игровой доске.
    def __init__(self, nose, length, position): # конструктор инициализирующий класс
        self.nose = nose      #нос коробля
        self.length = length  #длина
        self.position = position # положение, вертикальное 1 или горизонтальное 0
        self.lives = length # количество жизней коробля, равно длине коробля


    @property
    def points(self): # создание списка с точками корабля
        set_points = []
        for i in range(self.length):
            point_x = self.nose.x
            point_y = self.nose.y

            if self.position == 0:
                point_x += i

            elif self.position == 1:
                point_y += i

            set_points.append(Point(point_x, point_y))

        return set_points

    def hit(self, shot): # определение есть ли попадание в корабль
        return shot in self.points

class Board: # класс игровой доски
    def __init__(self, viz=False, size=6):
        self.size = size # размер
        self.viz = viz # видимость
        self.field = [["O"] * size for _ in range(size)] # игровое поле
        self.count = 0
        self.busy = [] # список для растановки короблей и для хранения выстрелов
        self.ships = []

    def __str__(self): # вывод доски на консоль
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.viz: # условие для скрытия короблей если viz = 1
            res = res.replace("■", "O")
        return res

    def out(self, d): # проверка не выходит ли точка за границы поля
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb=False): # описание списка коробля
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.points:
            for dx, dy in near:
                cur = Point(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def add_ship(self, ship): # добавление коробля

        for d in ship.points:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.points:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)


    def shot(self, d): # проверка на попадание и на уничтожение коробля
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.points:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Уничтожил")
                    return False
                else:
                    print("Ранил")
                    return True

        self.field[d.x][d.y] = "."
        print("Промазал")
        return False

    def begin(self): # очищаем список в начале игры
        self.busy = []


class Gamer: # класс описывающий игрока
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class PC(Gamer): # класс описывающий ПК
    def ask(self):
        d = Point(randint(0, 5), randint(0, 5))
        print(f"Ход противника: {d.x + 1} {d.y + 1}")
        return d


class User(Gamer): # класс описывающий пользователя игры
    def ask(self):
        while True:
            cords = input("Ходи: ").split()

            if len(cords) != 2:
                print(" Нужно ввести 2 координаты. ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Нужно ввести числа. ")
                continue

            x, y = int(x), int(y)

            return Point(x - 1, y - 1)


class Game: # класс игры
    def __init__(self, size=6):
        self.size = size
        pl = self.user_board()
        co = self.random_board()
        co.hid = True

        self.ai = PC(co, pl)
        self.us = User(pl, co)

    def user_board(self):
        board = None

        while board is None:
            board = self.user_place()
        return board


    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def in_ship(self, l):
        while True:
            ship_pos = input(f'Введите через пробел кординаты и \nположение для коробля длиной {l}:').split()

            if len(ship_pos) != 3:
                print(" Нужно ввести 3 значения. ")
                continue

            x, y, z = ship_pos

            if not (x.isdigit()) or not (y.isdigit()) or not (z.isdigit()):
                print(" Нужно ввести числа. ")
                continue

            x, y, z = int(x), int(y), int(z)
            break
        return Ship(Point(x - 1, y - 1), l, z)


    def user_place(self):
        lens = [4, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        print("Для установк коробля ведите параметры через пробел:")
        print("1. Номер строки от 1 до 6\n2. Номер столбца от 1 до 6\n3. Положение: 0-вертикально, 1-горизонтально\n")


        for l in lens:
            while True:
                ship = self.in_ship(l)
                try:
                    board.add_ship(ship)
                    print(board)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board



    def random_place(self): # рандомное выставление кораблей
        lens = [4, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Point(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def rules(self): # инструкция
        print("Для выстрела введите через пробел X и Y \n X-строка, Y-столбец")


    def loop(self): # тело игры
        num = 0
        while True:
            print("-" * 20)
            print("Ваша доска:")
            print(self.us.board)
            print("_" * 25)
            print("Доска ПК:")
            print(self.ai.board)
            if num % 2 == 0:
                print("_" * 25)
                repeat = self.us.move()
            else:
                print("_" * 25)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self): # начало игры
        self.rules()
        self.loop()


g = Game()
g.start()