"""
-- Day 9: Smoke Basin ---
These caves seem to be lava tubes. Parts are even still volcanically active; small hydrothermal vents release smoke into the caves that slowly settles like rain.

If you can model how the smoke flows through the caves, you might be able to avoid it and be that much safer. The submarine generates a heightmap of the floor of the nearby caves for you (your puzzle input).

Smoke flows to the lowest point of the area it's in. For example, consider the following heightmap:

2199943210
3987894921
9856789892
8767896789
9899965678

Each number corresponds to the height of a particular location, where 9 is the highest and 0 is the lowest a location can be.

Your first goal is to find the low points - the locations that are lower than any of its adjacent locations. Most locations have four adjacent locations (up, down, left, and right); locations on the edge or corner of the map have three or two adjacent locations, respectively. (Diagonal locations do not count as adjacent.)

In the above example, there are four low points, all highlighted: two are in the first row (a 1 and a 0), one is in the third row (a 5), and one is in the bottom row (also a 5). All other locations on the heightmap have some lower adjacent location, and so are not low points.

The risk level of a low point is 1 plus its height. In the above example, the risk levels of the low points are 2, 1, 6, and 6. The sum of the risk levels of all low points in the heightmap is therefore 15.

Find all of the low points on your heightmap. What is the sum of the risk levels of all low points on your heightmap?

--- Part Two ---
Next, you need to find the largest basins so you know what areas are most important to avoid.

A basin is all locations that eventually flow downward to a single low point. Therefore, every low point has a basin, although some basins are very small. Locations of height 9 do not count as being in any basin, and all other locations will always be part of exactly one basin.

The size of a basin is the number of locations within the basin, including the low point. The example above has four basins.

The top-left basin, size 3:

2199943210
3987894921
9856789892
8767896789
9899965678
The top-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678
The middle basin, size 14:

2199943210
3987894921
9856789892
8767896789
9899965678
The bottom-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678
Find the three largest basins and multiply their sizes together. In the above example, this is 9 * 14 * 9 = 1134.

What do you get if you multiply together the sizes of the three largest basins?
"""
import math
import sys

def follow(row, col, s):
    for y, x in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
        if (row + y, col + x) not in s:
            if row + y >= 0 and row + y < len(data):
                if col + x < len(data[0]) and col + x >= 0:
                    if data[row + y][col + x] != "9":
                        s.add((row + y, col + x))
                        follow(row + y, col + x, s)
    return s


data = sys.stdin.read().strip().split("\n")
lows = []
basins = []
for row in range(len(data)):
    for col in range(len(data[0])):
        cur = int(data[row][col])
        n = int(data[row - 1][col]) if row > 0 else 9999
        s = int(data[row + 1][col]) if row < len(data) - 1 else 9999
        e = int(data[row][col + 1]) if col < len(data[0]) - 1 else 9999
        w = int(data[row][col - 1]) if col > 0 else 9999
        if cur < min([n, s, e, w]):
            lows.append(cur)
            basins.append(len(follow(row, col, {(row, col)})))
print(math.prod(sorted(list(basins), reverse=True)[:3]))