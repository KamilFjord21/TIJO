import enum

from sqlalchemy import Enum, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"


class ActivityLevel(str, enum.Enum):
    SEDENTARY = "sedentary"
    LIGHT = "light"
    MODERATE = "moderate"
    ACTIVE = "active"
    VERY_ACTIVE = "very_active"


class DietGoal(str, enum.Enum):
    REDUCTION = "reduction"
    MAINTENANCE = "maintenance"
    BULKING = "bulking"


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    gender: Mapped[Gender] = mapped_column(Enum(Gender), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    weight_kg: Mapped[float] = mapped_column(Float, nullable=False)
    height_cm: Mapped[float] = mapped_column(Float, nullable=False)
    activity_level: Mapped[ActivityLevel] = mapped_column(Enum(ActivityLevel), nullable=False)
    goal: Mapped[DietGoal] = mapped_column(Enum(DietGoal), nullable=False)
