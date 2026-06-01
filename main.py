import random
from typing import Self
import pygame
import os

ADJACENCYVECTORS = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
SPRITEDIR = os.path.join(os.path.dirname(__file__), "sprites")

MAXWINDOWWIDTH, MAXWINDOWHEIGHT = 1280, 720
MINSQUARESIZE = 8
MAXSQUARESIZE = 64

BOARDWIDTH = 30
BOARDHEIGHT = 16
MINES = 99

SQUARESIZE = min(max(min(MAXWINDOWWIDTH//BOARDWIDTH, MAXWINDOWHEIGHT//BOARDHEIGHT), MINSQUARESIZE), MAXSQUARESIZE)

SPRITES = {
    0: pygame.image.load(os.path.join(SPRITEDIR,"0.png")),
    1: pygame.image.load(os.path.join(SPRITEDIR,"1.png")),
    2: pygame.image.load(os.path.join(SPRITEDIR,"2.png")),
    3: pygame.image.load(os.path.join(SPRITEDIR,"3.png")),
    4: pygame.image.load(os.path.join(SPRITEDIR,"4.png")),
    5: pygame.image.load(os.path.join(SPRITEDIR,"5.png")),
    6: pygame.image.load(os.path.join(SPRITEDIR,"6.png")),
    7: pygame.image.load(os.path.join(SPRITEDIR,"7.png")),
    8: pygame.image.load(os.path.join(SPRITEDIR,"8.png")),
    "flag": pygame.image.load(os.path.join(SPRITEDIR,"flag.png")),
    "mine": pygame.image.load(os.path.join(SPRITEDIR,"mine.png")),
    "undug": pygame.image.load(os.path.join(SPRITEDIR,"undug.png")),
    "wrongdig": pygame.image.load(os.path.join(SPRITEDIR,"wrongdig.png")),
    "wrongflag": pygame.image.load(os.path.join(SPRITEDIR,"wrongflag.png"))
}

class Tile():
    x: int
    y: int
    grid: list[list[Self]]
    count: int|None #0-8 or -1 for mine. None means uninitialised
    flagged: bool
    dug: bool

    def __init__(self, x: int, y: int, grid: list[list[Self]], flagged:bool = False, dug:bool = False, count:int|None = None):
        self.x = x
        self.y = y
        self.grid = grid
        self.count = count
        self.flagged = flagged
        self.dug = dug

    def __repr__(self):
        return f"Tile(x={self.x},y={self.y},count={self.count},flagged={self.flagged}, dug={self.dug})"

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
    
    def dig(self, chord:bool = False) -> bool:
        if not self.flagged:
            if not self.dug:
                self.dug = True
                if self.count == 0:
                    for tile in self.getAdjacentTiles():
                        try:
                            tile.dig()
                        except RecursionError:
                            queue.append(tile)
                else:
                    return self.count == -1
            elif not chord:
                flagCount = 0
                for tile in self.getAdjacentTiles():
                    if tile.flagged:
                        flagCount += 1
                if flagCount == self.count:
                    if any([tile.dig(chord=True) for tile in self.getAdjacentTiles()]):
                        return True
        return False
    
    def flag(self) -> None:
        if not self.dug:
            self.flagged = not self.flagged
            
    def draw(self, surface: pygame.Surface, displayMines:bool = False) -> None:
        if self.flagged:
            if displayMines and self.count != -1:
                sprite = SPRITES["wrongflag"]
            else:
                sprite = SPRITES["flag"]
        elif not self.dug and (self.count != -1 or not displayMines):
            sprite = SPRITES["undug"]
        elif self.count == -1:
            if self.dug:
                sprite = SPRITES["wrongdig"]
            else:
                sprite = SPRITES["mine"]
        elif self.count != None:
            sprite = SPRITES[self.count]
        
        surface.blit(pygame.transform.scale(sprite, (SQUARESIZE, SQUARESIZE)), (self.x*SQUARESIZE, self.y*SQUARESIZE))

queue: list[Tile] = []       


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
            if not tile.dug and not tile.count == -1:
                return False
    return True

grid = initialiseGrid(width=BOARDWIDTH, height=BOARDHEIGHT, mines=MINES)

pygame.init()
screen = pygame.display.set_mode((BOARDWIDTH*SQUARESIZE,BOARDHEIGHT*SQUARESIZE))
clock = pygame.time.Clock()
running = True
finished = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            mouseX,mouseY = pygame.mouse.get_pos()
            x = mouseX//SQUARESIZE
            y = mouseY//SQUARESIZE
            if event.button == 1:
                if grid[x][y].dig():
                    finished = True
                if hasWon(grid):
                    finished = True
            elif event.button == 3:
                grid[x][y].flag()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                finished = False
                grid = initialiseGrid(width=BOARDWIDTH, height=BOARDHEIGHT, mines=MINES)
            
    screen.fill("light grey")
    
    while len(queue) > 0:
        queue.pop(0).dig()
    
    for column in grid:
        for tile in column:
            tile.draw(screen, displayMines=finished)
    
    pygame.display.flip()
    
    clock.tick(60)