import numpy as np

items = [0, 1, 2, 3, 4, 5, 6, 7, 8]


def get_map_from_id(id, width, height):
    game_map = np.zeros(shape=(width, height))
    for i in range(0, len(id)):
        y = i / height
        x = i % height
        if id[i] in items:
            game_map[y][x] = int(id[i])
        elif id[i] == 'a':
            game_map[y][x] = -2
        elif id[i] == '9':
            game_map[y][x] = -1
    return game_map


def get_id_from_map(game_map):
    result = ""
    for i in range(0, len(game_map)):
        for j in range(0, len(game_map[i])):
            if game_map[i][j] >= 0:
                t = str(game_map[i][j])
                result += t[0]
            elif game_map[i][j] == -1:
                result += "9"
            elif game_map[i][j] == -2:
                result += "a"
    return result
