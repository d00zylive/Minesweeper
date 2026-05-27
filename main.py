import random

class Cell():
    x: int
    y: int
    value: int|None #0-8 or -1 for mine
    flagged: bool
    mined: bool

    def __init__(self, x: int, y: int, flagged:bool = False, mined:bool = False, value:int|None = None):
        self.x = x
        self.y = y
        self.value = value
        self.flagged = flagged
        self.mined = mined

    def __repr__(self):
        return f"Cell(x={self.x},y={self.y},value={self.value},flagged={self.flagged}, mined={self.mined})"
    
    def __str__(self):
        if self.mined:
            if self.value == -1:
                return "@"
            return str(self.value)
        elif self.flagged:
            return "F"
        else:
            return "#"

def initialiseGrid(width:int, height:int, mines:int) -> list[list[Cell]]:
    if mines > width*height:
        raise ValueError("More mines than cells")

    grid = [[Cell(x=x, y=y) for y in range(height)] for x in range(width)]

    for _ in range(mines):
            cell = grid[random.randint(0,width-1)][random.randint(0,height-1)]
            if cell.value == None:
                cell.value = -1

    return grid

def printGrid(grid:list[list[Cell]]) -> None:
    for column in grid:
        for cell in column:
            print(str(cell), end="")
        print()

printGrid(initialiseGrid(width=10, height=10, mines=10))