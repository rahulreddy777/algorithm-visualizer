import matplotlib
matplotlib.use('Agg')  # required for server

import matplotlib.pyplot as plt
import numpy as np
import os
from flask import Flask, send_file

from problems.tsp import TSP
from problems.knapsack import KnapsackProblem
from algorithms.greedy import GreedyTSPSolver, GreedyKnapsackSolver
from algorithms.backtracking import BacktrackingTSPSolver
from algorithms.dynamic_programming import DPKnapsackSolver
from algorithms.branch_and_bound import BranchAndBoundTSPSolver

app = Flask(__name__)   # 🔥 REQUIRED


# --- Helper function ---
def get_data_path(*subpaths):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "data", *subpaths)


# --- Experiment ---
def run_experiment(problem_instance, solvers):
    all_results = {}
    for name, solver_class in solvers.items():
        solver = solver_class(problem_instance)
        results = solver.solve()
        all_results[name] = results
    return all_results


# --- Plot ---
def plot_results(results, title):
    labels = list(results.keys())
    times = [res['execution_time'] for res in results.values()]
    qualities = [res['objective_value'] for res in results.values()]

    x = np.arange(len(labels))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    ax1.bar(x, qualities)
    ax1.set_title("Quality")

    ax2.bar(x, times)
    ax2.set_title("Time")

    filename = "output.png"
    plt.savefig(filename)
    plt.close()

    return filename


# 🔥 ROUTE (this runs in browser)
@app.route("/")
def home():
    tsp_path = get_data_path("tsp_datasets", "sample.txt")
    tsp_problem = TSP(tsp_path)

    tsp_solvers = {
        'Greedy': GreedyTSPSolver,
        'Backtracking': BacktrackingTSPSolver,
        'Branch & Bound': BranchAndBoundTSPSolver
    }

    results = run_experiment(tsp_problem, tsp_solvers)
    img = plot_results(results, "TSP")

    return send_file(img, mimetype='image/png')


# local run
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
