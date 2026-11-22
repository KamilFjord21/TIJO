from sqlalchemy.orm import Session

from app.models.product import Product
from app.repositories.product_repository import ProductRepository


SEED_PRODUCTS: list[dict] = [
    {"name": "Chicken breast", "kcal_per_100g": 165, "protein_per_100g": 31.0, "carbs_per_100g": 0.0, "fat_per_100g": 3.6},
    {"name": "White rice (cooked)", "kcal_per_100g": 130, "protein_per_100g": 2.7, "carbs_per_100g": 28.0, "fat_per_100g": 0.3},
    {"name": "Brown rice (cooked)", "kcal_per_100g": 123, "protein_per_100g": 2.7, "carbs_per_100g": 25.6, "fat_per_100g": 1.0},
    {"name": "Oatmeal (dry)", "kcal_per_100g": 379, "protein_per_100g": 13.2, "carbs_per_100g": 67.7, "fat_per_100g": 6.5},
    {"name": "Egg (whole)", "kcal_per_100g": 155, "protein_per_100g": 13.0, "carbs_per_100g": 1.1, "fat_per_100g": 11.0},
    {"name": "Banana", "kcal_per_100g": 89, "protein_per_100g": 1.1, "carbs_per_100g": 22.8, "fat_per_100g": 0.3},
    {"name": "Apple", "kcal_per_100g": 52, "protein_per_100g": 0.3, "carbs_per_100g": 13.8, "fat_per_100g": 0.2},
    {"name": "Whole milk", "kcal_per_100g": 61, "protein_per_100g": 3.2, "carbs_per_100g": 4.8, "fat_per_100g": 3.3},
    {"name": "Greek yogurt (natural)", "kcal_per_100g": 59, "protein_per_100g": 10.0, "carbs_per_100g": 3.6, "fat_per_100g": 0.4},
    {"name": "Almonds", "kcal_per_100g": 579, "protein_per_100g": 21.2, "carbs_per_100g": 21.6, "fat_per_100g": 49.9},
    {"name": "Peanut butter", "kcal_per_100g": 588, "protein_per_100g": 25.0, "carbs_per_100g": 20.0, "fat_per_100g": 50.0},
    {"name": "Olive oil", "kcal_per_100g": 884, "protein_per_100g": 0.0, "carbs_per_100g": 0.0, "fat_per_100g": 100.0},
    {"name": "Salmon (raw)", "kcal_per_100g": 208, "protein_per_100g": 20.0, "carbs_per_100g": 0.0, "fat_per_100g": 13.0},
    {"name": "Tuna in brine", "kcal_per_100g": 116, "protein_per_100g": 26.0, "carbs_per_100g": 0.0, "fat_per_100g": 1.0},
    {"name": "Whole wheat bread", "kcal_per_100g": 247, "protein_per_100g": 13.0, "carbs_per_100g": 41.0, "fat_per_100g": 3.4},
    {"name": "Broccoli", "kcal_per_100g": 34, "protein_per_100g": 2.8, "carbs_per_100g": 7.0, "fat_per_100g": 0.4},
    {"name": "Tomato", "kcal_per_100g": 18, "protein_per_100g": 0.9, "carbs_per_100g": 3.9, "fat_per_100g": 0.2},
    {"name": "Potato (boiled)", "kcal_per_100g": 87, "protein_per_100g": 1.9, "carbs_per_100g": 20.0, "fat_per_100g": 0.1},
]


def seed_products_if_empty(db: Session) -> None:
    repository = ProductRepository(db)
    if repository.count() > 0:
        return
    repository.bulk_add([Product(**data) for data in SEED_PRODUCTS])
