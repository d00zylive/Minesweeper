import random
from typing import Self

ADJACENCYVECTORS = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]

class Cell():
    x: int
    y: int
    grid: list[list[Self]]
    count: int|None #0-8 or -1 for mine
    flagged: bool
    mined: bool

    def __init__(self, x: int, y: int, grid: list[list[Self]], flagged:bool = False, mined:bool = False, count:int|None = None):
        self.x = x
        self.y = y
        self.grid = grid
        self.count = count
        self.flagged = flagged
        self.mined = mined

    def __repr__(self):
        return f"Cell(x={self.x},y={self.y},count={self.count},flagged={self.flagged}, mined={self.mined})"

    def getAdjacentCells(self) -> list[Self]:
        adjacentCells = []
        for vector in ADJACENCYVECTORS:
            x = self.x+vector[0]
            y = self.y+vector[1]
            if x < 0 or y < 0 or x >= len(self.grid) or y >= len(self.grid[0]):
                continue
            adjacentCells.append(self.grid[x][y])
        return adjacentCells
            
    def intialiseCount(self) -> None:
        if self.count != -1:
            self.count = 0
            for cell in self.getAdjacentCells():
                if cell.count == -1:
                    self.count += 1
    
    def mine(self) -> bool:
        if not self.mined:
            self.mined = True
            if self.count == 0:
                for cell in self.getAdjacentCells():
                    cell.mine()
            return self.count == -1
        return False
            

def initialiseGrid(width:int, height:int, mines:int) -> list[list[Cell]]:
    if mines > width*height:
        raise ValueError("More mines than cells")

    grid: list[list[Cell]] = []
    for x in range(width):
        grid.append([Cell(x=x, y=y, grid=grid) for y in range(height)])

    for _ in range(mines):
            cell = grid[random.randint(0,width-1)][random.randint(0,height-1)]
            if cell.count == None:
                cell.count = -1

    for column in grid:
        for cell in column:
            cell.intialiseCount()

    return grid

def hasWon(grid) -> bool:
    for column in grid:
        for cell in column:
            if not cell.mined and not cell.count == -1:
                return False
    return True

def printGrid(grid:list[list[Cell]], ignoreMined: bool = False) -> None:
    for column in grid:
        for cell in column:
            if cell.mined or ignoreMined:
                if cell.count == -1:
                    print("@",end="")
                else:
                    print(cell.count,end="")
            elif cell.flagged:
                print("F",end="")
            else:
                print("#",end="")
        print()

grid = initialiseGrid(width=10, height=10, mines=10)

printGrid(grid, True)
printGrid(grid)
while True:
    if random.choice(random.choice(grid)).mine(): # grid[int(input("y:   "))][int(input("x:   "))].mine():
        print("BOOM!")
    if hasWon(grid):
        print("WON!")
    printGrid(grid)