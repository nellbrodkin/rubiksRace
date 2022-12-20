import math
import random


def setup_indices(size):
    indices = {i: [] for i in range(size ** 2)}

    for i in range(size ** 2):
        # set adjacent neighbors
        if i != 0:
            indices[i].append(i - 1)
            indices[i - 1].append(i)

        # set vertically adjacent neighbors
        if i / (size - 1) > 1:
            indices[i].append(i - size)
            indices[i - size].append(i)

    return indices


class Tile:
    def __init__(self, color):
        self.color = color
        self.x = 0
        self.y = 0

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        return (self.x, self.y)

    def get_color(self):
        return self.color

    def is_empty(self):
        return self.color == 'black'


class Board:
    def __init__(self, size=5):
        self.size = size
        colors = ['red', 'orange', 'yellow', 'green', 'blue', 'white']
        self.board = [Tile(i) for i in colors * (size - 1)] + [Tile('black')]
        self.indices = setup_indices(size)
        self.shuffle()

    def __str__(self):
        s = ''
        for i in range(len(self.board)):
            if self.board[i].get_color() == 'black':
                s += '  '
            else:
                s += self.board[i].get_color()[0] + ' '
            if i % self.size == self.size - 1:
                s += '\n'

        return s

    def get_color(self, index):
        return self.board[index].get_color()

    def get_empty_index(self):
        for i in range(len(self.board)):
            if self.board[i].is_empty():
                return i
        return None

    def update(self, index):
        empty_index = self.get_empty_index()
        if self.is_move(index):
            if empty_index in self.indices[index]:
                self.swap(empty_index, index)
            else:
                self.move_row(index)

    def shuffle(self, moves=100):
        for i in range(moves):
            empty_index = self.get_empty_index()
            index = random.choice(self.indices[empty_index])
            self.update(index)

    def get_interior_tiles(self):
        b = []
        for i in range(len(self.board)):
            if i // self.size != 0 and i // self.size != self.size - 1:
                if i % self.size != 0 and i % self.size != self.size - 1:
                    b.append(self.board[i])
        return b

    def move_row(self, tile_index):
        row = []
        empty_index = self.get_empty_index()
        start = min(tile_index, empty_index)
        end = max(tile_index, empty_index)
        backwards = True
        if start == empty_index:
            backwards = False
        if (end - start) < self.size:
            row = [i for i in range(start, end+1)]
        else:
            row = [i for i in range(start, end+1, self.size)]
        if backwards:
            for i in reversed(range(len(row) - 1)):
                self.swap(row[i], row[i - 1])
        else:
            for i in range(len(row)-1):
                self.swap(row[i], row[i+1])


    def swap(self, index1, index2):
        self.board[index1], self.board[index2] = self.board[index2], self.board[index1]

    def is_move(self, index):
        empty_space = self.get_empty_index()
        if index in self.indices:
            # if in same row
            if index // self.size == empty_space // self.size:
                return True
            # if in same column
            elif index % self.size == empty_space % self.size:
                return True
        return False

    def __eq__(self, other):
        tiles1 = self.get_interior_tiles()
        tiles2 = other.get_interior_tiles()
        for i in range(len(tiles1)):
            if tiles1[i].get_color() != tiles2[i].get_color():
                return False
        return True



class Reference(Board):
    def __init__(self, size=5):
        super().__init__(size)
        self.shuffle()

    def shuffle(self, moves=100):
        super().shuffle(moves)
        interior = self.get_interior_tiles()
        for tile in interior:
            if tile.get_color() == 'black':
                empty_index = self.get_empty_index()
                self.swap(empty_index, 0)

    def __str__(self):
        s = ''
        tiles = self.get_interior_tiles()
        size = math.sqrt(len(tiles))
        for i in range(len(tiles)):
            s += tiles[i].get_color()[0] + ' '
            if i % size == size - 1:
                s += '\n'
        return s


if __name__ == '__main__':
    running = True

    board = Board()
    reference = Reference()

    while running:

        print('-----------board-----------')
        print(board)
        print('-----------reference-----------')
        print(reference)

        move = input('choose index to move (0-24):')
        board.update(int(move))

        if board.get_interior_tiles() == reference.get_interior_tiles():
            running = False
            print('congratulations! you won!')
