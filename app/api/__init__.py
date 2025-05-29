from fastapi import APIRouter

from .v1 import (
    router as v1_router,
    ws_router as v1_ws_router
)


router = APIRouter(prefix="/api")
ws_router = APIRouter(prefix="/ws")

router.include_router(v1_router)
ws_router.include_router(v1_ws_router)
