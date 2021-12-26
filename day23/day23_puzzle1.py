"""
--- Day 23: Amphipod ---
A group of amphipods notice your fancy submarine and flag you down. "With such an impressive shell," one amphipod says, "surely you can help us with a question that has stumped our best scientists."

They go on to explain that a group of timid, stubborn amphipods live in a nearby burrow. Four types of amphipods live there: Amber (A), Bronze (B), Copper (C), and Desert (D). They live in a burrow that consists of a hallway and four side rooms. The side rooms are initially full of amphipods, and the hallway is initially empty.

They give you a diagram of the situation (your puzzle input), including locations of each amphipod (A, B, C, or D, each of which is occupying an otherwise open space), walls (#), and open space (.).

For example:

#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
The amphipods would like a method to organize every amphipod into side rooms so that each side room contains one type of amphipod and the types are sorted A-D going left to right, like this:

#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########
Amphipods can move up, down, left, or right so long as they are moving into an unoccupied open space. Each type of amphipod requires a different amount of energy to move one step: Amber amphipods require 1 energy per step, Bronze amphipods require 10 energy, Copper amphipods require 100, and Desert ones require 1000. The amphipods would like you to find a way to organize the amphipods that requires the least total energy.

However, because they are timid and stubborn, the amphipods have some extra rules:

Amphipods will never stop on the space immediately outside any room. They can move into that space so long as they immediately continue moving. (Specifically, this refers to the four open spaces in the hallway that are directly above an amphipod starting position.)
Amphipods will never move from the hallway into a room unless that room is their destination room and that room contains no amphipods which do not also have that room as their own destination. If an amphipod's starting room is not its destination room, it can stay in that room until it leaves the room. (For example, an Amber amphipod will not move from the hallway into the right three rooms, and will only move into the leftmost room if that room is empty or if it only contains other Amber amphipods.)
Once an amphipod stops moving in the hallway, it will stay in that spot until it can move into a room. (That is, once any amphipod starts moving, any other amphipods currently in the hallway are locked in place and will not move again until they can move fully into a room.)
In the above example, the amphipods can be organized using a minimum of 12521 energy. One way to do this is shown below.

Starting configuration:

#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
One Bronze amphipod moves into the hallway, taking 4 steps and using 40 energy:

#############
#...B.......#
###B#C#.#D###
  #A#D#C#A#
  #########
The only Copper amphipod not in its side room moves there, taking 4 steps and using 400 energy:

#############
#...B.......#
###B#.#C#D###
  #A#D#C#A#
  #########
A Desert amphipod moves out of the way, taking 3 steps and using 3000 energy, and then the Bronze amphipod takes its place, taking 3 steps and using 30 energy:

#############
#.....D.....#
###B#.#C#D###
  #A#B#C#A#
  #########
The leftmost Bronze amphipod moves to its room using 40 energy:

#############
#.....D.....#
###.#B#C#D###
  #A#B#C#A#
  #########
Both amphipods in the rightmost room move into the hallway, using 2003 energy in total:

#############
#.....D.D.A.#
###.#B#C#.###
  #A#B#C#.#
  #########
Both Desert amphipods move into the rightmost room using 7000 energy:

#############
#.........A.#
###.#B#C#D###
  #A#B#C#D#
  #########
Finally, the last Amber amphipod moves into its room, using 8 energy:

#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########
What is the least energy required to organize the amphipods?
"""
import sys
import collections


def find_path(start, value, grid, goals, total):
    q = collections.deque([[(start[0], start[1], total)]])
    prev = set([start])
    steps = {}
    while q:
        path = q.popleft()
        x, y, cur = path[-1]
        if (x, y) in goals:
            steps[(x, y)] = cur
        for a, b in adj(x, y):
            if (a, b) in grid and (not grid[(a, b)].isalpha() and (a, b) not in prev):
                q.append(path + [(a, b, cur + cost[value])])
                prev.add((a, b))
    return {k:v for k, v in steps.items()}


def find_route(grid, total):
    state = tuple(sorted(grid.items()))
    if (bests and total >= min(bests)) or (state in states and states[state] <= total):
        return
    states[state] = total
    if not any(v.isalpha() for v in grid.values()):
        bests.append(total)
        return
    for k, v in sorted(grid.items(), key=lambda x: x[0] not in [5, 7]):
        if v.isalpha() and ((k[0], k[1] - 1) not in grid or grid[k[0], k[1] - 1] == '.'):
            goals = []
            valid_grid = {(x, 1) : grid[x, 1] for x in range(min(vald), max(vald) + 1)}
            column = [(x, y) for x, y in grid.keys() if x == ends[v] and y > 1]
            if not any(grid[x].isalpha() for x in column):
                valid_grid.update({x: grid[x] for x in column})
                goals += [max(column)]
            if k[1] > 1:
                goals += [(x, 1) for x in vald]
                valid_grid.update({(k[0], y): grid[k[0], y] for y in range(1, k[1] + 1)})
            possibilities = find_path(k, v, valid_grid, goals, total)
            for trial, steps in sorted(possibilities.items(), key=lambda x: x[0][1] < 2):
                trial_grid = {kn: kv for kn, kv in grid.items()}
                if column and trial == max(column):
                    trial_grid.pop(trial)
                else:
                    trial_grid[trial] = v
                trial_grid[k] = '.'
                find_route({ka: va for ka, va in trial_grid.items()}, steps)


data = sys.stdin.read().splitlines()
data = [x + ' ' * (len(data[0]) - len(x)) for x in data]
grid = {(x, y) : data[y][x] for x in range(len(data[0])) for y in range(len(data)) if (data[y][x] == '.' or data[y][x].isalpha())}
adj = lambda x, y: ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
cost = {'A' : 1, 'B' : 10, 'C': 100, 'D' : 1000}
ends = {'A' : 3, 'B' : 5, 'C': 7, 'D' : 9}
vald = [1, 2, 4, 6, 8, 10, 11]
bests = []
states = {}
find_route({k: v for k, v in grid.items()}, 0)
print(min(bests))