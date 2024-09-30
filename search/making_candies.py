import math

def minimumPasses(machines, workers, price, target):
    if target <= price: return math.ceil(target / (machines * workers))

    candies = 0
    iterations = 0
    current = float('inf')

    while candies < target:
        # Keep producing candy until you can actually buy something.
        # If you've spend too many candies, you'll have to use some
        # cycles.
        if candies < price:
            i = math.ceil((price - candies) / (machines * workers))
            iterations += i
            candies += machines * workers * i
            # Check again if candies < target.
            continue

        # Spend all the candies you can.
        purchased, candies = divmod(candies, price)
        assets = machines + workers + purchased
        half = assets // 2

        # We want to keep machines & workers equal.
        # So add workers first, if there are currently
        # fewer workers than machines, and v.v.
        if machines > workers :
            machines = max(machines, half)
            workers = assets - machines
        else:
            workers = max(workers, half)
            machines = assets - workers

        iterations += 1
        candies += machines * workers
        # How many more iterations would you need if you spent no more candy?
        current = min(current, iterations + math.ceil((target - candies) / (machines * workers)))

    return min(current, iterations)

# 3
print(minimumPasses(3, 1, 2, 12)) 
#16 
print(minimumPasses(1, 1, 6, 45))
#1
print(minimumPasses(5184889632, 5184889632, 20, 10000))