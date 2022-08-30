import sys, pygame as pg
from turtle import clear
from tracemalloc import start
from collections import defaultdict
import solver
import copy


#initialize screen
pg.init()
screen_size = 750, 750
screen = pg.display.set_mode(screen_size)
font = pg.font.SysFont(None, 80)

# storage of all the cells needed to check if the board would be valid with another input 
rows = defaultdict(set)
cols = defaultdict(set)
squares = defaultdict(set)
starting = set()

# TODO input your desired sodoku board in here
number_grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# starting grid for game reset purposes
starting_grid = copy.deepcopy(number_grid)

# nessecary global variables and constants
curr_y = 0
curr_x = 0
count = 0
GRID_SIZE = 77
sqaure_x = 17
square_y = 17

# drawing the grid board
def draw_background():
    screen.fill(pg.Color("white"))
    pg.draw.rect(screen, pg.Color("black"), pg.Rect(15, 15, 720, 720), 3)
    
    i = 1
    while (i * 80) < 720:
        line_width = 5 if i % 3 > 0 else 10
        pg.draw.line(screen, pg.Color("black"), pg.Vector2((i * 80) + 15, 15), pg.Vector2((i * 80) + 15, 733), line_width)
        pg.draw.line(screen, pg.Color("black"), pg.Vector2(15, (i * 80) + 15), pg.Vector2(733, (i * 80) + 15), line_width)
        i+=1
    
    pg.draw.rect(screen, pg.Color("red"), pg.Rect( (curr_x) * 80  + sqaure_x, (curr_y) * 80 + square_y, 80, 80), 3)
    
# drawing all the inputted numbers on the board
def draw_numbers():
    global count
    count+=1
    offsetX = 40
    offsetY = 33

    for i in range(9):
        for j in range(9):
            output = str(number_grid[i][j]) if number_grid[i][j] != 0 else ""
            if (i, j) in starting:
                n_text = font.render(str(output), True, pg.Color('black'))
            else:
                n_text = font.render(str(output), True, pg.Color('blue'))
            screen.blit(n_text, pg.Vector2((j * 80) + offsetX, ( i * 80) + offsetY))

# helper function used to check if cell is valid for insertion
def isValid(x, y, val):
    if val not in range(1, 10) or (x, y) in starting or val in rows[x] or val in cols[y] or val in squares[(x//3, y//3)]: return False
    return True

# function used to process a mouse click to change the target cell
def process_click(x, y):
    global curr_y
    global curr_x
    
    if x < 0 or x > 700 or y < 0 or y > 700: return
    curr_x = x//GRID_SIZE
    curr_y = y//GRID_SIZE

# function used to delete an input
def delete(x, y):
    if (curr_y, curr_x) not in starting and number_grid[curr_y][curr_x] != 0:
        deleteVal = number_grid[x][y]
        number_grid[x][y] = 0
        rows[x].remove(deleteVal)
        cols[y].remove(deleteVal)
        squares[(x//3, y//3)].remove(deleteVal)
    
# function used to process a key press
def process_key(val):
    global number_grid
    if isValid(curr_y, curr_x, val):
        delete(curr_y, curr_x)
        number_grid[curr_y][curr_x] = val
        rows[curr_y].add(val)
        cols[curr_x].add(val)
        squares[(curr_y//3, curr_x//3)].add(val)
    if val == -40: delete(curr_y, curr_x)

# function used to reset the game entirely
def reset():
    global number_grid
    number_grid = copy.deepcopy(starting_grid)
    rows.clear()
    cols.clear()
    squares.clear()
    process_starting()

# loop that is called at every frame of the game
def game_loop():
    draw_background()
    draw_numbers()
    for event in pg.event.get():
        if event.type == pg.QUIT: sys.exit()
        if event.type == pg.MOUSEBUTTONUP: 
            mouse_pos = pg.mouse.get_pos()
            process_click(event.pos[0] - 26, event.pos[1] - 26)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                solver.solve(False)
            elif event.key == pg.K_a:
                solver.solve(True)
            elif event.key == pg.K_c:
                reset()

            process_key(event.key - 48)
    pg.display.flip()

# function called at the start and every reset of game
def process_starting():
    global starting
    global rows
    global cols
    global squares
    for i in range(9):
        for j in range(9):
            if number_grid[i][j] != 0: 
                starting.add((i, j))
                rows[i].add(number_grid[i][j])
                cols[j].add(number_grid[i][j])
                squares[(i//3, j//3)].add(number_grid[i][j])