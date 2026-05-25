import csv
import ast
import random
from typing import Any, Iterable
from graph import Node, Graph
import gui
import time
import numpy as np
import logger
from tqdm import tqdm
import matplotlib.pyplot as plt

def file_read(filename: str) -> Graph:
    graph: Graph = Graph()
    try:
        with open(filename, mode="r", encoding="utf-8", newline="") as save:
            s_lines: Iterable = csv.reader(save, skipinitialspace=True)
            lines: list[list] = list(s_lines)
            for n in lines[1:]:
                x, y = n[2].split()
                edges = ast.literal_eval(n[1])
                graph.node_add(n[0], edges, xpos=int(x), ypos=int(y))
    except FileNotFoundError:
        print(f"File '{filename}' could not be found. Returning an empty graph...")
    return graph

def log_read(filename: str):
    nodes = {}
    try:
        with open(filename, mode="r", encoding="utf-8") as save:
            lines = save.readlines()
            for line in lines:
                attributes = line.split(" | ")
                times = attributes[3].strip().removeprefix("(np.float64(")[:16].removesuffix(")")
                nodes[attributes[-1].removesuffix("\n")] = float(times)
    except FileNotFoundError:
        print(f"File '{filename}' could not be found. Returning an empty list...")
    return nodes

def compare():
    larger: int = 0
    smaller: int = 0
    same: int = 0
    for _ in range(1000):
        graph = file_read("nodes_v1.csv")
        graph.add_children((1, 15), "c")
        start, end = ["0","80"]
        djik, d_weight = graph.dijkstra(graph.node_get(start), graph.node_get(end))
        bfs, b_weight = graph.bfs(graph.node_get(start), graph.node_get(end))
        #print(f"Djikstra | Steps: {len(djik)}, Weight: {d_weight}, Path: {djik}")
        #print(f"BFS      | Steps: {len(bfs)}, Weight: {b_weight}, Path: {bfs}")
        if d_weight > b_weight:
            larger += 1
        if d_weight < b_weight:
            smaller += 1
        if d_weight == b_weight:
            same += 1
    print("Larger | Smaller | Same")
    print(f"   {larger}        {smaller}        {same}")

def ferenius_compare(nodes: list[int] = [5], comparisons: int = 3, draw=False):
    def calc_devi(a, b):
        """Parameters:
        - a: comparing value
        - b: optimal value
        Returns:
        - deviation"""
        deviation = (a/b)-1
        if -0.0000001 < deviation < 0.0000001:
            return 0
        return deviation
    a_time = []
    b_time = []
    c_time = []
    d_time = []
    e_time = []
    f_time = []
    g_time = []
    deviation = []
    a_acc = {}
    b_acc = {}
    c_acc = {}
    d_acc = {}
    e_acc = {}
    f_acc = {}
    g_acc = {}
    a_vars = {}
    b_vars = {}
    d_vars = {}
    e_vars = {}
    f_vars = {}
    g_vars = {}
    for n in nodes:
        v1_faster, v1_slower, v1_same = 0, 0, 0
        v2_faster, v2_slower, v2_same = 0, 0, 0
        v3_faster, v3_slower, v3_same = 0, 0, 0
        v4_faster, v4_slower, v4_same = 0, 0, 0
        v5_faster, v5_slower, v5_same = 0, 0, 0
        v6_faster, v6_slower, v6_same = 0, 0, 0
        _a_time = []
        _b_time = []
        _c_time = []
        _d_time = []
        _e_time = []
        _f_time = []
        _g_time = []
        v1_devi = []
        v2_devi = []
        v3_devi = []
        v4_devi = []
        v5_devi = []
        v6_devi = []

        for i in tqdm(range(comparisons), desc=f"Comparing Algorithms... for N={n}"):
            graph = file_read("nodes_v2.csv")
            graph.add_children()
            targets: list[str] = []
            for _ in range(n):
                while True:
                    target = str(random.randint(1, 104))
                    if target not in targets:
                        targets.append(target)
                        break
            target_nodes: list[Node] = [graph.node_get(target) for target in targets]
            start: Node = target_nodes[0]
            target_nodes.append(start)

            # Ferenius V1 -----------------------
            a_time_start = time.perf_counter()
            
            route_nodes, v1_sweep = graph.ferenius(start, target_nodes)
            route, distance = graph.create_route(route_nodes)
            a_label = "Ferenius"

            a_time_end = time.perf_counter()
            # ----------------------------------------------

            # Ferenius V2 --------------------------------
            b_time_start = time.perf_counter()
            route_nodes_xy = graph.ferenius(start, target_nodes, version=2)
            b_label = "V2"
            route_x, distance_x = graph.create_route(route_nodes_xy[0])
            route_y, distance_y = graph.create_route(route_nodes_xy[1])
            comp_r = 0
            if distance_x < distance_y:
                comp_route = route_x
                comp_dist = distance_x
            else:
                comp_route = route_y
                comp_dist = distance_y
                comp_r = 1
            b_time_end = time.perf_counter()
            # ----------------------------------------------

            # Brute --------------------------------
            c_time_start = time.perf_counter()
            c_route, c_dist, perm = graph.multi_brute(start, target_nodes[1:])
            c_label = "Brute"
            c_time_end = time.perf_counter()
            # ----------------------------------------------

            # Ferenius V3 --------------------------------
            d_time_start = time.perf_counter()
            d_route_nodes_xy = graph.ferenius(start, target_nodes, version=3)
            d_label = "V3"
            route_x, distance_x = graph.create_route(d_route_nodes_xy[0])
            route_y, distance_y = graph.create_route(d_route_nodes_xy[1])
            d_r = 0
            if distance_x < distance_y:
                d_route = route_x
                d_dist = distance_x
            else:
                d_route = route_y
                d_dist = distance_y
                d_r = 1
            d_time_end = time.perf_counter()
            # ----------------------------------------------

            # Ferenius V4 --------------------------------
            e_time_start = time.perf_counter()
            e_route_nodes_xy = graph.ferenius(start, target_nodes, version=3)
            e_label = "V4"
            route_x, distance_x = graph.create_route(e_route_nodes_xy[0], 4)
            route_y, distance_y = graph.create_route(e_route_nodes_xy[1], 4)
            e_r = 0
            if distance_x < distance_y:
                e_route = route_x
                e_dist = distance_x
            else:
                e_route = route_y
                e_dist = distance_y
                e_r = 1
            e_time_end = time.perf_counter()
            # ----------------------------------------------

            # Ferenius V5 --------------------------------
            f_time_start = d_time_start
            f_label = "V5"
            if e_dist < d_dist:
                f_route = e_route
                f_dist = e_dist
                f_r = e_r
            else:
                f_route = d_route
                f_dist = d_dist
                f_r = d_r
            f_time_end = time.perf_counter()
            # ----------------------------------------------

            # NN --------------------------------
            g_time_start = time.perf_counter()
            g_route, g_dist = graph.nn(start, target_nodes)
            g_label = "NN"
            g_time_end = time.perf_counter()
            # ----------------------------------------------

            _a_time.append(a_time_end-a_time_start)
            _b_time.append(b_time_end-b_time_start)
            _c_time.append(c_time_end-c_time_start)
            _d_time.append(d_time_end-d_time_start)
            _e_time.append(e_time_end-e_time_start)
            _f_time.append(f_time_end-f_time_start)
            _g_time.append(g_time_end-g_time_start)

            #print(comp_route, comp_dist)
            #if distance != comp_dist:
            if draw:
                gui.draw_graph(graph, comp_route, route_nodes_xy[comp_r], comp_dist, "red", comp_r, c_route, c_dist, "green", perm, e_route, e_dist, "blue", e_route_nodes_xy[e_r], e_r)
            #gui.draw_graph(graph, route, route_nodes, distance)

            # Slower, Same, Faster
            # V1
            if distance > c_dist:
                v1_slower += 1
            elif distance == c_dist:
                v1_same += 1
            else:
                v1_faster += 1
            
            # V2
            if comp_dist > c_dist:
                v2_slower += 1
            elif comp_dist == c_dist:
                v2_same += 1
            else:
                v2_faster += 1
            
            # V3
            if d_dist > c_dist:
                v3_slower += 1
            elif d_dist == c_dist:
                v3_same += 1
            else:
                v3_faster += 1

            # V4
            if e_dist > c_dist:
                v4_slower += 1
            elif e_dist == c_dist:
                v4_same += 1
            else:
                v4_faster += 1
            
            # V5
            if f_dist > c_dist:
                v5_slower += 1
            elif f_dist == c_dist:
                v5_same += 1
            else:
                v5_faster += 1

            # NN
            if g_dist > c_dist:
                v6_slower += 1
            elif g_dist == c_dist:
                v6_same += 1
            else:
                v6_faster += 1

            # Add deviations
            if (distance/c_dist)-1 != 0:
                v1_devi.append(calc_devi(distance, c_dist))
            if (comp_dist/c_dist)-1 != 0:
                v2_devi.append(calc_devi(comp_dist, c_dist))
            if (d_dist/c_dist)-1 != 0:
                v3_devi.append(calc_devi(d_dist, c_dist))
            if (e_dist/c_dist)-1 != 0:
                v4_devi.append(calc_devi(e_dist, c_dist))
            if (f_dist/c_dist)-1 != 0:
                v5_devi.append(calc_devi(f_dist, c_dist))
            if (g_dist/c_dist)-1 != 0:
                v6_devi.append(calc_devi(g_dist, c_dist))

            # Add accuracies
            if not a_acc.get(n):
                a_acc[n] = [c_dist]
            else:
                a_acc[n].append(c_dist)
            if not b_acc.get(n):
                b_acc[n] = [comp_dist]
            else:
                b_acc[n].append(comp_dist)
            if not c_acc.get(n):
                c_acc[n] = [distance]
            else:
                c_acc[n].append(distance)
            if not d_acc.get(n):
                d_acc[n] = [d_dist]
            else:
                d_acc[n].append(d_dist)
            if not e_acc.get(n):
                e_acc[n] = [e_dist]
            else:
                e_acc[n].append(e_dist)
            if not f_acc.get(n):
                f_acc[n] = [f_dist]
            else:
                f_acc[n].append(f_dist)
            if not g_acc.get(n):
                g_acc[n] = [g_dist]
            else:
                g_acc[n].append(g_dist)

            logger.log_csv(f"data/ferenius/{n}.csv", [a_time_end-a_time_start, distance, targets, route])
            logger.log_csv(f"data/ferenius_v2/{n}.csv", [b_time_end-b_time_start, comp_dist, targets, comp_route])
            logger.log_csv(f"data/ferenius_v3/{n}.csv", [d_time_end-d_time_start, d_dist, targets, d_route])
            logger.log_csv(f"data/ferenius_v4/{n}.csv", [e_time_end-e_time_start, e_dist, targets, e_route])
            logger.log_csv(f"data/ferenius_v5/{n}.csv", [f_time_end-f_time_start, f_dist, targets, f_route])
            logger.log_csv(f"data/brute/{n}.csv", [c_time_end-c_time_start, c_dist, targets, c_route])
            logger.log_csv(f"data/nn/{n}.csv", [g_time_end-g_time_start, g_dist, targets, g_route])

        if not v1_devi:
            v1_devi.append(0)
        if not v2_devi:
            v2_devi.append(0)
        if not v3_devi:
            v3_devi.append(0)
        if not v4_devi:
            v4_devi.append(0)
        if not v5_devi:
            v5_devi.append(0)
        if not v6_devi:
            v6_devi.append(0)

        print("\nFerenius-----------------------")
        print(f"Slower | Same | Faster (N={n})")
        print(f"{v1_slower}       {v1_same}    {v1_faster}")
        print(f"Average deviation: {(sum(v1_devi))/comparisons}")
        print(f"Min: {min(v1_devi)}\nMax: {max(v1_devi)}")

        print("\nFerenius V2-----------------------")
        print(f"Slower | Same | Faster (N={n})")
        print(f"{v2_slower}       {v2_same}    {v2_faster}")
        print(f"Average deviation: {(sum(v2_devi))/comparisons}")
        print(f"Min: {min(v2_devi)}\nMax: {max(v2_devi)}")

        print("\nFerenius V3-----------------------")
        print(f"Slower | Same | Faster (N={n})")
        print(f"{v3_slower}       {v3_same}    {v3_faster}")
        print(f"Average deviation: {(sum(v3_devi))/comparisons}")
        print(f"Min: {min(v3_devi)}\nMax: {max(v3_devi)}")

        print("\nFerenius V4-----------------------")
        print(f"Slower | Same | Faster (N={n})")
        print(f"{v4_slower}       {v4_same}    {v4_faster}")
        print(f"Average deviation: {(sum(v4_devi))/comparisons}")
        print(f"Min: {min(v4_devi)}\nMax: {max(v4_devi)}")

        print("\nFerenius V5-----------------------")
        print(f"Slower | Same | Faster (N={n})")
        print(f"{v5_slower}       {v5_same}    {v4_faster}")
        print(f"Average deviation: {(sum(v5_devi))/comparisons}")
        print(f"Min: {min(v5_devi)}\nMax: {max(v5_devi)}")

        print("\nNearest Neighbour-----------------------")
        print(f"Slower | Same | Faster (N={n})")
        print(f"{v6_slower}       {v6_same}    {v6_faster}")
        print(f"Average deviation: {(sum(v6_devi))/comparisons}")
        print(f"Min: {min(v6_devi)}\nMax: {max(v6_devi)}")

        a_time.append(np.mean(_a_time))
        b_time.append(np.mean(_b_time))
        c_time.append(np.mean(_c_time))
        d_time.append(np.mean(_d_time))
        e_time.append(np.mean(_e_time))
        f_time.append(np.mean(_f_time))
        g_time.append(np.mean(_g_time))
        deviation.append(np.mean(v1_devi))
        a_vars[n] = (v1_slower, v1_same, v1_faster)
        b_vars[n] = (v2_slower, v2_same, v2_faster)
        d_vars[n] = (v3_slower, v3_same, v3_faster)
        e_vars[n] = (v4_slower, v4_same, v4_faster)
        f_vars[n] = (v5_slower, v5_same, v5_faster)
        g_vars[n] = (v6_slower, v6_same, v6_faster)
        #logger.log("log.txt", f"{v1_slower, v1_same, v1_faster} | {np.mean(v1_devi)} | {min(v1_devi), max(v1_devi)} | {np.mean(_a_time), np.mean(_b_time)} | {n} | {route_nodes}\n")
    gui.draw_time(a_time, b_time, deviation, nodes, comparisons, b_label, c_time, c_label, d_time, d_label, e_time, e_label, f_time, f_label, g_time, g_label)
    gui.draw_deviation(nodes, a_acc, b_acc, b_label, a_label, c_acc, d_label, d_acc, e_label, e_acc, f_acc, f_label, g_acc, g_label)
    gui.draw_accuracy(nodes, a_vars, b_vars, "Ferenius", b_label, d_vars, d_label, e_vars, e_label, f_vars, f_label, g_vars, g_label)

def algo_compare(nodes: list[int] = [5], comparisons: int = 3, draw=False):
    def calc_devi(a, b):
        """Parameters:
        - a: comparing value
        - b: optimal value
        Returns:
        - deviation"""
        deviation = (a/b)-1
        if -0.0000001 < deviation < 0.0000001:
            return 0
        return deviation
    a_time = []
    b_time = []
    c_time = []
    a_acc = {}
    b_acc = {}
    c_acc = {}
    b_vars = {}
    c_vars = {}
    for n in nodes:
        v1_faster, v1_slower, v1_same = 0, 0, 0
        v2_faster, v2_slower, v2_same = 0, 0, 0
        _a_time = []
        _b_time = []
        _c_time = []
        v1_devi = []
        v2_devi = []

        for i in tqdm(range(comparisons), desc=f"Comparing Algorithms... for N={n}"):
            graph = file_read("nodes_v2.csv")
            graph.add_children()
            targets: list[str] = []
            for _ in range(n):
                while True:
                    target = str(random.randint(1, 104))
                    if target not in targets:
                        targets.append(target)
                        break
            target_nodes: list[Node] = [graph.node_get(target) for target in targets]
            start: Node = target_nodes[0]
            target_nodes.append(start)

            # Brute --------------------------------
            a_time_start = time.perf_counter()
            if n < 7:
                a_route, a_dist, perm = graph.brute(start, target_nodes[1:])
            else:
                a_route, a_dist, perm = graph.multi_brute(start, target_nodes[1:])
            a_label = "Brute"
            a_time_end = time.perf_counter()
            # ----------------------------------------------

            # Ferenius V7 --------------------------------
            #b_time_start = time.perf_counter()
            #b_route_nodes_xy = graph.ferenius(start, target_nodes, version=2)
            #b_label = "V7"
            #route_x, distance_x = graph.create_route(b_route_nodes_xy[0], 7)
            #route_y, distance_y = graph.create_route(b_route_nodes_xy[1], 7)
            #b_r = 0
            #if distance_x < distance_y:
            #    b_route = route_x
            #    b_dist = distance_x
            #else:
            #    b_route = route_y
            #    b_dist = distance_y
            #    b_r = 1
            #b_time_end = time.perf_counter()
            # ----------------------------------------------

            # 2-opt --------------------------------
            b_time_start = time.perf_counter()
            b_label = "2-opt"
            b_route_nodes = graph.sep_two_opt(start, target_nodes)
            b_route, b_dist = graph.create_route(b_route_nodes)
            b_route_nodes_xy = b_route_nodes, b_route_nodes
            b_r = 0
            b_time_end = time.perf_counter()
            # ----------------------------------------------


            # Ferenius V2 --------------------------------
            c_time_start = time.perf_counter()
            c_route_nodes_xy = graph.ferenius(start, target_nodes, version=2)
            c_label = "V2"
            route_x, distance_x = graph.create_route(c_route_nodes_xy[0])
            route_y, distance_y = graph.create_route(c_route_nodes_xy[1])
            c_r = 0
            if distance_x < distance_y:
                c_route = route_x
                c_dist = distance_x
            else:
                c_route = route_y
                c_dist = distance_y
                c_r = 1
            c_time_end = time.perf_counter()
            # ----------------------------------------------

            # NN --------------------------------
            #c_time_start = time.perf_counter()
            #c_route, c_dist = graph.nn(start, target_nodes)
            #c_label = "NN"
            #c_time_end = time.perf_counter()
            # ----------------------------------------------

            _a_time.append(a_time_end-a_time_start)
            _b_time.append(b_time_end-b_time_start)
            _c_time.append(c_time_end-c_time_start)

            #print(comp_route, comp_dist)
            #if distance != comp_dist:
            if draw:
                gui.draw_graph(graph, b_route, b_route_nodes_xy[b_r], b_dist, "red", b_r, a_route, a_dist, "green", perm, c_route, c_dist, "blue", c_route_nodes_xy[c_r], c_r)
            #gui.draw_graph(graph, route, route_nodes, distance)

            # Slower, Same, Faster
            # V1
            if b_dist > a_dist:
                v1_slower += 1
            elif b_dist == a_dist:
                v1_same += 1
            else:
                v1_faster += 1
            
            # V2
            if c_dist > a_dist:
                v2_slower += 1
            elif c_dist == a_dist:
                v2_same += 1
            else:
                v2_faster += 1

            # Add deviations
            if (b_dist/a_dist)-1 != 0:
                v1_devi.append(calc_devi(b_dist, a_dist))
            if (c_dist/a_dist)-1 != 0:
                v2_devi.append(calc_devi(c_dist, a_dist))

            # Add accuracies
            if not a_acc.get(n):
                a_acc[n] = [a_dist]
            else:
                a_acc[n].append(a_dist)
            if not b_acc.get(n):
                b_acc[n] = [b_dist]
            else:
                b_acc[n].append(b_dist)
            if not c_acc.get(n):
                c_acc[n] = [c_dist]
            else:
                c_acc[n].append(c_dist)

        if not v1_devi:
            v1_devi.append(0)
        if not v2_devi:
            v2_devi.append(0)

        print("\nAlgorithm 1-----------------------")
        print(f"Slower | Same | Faster (N={n})")
        print(f"{v1_slower}       {v1_same}    {v1_faster}")
        print(f"Average deviation: {(sum(v1_devi))/comparisons}")
        print(f"Min: {min(v1_devi)}\nMax: {max(v1_devi)}")

        print("\nAlgorithm 2-----------------------")
        print(f"Slower | Same | Faster (N={n})")
        print(f"{v2_slower}       {v2_same}    {v2_faster}")
        print(f"Average deviation: {(sum(v2_devi))/comparisons}")
        print(f"Min: {min(v2_devi)}\nMax: {max(v2_devi)}")

        a_time.append(np.mean(_a_time))
        b_time.append(np.mean(_b_time))
        c_time.append(np.mean(_c_time))
        b_vars[n] = (v1_slower, v1_same, v1_faster)
        c_vars[n] = (v2_slower, v2_same, v2_faster)
        logger.log("log.txt", f"{v1_slower, v1_same, v1_faster} | {np.mean(v1_devi)} | {min(v1_devi), max(v1_devi)} | {np.mean(_a_time), np.mean(_b_time)} | {n} | {a_route}\n")
    deviation = 0
    gui.draw_time(b_time, c_time, deviation, nodes, comparisons, c_label)
    gui.draw_deviation(nodes, a_acc, b_acc, b_label, c_label, c_acc)
    gui.draw_accuracy(nodes, b_vars, c_vars, b_label, c_label)

def graph_file():
    nodes_1 = log_read("log_comp50_3-10.txt")
    nodes_2 = log_read("log_comp50_3-10_v2.txt")
    gui.draw_time(nodes_1.values(), nodes_2.values(), [0], nodes_1.keys(), 50, "Ferenius v2")

def load_tot():
    data: dict[int, dict[str, list[list[float], list[float], list[float], int]]] = {}
    for file in ["brute", "ferenius", "ferenius_v2", "ferenius_v3", "ferenius_v4", "ferenius_v5", "nn"]:
        for n in range(3, 11):
            times, distances = logger.csv_load(f"data_500/{file}/{n}.csv")
            #print(data)
            if file != "brute":
                brute_dist = np.array(data[n]["brute"][0][1])
                file_dist = np.array(distances)
                deviations = (file_dist - brute_dist) / brute_dist
                opt = 0
                for devi in deviations:
                    if devi < 0.0001:
                        opt += 1
            else:
                deviations = np.zeros_like(times)
                opt = len(times)
            if data.get(n):
                n_dict = data.get(n)
                if n_dict.get(file):
                    n_dict[file].append([times, distances, deviations, opt])
                else:
                    n_dict[file] = [[times, distances, deviations, opt]]
            else:
                data[n] = {file: [[times, distances, deviations, opt]]}
    
    # Times:
    time_brute = [np.mean(algos["brute"][0][0]) for algos in data.values()]
    time_nn = [np.mean(algos["nn"][0][0]) for algos in data.values()]
    time_ferenius = [np.mean(algos["ferenius"][0][0]) for algos in data.values()]
    time_ferenius_v2 = [np.mean(algos["ferenius_v2"][0][0]) for algos in data.values()]
    time_ferenius_v3 = [np.mean(algos["ferenius_v3"][0][0]) for algos in data.values()]
    time_ferenius_v4 = [np.mean(algos["ferenius_v4"][0][0]) for algos in data.values()]
    time_ferenius_v5 = [np.mean(algos["ferenius_v5"][0][0]) for algos in data.values()]
    gui.draw_time(time_ferenius, time_ferenius_v2, 0, range(3, 11), len(data[10]["brute"][0][0]), "Ferenius V2", time_brute, "Brute", time_ferenius_v3, "Ferenius V3", time_ferenius_v4, "Ferenius V4", time_ferenius_v5, "Ferenius V5", time_nn, "Nearest Neighbor")
    
    # Deviations:
    devi_nn = [np.mean(algos["nn"][0][2])*100 for algos in data.values()]
    devi_ferenius = [np.mean(algos["ferenius"][0][2])*100 for algos in data.values()]
    devi_ferenius_v2 = [np.mean(algos["ferenius_v2"][0][2])*100 for algos in data.values()]
    devi_ferenius_v3 = [np.mean(algos["ferenius_v3"][0][2])*100 for algos in data.values()]
    devi_ferenius_v4 = [np.mean(algos["ferenius_v4"][0][2])*100 for algos in data.values()]
    devi_ferenius_v5 = [np.mean(algos["ferenius_v5"][0][2])*100 for algos in data.values()]
    plt.figure()
    x = range(3, 11)
    plt.plot(x, devi_ferenius, marker="o", label="Ferenius", color="blue")
    plt.plot(x, devi_ferenius_v2, marker="s", label="Ferenius V2", color="orange")
    plt.plot(x, devi_ferenius_v3, marker="x", label="Ferenius V3", color="red")
    plt.plot(x, devi_ferenius_v4, marker="h", label="Ferenius V4", color="purple")
    plt.plot(x, devi_ferenius_v5, marker="D", label="Ferenius V5", color="olive")
    plt.plot(x, devi_nn, marker="d", label="Nearest Neighbor", color="magenta")
    plt.xlabel("Input Size (N)")
    plt.ylabel("Deviation from optimal route in %")
    plt.title("Deviation from optimal route in %")
    plt.legend()
    plt.tight_layout()
    plt.grid(True)
    plt.show()

    # Optimality:
    acc_nn = [algos["nn"][0][3]/algos["brute"][0][3] for algos in data.values()]
    acc_ferenius = [algos["ferenius"][0][3]/algos["brute"][0][3] for algos in data.values()]
    acc_ferenius_v2 = [algos["ferenius_v2"][0][3]/algos["brute"][0][3] for algos in data.values()]
    acc_ferenius_v3 = [algos["ferenius_v3"][0][3]/algos["brute"][0][3] for algos in data.values()]
    acc_ferenius_v4 = [algos["ferenius_v4"][0][3]/algos["brute"][0][3] for algos in data.values()]
    acc_ferenius_v5 = [algos["ferenius_v5"][0][3]/algos["brute"][0][3] for algos in data.values()]
    plt.figure()
    plt.plot(x, acc_ferenius, marker="o", label="Ferenius", color="blue")
    plt.plot(x, acc_ferenius_v2, marker="s", label="Ferenius V2", color="orange")
    plt.plot(x, acc_ferenius_v3, marker="x", label="Ferenius V3", color="red")
    plt.plot(x, acc_ferenius_v4, marker="h", label="Ferenius V4", color="purple")
    plt.plot(x, acc_ferenius_v5, marker="D", label="Ferenius V5", color="olive")
    plt.plot(x, acc_nn, marker="d", label="Nearest Neighbor", color="magenta")
    plt.xlabel("Input Size (N)")
    plt.ylabel("Achieved optimal route in  %")
    plt.title("Achieved optimal route in  %")
    plt.legend()
    plt.tight_layout()
    plt.grid(True)
    plt.show()

def run_ferenius(nodes: int):
    graph = file_read("nodes_v2.csv")
    graph.add_children()
    targets: list[str] = []
    for _ in range(nodes):
        while True:
            target = str(random.randint(1, 104))
            if target not in targets:
                targets.append(target)
                break
    target_nodes: list[Node] = [graph.node_get(target) for target in targets]
    start: Node = target_nodes[0]
    target_nodes.append(start)

    # Ferenius V4 --------------------------------
    e_time_start = time.perf_counter()
    e_route_nodes_xy = graph.ferenius(start, target_nodes, version=3)
    e_label = "V4"
    route_x, distance_x = graph.create_route(e_route_nodes_xy[0], 4)
    route_y, distance_y = graph.create_route(e_route_nodes_xy[1], 4)
    e_r = 0
    if distance_x < distance_y:
        e_route = route_x
        e_dist = distance_x
    else:
        e_route = route_y
        e_dist = distance_y
        e_r = 1
    e_time_end = time.perf_counter()
    print(e_time_end-e_time_start)
    # ----------------------------------------------
    gui.draw_graph(graph, e_route, e_route_nodes_xy[e_r], e_dist, "red")

def main():
    ferenius_compare(range(3, 11), 10, False)
    #logger.csv_combine("data_100", "data_500")
    #logger.csv_sort("data_500")
    #algo_compare(range(3, 8), 15, False)
    #run_ferenius(30)
    #graph_file()
    #load_tot()
if __name__ == "__main__":
    main()
