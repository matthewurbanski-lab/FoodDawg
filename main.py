from fastapi import FastAPI

from app.db.session import engine
from app.db.base import Base
from app.api.health import router as health_router
from app.api.inventory import router as inventory_router
from app.api.purchasing import router as purchasing_router
from app.api.reporting import router as reporting_router

def create_app() -> FastAPI:
    app = FastAPI(title="FoodDawg", version="0.1.0")
    Base.metadata.create_all(bind=engine)

    app.include_router(health_router)
    app.include_router(inventory_router)
    app.include_router(purchasing_router)
    app.include_router(reporting_router)
    return app

app = create_app()
