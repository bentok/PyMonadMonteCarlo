import random
from pymonad import Just, curry

def dice():
    return (random.randint(1,6), random.randint(1,6))

@curry
def come_out_roll(dice, status):
    d = dice()
    if sum(d) in (7, 11):
        return Just(('win', sum(d), [d]))
    elif sum(d) in (2, 3, 12):
        return Just(('lose', sum(d), [d]))
    else:
        return Just(('point', sum(d), [d]))

@curry
def point_roll(dice, status):
    prev, point, so_far = status
    if prev != 'point':
        return Just(status)
    d = dice()
    if sum(d) == 7:
        return Just(('craps', point, so_far+[d]))
    elif sum(d) == point:
        return Just(('win', point, so_far+[d]))
    else:
        return (
            Just(('point', point, so_far+[d]))
            >> point_roll(dice)
        )

def craps():
    return (
        Just(('', 0, [])) >> come_out_roll(dice)
                          >> point_roll(dice)
    )

def main():
    print(craps())

if __name__ == "__main__":
    main()