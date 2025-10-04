# --- 1. All Imports at the Top ---
import matplotlib.pyplot as plt
import numpy as np
import os

from problems.tsp import TSP
from problems.knapsack import KnapsackProblem
from algorithms.greedy import GreedyTSPSolver, GreedyKnapsackSolver
from algorithms.backtracking import BacktrackingTSPSolver
from algorithms.dynamic_programming import DPKnapsackSolver
from algorithms.branch_and_bound import BranchAndBoundTSPSolver


# --- Helper function to always resolve correct data path ---
def get_data_path(*subpaths):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "data", *subpaths)


# --- 2. The Experiment Runner Function (Modified to return results) ---
def run_experiment(problem_instance, solvers):
    """Runs a set of solvers on a given problem and returns the results."""
    print(f"--- Running Experiment on {problem_instance.data_path} ---")

    all_results = {}
    for name, solver_class in solvers.items():
        solver = solver_class(problem_instance)
        results = solver.solve()
        all_results[name] = results

        # We still print the details for clarity
        solution_value = results['objective_value']
        time_taken = results['execution_time']
        print(f"\nAlgorithm: {name}")
        print(f"  - Solution Quality: {solution_value:.2f}")
        print(f"  - Execution Time: {time_taken:.6f} seconds")

    print("--------------------------------------------------\n")
    return all_results


# --- 3. Visualization Function ---
def plot_results(results, title):
    """Creates bar charts to compare algorithm performance."""
    labels = list(results.keys())
    times = [res['execution_time'] for res in results.values()]
    qualities = [res['objective_value'] for res in results.values()]

    x = np.arange(len(labels))
    width = 0.35

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle(title, fontsize=16)

    # Plot for Solution Quality
    ax1.bar(x, qualities, width, label='Solution Quality', color='skyblue')
    ax1.set_ylabel('Objective Value (e.g., Distance or Value)')
    ax1.set_title('Comparison of Solution Quality')
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=45, ha="right")
    ax1.legend()

    # Plot for Execution Time
    ax2.bar(x, times, width, label='Execution Time', color='salmon')
    ax2.set_ylabel('Time (seconds)')
    ax2.set_title('Comparison of Execution Time')
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels, rotation=45, ha="right")
    ax2.legend()
    ax2.set_yscale('log')

    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()


# --- 4. Main Execution Block (Fixed) ---
if __name__ == "__main__":
    # --- TSP Experiment ---
    print("========= TSP EXPERIMENT =========")
    tsp_path = get_data_path("tsp_datasets", "sample.txt")
    tsp_problem = TSP(tsp_path)
    tsp_solvers = {
        'Greedy': GreedyTSPSolver,
        'Backtracking': BacktrackingTSPSolver,
        'Branch & Bound': BranchAndBoundTSPSolver
    }
    tsp_results = run_experiment(tsp_problem, tsp_solvers)
    plot_results(tsp_results, 'TSP Performance Comparison')

    # --- Knapsack Experiment ---
    print("\n========= KNAPSACK EXPERIMENT =========")
    knapsack_path = get_data_path("knapsack_datasets", "sample1.json")
    knapsack_problem = KnapsackProblem(knapsack_path)
    knapsack_solvers = {
        'Greedy': GreedyKnapsackSolver,
        'Dynamic Prog.': DPKnapsackSolver
    }
    knapsack_results = run_experiment(knapsack_problem, knapsack_solvers)
    plot_results(knapsack_results, 'Knapsack Performance Comparison')
