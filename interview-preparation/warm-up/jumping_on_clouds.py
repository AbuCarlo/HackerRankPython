'''https://www.hackerrank.com/challenges/jumping-on-the-clouds/problem'''

# pylint: disable=C0103
def jumpingOnClouds(c):
    position = 0
    jumps = 0
    while position < len(c) - 1:
        # The game is guaranteed to be winnable,
        # so we can always jump from the second-to-
        # last position to the very last. Otherwise,
        # check if there's a forbidden cloud there;
        # if not, go ahead and jump.
        if position == len(c) - 2 or c[position + 2]:
            position += 1
        else:
            position += 2
        jumps +=1
    return jumps
