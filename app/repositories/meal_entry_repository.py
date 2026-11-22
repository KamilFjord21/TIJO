from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.meal_entry import MealEntry


class MealEntryRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def list_for_date(self, entry_date: date) -> list[MealEntry]:
        statement = (
            select(MealEntry)
            .where(MealEntry.entry_date == entry_date)
            .order_by(MealEntry.category.asc(), MealEntry.id.asc())
        )
        return list(self._db.execute(statement).scalars().all())

    def get_by_id(self, entry_id: int) -> MealEntry | None:
        return self._db.get(MealEntry, entry_id)

    def add(self, entry: MealEntry) -> MealEntry:
        self._db.add(entry)
        self._db.commit()
        self._db.refresh(entry)
        return entry

    def update(self, entry: MealEntry) -> MealEntry:
        self._db.commit()
        self._db.refresh(entry)
        return entry

    def delete(self, entry: MealEntry) -> None:
        self._db.delete(entry)
        self._db.commit()
