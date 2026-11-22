from pydantic import BaseModel, ConfigDict, Field

from app.models.user_profile import ActivityLevel, DietGoal, Gender


class UserProfileBase(BaseModel):
    gender: Gender
    age: int = Field(ge=1, le=120)
    weight_kg: float = Field(gt=0, le=500)
    height_cm: float = Field(gt=0, le=272)
    activity_level: ActivityLevel
    goal: DietGoal


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileRead(UserProfileBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class NutritionTargets(BaseModel):
    bmr_kcal: float
    tdee_kcal: float
    target_kcal: float
    protein_g: float
    carbs_g: float
    fat_g: float
