import random

# Function that generates grid
def generate(height, width, mines_number):
    
    # Prepare grid by setting all tiles to 0
    grid = []

    for i in range(height):
        grid.append([])
        for j in range(width):
            grid[i].append(0)

    for i in range(mines_number):
        while True:
            # Generate radom mine position
            mine_y = random.randint(0, height - 1)
            mine_x = random.randint(0, width - 1)

            neighbour_mines = 0

            # Check if there are any mines nearby
            for y in range(mine_y - 1, mine_y + 3):
                for x in range(mine_x - 1, mine_x + 3):
                    try:
                        if grid[y][x] == -1:
                            neighbour_mines += 1
                    except: pass

            # Check if there is already a mine
            if grid[mine_y][mine_x] != -1 and neighbour_mines <= 3:
                grid[mine_y][mine_x] = -1
            
                # Set neighbour tile to number of mines it's touching 
                for y in range(mine_y - 1, mine_y + 2):
                    for x in range(mine_x - 1, mine_x + 2):
                        try:
                            if grid[y][x] != -1 and y >= 0 and x >= 0:
                                grid[y][x] += 1
                        except: pass
            
                break

    return grid