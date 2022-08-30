import sudoku
import pygame as pg
from functools import lru_cache

# algorithm that solves the sodoku board (uses memoization + backtracking)
@lru_cache
def solve(animate):
    finished = False

    # backtracking function that brute forces all the possible cases
    def dfs(x, y):
        if animate:
            sudoku.game_loop()
            pg.time.delay(100)
        nonlocal finished
        if finished: return
        if x >= 9:
            finished = True
            return
        if y >= 9:
            dfs(x+1, 0)
            return
        if sudoku.number_grid[x][y] != 0: 
            dfs(x, y+1)
            return
        
        for i in range(1, 10):
            if i in sudoku.rows[x] or i in sudoku.cols[y] or i in sudoku.squares[(x//3, y//3)]:
                continue
            sudoku.number_grid[x][y] = i
            sudoku.rows[x].add(i)
            sudoku.cols[y].add(i)
            sudoku.squares[(x//3, y//3)].add(i)
            dfs(x, y+1)
            if not finished:
                sudoku.rows[x].remove(i)
                sudoku.cols[y].remove(i)
                sudoku.squares[(x//3, y//3)].remove(i)
        
        if not finished: 
            sudoku.number_grid[x][y] = 0
    dfs(0, 0)