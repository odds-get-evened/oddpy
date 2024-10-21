import secrets


def roll(arr: list[int], n: int, direction='+') -> list[int]:
    '''
    shift non-zero elements of a buffered list n times, preserving order of items
    :param arr: original list
    :param n: how many times to shift each item
    :param direction: left (-) or right (+)
    :return: shifted list
    '''
    c = []
    c.extend(arr)

    if direction is '+':
        [c.insert(0, c.pop()) for _ in range(n)]
    else:
        [c.append(c.pop(0)) for _ in range(n)]

    return c


def random_roll(arr: list[int], direction='+') -> tuple:
    '''
    shift non-zero elements of a buffered list to a new random starting index, preserving the order of items
    :param arr: original list
    :param direction: left (-) or right (+)
    :return: shifted list, and the start of the shift's index
    '''
    room = len([i for i in arr if i != 0]) + 1
    rand = secrets.choice([_ for _ in range(room)])

    return roll(arr, rand, direction), rand
