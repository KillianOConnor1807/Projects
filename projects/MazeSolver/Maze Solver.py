# Author - Killian O'Connor
# Date - 02/08/2025
# Description - A simple maze solver using a BFS and DFS - goal to implement and visualise the algorithms - adapted from 'Tech With Tim' 

import curses # allows to update what's in the terminal
from curses import wrapper
import queue
import time

maze = [
    ["#", "#", "#", "#", "#", "O", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]

def print_maze(maze , stdscr , path =[]):
    BLUE = curses.color_pair(1)
    RED = curses.color_pair(2)
    
    for i , row in enumerate(maze): # goes through each row in the list - i = index , row = the array of the given row
        for j , value in enumerate(row): # goes through each cell in the row - j = index , value = the contents
            if (i , j) in path:
                stdscr.addstr(i , j*2 , "X" , RED) # multiply by 2 because the print was too squished together
            else:
                stdscr.addstr(i , j*2 , value , BLUE) # multiply by 2 because the print was too squished together

def find_path(maze , stdscr , alg):
    start = "O"
    end = "X"
    start_pos = find_start(maze , start)
    if alg == 1:
        BFS(maze , start , end , start_pos, stdscr)
    if alg == 2:
        DFS(maze , start , end , start_pos, stdscr)

def BFS(maze , start , end , start_pos, stdscr):
    q = queue.Queue()
    q.put((start_pos , [start_pos] )) # stores the current position and the path taken
    
    visited = set()
    
    while not q.empty():
        current_pos , path = q.get() # fixed: use q.get(), not queue.get()
        row , col = current_pos # row and col from position
        
        # changing the colours of the maze as the search runs, gets updated each iteration
        stdscr.clear()
        print_maze(maze , stdscr , path)
        stdscr.refresh()
        time.sleep(0.1) # small delay so we can see the search

        if maze[row][col] == end: # if the position = X
            return path
        
        neighbours = find_neighbours(maze , row , col)
        for neighbour in neighbours:
            if neighbour in visited:  # if already visited move on
                continue
            r , c = neighbour
            if maze[r][c] == "#" :
                continue
            
            new_path = path + [neighbour] # attaching the neighbour to the current path
            q.put((neighbour, new_path)) # fixed: must push both position and path
            visited.add(neighbour)
def DFS(maze , start , end , start_pos , stdscr):
    stack = [(start_pos, [start_pos])]  # first in last out
    visited = set() # record visited

    while stack: # while the stacks not empty
        current_pos, path = stack.pop() # remove from stack
        row, col = current_pos

        # display as loop iterates
        ######
        stdscr.clear()
        print_maze(maze, stdscr, path)
        time.sleep(0.1)
        stdscr.refresh()
        ######

        if maze[row][col] == end:
            return path

        if current_pos in visited:
            continue

        visited.add(current_pos)
        

        neighbours = find_neighbours(maze , row , col)
        for neighbour in neighbours:
            if neighbour in visited:  # if already visited move on
                continue
            r , c = neighbour
            if maze[r][c] == "#" :
                continue
            new_path = path + [neighbour]  # attaching the neighbour to the current path
            stack.append((neighbour , new_path))



def find_neighbours(maze , row , col):
    neighbours = []
    
    if row > 0:
        neighbours.append((row - 1 , col))
    if row + 1 < len(maze):
        neighbours.append((row + 1 , col))
    if col > 0:
        neighbours.append((row , col - 1))
    if col + 1 < len(maze[0]):  
        neighbours.append((row , col + 1))  
    return neighbours
    
# function to find the start of the maze 
def find_start(maze , start):
    for i , row in enumerate(maze):
        for j , value in enumerate(row):
            if value == start:
                return i , j
    return None

def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE , curses.COLOR_BLACK) # background = black , maze colour = blue
    curses.init_pair(2, curses.COLOR_RED , curses.COLOR_BLACK) # path colour = red
    #show the bfs then the dfs
    find_path(maze , stdscr , 1)
    find_path(maze , stdscr , 2)
    stdscr.getch() # wait for key before closing

wrapper(main)
