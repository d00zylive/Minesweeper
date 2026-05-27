import random
from typing import Self

ADJACENCYVECTORS = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]

class Cell():
    x: int
    y: int
    grid: list[list[Self]]
    value: int|None #0-8 or -1 for mine
    flagged: bool
    mined: bool

    def __init__(self, x: int, y: int, grid: list[list[Self]], flagged:bool = False, mined:bool = False, value:int|None = None):
        self.x = x
        self.y = y
        self.grid = grid
        self.value = value
        self.flagged = flagged
        self.mined = mined

    def __repr__(self):
        return f"Cell(x={self.x},y={self.y},value={self.value},flagged={self.flagged}, mined={self.mined})"
        
    def intialiseValue(self) -> None:
        if self.value != -1:
            self.value = 0
            for vector in ADJACENCYVECTORS:
                x = self.x+vector[0]
                y = self.y+vector[1]
                if x < 0 or y < 0 or x >= len(self.grid) or y >= len(self.grid[0]):
                    continue
                if self.grid[x][y].value == -1:
                    self.value += 1
            

def initialiseGrid(width:int, height:int, mines:int) -> list[list[Cell]]:
    if mines > width*height:
        raise ValueError("More mines than cells")

    grid: list[list[Cell]] = []
    for x in range(width):
        grid.append([Cell(x=x, y=y, grid=grid) for y in range(height)])

    for _ in range(mines):
            cell = grid[random.randint(0,width-1)][random.randint(0,height-1)]
            if cell.value == None:
                cell.value = -1

    for column in grid:
        for cell in column:
            cell.intialiseValue()

    return grid

def printGrid(grid:list[list[Cell]], ignoreMined: bool = False) -> None:
    for column in grid:
        for cell in column:
            if cell.mined or ignoreMined:
                if cell.value == -1:
                    print("@",end="")
                else:
                    print(cell.value,end="")
            elif cell.flagged:
                print("F",end="")
            else:
                print("#",end="")
        print()

grid = initialiseGrid(width=10, height=10, mines=10)