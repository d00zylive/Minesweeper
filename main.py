import random
from typing import Self

ADJACENCYVECTORS = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]

class Tile():
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
        return f"Tile(x={self.x},y={self.y},count={self.count},flagged={self.flagged}, mined={self.mined})"

    def getAdjacentTiles(self) -> list[Self]:
        adjacentTiles = []
        for vector in ADJACENCYVECTORS:
            x = self.x+vector[0]
            y = self.y+vector[1]
            if x < 0 or y < 0 or x >= len(self.grid) or y >= len(self.grid[0]):
                continue
            adjacentTiles.append(self.grid[x][y])
        return adjacentTiles
            
    def intialiseCount(self) -> None:
        if self.count != -1:
            self.count = 0
            for tile in self.getAdjacentTiles():
                if tile.count == -1:
                    self.count += 1
    
    def mine(self, chord:bool = False) -> bool:
        if not self.flagged:
            if not self.mined:
                self.mined = True
                if self.count == 0:
                    for tile in self.getAdjacentTiles():
                        tile.mine()
                else:
                    return self.count == -1
            elif not chord:
                flagCount = 0
                for tile in self.getAdjacentTiles():
                    if tile.flagged:
                        flagCount += 1
                if flagCount == self.count:
                    if any([tile.mine(chord=True) for tile in self.getAdjacentTiles()]):
                        return True
        return False
    
    def flag(self) -> None:
        self.flagged = not self.flagged
          

def initialiseGrid(width:int, height:int, mines:int) -> list[list[Tile]]:
    if mines > width*height:
        raise ValueError("More mines than tiles")

    grid: list[list[Tile]] = []
    for x in range(width):
        grid.append([Tile(x=x, y=y, grid=grid) for y in range(height)])

    for _ in range(mines):
            tile = grid[random.randint(0,width-1)][random.randint(0,height-1)]
            if tile.count == None:
                tile.count = -1

    for column in grid:
        for tile in column:
            tile.intialiseCount()

    return grid

def hasWon(grid) -> bool:
    for column in grid:
        for tile in column:
            if not tile.mined and not tile.count == -1:
                return False
    return True

def printGrid(grid:list[list[Tile]], ignoreMined: bool = False) -> None:
    for column in grid:
        for tile in column:
            if tile.mined or ignoreMined:
                if tile.count == -1:
                    print("@",end="")
                else:
                    print(tile.count,end="")
            elif tile.flagged:
                print("F",end="")
            else:
                print("#",end="")
        print()

grid = initialiseGrid(width=10, height=10, mines=10)

printGrid(grid, True)
print()
printGrid(grid)
print()
while True:
    if random.choice(random.choice(grid)).mine(): # grid[int(input("y:   "))][int(input("x:   "))].mine():
        print("BOOM!")
    if hasWon(grid):
        print("WON!")
    printGrid(grid)
    print()
    input()
    
#TODO: Pygame