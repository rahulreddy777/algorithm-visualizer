from abc import ABC, abstractmethod
import time

class BaseSolver(ABC):
    """Abstract base class for a solving strategy."""
    def __init__(self, problem):
        self.problem = problem

    def solve(self):
        """Solves the problem and tracks performance."""
        start_time = time.time()
        solution = self._execute()
        end_time = time.time()

        execution_time = end_time - start_time
        objective_value = self.problem.evaluate_solution(solution)

        return {
            'solution': solution,
            'objective_value': objective_value,
            'execution_time': execution_time
        }

    @abstractmethod
    def _execute(self):
        """The core logic of the algorithm."""
        pass