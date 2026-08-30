import random
from typing import Self
import pygame
import os

ADJACENCYVECTORS = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
SPRITEDIR = os.path.join(os.path.dirname(__file__), "sprites")

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
    "wrongflag": pygame.image.load(os.path.join(SPRITEDIR,"wrongflag.png")),
    "missing": pygame.image.load(os.path.join(SPRITEDIR,"missing.png")),
    "mark": pygame.image.load(os.path.join(SPRITEDIR,"mark.png")),
    }

class Tile():
    """A single minesweeper tile

    Attributes:
        x: The x position of the tile in the grid.
        y: The y position of the tile in the grid.
        grid: The grid which it is a part of.
        count: The amount of adjacent mines or -1 if it is a mine.
        flagged: Whether the tile has been flagged as a mine or not.
        dug: Whether the tile has been dug/revealed or not.
    """    

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
        """Gets the adjacent tiles

        Returns:
            list[Tile]: The list of the adjacent tiles.
        """        

        adjacentTiles = []
        for vector in ADJACENCYVECTORS:
            x = self.x+vector[0]
            y = self.y+vector[1]
            if x < 0 or y < 0 or x >= len(self.grid) or y >= len(self.grid[0]):
                continue
            adjacentTiles.append(self.grid[x][y])
        return adjacentTiles
            
    def intialiseCount(self) -> None:
        """Checks adjacent tiles to set it's own count appropriatelty.
        """        

        if self.count != -1:
            self.count = 0
            for tile in self.getAdjacentTiles():
                if tile.count == -1:
                    self.count += 1
    
    def dig(self, queue:list[Self]|None = None, depth:int = 0) -> bool:
        """Digs or chords this tile. If it reveals a 0 tile, it will flood dig.

        Args:
            queue (list[Self] | None, optional): *Should not be accessed.* The queue of of chains to start. Defaults to None.
            depth (int, optional): *Should not be accessed.* The depth at which it is currently operating. Defaults to 0.

        Returns:
            bool: Whether this dig has revealed a mine or not.
        """

        if queue is None: queue = []

        if not self.flagged:
            if not self.dug:
                self.dug = True
                if self.count == 0:
                    for tile in self.getAdjacentTiles():
                        try:
                            if not tile.dug: tile.dig(queue=queue, depth=depth+1)
                        except RecursionError:
                            for adjacent in tile.getAdjacentTiles():
                                if not adjacent.dug: queue.append(adjacent)
                    while len(queue) > 0 and depth == 0:
                        tile = queue.pop(0)
                        if not tile.dug:
                            tile.dig(queue=queue, depth=depth+1)
                else:
                    return self.count == -1
            elif depth == 0:
                flagCount = 0
                for tile in self.getAdjacentTiles():
                    if tile.flagged:
                        flagCount += 1
                if flagCount == self.count:
                    if any([tile.dig(queue=queue, depth=depth+1) for tile in self.getAdjacentTiles()]):
                        return True
        return False
    
    def flag(self) -> None:
        """Flags this tile, if it has not been dug.
        """

        if not self.dug:
            self.flagged = not self.flagged
            
    def draw(self, surface: pygame.Surface, squareSize: int, displayMines:bool = False, mark: bool = False) -> None:
        """Draws this tile to the screen

        Args:
            surface (pygame.Surface): The screen to which the tile should be drawn.
            squareSize (int): The size (in pixels) at which the tile should be drawn.
            displayMines (bool, optional): Whether mines and incorrect flags should be displayed or not. Defaults to False.
            mark (bool, optional): Whether this tile should be marked with an identifiable texture for debugging. Defaults to False.
        """

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
        else:
            sprite = SPRITES["missing"]
        
        surface.blit(pygame.transform.scale(sprite, (squareSize, squareSize)), (self.x*squareSize, self.y*squareSize))
        if mark: surface.blit(pygame.transform.scale(SPRITES["mark"], (squareSize, squareSize)), (self.x*squareSize, self.y*squareSize))


def initialiseGrid(width: int, height: int, mines: int, maxWindowWidth:int = 1280, maxWindowHeight:int = 720, minSquareSize:int = 8, maxSquareSize:int = 64) -> tuple[list[list[Tile]],int]:
    """Initialises the grid and calculates the appropriate size for the tiles.

    Args:
        width (int): The width of the board in amount of tiles.
        height (int): The height of the board in amount of tiles.
        mines (int): The amount of mines that should be on the board.
        maxWindowWidth (int, optional): The maximum width (in pixels) the window should be (minSquareSize takes priority). Defaults to 1280.
        maxWindowHeight (int, optional): The maximum height (in pixels) the window should be (minSquareSize takes priority). Defaults to 720.
        minSquareSize (int, optional): The minimum size (in pixels) the tiles are allowed to be. Defaults to 8.
        maxSquareSize (int, optional): The maximum size (in pixels) the tiles are allowed to be. Defaults to 64.

    Raises:
        ValueError: More mines than tiles.

    Returns:
        tuple[list[list[Tile]],int]: _description_
    """

    squareSize = min(max(min(maxWindowWidth//width, maxWindowHeight//width), minSquareSize), maxSquareSize)

    if mines > width*height:
        raise ValueError("More mines than tiles.")

    grid: list[list[Tile]] = []
    for x in range(width):
        grid.append([Tile(x=x, y=y, grid=grid) for y in range(height)])

    for _ in range(mines):
            tile = grid[random.randint(0,width-1)][random.randint(0,height-1)]
            while tile.count is not None:
                tile = grid[random.randint(0,width-1)][random.randint(0,height-1)]
            tile.count = -1

    for column in grid:
        for tile in column:
            tile.intialiseCount()

    return grid, squareSize

def getMineCount(grid: list[list[Tile]]) -> int:
    """Returns the current (unflagged) minecount.

    Args:
        grid (list[list[Tile]]): The grid for which to get the minecount.
    """

    mines: int = 0
    flags: int = 0

    for column in grid:
        for tile in column:
            if tile.count is not None:
                mines += tile.count == -1
            flags += tile.flagged

    return mines-flags

def hasWon(grid: list[list[Tile]]) -> bool:
    """Returns whether the board has been cleared or not.

    Args:
        grid (list[list[Tile]]): The grid for which to check if it has been cleared.
    """

    for column in grid:
        for tile in column:
            if not tile.dug and not tile.count == -1:
                return False
    return True

def init(width:int, height:int, mines:int, maxWindowWidth:int = 1280, maxWindowHeight:int = 720, minSquareSize:int = 8, maxSquareSize:int = 64) -> tuple[list[list[Tile]],int,pygame.Surface,pygame.time.Clock]:
    """Initialises pygame and the grid.

    Args:
        width (int): The amount of tiles wide the board should be.
        height (int): The amount of tiles high the board should be.
        mines (int): The amount of mines the board should contain.
        maxWindowWidth (int, optional): The maximum width (in pixels) the window should be (minSquareSize takes priority). Defaults to 1280.
        maxWindowHeight (int, optional): The maximum height (in pixels) the window should be (minSquareSize takes priority). Defaults to 720.
        minSquareSize (int, optional): The minimum size (in pixels) the tiles are allowed to be. Defaults to 8.
        maxSquareSize (int, optional): The maximum size (in pixels) the tiles are allowed to be. Defaults to 64.

    Returns:
        (tuple[list[list[Tile]],int,pygame.Surface,pygame.time.Clock]): A tuple (grid, squareSize, screen, clock), where
            grid is the initialised grid,
            squareSize is the size (in pixels) at which to display the tiles,
            screen is the Surface which represents the screen, and
            clock is the pygame clock.
    """

    pygame.init()
    grid, squareSize = initialiseGrid(width=width, height=height, mines=mines, maxWindowWidth=maxWindowWidth, maxWindowHeight=maxWindowHeight, minSquareSize=minSquareSize, maxSquareSize=maxSquareSize)
    screen = pygame.display.set_mode((width*squareSize,height*squareSize))
    clock = pygame.time.Clock()
    return grid, squareSize, screen, clock

def drawGrid(grid: list[list[Tile]], surface: pygame.Surface, squareSize: int, displayMines:bool = False) -> None:
    """Draws all the tiles of a grid to a Surface

    Args:
        grid (list[list[Tile]]): The grid that should be drawn to the surface.
        surface (pygame.Surface): The surface to which the grid should be drawn.
        squareSize (int): The size (in pixels) at which the tiles should be drawn.
        displayMines (bool, optional): Whether mines and incorrect flags should be displayed or not. Defaults to False.
    """

    for column in grid:
        for tile in column:
            tile.draw(surface=surface, squareSize=squareSize, displayMines=displayMines)

def main(width:int = 30, height:int = 16, mines:int = 99) -> None:
    """Runs the game for player interactivity.

    Args:
        width (int): The amount of tiles wide the board should be. defaults to 30.
        height (int): The amount of tiles high the board should be. defaults to 16.
        mines (int): The amount of mines the board should contain. defaults to 99.
    """

    grid, squareSize, screen, clock = init(width=width,height=height,mines=mines)

    running = True
    finished = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                mouseX,mouseY = pygame.mouse.get_pos()
                x = mouseX//squareSize
                y = mouseY//squareSize
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
                    grid, squareSize = initialiseGrid(width=width, height=height, mines=mines)
                
        screen.fill("light grey")
        
        drawGrid(grid=grid, surface=screen, squareSize=squareSize, displayMines=finished)
        pygame.display.set_caption(f"Mines: {getMineCount(grid=grid)}")
        
        pygame.display.flip()
        
        clock.tick(60)

if __name__ == "__main__":
    main()