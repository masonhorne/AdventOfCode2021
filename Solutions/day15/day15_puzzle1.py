"""
--- Day 15: Chiton ---
You've almost reached the exit of the cave, but the walls are getting closer together. Your submarine can barely still fit, though; the main problem is that the walls of the cave are covered in chitons, and it would be best not to bump any of them.

The cavern is large, but has a very low ceiling, restricting your motion to two dimensions. The shape of the cavern resembles a square; a quick scan of chiton density produces a map of risk level throughout the cave (your puzzle input). For example:

1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581

You start in the top left position, your destination is the bottom right position, and you cannot move diagonally. The number at each position is its risk level; to determine the total risk of an entire path, add up the risk levels of each position you enter (that is, don't count the risk level of your starting position unless you enter it; leaving it adds no risk to your total).

Your goal is to find a path with the lowest total risk. In this example, a path with the lowest total risk is highlighted here:

[1] 1  6  3  7  5  1  7  4  2
[1] 3  8  1  3  7  3  6  7  2
[2][1][3][6][5][1][1] 3  2  8
 3  6  9  4  9  3 [1][5] 6  9
 7  4  6  3  4  1  7 [1] 1  1
 1  3  1  9  1  2  8 [1][3] 7
 1  3  5  9  9  1  2  4 [2] 1
 3  1  2  5  4  2  1  6 [3] 9
 1  2  9  3  1  3  8  5 [2][1]
 2  3  1  1  9  4  4  5  8 [1]

The total risk of this path is 40 (the starting position is never entered, so its risk is not counted).

What is the lowest total risk of any path from the top left to the bottom right?
"""
import sys
import heapq

# Read input for cave layout
grid = []
for line in sys.stdin.readlines():
    row = [ch for ch in line.strip()]
    grid.append(row)

# Gather board dimensions and directions to travel
directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
rows = len(grid)
cols = len(grid[0])

# Label start and end locations and initialize heap of locations and priority
start = (0, 0)
end = (rows - 1, cols - 1)
to_visit = [(0, start)]
distances = {start: 0}
heapq.heapify(to_visit)
while to_visit:
    # Get the priority and location and with best priority from queue
    priority, loc = heapq.heappop(to_visit)
    if loc == end:
        break
    # Get the coordinates for the location and try all neighbors
    row, col = loc[0], loc[1]
    for rc, cc in directions:
        new_row = row + rc
        new_col = col + cc
        if 0 <= new_row <= rows - 1 and 0 <= new_col <= cols - 1:
            weight = int(grid[new_row][new_col])
            new_dist = distances[loc] + weight
            new_loc = (new_row, new_col)
            # With new location only add to queue if new distances is less than current for location
            # Or if the location has never been visited before
            if (new_loc in distances and new_dist < distances[new_loc]) or new_loc not in distances:
                distances[new_loc] = new_dist
                # Let priority be the distance traveled plus the distance to the edges needed
                priority = new_dist + (abs(new_row - end[0]) + abs(new_col - end[1]))
                heapq.heappush(to_visit, (priority, new_loc))
print(distances[end])