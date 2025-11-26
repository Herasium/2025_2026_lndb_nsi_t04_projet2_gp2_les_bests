
from arcade import Vec2
from modules.data import data

class _Mouse():

    def __init__(self):
        
        self._x = 0
        self._y = 0
        self._cursor = (0,0)
        self._position = (0,0)

        self.history = []
        self.direction = "RIGHT"
        self.previous_direction = "RIGHT"

        self.direction_bias = 0

        self._grid_size = data.UI_EDITOR_GRID_SIZE

    def _calculate_cursor(self):
        self._cursor = Vec2(round(self._x / self._grid_size)*self._grid_size,round(self._y / self._grid_size)*self._grid_size)
  

    def _calculate_direction(self):
        if len(self.history) > 4:
            self.history.pop(0)
            self.history.append(self.cursor)

            x1, y1 = self.history[0]
            x2, y2 = self.history[-1]

            dx = x2 - x1
            dy = y2 - y1

            self.previous_direction = self.direction

            if self.previous_direction == "RIGHT":
                dx += self.direction_bias
            if self.previous_direction == "LEFT":
                dx -= self.direction_bias

            if self.previous_direction == "UP":
                dy += self.direction_bias
            if self.previous_direction == "DOWN":
                dy -= self.direction_bias

            if abs(dx) >= abs(dy):
                self.direction = "RIGHT" if dx > 0 else "LEFT"
            else:
                self.direction =  "UP" if dy > 0 else "DOWN"

        else:
            self.history.append(self.cursor)



    @property
    def position(self):
        return self._position

    @position.setter
    def position(self,value):
        self._position = value
        self._x = self._position[0]
        self._y = self._position[1]
        self._calculate_cursor()
        self._calculate_direction()
        return self._position

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def cursor(self):
        return self._cursor
    
    @property
    def grid_size(self):
        return self._grid_size

    @grid_size.setter
    def grid_size(self,value):
        self._grid_size = value
        self._calculate_cursor()

mouse = _Mouse()