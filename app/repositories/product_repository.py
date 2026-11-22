from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product


class ProductRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def list_all(self, search: str | None = None) -> list[Product]:
        statement = select(Product)
        if search:
            statement = statement.where(Product.name.ilike(f"%{search}%"))
        statement = statement.order_by(Product.name.asc())
        return list(self._db.execute(statement).scalars().all())

    def get_by_id(self, product_id: int) -> Product | None:
        return self._db.get(Product, product_id)

    def get_by_name(self, name: str) -> Product | None:
        statement = select(Product).where(Product.name == name)
        return self._db.execute(statement).scalar_one_or_none()

    def add(self, product: Product) -> Product:
        self._db.add(product)
        self._db.commit()
        self._db.refresh(product)
        return product

    def delete(self, product: Product) -> None:
        self._db.delete(product)
        self._db.commit()

    def bulk_add(self, products: list[Product]) -> None:
        self._db.add_all(products)
        self._db.commit()

    def count(self) -> int:
        return self._db.query(Product).count()
