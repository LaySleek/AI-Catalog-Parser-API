from fastapi import APIRouter

from .routers import catalog, nomenclature

api_router = APIRouter()

api_router.include_router(
    catalog.router,
    prefix="/catalog",
    tags=["catalog"]
)
api_router.include_router(
    nomenclature.router,
    prefix="/nomenclature",
    tags=["nomenclature"],
)
