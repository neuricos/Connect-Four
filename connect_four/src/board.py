from enum import Enum, unique

@unique
class Color(Enum):
    RED = 'R'
    YELLOW = 'Y'
    EMPTY = ' '

    def __str__(self):
        return self.value


class IllegalMoveException(Exception):
    pass


class IllegalOperationException(Exception):
    pass


class UndefinedColorException(Exception):
    pass


class Board:
    def __init__(self):
        self.nrow = 6
        self.ncol = 7
        self.connect = 4
        self.game_over = False
        self.winner = None
        self.board = [Color.EMPTY for _ in range(self.nrow * self.ncol)]
        self.col_height = [0] * self.ncol

    def getGridIndex(self, row_index, col_index):
        return row_index * self.nrow + col_index

    def getGrid(self, row_index, col_index):
        return self.board[self.getGridIndex(row_index, col_index)]

    def put(self, color, col):
        assert(col >= 0 and col < self.ncol)

        if color is not Color.RED and color is not Color.YELLOW:
            return UndefinedColorException

        if self.col_height[col] + 1 > self.nrow:
            raise IllegalMoveException

        row = self.col_height[col]
        self.board[self.getGridIndex(row, col)] = color
        self.col_height[col] += 1

        # Check if the game is over
        self.checkHorizontal(row, col)
        self.checkVertical(row, col)
        self.checkUpperRight(row, col)
        self.checkBottomRight(row, col)

    def gameOver(self):
        return self.game_over

    def getWinner(self):
        if self.winner is None:
            raise IllegalOperationException
        return self.winner

    def validIndex(self, row_index, col_index):
        if row_index < 0 or row_index >= self.nrow or col_index < 0 or col_index >= self.ncol:
            return False
        return True

    def checkHorizontal(self, row_index, col_index):
        r_start = row_index - self.connect + 1
        for r in range(r_start, row_index + 1):
            if not self.validIndex(r, col_index):
                continue
            color = self.getGrid(r, col_index)
            if color == Color.EMPTY:
                continue
            connected = True
            for i in range(1, self.connect):
                if not self.validIndex(r + i, col_index) or self.getGrid(r + i, col_index) != color:
                    connected = False
                    break
            if connected:
                self.game_over = True
                self.winner = color
                return

    def checkVertical(self, row_index, col_index):
        c_start = col_index - self.connect + 1
        for c in range(c_start, col_index + 1):
            if not self.validIndex(row_index, c):
                continue
            color = self.getGrid(row_index, c)
            if color == Color.EMPTY:
                continue
            connected = True
            for j in range(1, self.connect):
                if not self.validIndex(row_index, c + j) or self.getGrid(row_index, c + j) != color:
                    connected = False
                    break
            if connected:
                self.game_over = True
                self.winner = color
                return

    def checkUpperRight(self, row_index, col_index):
        r_bound = self.nrow - self.connect  # <= r_bound
        c_bound = self.ncol - self.connect  # <= c_bound
        r_start = row_index - (self.connect - 1)
        c_start = col_index - (self.connect - 1)
        for k in range(self.connect):
            r = r_start + k
            c = c_start + k
            if not self.validIndex(r, c):
                continue
            if r > r_bound or c > c_bound:
                return
            color = self.getGrid(r, c)
            if color == Color.EMPTY:
                continue
            connected = True
            for m in range(1, self.connect):
                if not self.validIndex(r + m, c + m) or self.getGrid(r + m, c + m) != color:
                    connected = False
                    break
            if connected:
                self.game_over = True
                self.winner = color
                return

    def checkBottomRight(self, row_index, col_index):
        r_bound = self.connect - 1  # >= r_bound
        c_bound = self.ncol - self.connect  # <= c_bound
        r_start = row_index + (self.connect - 1)
        c_start = col_index - (self.connect - 1)
        for k in range(self.connect):
            r = r_start - k
            c = c_start + k
            if not self.validIndex(r, c):
                continue
            if r < r_bound or c > c_bound:
                return
            color = self.getGrid(r, c)
            if color == Color.EMPTY:
                continue
            connected = True
            for m in range(1, self.connect):
                if not self.validIndex(r - m, c + m) or self.getGrid(r - m, c + m) != color:
                    connected = False
                    break
            if connected:
                self.game_over = True
                self.winner = color
                return

    def __str__(self):
        s = ""
        for r in reversed(range(self.nrow)):
            for c in range(self.ncol):
                v = self.getGrid(r, c)
                s += f"[{v}]"
            s += "\n"
        return s
