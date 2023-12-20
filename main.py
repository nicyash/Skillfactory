game_list = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']] # список для хранения значений ходов

def print_list(g_list): #вывод в консоль поля игры
    print(' ', 0, 1, 2)
    for i in range(3):
        print(i, *g_list[i])

def equals_(a, b, c, p): # проверка на равенство значений в списке и кто ходил
    if a == b:
        if b == c:
            if c == p:
                return True
    else:
        return False
def win_player(g_list, p): #проверка не выиграл ли кто ни-будь
    if (equals_(g_list[0][0], g_list[1][0], g_list[2][0], p) or equals_(g_list[0][1], g_list[1][1], g_list[2][1], p) or
            equals_(g_list[0][2], g_list[1][2], g_list[2][2], p) or equals_(g_list[0][0], g_list[0][1], g_list[0][2], p) or
            equals_(g_list[1][0], g_list[1][1], g_list[1][2], p) or equals_(g_list[2][0], g_list[2][1], g_list[2][2], p) or
            equals_(g_list[0][0], g_list[1][1], g_list[2][2], p) or equals_(g_list[0][2], g_list[1][1], g_list[2][0], p)):
        print('Игрок 1 победил!' if p == 'x' else 'Игрок 2 победил!')
        print('Игра окончена.')
        return True

print_list(game_list)
p1, p2 = 'x', 'o'
print('''Инструкция: игрок вводит координату по горизонтали и нажимает Enter, 
         далее вводит координату по вертикалии и нажимает Enter, после другой
         игрок вводит координаты аналогично. \n Игра началась!!!''')
while True: # цикл основной программы, если кто то победит цикл прерветься
    while True: # в цикле проверяется не выходит ли за границы поля введенные координаты и не занята ли клетка для игрока 1
        x, y = int(input('Игрок 1, сделайте ход: ')), int(input())
        if 0 <= x <= 2 and 0 <= y <= 2:
            if game_list[y][x] == '-':
                game_list[y][x] = p1
                break
            else:
                print('Клетка занята, выбери другую!')
        else:
            print('Неправильнный ввод координат, введите еще раз правильно!')

    print_list(game_list)
    if win_player(game_list, p1):
        break
    if '-' not in game_list[0] and '-' not in game_list[1] and '-' not in game_list[2]: # проверка не закончились ли пустые клетки
        print('Победила дружба!!! \n Игра окончена!')
        break
    while True: # в цикле проверяется не выходит ли за границы поля введенные координаты и не занята ли клетка для игрока 2
        x, y = int(input('Игрок 2, сделайте ход: ')), int(input())
        if 0 <= x <= 2 and 0 <= y <= 2:
            if game_list[y][x] == '-':
                game_list[y][x] = p2
                break
            else:
                print('Клетка занята, выбери другую!')
        else:
            print('Неправильнный ввод координат, введите еще раз правильно!')
    print_list(game_list)
    if win_player(game_list, p2):
        break
