import pygame


# Цвета
SteelBlue = (70, 130, 180)
LightBlue = (145, 179, 242)
White = (255, 255, 255)
LightGrey = (210, 210, 210)

# размер блока
block_size = 40
# левый отспут
left_margin = 140
# верхний отспут
upper_margin = 80

# размер игрового окна
# ширина +30 т.к 2 сетки, в каждой по 10 клеток с пробелами
# 15 т.к одна сетка в высоту
size = (left_margin+30*block_size, upper_margin+15*block_size)


pygame.init()

# поверхность, на которой рисуем
screen = pygame.display.set_mode(size)
# заливка экрана
screen.fill(SteelBlue)
pygame.display.set_caption("Морской бой")

# размер шрифта
font_size = int(block_size / 1.5)
font = pygame.font.SysFont('bart', font_size)


def redraw_field(computer_ships, human_ships):
    # заливка экрана
    screen.fill(SteelBlue)

    draw_grid()
    draw_computer_ships(computer_ships)
    draw_human_ships(human_ships)

    pygame.display.update()


# Рисование кораблей
def draw_ships(ships_coordinates_list, offset=0):
    # Проход по каждому элементу
    for elem in ships_coordinates_list:
        # Начальная точка прямоугольника
        ship = sorted(elem)
        x_start = ship[0][0]
        y_start = ship[0][1]
        # Построение вертикальных кораблей
        # Проверка, что высота больше 1 и изменяются только y
        if len(ship) > 1 and ship[0][0] == ship[1][0]:
            ship_width = block_size
            # Высота длина клетки умноженная на высоту
            ship_height = block_size * len(ship)
        # Иначе строим горизонтальные или одноклеточные корабли
        else:
            ship_width = block_size * len(ship)
            ship_height = block_size
        x = block_size * (x_start - 1) + left_margin
        y = block_size * (y_start - 1) + upper_margin
        # Проверка в какой сетке рисовать 1 - компьютер 2 - человек
        x += offset
        pygame.draw.rect(
            screen, White, ((x, y), (ship_width, ship_height)), width=block_size//10)


def draw_computer_ships(ships):
    draw_ships(ships)


def draw_human_ships(ships):
    draw_ships(ships, 15 * block_size)


def draw_line(k1, k2, k3, k4):
    start_pos = (left_margin + k1*block_size, upper_margin + k2*block_size)
    end_pos = (left_margin + k3*block_size, upper_margin + k4*block_size)
    pygame.draw.line(screen, White, start_pos, end_pos, 1)


# рисование игровой сетки
def draw_grid():
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    # т.к поле 10 на 10 + внешняя граница
    for i in range(11):
        draw_line(0, i, 10, i)
        draw_line(i, 0, i, 10)
        draw_line(15, i, 25, i)
        draw_line(i+15, 0, i+15, 10)

        if i < 10:
            # Написать цифры
            num_ver = font.render(str(i+1), True, White)
            # Написать буквы
            letters_hor = font.render(letters[i], True, White)
            # Ширина
            num_ver_width = num_ver.get_width()
            # Высота
            num_ver_height = num_ver.get_height()
            # Высота совпадает с цифрами
            letters_hor_width = letters_hor.get_width()
            # Вертикальные цифры на 1 сетке
            screen.blit(num_ver, (left_margin - (block_size//2+num_ver_width//2),
                                  upper_margin + i*block_size + (block_size//2 - num_ver_height//2)))
            # Горизонтальные буквы на 1 сетке
            screen.blit(letters_hor, (left_margin + i*block_size + (block_size // 2 - letters_hor_width//2),
                                      upper_margin + 10.3*block_size))
            # Вертикальные цифры на 2 сетке
            screen.blit(num_ver, (left_margin - (block_size//2+num_ver_width//2) + 15 * block_size,
                                  upper_margin + i*block_size + (block_size//2 - num_ver_height//2)))
            # Горизонтальные буквы на 1 сетке
            screen.blit(letters_hor, (left_margin + (i+15)*block_size + (block_size//2 - letters_hor_width//2),
                                      upper_margin + 10.3*block_size))


class Button:
    def __init__(self, x_offset, button_title, color):
        self.__title = button_title
        self.__title_width, self.__title_height = font.size(self.__title)
        self.__button_width = self.__title_width + block_size
        self.__button_height = self.__title_height + block_size
        self.__x_start = x_offset
        self.__y_start = upper_margin + 10 * block_size + self.__button_height
        self.rect_for_draw = self.__x_start, self.__y_start, self.__button_width, self.__button_height
        self.rect = pygame.Rect(self.rect_for_draw)
        self.__rect_for_button_title = self.__x_start + self.__button_width / 2 - \
            self.__title_width / 2, self.__y_start + \
            self.__button_height / 2 - self.__title_height / 2
        self.__color = color
        self.__text_color = SteelBlue

    def draw_button(self, color=None, text_color=None):
        """
        Draws button as a rectangle of color (default is White)
        """
        if not color:
            color = self.__color
        if not text_color:
            text_color = self.__text_color
        pygame.draw.rect(screen, color, self.rect_for_draw)
        text_to_blit = font.render(self.__title, True, text_color)
        screen.blit(text_to_blit, self.__rect_for_button_title)

    def is_hovered(self):
        mouse_position = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_position):
            return True

        return False

    def redraw(self):
        if self.is_hovered():
            self.draw_button()
        else:
            self.draw_button(color=LightBlue, text_color=White)


class ShipsButton(Button):
    def __init__(self, offset=10):
        self.offset = left_margin + offset * block_size
        self.title = "Построить корабли"
        self.color = White
        self.hover_color = LightBlue

        super().__init__(self.offset, self.title, self.color)


class DiagramButton(Button):
    def __init__(self, offset=2):
        self.offset = left_margin + offset * block_size
        self.title = "Показать диаграмму"
        self.color = White
        self.hover_color = LightBlue

        super().__init__(self.offset, self.title, self.color)
