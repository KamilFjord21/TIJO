from fastapi import HTTPException, status

from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate


class ProductService:
    def __init__(self, repository: ProductRepository) -> None:
        self._repository = repository

    def list_products(self, search: str | None = None) -> list[Product]:
        return self._repository.list_all(search)

    def get_product(self, product_id: int) -> Product:
        product = self._repository.get_by_id(product_id)
        if product is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found")
        return product

    def create_product(self, data: ProductCreate) -> Product:
        if self._repository.get_by_name(data.name) is not None:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"Product with name '{data.name}' already exists",
            )
        product = Product(
            name=data.name,
            kcal_per_100g=data.kcal_per_100g,
            protein_per_100g=data.protein_per_100g,
            carbs_per_100g=data.carbs_per_100g,
            fat_per_100g=data.fat_per_100g,
        )
        return self._repository.add(product)

    def delete_product(self, product_id: int) -> None:
        product = self.get_product(product_id)
        self._repository.delete(product)
