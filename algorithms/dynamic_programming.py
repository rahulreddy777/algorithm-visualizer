from .base_solver import BaseSolver
import numpy as np

class DPKnapsackSolver(BaseSolver):
    """Solves the 0/1 Knapsack problem using dynamic programming."""
    def _execute(self):
        items = self.problem.items
        capacity = self.problem.capacity
        n = len(items)

        # dp[i][w] is the max value for weight w using items up to i
        dp = np.zeros((n + 1, capacity + 1), dtype=int)

        for i in range(1, n + 1):
            value, weight = items[i-1]
            for w in range(1, capacity + 1):
                if weight <= w:
                    # Option 1: Include the item
                    included_value = value + dp[i-1][w - weight]
                    # Option 2: Exclude the item
                    excluded_value = dp[i-1][w]
                    dp[i][w] = max(included_value, excluded_value)
                else:
                    # Cannot include item if its weight > current capacity
                    dp[i][w] = dp[i-1][w]

        # Backtrack to find which items were selected
        selected_indices = []
        w = capacity
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i-1][w]:
                # This means item i-1 was included
                selected_indices.append(i-1)
                value, weight = items[i-1]
                w -= weight

        selected_indices.reverse()
        return selected_indices