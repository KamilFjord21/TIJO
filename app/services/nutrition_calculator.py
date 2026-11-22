"""Pure, deterministic nutrition calculations (BMR, TDEE, macros, per-gram scaling).

Intentionally free of I/O, DB, and framework dependencies so unit tests in Stage 2
can call these functions directly.
"""
from dataclasses import dataclass

from app.models.user_profile import ActivityLevel, Gender


ACTIVITY_MULTIPLIERS: dict[ActivityLevel, float] = {
    ActivityLevel.SEDENTARY: 1.2,
    ActivityLevel.LIGHT: 1.375,
    ActivityLevel.MODERATE: 1.55,
    ActivityLevel.ACTIVE: 1.725,
    ActivityLevel.VERY_ACTIVE: 1.9,
}


@dataclass(frozen=True)
class MacroBreakdown:
    protein_g: float
    carbs_g: float
    fat_g: float


def calculate_bmr(gender: Gender, weight_kg: float, height_cm: float, age: int) -> float:
    """Mifflin-St Jeor equation."""
    if weight_kg <= 0 or height_cm <= 0 or age <= 0:
        raise ValueError("weight_kg, height_cm and age must be positive")
    base = 10.0 * weight_kg + 6.25 * height_cm - 5.0 * age
    return base + 5.0 if gender == Gender.MALE else base - 161.0


def calculate_tdee(bmr_kcal: float, activity_level: ActivityLevel) -> float:
    if bmr_kcal <= 0:
        raise ValueError("bmr_kcal must be positive")
    return bmr_kcal * ACTIVITY_MULTIPLIERS[activity_level]


def split_macros(
    target_kcal: float,
    protein_ratio: float,
    carbs_ratio: float,
    fat_ratio: float,
) -> MacroBreakdown:
    """Split a daily kcal target into macro grams.

    Energy density: protein 4 kcal/g, carbs 4 kcal/g, fat 9 kcal/g.
    """
    total = protein_ratio + carbs_ratio + fat_ratio
    if target_kcal <= 0:
        raise ValueError("target_kcal must be positive")
    if abs(total - 1.0) > 0.01:
        raise ValueError("macro ratios must sum to 1.0")
    return MacroBreakdown(
        protein_g=round((target_kcal * protein_ratio) / 4.0, 1),
        carbs_g=round((target_kcal * carbs_ratio) / 4.0, 1),
        fat_g=round((target_kcal * fat_ratio) / 9.0, 1),
    )


def scale_per_grams(value_per_100g: float, grams: float) -> float:
    if grams <= 0:
        raise ValueError("grams must be positive")
    return value_per_100g * grams / 100.0
