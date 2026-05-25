import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm
import numpy as np

def draw_graph(graph, path=None, targets=None, distance=0, color="r", a_sweep=None, comp_path=None, comp_dist=0, comp_color="green", comp_targets=None, c_path = None, c_dist=0, c_color="blue", c_targets=None, c_sweep=None):
    def split_route(route, targets):
        if not route or not targets:
            return []

        segments = []
        target_index = 0
        current_segment = []

        for node in route:
            current_segment.append(node)

            # When we reach the next target (but not the first one),
            # we close the segment.
            if (
                target_index + 1 < len(targets)
                and node == targets[target_index + 1]
            ):
                segments.append(current_segment)
                current_segment = [node]
                target_index += 1

        # Append final segment
        if current_segment:
            segments.append(current_segment)

        return segments
    plt.figure()

    # Draw base graph
    for node in graph.nodes.values():
        for nbr in node.edges:
            if id(node) < id(nbr):
                plt.plot(
                    [node.xpos, nbr.xpos],
                    [node.ypos, nbr.ypos],
                    color="lightgray",
                    linewidth=1
                )

    # Split route
    segments = split_route(path, targets)

    if color == "r":
        # Generate distinct colors
        cmap = cm.get_cmap("tab10", len(segments))

        for i, segment in enumerate(segments):
            color = cmap(i)

            for u, v in zip(segment, segment[1:]):
                plt.plot(
                    [u.xpos, v.xpos],
                    [u.ypos, v.ypos],
                    color=color,
                    linewidth=3
                )
    else:
        for segment in segments:

            for u, v in zip(segment, segment[1:]):
                plt.plot(
                    [u.xpos, v.xpos],
                    [u.ypos, v.ypos],
                    color=color,
                    linewidth=3
                )

    # Comp Route
    if comp_path:
        segments = split_route(comp_path, comp_targets)
        for segment in segments:

                for u, v in zip(segment, segment[1:]):
                    plt.plot(
                        [u.xpos, v.xpos],
                        [u.ypos, v.ypos],
                        color=comp_color,
                        linewidth=3
                    )
    if c_path:
        segments = split_route(c_path, c_targets)
        for segment in segments:

                for u, v in zip(segment, segment[1:]):
                    plt.plot(
                        [u.xpos, v.xpos],
                        [u.ypos, v.ypos],
                        color=c_color,
                        linewidth=3
                    )


    # Draw nodes (all same color)
    for node in graph.nodes.values():
        if node in targets:
            plt.scatter(node.xpos, node.ypos, color="red", s=60)
        else:
            plt.scatter(node.xpos, node.ypos, color="black", s=60)
        plt.text(node.xpos, node.ypos, str(node.prefix),
                 ha='right', va='bottom')

    plt.axis("equal")
    plt.axis("off")
    plt.title(f"Total distance: A:{distance}\nTotal distance: B:{c_dist}\n(Optimal Distance: {comp_dist})")
    plt.text(
        0.02, 0.98,
        f"Path A Path: {path}\nPath B Path: {c_path}\nPath C Path: {comp_path}",
        transform=plt.gca().transAxes,   # use axis coordinates
        verticalalignment='top',
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
    )
    plt.text(
        0.02, 0.92,
        f"A Targets: {targets}\nB Targets: {c_targets}\nOptimal Targets: {comp_targets}",
        transform=plt.gca().transAxes,   # use axis coordinates
        verticalalignment='top',
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
    )
    if type(a_sweep) == int:
        a_sweep = "x" if a_sweep == 0 else "y"
    if type(c_sweep) == int:
        c_sweep = "x" if c_sweep == 0 else "y"
    plt.text(
        0.02, 0.86,
        f"A Sweep: {a_sweep}\nB Sweep: {c_sweep}",
        transform=plt.gca().transAxes,   # use axis coordinates
        verticalalignment='top',
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
    )
    plt.show()

def draw_time(time_a, time_b, deviation, nodes, comparisons, b_label="Brute", time_c=None, c_label=None, time_d=None, d_label=None, time_e=None, e_label=None, time_f=None, f_label=None, time_g=None, g_label=None, time_h=None, h_label=None, time_i=None, i_label=None):
    plt.figure()

    if time_c:
        plt.plot(nodes, time_c, marker='x', label=c_label, color="green")
    plt.plot(nodes, time_a, marker='o', label="Ferenius", color="blue")
    plt.plot(nodes, time_b, marker='s', label=b_label, color="orange")
    if time_d:
        plt.plot(nodes, time_d, marker='x', label=d_label, color="red")
    if time_e:
        plt.plot(nodes, time_e, marker='h', label=e_label, color="purple")
    if time_f:
        plt.plot(nodes, time_f, marker='D', label=f_label, color="olive")
    if time_g:
        plt.plot(nodes, time_g, marker='d', label=g_label, color="magenta")
    if time_h:
        plt.plot(nodes, time_h, marker='d', label=h_label, color="gold")
    if time_i:
        plt.plot(nodes, time_i, marker='d', label=i_label, color="darkred")

    plt.xlabel("Input Size (N)")
    plt.ylabel("Execution Time (seconds)")
    plt.title(f"Runtime as a Function of Target Nodes ({comparisons} comparisons)")
    plt.legend()

    plt.yscale("log")

    plt.tight_layout()
    plt.grid(True)
    plt.show()

    #plt.figure()
    #plt.plot(nodes, deviation, marker='x', label="Deviation")
    #plt.xlabel("Input Size (N)")
    #plt.ylabel("Average Deviation %")
    #plt.title(f"Average Deviation % as a Function of Target Nodes ({comparisons} comparisons)")
    #plt.legend()

    #plt.yscale("log")

    #plt.tight_layout()
    #plt.grid(True)
    #plt.show()

def draw_deviation(n, a: dict[int, list[float]], b: dict[int, list[float]], b_label, c_label = None, c = None, d_label = None, d = None, e_label = None, e = None, f = None, f_label = None, g = None, g_label = None):
    """
    Parameters:
    - n: Amount of nodes
    - a: Dictionary where the int is the amount of nodes, and the value is a list of distances
    - b: Dictionary where the int is the amount of nodes, and the value is a list of distances
    - c: Dictionary where the int is the amount of nodes, and the value is a list of distances
    """
    optimal = [1 for _ in n]
    if not c:
        c = {ns: [] for ns in a.keys()}
    if not d:
        d = {ns: [] for ns in a.keys()}
    if not e:
        e = {ns: [] for ns in a.keys()}
    if not f:
        f = {ns: [] for ns in a.keys()}
    if not g:
        g = {ns: [] for ns in a.keys()}
    b_devi = []
    c_devi = []
    d_devi = []
    e_devi = []
    f_devi = []
    g_devi = []
    distances = {}
    for o_n in a.keys():
        distances[o_n] = (a[o_n], b[o_n], c[o_n], d[o_n], e[o_n], f[o_n], g[o_n])
    for key, (o_dist, b_dist, c_dist, d_dist, e_dist, f_dist, g_dist) in distances.items():
        _b_devi = []
        _c_devi = []
        _d_devi = []
        _e_devi = []
        _f_devi = []
        _g_devi = []
        for i, dist in enumerate(o_dist):
            if b_dist:
                _b_devi.append(b_dist[i]/dist - 1)
            if c_dist:
                _c_devi.append(c_dist[i]/dist - 1)
            if d_dist:
                _d_devi.append(d_dist[i]/dist - 1)
            if e_dist:
                _e_devi.append(e_dist[i]/dist - 1)
            if f_dist:
                _f_devi.append(f_dist[i]/dist - 1)
            if g_dist:
                _g_devi.append(g_dist[i]/dist - 1)
        b_devi.append(np.mean(_b_devi))
        c_devi.append(np.mean(_c_devi))
        d_devi.append(np.mean(_d_devi))
        e_devi.append(np.mean(_e_devi))
        f_devi.append(np.mean(_f_devi))
        g_devi.append(np.mean(_g_devi))
    plt.figure()

    #plt.plot(n, optimal, marker='o', label="Optimal")
    if c_devi:
        plt.plot(n, c_devi, marker='o', label=c_label, color="blue")
    if b_devi:
        plt.plot(n, b_devi, marker='s', label=b_label, color="orange")
    if d_devi:
        plt.plot(n, d_devi, marker='x', label=d_label, color="red")
    if e_devi:
        plt.plot(n, e_devi, marker='h', label=e_label, color="purple")
    if f_devi:
        plt.plot(n, f_devi, marker='D', label=f_label, color="olive")
    if g_devi:
        plt.plot(n, g_devi, marker='d', label=g_label, color="cyan")

    plt.xlabel("Input Size (N)")
    plt.ylabel("Average Deviation %")
    plt.title("Devation from Optimal solution of methods.")
    plt.legend()

    #plt.yscale("log")

    plt.tight_layout()
    plt.grid(True)
    plt.show()

def draw_accuracy(n, a: dict[int, tuple[int, int, int]], b: dict[int, tuple[int, int, int]], a_label, b_label, c=None, c_label=None, d=None, d_label=None, e=None, e_label=None, f=None, f_label=None, g=None, g_label=None, h=None, h_label= None):
    a_same = [vars[1]/sum(vars) for vars in a.values()]
    b_same = [vars[1]/sum(vars) for vars in b.values()]
    if c:
        c_same = [vars[1]/sum(vars) for vars in c.values()]
    if d:
        d_same = [vars[1]/sum(vars) for vars in d.values()]
    if e:
        e_same = [vars[1]/sum(vars) for vars in e.values()]
    if f:
        f_same = [vars[1]/sum(vars) for vars in f.values()]
    if g:
        g_same = [vars[1]/sum(vars) for vars in g.values()]
    if h:
        h_same = [vars[1]/sum(vars) for vars in h.values()]

    plt.figure()

    plt.plot(n, a_same, marker='o', label=a_label, color="blue")
    plt.plot(n, b_same, marker='s', label=b_label, color="orange")
    if c:
        plt.plot(n, c_same, marker='x', label=c_label, color="red")
    if d:
        plt.plot(n, d_same, marker='h', label=d_label, color="purple")
    if e:
        plt.plot(n, e_same, marker='D', label=e_label, color="olive")
    if f:
        plt.plot(n, f_same, marker='d', label=f_label, color="magenta")
    if g:
        plt.plot(n, f_same, marker='d', label=g_label, color="gold")
    if h:
        plt.plot(n, f_same, marker='d', label=h_label, color="darkred")

    plt.xlabel("Input Size (N)")
    plt.ylabel("Exact Optimal Routes in %")
    plt.title("Amount of Exact Optimal Routes in %")
    plt.legend()

    #plt.yscale("log")

    plt.tight_layout()
    plt.grid(True)
    plt.show()

def draw_max_devi():
    pass

def update_dji(graph, frames):
    fig, ax = plt.subplots()
    def all_nbrs_visited(node, visited):
        return all(nbr in visited for nbr in node.edges)
    def update(frame_idx):
        ax.clear()
        frame = frames[frame_idx]

        current = frame["current"]
        visited = frame["visited"]

        # Draw edges
        for node in graph.nodes.values():
            for nbr in node.edges:
                x1, y1 = node.xpos, node.ypos
                x2, y2 = nbr.xpos, nbr.ypos
                ax.plot([x1, x2], [y1, y2], linewidth=1, color="black")

        # Draw nodes
        for node in graph.nodes.values():
            x, y = node.xpos, node.ypos

            if node == current:
                color = "blue"  # currently exploring

            elif node in visited:
                if all_nbrs_visited(node, visited):
                    color = "green"
                else:
                    color = "orange"

            else:
                color = "gray"

            ax.scatter(x, y, color=color, s=80)

        ax.set_title(f"Step {frame_idx}")

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=len(frames),
        interval=500
    )

    plt.show()