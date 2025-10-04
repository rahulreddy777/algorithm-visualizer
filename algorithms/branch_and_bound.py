from .base_solver import BaseSolver
from .greedy import GreedyTSPSolver # Needed for initial bound
import numpy as np

class BranchAndBoundTSPSolver(BaseSolver):
    """Solves TSP using a Branch and Bound algorithm."""
    def __init__(self, problem):
        super().__init__(problem)
        self.num_cities = self.problem.data.shape[0]
        self.best_tour = []
        self.upper_bound = float('inf') # Best solution found so far

    def _calculate_lower_bound(self, current_tour):
        """
        Calculates a lower bound on the tour length from the current partial tour.
        A simple bound: cost of current path + cheapest edge from each unvisited
        node to any other node.
        """
        path_cost = 0
        for i in range(len(current_tour) - 1):
            path_cost += self.problem.data[current_tour[i]][current_tour[i+1]]

        bound = path_cost
        unvisited = [city for city in range(self.num_cities) if city not in current_tour]
        
        # For the last node in the current path, find the cheapest edge to an unvisited node
        last_node = current_tour[-1]
        if unvisited:
            bound += min(self.problem.data[last_node][j] for j in unvisited)

        # For all other unvisited nodes, add the cost of their cheapest edge to any node
        # (excluding itself)
        for node in unvisited:
            min_edge = min(self.problem.data[node][j] for j in range(self.num_cities) if j != node)
            bound += min_edge / 2 # Divide by 2 as each edge is counted twice

        return bound

    def _solve_recursively(self, current_tour):
        # Pruning Step: If current path's lower bound is worse than the best tour found, stop
        lower_bound = self._calculate_lower_bound(current_tour)
        if lower_bound >= self.upper_bound:
            return

        # If tour is complete, update the upper bound
        if len(current_tour) == self.num_cities:
            tour_dist = self.problem.evaluate_solution(current_tour)
            if tour_dist < self.upper_bound:
                self.upper_bound = tour_dist
                self.best_tour = current_tour
            return

        # Branch to the next unvisited cities
        for next_city in range(self.num_cities):
            if next_city not in current_tour:
                self._solve_recursively(current_tour + [next_city])

    def _execute(self):
        # Use a greedy solution to get an initial strong upper bound
        greedy_solver = GreedyTSPSolver(self.problem)
        initial_solution = greedy_solver._execute()
        self.upper_bound = self.problem.evaluate_solution(initial_solution)
        self.best_tour = initial_solution
        
        start_city = self.problem.get_initial_state()
        self._solve_recursively([start_city])
        
        return self.best_tour