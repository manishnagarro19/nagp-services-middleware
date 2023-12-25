from fastapi import APIRouter

from api.v1.product import product_router

router = APIRouter()
router.include_router(product_router, prefix="/v1", tags=["v1"])


__all__ = ["router"]
