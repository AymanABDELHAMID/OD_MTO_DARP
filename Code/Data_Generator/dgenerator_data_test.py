import re

second_part = False
costs = []


with open("data/darp_instances/RL_DARP/RL_d01.txt", "r") as f:
    for line in f.readlines()[4:]:
        if line[0] == "*":
            second_part = True
        if not second_part:
            line_numbers = list(re.split('\s+', line))
            line_numbers.pop(0)
            line_numbers.pop()
            costs.append([int(n) for n in line_numbers])

print(costs)
