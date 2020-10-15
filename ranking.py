import pandas as pd 
import csv
import sys
import random

ROUNDS = 1000

def read_data(filename):
    roster = {}
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            student = list(row.values())
            roster[student[0]] = student[1:]
    return roster

def rank(roster, num_groups):
    groups = {choice: list() for choice in choices}
    order = list(roster.keys())
    random.shuffle(order)
    for student in order:
        assigned = False
        for choice in roster[student]:
            if len(groups[choice]) < len(roster) // num_groups:
                assigned = True
                groups[choice].append(student)
                break
        if not assigned:
            smallest_group = sorted(groups.keys(), key=lambda x: len(groups[x]))[0]
            groups[smallest_group].append(student)
    return groups

def evaluate(assignment):
    loss = 0
    for key, value in assignment.items():
        for student in value:
            try:
                loss += roster[student].index(key)
            except ValueError:
                loss += num_groups
    return loss

def run_sort():
    assignment = rank(roster, num_groups)
    for ROUND in range(ROUNDS):
        new_assignment = rank(roster, num_groups)
        old_loss, new_loss = evaluate(assignment), evaluate(new_assignment)
        if new_loss < old_loss:
            print(f"GOING FROM LOSS OF {old_loss} to {new_loss}")
            assignment = new_assignment

    print([len(x) for x in assignment.values()])
    data = pd.DataFrame.from_dict(assignment)
    data.to_csv("rankings.csv", index=False)

if __name__ == '__main__':
    num_groups = int(sys.argv[2])
    roster = read_data(sys.argv[1])
    choices = set(sorted(rank for ranks in roster.values() for rank in ranks))
    run_sort()
