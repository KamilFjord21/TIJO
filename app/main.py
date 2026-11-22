from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.database import Base, SessionLocal, engine
from app.models import MealEntry, Product, UserProfile  # noqa: F401 (ensure mapping)
from app.routers import meal_entries, products, user_profile
from app.seed import seed_products_if_empty


STATIC_DIR = Path(__file__).resolve().parent.parent / "static"


def create_app() -> FastAPI:
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        seed_products_if_empty(db)

    application = FastAPI(
        title="Calorie Balance & Diet Planner",
        version="0.1.0",
    )

    application.include_router(products.router)
    application.include_router(user_profile.router)
    application.include_router(meal_entries.router)

    application.mount(
        "/static",
        StaticFiles(directory=str(STATIC_DIR)),
        name="static",
    )

    @application.get("/", include_in_schema=False)
    def serve_index() -> FileResponse:
        return FileResponse(str(STATIC_DIR / "index.html"))

    return application


app = create_app()
