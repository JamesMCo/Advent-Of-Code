import collections

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def euclidian_distance(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5


class World:
    def __init__(self, empty_cell, ddict=False):
        if ddict:
            self.grid = collections.defaultdict(lambda: empty_cell)
        else:
            self.grid = collections.defaultdict(None)
        self.empty_cell = empty_cell
        self.ddict      = ddict
        self.min_x = self.max_x = 0
        self.min_y = self.max_y = 0

    def load_from_lists(self, l, origin=(0, 0), filter_func=None):
        self.grid.clear()
        self.min_x = self.max_x = 0
        self.min_y = self.max_y = 0

        for y, row in enumerate(l):
            for x, col in enumerate(row):
                if filter_func == None or (filter_func and filter_func(col)):
                    self.grid[(x - origin[0], y - origin[1])] = col
                    
                    if x - origin[0] < self.min_x: self.min_x = x - origin[0]
                    if x - origin[0] > self.max_x: self.max_x = x - origin[0]
                    if y - origin[1] < self.min_y: self.min_y = y - origin[1]
                    if y - origin[1] > self.max_y: self.max_y = y - origin[1]

    def load_from_dict(self, d, filter_func=None):
        self.grid.clear()
        self.min_x = self.max_x = 0
        self.min_y = self.max_y = 0

        for x, y in d:
            if filter_func == None or (filter_func and filter_func(v)):
                self.grid[(x, y)] = d[(x, y)]

                if x < self.min_x: self.min_x = x
                if x > self.max_x: self.max_x = x
                if y < self.min_y: self.min_y = y
                if y > self.max_y: self.max_y = y

    def keys(self):
        return self.grid.keys()

    def values(self):
        return self.grid.values()

    def __getitem__(self, key):
        return self.grid[key]

    def in_bounds(self, x, y):
        return self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y

    def __str__(self):
        self.grid.default_factory = None
        s = ""

        for y in range(self.min_y, self.max_y + 1):
            for x in range(self.min_x, self.max_x + 1):
                try:
                    s += self.grid[(x, y)]
                except KeyError:
                    s += self.empty_cell
            s += "\n"

        if self.ddict:
            self.grid.default_factory = lambda: self.empty_cell

        return s