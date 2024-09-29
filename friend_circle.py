def find_root(roots, v):
    while v != roots[v]:
        v = roots[v]
    return v

def friendcircle(queries):
    roots = {}
    sizes = {}
    max_size = 0
    result = []
    for left, right in queries:
        if left not in roots:
            roots[left] = left
            sizes[left] = 1
        else:
            left = find_root(roots, left)
        if right not in roots:
            roots[right] = left
            sizes[right] = 1
        else:
            right = find_root(roots, right)
        if sizes[left] < sizes[right]:
            left, right = right, left
        # Now compress the path from right to the root.
        if left != right:     
            sizes[left] += sizes[right]
            roots[right] = left
            max_size = max(max_size, sizes[left])

        result.append(max_size)
  
    return result

print(friendcircle([[1, 2], [1, 3]]))
print(friendcircle([[1, 2], [3, 4], [2, 3]]))
print(friendcircle([
    			[6, 4],
				[5, 9],
				[8, 5],
				[4, 1],
				[1, 5],
				[7, 2],
				[4, 2],
				[7, 6],
]))