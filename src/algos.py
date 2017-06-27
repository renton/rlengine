from random import randint, choice, random
from bisect import bisect

def roll(num, sides, modifier = 0):
    total = 0
    for i in range(num):
        if sides <= 1:
            total += 1
        else:
            total += randint(1, sides)
    return total + modifier

# http://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice
def weighted_choice(choices):
    values, weights = zip(*choices)
    total = 0
    cum_weights = []
    for w in weights:
        total += w
        cum_weights.append(total)
    x = random() * total
    i = bisect(cum_weights, x)
    return values[i]

def perc_pass(percent):
    return randint(1, 100) <= percent

def perc_bound(value):
    if value > 100:
        return 100
    if value < 0:
        return 0
    return value
