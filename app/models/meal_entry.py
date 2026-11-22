import enum
from datetime import date

from sqlalchemy import Date, Enum, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.product import Product


class MealCategory(str, enum.Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"


class MealEntry(Base):
    __tablename__ = "meal_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    entry_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    category: Mapped[MealCategory] = mapped_column(Enum(MealCategory), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    grams: Mapped[float] = mapped_column(Float, nullable=False)

    product: Mapped[Product] = relationship("Product", lazy="joined")
