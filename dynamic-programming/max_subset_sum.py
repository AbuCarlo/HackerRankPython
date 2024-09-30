def maxSubsetSum(a):
    far = 0
    near = 0
    for n in a:
        if n <= 0:
            far = max(far, near)
        else:
            # "far" is now far, so we can assign it
            # to "near". We can bump "near".
            near, far =  (far + n, max(far, near))
    return max(far, near)