from abc import ABC, abstractmethod

class BaseProblem(ABC):
    """Abstract base class for a combinatorial optimization problem."""
    def __init__(self, data_path):
        self.data = self.load_data(data_path)

    @abstractmethod
    def load_data(self, data_path):
        """Loads and parses the problem-specific data."""
        pass

    @abstractmethod
    def get_initial_state(self):
        """Returns the starting point for a search."""
        pass

    @abstractmethod
    def evaluate_solution(self, solution):
        """Calculates the cost or value of a given solution."""
        pass