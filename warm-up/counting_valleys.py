def countingValleys(steps, path):
    profile = [0]
    elevation = 0
    for step in path:
        if step == 'U':
            elevation += 1
        else:
            elevation -= 1
        profile.append(elevation)
    valleys = 0
    mountains = 0
    # Compare adjacent elevations.
    for l, r in zip(profile, profile[1:]):
        if r != 0:
            continue
        # We just came off a mountain.
        if l > 0:
            mountains += 1
        else:
            valleys += 1
    return valleys

# sample
print(countingValleys(8, 'UDDDUDUU'))
        
# Test Case 2
print(countingValleys(10, 'UDUUUDUDDD'))
        