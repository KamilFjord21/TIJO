from datetime import date

from fastapi import APIRouter, Depends, Query, status

from app.routers.dependencies import get_meal_entry_service
from app.schemas.meal_entry import (
    DailySummary,
    MealEntryCreate,
    MealEntryRead,
    MealEntryUpdate,
)
from app.services.meal_entry_service import MealEntryService


router = APIRouter(prefix="/api/meal-entries", tags=["meal-entries"])


@router.get("", response_model=DailySummary)
def get_daily_summary(
    entry_date: date = Query(default_factory=date.today),
    service: MealEntryService = Depends(get_meal_entry_service),
) -> DailySummary:
    return service.daily_summary(entry_date)


@router.post("", response_model=MealEntryRead, status_code=status.HTTP_201_CREATED)
def create_meal_entry(
    payload: MealEntryCreate,
    service: MealEntryService = Depends(get_meal_entry_service),
) -> MealEntryRead:
    entry = service.create(payload)
    return service.to_read_model(entry)


@router.patch("/{entry_id}", response_model=MealEntryRead)
def update_meal_entry(
    entry_id: int,
    payload: MealEntryUpdate,
    service: MealEntryService = Depends(get_meal_entry_service),
) -> MealEntryRead:
    entry = service.update(entry_id, payload)
    return service.to_read_model(entry)


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_meal_entry(
    entry_id: int,
    service: MealEntryService = Depends(get_meal_entry_service),
) -> None:
    service.delete(entry_id)
