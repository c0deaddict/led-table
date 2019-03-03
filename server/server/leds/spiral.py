# Spiral with the clock, starting right.
def calc_spiral_coords(size):
    result = dict()

    def emit(i, x, y):
        result[(x + size, y + size)] = i

    def enum_spiral(offset, n):
        if n == 0:
            emit(offset, 0, 0)
            enum_spiral(offset + 1, n + 1)
        elif n <= size:
            x = n
            y = n - 1
            i = offset
            emit(i, x, y)
            for j in range(0, 2 * n - 1):
                y = y - 1
                i = i + 1
                emit(i, x, y)
            for j in range(0, 2 * n):
                x = x - 1
                i = i + 1
                emit(i, x, y)
            for j in range(0, 2 * n):
                y = y + 1
                i = i + 1
                emit(i, x, y)
            for j in range(0, 2 * n):
                x = x + 1
                i = i + 1
                emit(i, x, y)

            enum_spiral(i + 1, n + 1)

    enum_spiral(0, 0)
    return result
