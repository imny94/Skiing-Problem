
# coding: utf-8

# In[93]:


'''
Easy Skiing Question

Goal:
    Find the longest path on a given mountain, with the largest difference in elevation

Format:
    The first line will represent the size of the map

    Every line after that will represent the elevation at that given point

Rules:
    One can only travel north, south, east or west
'''


# In[133]:
import time
start_time = time.time()

input_file = "map.txt"
grid = []
grid_rows, grid_cols = 0,0
longest_path = []
largest_diff_in_elevation = 0

def parse_file(input_file):
    global grid, grid_rows, grid_cols
    fp_in = open(input_file, "r")

    first_line = fp_in.readline()
    grid_rows, grid_cols = [int(i) for i in first_line.strip().split(" ")]
    for i in range(grid_cols):
        grid.append([[int(l), [], 0] for l in fp_in.readline().strip().split(" ")])

    fp_in.close()
    
# Format of each point on the grid will be (Current_elevation, current_best_path_for_point, current_best_diff_in_elevation)

# In[59]:


def possibleMoves(row, col):
    moves = [
            (row+1, col),          # Move South
            (row-1, col),          # Move North
            (row, col-1),          # Move West
            (row, col+1)           # Move East
            ]
    return moves


# In[129]:


def runSearch():
    global grid, grid_rows, grid_cols, longest_path, largest_diff_in_elevation
    for row in range(grid_rows):
        for col in range(grid_cols):
            current_elevation = grid[row][col][0]
            tryMoving(current_elevation, row, col)
            # print("Ended one point")
    for row in range(grid_rows):
        for col in range(grid_cols):
            if len(grid[row][col][1]) >= len(longest_path) and len(grid[row][col][1]) >= 2:
                if len(grid[row][col][1]) == len(longest_path):
                    if largest_diff_in_elevation > grid[row][col][2]:
                        continue
                largest_diff_in_elevation = grid[row][col][1][0] - grid[row][col][1][-1]
                longest_path = grid[row][col][1]


# In[124]:


import copy
def tryMoving(current_elevation, row, col):
    global grid
    if grid[row][col][1] != []:
        return copy.deepcopy(grid[row][col][1])
        
    moves = possibleMoves(row, col)
    for i,j in moves:
        if i < 0 or j < 0:
            continue
        try:
            new_elevation = grid[i][j][0]
        except IndexError:
            # Move is not feasible
            continue
        
        if new_elevation >= current_elevation:
            # You cannot stay at the same elevation or go higher
            # This is a one full path that has been found
            continue

        # The new_elevation is smaller than the current elevation
        # Now we need to repeat the above steps
        next_best_elevation = tryMoving(new_elevation, i, j)
        next_best_elevation.insert(0, current_elevation)
        if len(grid[row][col][1]) <= len(next_best_elevation):
            if len(grid[row][col][1]) < len(next_best_elevation):
                grid[row][col][1] = next_best_elevation
                grid[row][col][2] = next_best_elevation[0] - next_best_elevation[-1]
            elif grid[row][col][2] < next_best_elevation[0] - next_best_elevation[-1]:
                grid[row][col][1] = next_best_elevation
                grid[row][col][2] = next_best_elevation[0] - next_best_elevation[-1]
    if grid[row][col][1] == []:
        return [current_elevation]
    else:
        return copy.deepcopy(grid[row][col][1])


# In[130]:


print("Parsing file ...")
parse_file(input_file)
print("Completed parsing file ...")
print("Running Search ...")
runSearch()
print("Search completed, longest path is :")


# In[131]:

end_time = time.time()
print(longest_path)
print("Total Time taken : {}".format(end_time-start_time))