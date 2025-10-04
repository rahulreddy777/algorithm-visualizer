from .base_solver import BaseSolver
import numpy as np

# Solver for the Traveling Salesperson Problem
class GreedyTSPSolver(BaseSolver):
    """Solves TSP using the Nearest Neighbor heuristic."""
    def _execute(self):
        num_cities = self.problem.data.shape[0]
        start_city = self.problem.get_initial_state()
        
        unvisited = list(range(num_cities))
        tour = []
        
        current_city = start_city
        tour.append(current_city)
        unvisited.remove(current_city)
        
        while unvisited:
            nearest_city = min(unvisited, key=lambda city: self.problem.data[current_city][city])
            tour.append(nearest_city)
            unvisited.remove(nearest_city)
            current_city = nearest_city
            
        return tour

# Solver for the 0/1 Knapsack Problem
class GreedyKnapsackSolver(BaseSolver):
    """Solves the Knapsack problem using a value-to-weight ratio heuristic."""
    def _execute(self):
        num_items = len(self.problem.items)
        # Create a list of items with their original index and ratio
        # Adding a small epsilon to avoid division by zero for items with zero weight
        items_with_ratio = [
            (i, self.problem.items[i][0] / (self.problem.items[i][1] + 1e-9))
            for i in range(num_items)
        ]

        # Sort items by ratio in descending order
        items_with_ratio.sort(key=lambda x: x[1], reverse=True)

        selected_indices = []
        current_weight = 0

        for i, ratio in items_with_ratio:
            item_value, item_weight = self.problem.items[i]
            if current_weight + item_weight <= self.problem.capacity:
                selected_indices.append(i)
                current_weight += item_weight

        return selected_indices