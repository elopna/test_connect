import numpy as np
from sys import exit

field_size = (6, 7)
state = np.full(field_size, " ")


def maybe_positions(position: tuple[int, int]) -> list[tuple[int, int]]:
    """
    Возврат возможных успешных позиций для первой точки.
    Возвращает список из 4 позиция (справа, справа-сверху, сверху, слева-сверху)
    """
    new_positions = []
    next_row = position[0] - 1
    next_col = position[1] + 1
    prev_col = position[1] - 1
    if next_row >= 0:
        new_positions.append([next_row, position[1]])
        if prev_col >= 0:
            new_positions.append([next_row, prev_col])
        if next_col <= field_size[1]:
            new_positions.append([next_row, next_col])
            new_positions.append([position[0], next_col])
    return new_positions


def check_player_position(player: str, position: tuple[int, int]):
    """
    Проверка, что данный игрок есть в данной позиции

    Args:
        player: str - игрок
        position: проверяемая позиция
    """
    # player = str(player)
    row = position[0]
    column = position[1]
    if state[row][column] == player:
        return True


def maybe_direct_position(position1: tuple[int, int], position2: tuple[int, int]) -> tuple[int, int]:
    """Возврат третьей точки по направлению предыдущих двух

    Args:
        position1: tuple[int, int] - позиция первой точки
        position2: tuple[int, int] - позиция второй точки

    Return:
        третья точка, продолжающая 2 переданные
    """
    if (position2[1] - position1[1] != 0) and (position2[0] - position1[0] != 0):
        if (position2[1] - position1[1] == 0):
            return [position2[0] - 1, position2[1] + 1]
        else:
            return [position2[0] - 1, position2[1] + 1]
    if (position2[0] - position1[0] != 0) and (position2[1] - position1[1] == 0):
            return [position2[0] - 1, position2[1]]
    if (position2[0] - position1[0] == 0) and (position2[1] - position1[1] != 0):
            return [position2[0], position2[1] + 1]

def search_winner(player: bool) -> bool:
    """Проверка пользователя на факт его победы
    
    Args:
        player: bool - игрок
        
    Returns:
        True если игрок выиграл
        False если нет
    """
    player = str(int(player))
    player_max_score = 0
    for column_num, column in enumerate(state[::-1]):
        column_num = field_size[0] - 1 - column_num
        for row_num, el in enumerate(column):
            if el == player:
                player_max_score += 1
                start_position = (column_num, row_num)
                for position in maybe_positions(start_position):
                    if check_player_position(player, position):
                        player_max_score += 1
                        new_position = maybe_direct_position(start_position, position)
                        if check_player_position(player, new_position):
                            player_max_score += 1
                            new_position = maybe_direct_position(start_position, new_position)
                            if check_player_position(player, new_position):
                                game_is_active = False
                                print(f"!!! Игрок {int(player) + 1} победил !!!")
                                return True, game_is_active
    game_is_active = True
    return False, game_is_active

def new_state(player: bool, column: int):
    """
    Обновление после очередного хода

    Args:
        player: bool - игрок
        column: int - ход
    """
    new_column: int = column - 1
    for index, row in enumerate(state[::-1]):
        if row[new_column] != " ":
            continue
        else:
            row[new_column] = int(player)
            print(state)
            print()
            break

def check_input(line, player):
    """
    Проверка введенного значения
    """
    if line.lower() == "stop":
        print("Стоп-игра!")
        exit()
    elif (not line.isdigit()) or (int(line) <= 0) or (int(line) > field_size[1]):
        return 0
    else:
        return int(line)

def run():
    """
    Ход, обновление поля, поиск победителя
    """
    game_is_active = True
    player = False
    while game_is_active:
        current_turn = make_turn(player)
        new_state(player, current_turn)
        is_winner, game_is_active = search_winner(player)
        player = not player

def make_turn(player):
    """
    Ход и проверка введенного значения

    Args:
    player: bool - игрок
    """
    a = 0
    while a == 0:
        a = input(f"Игрок {int(player) + 1}, Ваш ход (1-{field_size[1]}): ")
        a = check_input(a, player)
    return a

run()