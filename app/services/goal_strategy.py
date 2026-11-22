"""Strategy pattern: different diet goals adjust TDEE and macro distribution."""
from abc import ABC, abstractmethod

from app.models.user_profile import DietGoal
from app.services.nutrition_calculator import MacroBreakdown, split_macros


class DietGoalStrategy(ABC):
    @abstractmethod
    def target_kcal(self, tdee_kcal: float) -> float:
        ...

    @abstractmethod
    def macros(self, target_kcal: float) -> MacroBreakdown:
        ...


class ReductionStrategy(DietGoalStrategy):
    """Caloric deficit (~20%), higher protein to preserve muscle mass."""

    def target_kcal(self, tdee_kcal: float) -> float:
        return round(tdee_kcal * 0.80, 0)

    def macros(self, target_kcal: float) -> MacroBreakdown:
        return split_macros(target_kcal, protein_ratio=0.35, carbs_ratio=0.40, fat_ratio=0.25)


class MaintenanceStrategy(DietGoalStrategy):
    def target_kcal(self, tdee_kcal: float) -> float:
        return round(tdee_kcal, 0)

    def macros(self, target_kcal: float) -> MacroBreakdown:
        return split_macros(target_kcal, protein_ratio=0.30, carbs_ratio=0.40, fat_ratio=0.30)


class BulkingStrategy(DietGoalStrategy):
    """Caloric surplus (~15%), more carbs for training."""

    def target_kcal(self, tdee_kcal: float) -> float:
        return round(tdee_kcal * 1.15, 0)

    def macros(self, target_kcal: float) -> MacroBreakdown:
        return split_macros(target_kcal, protein_ratio=0.25, carbs_ratio=0.50, fat_ratio=0.25)


_STRATEGIES: dict[DietGoal, DietGoalStrategy] = {
    DietGoal.REDUCTION: ReductionStrategy(),
    DietGoal.MAINTENANCE: MaintenanceStrategy(),
    DietGoal.BULKING: BulkingStrategy(),
}


def get_strategy(goal: DietGoal) -> DietGoalStrategy:
    return _STRATEGIES[goal]
