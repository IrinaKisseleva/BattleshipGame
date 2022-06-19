import random


# Постройка кораблей
class ShipsOnGrid:
    def __init__(self):
        # Хранение свободных клеток
        # Помещаем все клетки
        self.available_blocks = set((a, b)
                                    for a in range(1, 11) for b in range(1, 11))
        # Хранение координат клеток, которые заняты под корабли
        self.ships_set = set()
        # Список всех кораблей
        self.ships = self.populate_grid()

    def get_ships(self):
        return self.ships

    # Вектор создания корабля
    def create_start_block(self, available_blocks):
        # 0 - горизонтальный 1 - вертикальный
        x_or_y = random.randint(0, 1)
        # -1 - в обратном направлении
        str_rev = random.choice((-1, 1))
        # выбираем случайную свободную клетку
        x, y = random.choice(tuple(available_blocks))
        return x, y, x_or_y, str_rev

    # Создаёт 1 корабль
    def create_ship(self, number_of_blocks, available_blocks):
        ship_coordinates = []
        x, y, x_or_y, str_rev = self.create_start_block(available_blocks)
        # Проход по всем клеткам
        for _ in range(number_of_blocks):
            ship_coordinates.append((x, y))
            # Проверка, что не вышло за пределы сетки
            if not x_or_y:
                str_rev, x = self.add_block_to_ship(
                    x, str_rev, x_or_y, ship_coordinates)
            else:
                str_rev, y = self.add_block_to_ship(
                    y, str_rev, x_or_y, ship_coordinates)
        # Проверка, правильный ли корабль
        if self.is_ship_valid(ship_coordinates):
            return ship_coordinates
        return self.create_ship(number_of_blocks, available_blocks)

    def add_block_to_ship(self, coor, str_rev, x_or_y, ship_coordinates):
        # если выходим за рамки сетки, то меняем направление
        if (coor <= 1 and str_rev == -1) or (coor >= 10 and str_rev == 1):
            str_rev *= -1
            return str_rev, ship_coordinates[0][x_or_y] + str_rev
        else:
            return str_rev, ship_coordinates[-1][x_or_y] + str_rev

    def is_ship_valid(self, new_ship):
        ship = set(new_ship)
        # Входит ли корабль в множество свободных клеток
        return ship.issubset(self.available_blocks)

    #  Добавить координаты нового корабля
    def add_new_ship_to_set(self, new_ship):
        for elem in new_ship:
            self.ships_set.add(elem)

    # Удаление всех клеток вокруг корабля из свободнх клеток
    def update_available_blocks_for_creating_ships(self, new_ship):
        for elem in new_ship:
            for k in range(-1, 2):
                for m in range(-1, 2):
                    # Проверка, что нет выхода за пределы сетки
                    if 0 < (elem[0]+k) < 11 and 0 < (elem[1]+m) < 11:
                        self.available_blocks.discard((elem[0]+k, elem[1]+m))

    #  Список со списками кораблей
    def populate_grid(self):
        # Список из координат всех кораблей
        ships_coordinates_list = []
        # Количество кораблей обратно пропорционально длине корабля
        #  Цикл по длине корабля
        for number_of_blocks in range(4, 0, -1):
            # Цикл по количеству кораблей
            for _ in range(5-number_of_blocks):
                new_ship = self.create_ship(
                    number_of_blocks, self.available_blocks)
                # Добавление корабля в общий список всех кораблей
                ships_coordinates_list.append(new_ship)
                # Добавление клеток в занятые
                self.add_new_ship_to_set(new_ship)
                # Обновление списка свободных клеток
                self.update_available_blocks_for_creating_ships(new_ship)
        return ships_coordinates_list


if __name__ == '__main__':
    placement = ShipsOnGrid()

    # заполение двумерного массива 1 - x 2 - y
    matrix = [[0] * 10 for _ in range(10)]
    for ship in placement.ships:
        # нахождение кординат кораблей
        for i in range(len(ship)):
            x = ship[i][0] - 1
            y = ship[i][1] - 1
            matrix[x][y] = 1

    # записываем данные в файл
    with open('ships.txt', 'w') as f:
        _str = ''
        for i in range(10):
            _str += ' '.join(map(str, matrix[i])) + '\n'
        f.write(_str)
