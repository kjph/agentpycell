""" Data model for this package
"""

class list2(object):

    def __init__(self, nrow, ncol, init=None):

        self._dim = (nrow, ncol)
        self._array = [[init for c in range(ncol)] for r in range(nrow)]

        self.set_sweep('dr')

    def __iter__(self):
        """ Linear iterator, this goes through the elements
        from top-down then left-right; same as MATLAB.
        """
        
        nrow, ncol = self._dim
        for c in range(ncol):
            for r in range(nrow):
                yield self._array[r][c]

    def __getitem__(self, key):

        return self._array[key]

    def __len__(self):

        return self._dim[0] * self._dim[1]

    def __str__(self):
        s = ''

        # Go right-down
        nrow, ncol = self._dim
        for r in range(nrow):
            for c in range(ncol):
                s += ' {}'.format(str(self._array[r][c]))
            s += '\n'
        
        return s

    @property
    def dim(self):
        return self._dim

    def items(self):

        nrow, ncol = self._dim
        for c in range(ncol):
            for r in range(nrow):
                yield self._array[r][c], (r,c)

    def set_sweep(self, direction):
        """ Sweeping allows you to specify the direction
        of iteration. Note that the default iter/items()
        yields in the 'dr' direction
        
        Directions:
            - dr: start top left, move down then right
            - rd: start top left, move right then down
            - dl: start top right, move down then left
            - ld: start top right, move left then down
            - ul: start bottom right, move up then left
            - lu: start bottom right, move left then up
            - ur: start bottom left, move up then right
            - ru: start bottom left, move right then up
        """

        self._sweep = [None]*len(self)
        nrow, ncol = self._dim
        i = 0

        if direction == 'dr':
            for c in range(ncol):
                for r in range(nrow):
                    self._sweep[i] = (r,c)
                    i += 1
        elif direction == 'rd':
            for r in range(nrow):
                for c in range(ncol):
                    self._sweep[i] = (r,c)
                    i += 1
        elif direction == 'dl':
            for c in reversed(range(ncol)):
                for r in range(nrow):
                    self._sweep[i] = (r,c)
                    i += 1
        elif direction == 'ld':
            for r in range(nrow):
                for c in reversed(range(ncol)):
                    self._sweep[i] = (r,c)
                    i += 1
        elif direction == 'lu':
            for r in reversed(range(nrow)):
                for c in reversed(range(ncol)):
                    self._sweep[i] = (r,c)
                    i += 1
        elif direction == 'ul':
            for c in reversed(range(ncol)):
                for r in reversed(range(nrow)):
                    self._sweep[i] = (r,c)
                    i += 1
        elif direction == 'ur':
            for c in range(ncol):
                for r in reversed(range(nrow)):
                    self._sweep[i] = (r,c)
                    i += 1
        elif direction == 'ru':
            for r in reversed(range(nrow)):
                for c in range(ncol):
                    self._sweep[i] = (r,c)
                    i += 1

    def sweep(self):

        for r, c in self._sweep:
            yield self._array[r][c], (r,c)

    def subset(self, start, nrow, ncol):

        subset = list2(nrow, ncol)
        sr, sc = start

        for c in range(ncol):
            for r in range(nrow):
                subset[r][c] = self._array[r+sr][c+sc]

        return subset