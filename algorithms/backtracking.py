from .base_solver import BaseSolver
import sys

class BacktrackingTSPSolver(BaseSolver):
    """Solves TSP using a brute-force backtracking search."""
    def __init__(self, problem):
        super().__init__(problem)
        self.best_tour = []
        self.min_distance = float('inf')
        self.num_cities = self.problem.data.shape[0]

    def _solve_recursively(self, current_tour, current_distance):
        # If the tour is complete
        if len(current_tour) == self.num_cities:
            # Add distance from last city back to start
            final_distance = current_distance + self.problem.data[current_tour[-1]][current_tour[0]]
            if final_distance < self.min_distance:
                self.min_distance = final_distance
                # Save the tour without the repeated start node at the end
                self.best_tour = current_tour[:]
            return

        # Explore next cities
        last_city = current_tour[-1]
        for city in range(self.num_cities):
            if city not in current_tour:
                new_distance = current_distance + self.problem.data[last_city][city]
                # Pruning: if current path is already worse than best found, stop
                if new_distance < self.min_distance:
                    self._solve_recursively(current_tour + [city], new_distance)
    
    def _execute(self):
        start_city = self.problem.get_initial_state()
        self._solve_recursively([start_city], 0)
        return self.best_tour