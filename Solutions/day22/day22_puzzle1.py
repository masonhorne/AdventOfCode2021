"""
--- Day 22: Reactor Reboot ---
Operating at these extreme ocean depths has overloaded the submarine's reactor; it needs to be rebooted.

The reactor core is made up of a large 3-dimensional grid made up entirely of cubes, one cube per integer 3-dimensional coordinate (x,y,z). Each cube can be either on or off; at the start of the reboot process, they are all off. (Could it be an old model of a reactor you've seen before?)

To reboot the reactor, you just need to set all of the cubes to either on or off by following a list of reboot steps (your puzzle input). Each step specifies a cuboid (the set of all cubes that have coordinates which fall within ranges for x, y, and z) and whether to turn all of the cubes in that cuboid on or off.

For example, given these reboot steps:

on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10
The first step (on x=10..12,y=10..12,z=10..12) turns on a 3x3x3 cuboid consisting of 27 cubes:

10,10,10
10,10,11
10,10,12
10,11,10
10,11,11
10,11,12
10,12,10
10,12,11
10,12,12
11,10,10
11,10,11
11,10,12
11,11,10
11,11,11
11,11,12
11,12,10
11,12,11
11,12,12
12,10,10
12,10,11
12,10,12
12,11,10
12,11,11
12,11,12
12,12,10
12,12,11
12,12,12
The second step (on x=11..13,y=11..13,z=11..13) turns on a 3x3x3 cuboid that overlaps with the first. As a result, only 19 additional cubes turn on; the rest are already on from the previous step:

11,11,13
11,12,13
11,13,11
11,13,12
11,13,13
12,11,13
12,12,13
12,13,11
12,13,12
12,13,13
13,11,11
13,11,12
13,11,13
13,12,11
13,12,12
13,12,13
13,13,11
13,13,12
13,13,13
The third step (off x=9..11,y=9..11,z=9..11) turns off a 3x3x3 cuboid that overlaps partially with some cubes that are on, ultimately turning off 8 cubes:

10,10,10
10,10,11
10,11,10
10,11,11
11,10,10
11,10,11
11,11,10
11,11,11
The final step (on x=10..10,y=10..10,z=10..10) turns on a single cube, 10,10,10. After this last step, 39 cubes are on.

The initialization procedure only uses cubes that have x, y, and z positions of at least -50 and at most 50. For now, ignore cubes outside this region.

Here is a larger example:

on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682
The last two steps are fully outside the initialization procedure area; all other steps are fully within it. After executing these steps in the initialization procedure region, 590784 cubes are on.

Execute the reboot steps. Afterward, considering only cubes in the region x=-50..50,y=-50..50,z=-50..50, how many cubes are on?
"""
import sys


def combine(cube, cubes):
    state, ((x1, x2), (y1, y2), (z1, z2)) = cube
    to_del = set()
    to_add = set()
    self_added = False
    for (s1, xx1, xx2, yy1, yy2, zz1, zz2) in cubes:
        # If not intersecting
        if not (xx1 <= x2 and x1 <= xx2 and yy1 <= y2 and y1 <= yy2 and zz1 <= z2 and z1 <= zz2):
            continue
        nx1 = max(xx1, x1)
        nx2 = min(xx2, x2)
        ny1 = max(yy1, y1)
        ny2 = min(yy2, y2)
        nz1 = max(zz1, z1)
        nz2 = min(zz2, z2)
        to_del.add((s1, xx1, xx2, yy1, yy2, zz1, zz2))
        self_added = True
        if xx1 < nx1:
            to_add.add((s1, xx1, nx1 - 1, yy1, yy2, zz1, zz2))
        if nx2 < xx2:
            to_add.add((s1, nx2 + 1, xx2, yy1, yy2, zz1, zz2))
        if yy1 < ny1:
            to_add.add((s1, nx1, nx2, yy1, ny1 - 1, zz1, zz2))
        if ny2 < yy2:
            to_add.add((s1, nx1, nx2, ny2 + 1, yy2, zz1, zz2))
        if zz1 < nz1:
            to_add.add((s1, nx1, nx2, ny1, ny2, zz1, nz1 - 1))
        if nz2 < zz2:
            to_add.add((s1, nx1, nx2, ny1, ny2, nz2 + 1, zz2))
        to_add.add((state, min(nx1, x1), max(nx2, x2), min(ny1, y1), max(ny2, y2), min(nz1, z1), max(nz2, z2)))
    for remove in to_del:
        cubes.remove(remove)
    for add in to_add:
        cubes.add(add)
    if not self_added:
        cubes.add((state, x1, x2, y1, y2, z1, z2))


cubes = set()
rules = sys.stdin.readlines()
instructions = [(x.split()[0], x.split()[1]) for x in rules]
for inst in instructions:
    vals = []
    for x in inst[1].split(','):
        a, b = [int(i) for i in x.split('=')[1].split('..')]
        vals.append((a, b))
    combine((inst[0], vals), cubes)
total = 0
for state, x1, x2, y1, y2, z1, z2 in cubes:
    if state == 'on':
        for i in range(max(-50, x1), min(50, x2) + 1):
            for j in range(max(-50, y1), min(50, y2) + 1):
                for k in range(max(-50, z1), min(50, z2) + 1):
                    total += 1
print(total)