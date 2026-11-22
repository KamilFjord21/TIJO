from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from app.models.meal_entry import MealCategory
from app.schemas.product import ProductRead


class MealEntryBase(BaseModel):
    entry_date: date
    category: MealCategory
    product_id: int
    grams: float = Field(gt=0, le=5000)


class MealEntryCreate(MealEntryBase):
    pass


class MealEntryUpdate(BaseModel):
    entry_date: date | None = None
    category: MealCategory | None = None
    product_id: int | None = None
    grams: float | None = Field(default=None, gt=0, le=5000)


class MealEntryRead(MealEntryBase):
    id: int
    product: ProductRead
    kcal: float
    protein_g: float
    carbs_g: float
    fat_g: float

    model_config = ConfigDict(from_attributes=True)


class DailyTotals(BaseModel):
    kcal: float
    protein_g: float
    carbs_g: float
    fat_g: float


class DailySummary(BaseModel):
    entry_date: date
    totals: DailyTotals
    targets: "NutritionTargets | None" = None
    remaining_kcal: float | None = None
    over_limit: bool = False
    entries: list[MealEntryRead]


from app.schemas.user_profile import NutritionTargets  # noqa: E402

DailySummary.model_rebuild()
