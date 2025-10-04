import numpy as np
from .base_problem import BaseProblem

class TSP(BaseProblem):
    """Represents the Traveling Salesperson Problem."""
    def load_data(self, data_path):
        """Loads a distance matrix from a text file."""
        # Ensure the data_path is passed to the loader
        self.data_path = data_path 
        return np.loadtxt(data_path)

    def get_initial_state(self):
        """Returns a starting city index (e.g., 0)."""
        return 0

    def evaluate_solution(self, tour):
        """Calculates the total distance of a tour."""
        if not tour or len(tour) != self.data.shape[0]:
            return float('inf') # Invalid tour

        total_distance = 0
        num_cities = len(tour)
        for i in range(num_cities):
            from_city = tour[i]
            # Connect back to the start city at the end
            to_city = tour[(i + 1) % num_cities]
            total_distance += self.data[from_city][to_city]
        return total_distance