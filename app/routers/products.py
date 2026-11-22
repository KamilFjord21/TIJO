from fastapi import APIRouter, Depends, Query, status

from app.routers.dependencies import get_product_service
from app.schemas.product import ProductCreate, ProductRead
from app.services.product_service import ProductService


router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("", response_model=list[ProductRead])
def list_products(
    search: str | None = Query(default=None, min_length=1, max_length=128),
    service: ProductService = Depends(get_product_service),
) -> list[ProductRead]:
    return [ProductRead.model_validate(p) for p in service.list_products(search)]


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    payload: ProductCreate,
    service: ProductService = Depends(get_product_service),
) -> ProductRead:
    return ProductRead.model_validate(service.create_product(payload))


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
) -> None:
    service.delete_product(product_id)
