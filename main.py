import pygame
from logic import ShipsOnGrid
from graphics import draw
from graphics.draw import ShipsButton, DiagramButton
from plots import show_ships_diagram


def main():
    game_over = False

    computer = None
    human = None

    ships_button = ShipsButton()
    computer_diagram_button = DiagramButton(offset=2)
    human_diagram_button = DiagramButton(offset=17.5)

    draw.draw_grid()
    ships_button.draw_button()
    computer_diagram_button.draw_button()
    human_diagram_button.draw_button()

    # обновление игрового экрана
    pygame.display.update()

    while not game_over:
        # закрывать окно без ошибки
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ships_button.is_hovered():
                    computer = ShipsOnGrid()
                    human = ShipsOnGrid()

                    draw.redraw_field(computer.ships, human.ships)

                elif computer_diagram_button.is_hovered() and computer:
                    show_ships_diagram(computer.ships)

                elif human_diagram_button.is_hovered() and human:
                    show_ships_diagram(human.ships)

        ships_button.redraw()
        computer_diagram_button.redraw()
        human_diagram_button.redraw()

        pygame.display.update()


if __name__ == '__main__':
    main()
    pygame.quit()
