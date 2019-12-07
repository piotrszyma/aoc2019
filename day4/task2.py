pswd_min, pswd_max = 264793, 803935


def meets_criteria(num):
    num = str(num)
    adjacent = False
    for l, r in zip(num[:-1], num[1:]):
        if int(l) > int(r):
            return False
        if l == r and not adjacent and num.count(l) == 2:
            adjacent = True
    return adjacent


print(sum(1 for num in range(pswd_min, pswd_max + 1) if meets_criteria(num)))
