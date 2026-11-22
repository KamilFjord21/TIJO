from app.models.user_profile import UserProfile
from app.repositories.user_profile_repository import UserProfileRepository
from app.schemas.user_profile import NutritionTargets, UserProfileCreate
from app.services.goal_strategy import get_strategy
from app.services.nutrition_calculator import calculate_bmr, calculate_tdee


class UserProfileService:
    def __init__(self, repository: UserProfileRepository) -> None:
        self._repository = repository

    def get_current(self) -> UserProfile | None:
        return self._repository.get_current()

    def save(self, data: UserProfileCreate) -> UserProfile:
        profile = UserProfile(
            gender=data.gender,
            age=data.age,
            weight_kg=data.weight_kg,
            height_cm=data.height_cm,
            activity_level=data.activity_level,
            goal=data.goal,
        )
        return self._repository.save(profile)

    def compute_targets(self, profile: UserProfile) -> NutritionTargets:
        bmr = calculate_bmr(profile.gender, profile.weight_kg, profile.height_cm, profile.age)
        tdee = calculate_tdee(bmr, profile.activity_level)
        strategy = get_strategy(profile.goal)
        target_kcal = strategy.target_kcal(tdee)
        macros = strategy.macros(target_kcal)
        return NutritionTargets(
            bmr_kcal=round(bmr, 1),
            tdee_kcal=round(tdee, 1),
            target_kcal=target_kcal,
            protein_g=macros.protein_g,
            carbs_g=macros.carbs_g,
            fat_g=macros.fat_g,
        )
