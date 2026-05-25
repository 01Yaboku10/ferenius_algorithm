import csv
from typing import Iterable
import ast
import os

def log(filename, data):
    with open(filename, "a", encoding="utf-8") as file:
        file.write(data)

def log_csv(filename, data):
    fields=["Time", "Distance", "Targets", "Route"]
    with open(filename, "a", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writerow({"Time":data[0], "Distance":data[1], "Targets":data[2], "Route":data[3]})

def csv_load(filename, mode="d"):
    times = []
    distances = []
    targets = []
    route = []
    try:
        with open(filename, mode="r", encoding="utf-8", newline="") as save:
            s_lines: Iterable = csv.reader(save, skipinitialspace=True)
            lines: list[list] = list(s_lines)
            for line in lines[1:]:
                if not line:
                    continue
                times.append(ast.literal_eval(line[0]))
                distances.append(ast.literal_eval(line[1]))
                targets.append(ast.literal_eval(line[2]))
                route.append(ast.literal_eval(line[3]))
    except FileNotFoundError:
        print(f"File '{filename}' could not be found. Returning an empty list...")
    
    if mode == "d":
        return times, distances
    else:
        return times, distances, targets, route

def csv_combine(from_file, to_file):
    for _dir in os.listdir(from_file):
        if _dir not in ["2opt", "brute", "nn",
                        "ferenius", "ferenius_v2", "ferenius_v3",
                        "ferenius_v4", "ferenius_v5", "ferenius_v6",
                        "ferenius_v7", "ferenius_v8"]:
            continue
        print(f"Reading data from {from_file}/{_dir}")
        for n in range(1, 11):
            times, distances, targets, routes = csv_load(f"{from_file}/{_dir}/{n}.csv", "combine")
            for i in range(len(times)-1):
                log_csv(f"{to_file}/{_dir}/{n}.csv", [times[i], distances[i], targets[i], routes[i]])
        print(f"{_dir} transfer complete from {from_file} to {to_file}")
    print(f"Transfer complete from {from_file} to {to_file}")

def csv_sort(dir_name):
    class Data():
        def __init__(self, time, distance, targets, route) -> None:
            self.time = time
            self.distance = distance
            self.targets = targets
            self.route = route
    
    def is_same(brute, algo):
        shortest = min(len(brute), len(algo))
        for i in range(shortest-1):
            if brute[i].targets != algo[i].targets:
                print(f"Fault at data point {i*2}. {brute[i].targets} != {algo[i].targets}")
                return False, i
        return True, 0

    data: dict[str, dict[int, list]] = {}
    new_data: dict[str, dict[int, list]] = {name: {} for name in data}
    for _dir in os.listdir(dir_name):
        if _dir not in ["2opt", "brute", "nn",
                        "ferenius", "ferenius_v2", "ferenius_v3",
                        "ferenius_v4", "ferenius_v5", "ferenius_v6",
                        "ferenius_v7", "ferenius_v8"]:
            continue
        print(f"Reading data from {dir_name}/{_dir}")
        for n in range(1, 11):
            times, distances, targets, routes = csv_load(f"{dir_name}/{_dir}/{n}.csv", "full")
            for i in range(len(times)-1):
                if data.get(_dir):
                    algo = data[_dir]
                    _n = algo.get(n)
                    if _n:
                        algo[n].append(Data(times[i], distances[i], targets[i], routes[i]))
                    else:
                        algo[n] = [Data(times[i], distances[i], targets[i], routes[i])]
                else:
                    data[_dir] = {n: [Data(times[i], distances[i], targets[i], routes[i])]}

    for n in range(3, 11):
        n_dicts = []
        for algo in data.values():
            n_dicts.append({obj.targets: obj for obj in algo[n]})
        
        common = set.intersection(*(set(d.keys()) for d in n_dicts))
        alligned = [list(d[k] for d in n_dicts) for k in common]
        for i, name in enumerate(data.keys()):
            new_data[name][n] = alligned[i]

    