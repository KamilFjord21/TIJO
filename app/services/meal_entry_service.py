from datetime import date

from fastapi import HTTPException, status

from app.models.meal_entry import MealEntry
from app.repositories.meal_entry_repository import MealEntryRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.meal_entry import (
    DailySummary,
    DailyTotals,
    MealEntryCreate,
    MealEntryRead,
    MealEntryUpdate,
)
from app.services.nutrition_calculator import scale_per_grams
from app.services.user_profile_service import UserProfileService


class MealEntryService:
    def __init__(
        self,
        meal_repository: MealEntryRepository,
        product_repository: ProductRepository,
        user_profile_service: UserProfileService,
    ) -> None:
        self._meals = meal_repository
        self._products = product_repository
        self._profiles = user_profile_service

    # ---------- CRUD ----------
    def create(self, data: MealEntryCreate) -> MealEntry:
        product = self._products.get_by_id(data.product_id)
        if product is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found")
        entry = MealEntry(
            entry_date=data.entry_date,
            category=data.category,
            product_id=data.product_id,
            grams=data.grams,
        )
        return self._meals.add(entry)

    def update(self, entry_id: int, data: MealEntryUpdate) -> MealEntry:
        entry = self._meals.get_by_id(entry_id)
        if entry is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Meal entry not found")
        if data.product_id is not None:
            if self._products.get_by_id(data.product_id) is None:
                raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found")
            entry.product_id = data.product_id
        if data.entry_date is not None:
            entry.entry_date = data.entry_date
        if data.category is not None:
            entry.category = data.category
        if data.grams is not None:
            entry.grams = data.grams
        return self._meals.update(entry)

    def delete(self, entry_id: int) -> None:
        entry = self._meals.get_by_id(entry_id)
        if entry is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Meal entry not found")
        self._meals.delete(entry)

    # ---------- Projection / summary ----------
    def to_read_model(self, entry: MealEntry) -> MealEntryRead:
        product = entry.product
        return MealEntryRead(
            id=entry.id,
            entry_date=entry.entry_date,
            category=entry.category,
            product_id=entry.product_id,
            grams=entry.grams,
            product=product,  # type: ignore[arg-type]
            kcal=round(scale_per_grams(product.kcal_per_100g, entry.grams), 1),
            protein_g=round(scale_per_grams(product.protein_per_100g, entry.grams), 1),
            carbs_g=round(scale_per_grams(product.carbs_per_100g, entry.grams), 1),
            fat_g=round(scale_per_grams(product.fat_per_100g, entry.grams), 1),
        )

    def daily_summary(self, entry_date: date) -> DailySummary:
        entries = self._meals.list_for_date(entry_date)
        read_entries = [self.to_read_model(e) for e in entries]

        totals = DailyTotals(
            kcal=round(sum(e.kcal for e in read_entries), 1),
            protein_g=round(sum(e.protein_g for e in read_entries), 1),
            carbs_g=round(sum(e.carbs_g for e in read_entries), 1),
            fat_g=round(sum(e.fat_g for e in read_entries), 1),
        )

        profile = self._profiles.get_current()
        targets = None
        remaining = None
        over_limit = False
        if profile is not None:
            targets = self._profiles.compute_targets(profile)
            remaining = round(targets.target_kcal - totals.kcal, 1)
            over_limit = totals.kcal > targets.target_kcal

        return DailySummary(
            entry_date=entry_date,
            totals=totals,
            targets=targets,
            remaining_kcal=remaining,
            over_limit=over_limit,
            entries=read_entries,
        )
