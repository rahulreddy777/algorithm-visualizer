from .base_problem import BaseProblem
import json

class KnapsackProblem(BaseProblem):
    """Represents the 0/1 Knapsack Problem."""
    def load_data(self, data_path):
        """Loads knapsack data from a JSON file."""
        self.data_path = data_path
        with open(data_path, 'r') as f:
            data = json.load(f)
        self.capacity = data['capacity']
        self.items = [(item['value'], item['weight']) for item in data['items']]
        return data

    def get_initial_state(self):
        """The initial state is an empty knapsack."""
        return []

    def evaluate_solution(self, solution_indices):
        """Calculates the total value of the selected items."""
        total_value = 0
        total_weight = 0
        for index in solution_indices:
            value, weight = self.items[index]
            total_value += value
            total_weight += weight

        if total_weight > self.capacity:
            return 0
        return total_value