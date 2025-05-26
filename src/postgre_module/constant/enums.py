from enum import Enum


class SolutionStatus(Enum, str):
    ON_EVALUATION = "on_evaluation"
    ON_PROGRESS = "on_progress"
    EVALUATED = "evaluated"

    def __str__(self):
        return self.value
