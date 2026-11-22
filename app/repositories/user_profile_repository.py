from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user_profile import UserProfile


class UserProfileRepository:
    """Single-profile repository (single-user application)."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def get_current(self) -> UserProfile | None:
        statement = select(UserProfile).order_by(UserProfile.id.asc()).limit(1)
        return self._db.execute(statement).scalar_one_or_none()

    def save(self, profile: UserProfile) -> UserProfile:
        existing = self.get_current()
        if existing is None:
            self._db.add(profile)
        else:
            existing.gender = profile.gender
            existing.age = profile.age
            existing.weight_kg = profile.weight_kg
            existing.height_cm = profile.height_cm
            existing.activity_level = profile.activity_level
            existing.goal = profile.goal
            profile = existing
        self._db.commit()
        self._db.refresh(profile)
        return profile
