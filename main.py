from time import sleep

from src import GameBoard, TerminalInterface


def main():
    t = TerminalInterface()
    game_board = GameBoard(*t.max_board_size, random_=0.4)

    while True:
        t.print_game_board(game_board)
        game_board.update()
        sleep(0.5)


if __name__ == "__main__":
    main()
