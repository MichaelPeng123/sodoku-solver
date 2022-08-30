import sodoku
import pygame as pg
from functools import lru_cache

# algorithm that solves the sodoku board (uses memoization + backtracking)
@lru_cache
def solve(animate):
    finished = False

    # backtracking function that brute forces all the possible cases
    def dfs(x, y):
        if animate:
            sodoku.game_loop()
            pg.time.delay(100)
        nonlocal finished
        if finished: return
        if x >= 9:
            finished = True
            return
        if y >= 9:
            dfs(x+1, 0)
            return
        if sodoku.number_grid[x][y] != 0: 
            dfs(x, y+1)
            return
        
        for i in range(1, 10):
            if i in sodoku.rows[x] or i in sodoku.cols[y] or i in sodoku.squares[(x//3, y//3)]:
                continue
            sodoku.number_grid[x][y] = i
            sodoku.rows[x].add(i)
            sodoku.cols[y].add(i)
            sodoku.squares[(x//3, y//3)].add(i)
            dfs(x, y+1)
            if not finished:
                sodoku.rows[x].remove(i)
                sodoku.cols[y].remove(i)
                sodoku.squares[(x//3, y//3)].remove(i)
        
        if not finished: 
            sodoku.number_grid[x][y] = 0
    dfs(0, 0)