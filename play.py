import numpy as np

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
        new_positions.append([[next_row, position[1]]])
        if prev_col >= 0:
            new_positions.append([[next_row, prev_col]])
        if next_col <= field_size[1]:
            new_positions.append([[next_row, next_col]])
            new_positions.append([[position[0], next_col]])
    return new_positions


def check_player_position(player: str, position: tuple[int, int]):
    """
    Проверка, что данный игрок есть в данной позиции

    Args:
        player: str - игрок
        position: проверяемая позиция
    """
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
        третья точка
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

def search_winner(player: str) -> bool:
    """Проверка пользователя на факт его победы
    
    Args:
        player: str - игрок
        
    Returns:
        True если игрок выиграл
        False если нет
    """
    player_max_score = 0
    for column_num, column in enumerate(state[::-1]):
        column_num = 5 - column_num
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
                            new_position = maybe_direct_position(start_position, position)
                            if check_player_position(player, new_position):
                                return True
    return False

def new_state(player: int, column: int):
    """
    Обновление после ввода
    """
    new_column: int = column - 1
    for index, row in enumerate(state[::-1]):
        if row[new_column] != " ":
            continue
        else:
            row[new_column] = player
            print(state)
            break


# a = input(f"Игрок 1, Ваш ход (1-{field_size[1]})")

# if a < 0 or a > field_size[1]:
#     a = input(f"Игрок 1, еще раз (1-{field_size[1]})")

def run(player, column):
    """
    Обновление хода - обновляем текущее состояние поля и ищем победителя
    """
    new_state(player, column)
    is_winner = search_winner(player)

# b = input(f"Игрок 2, Ваш ход (1-{field_size[1]})")

            

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--player_number", dest="player_number", help="player_number")
    parser.add_argument("--column_number", dest="column_number", help="column_number path")
    args = parser.parse_args()


    run(args.player_number, args.column_number)
