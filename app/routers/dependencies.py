from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.meal_entry_repository import MealEntryRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.user_profile_repository import UserProfileRepository
from app.services.meal_entry_service import MealEntryService
from app.services.product_service import ProductService
from app.services.user_profile_service import UserProfileService


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    return ProductService(ProductRepository(db))


def get_user_profile_service(db: Session = Depends(get_db)) -> UserProfileService:
    return UserProfileService(UserProfileRepository(db))


def get_meal_entry_service(db: Session = Depends(get_db)) -> MealEntryService:
    product_repo = ProductRepository(db)
    meal_repo = MealEntryRepository(db)
    profile_service = UserProfileService(UserProfileRepository(db))
    return MealEntryService(meal_repo, product_repo, profile_service)
