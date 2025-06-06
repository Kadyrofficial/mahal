from fastapi import APIRouter

from .users.views import router as users_router
from .authentication.views import router as auth_router
from app.routers.v1_ws.authentication.ws import ws_router as auth_ws_router
from .carts.views import router as carts_router


router = APIRouter(prefix="/v1")
ws_router = APIRouter(prefix="/v1")

router.include_router(users_router)
router.include_router(auth_router)
router.include_router(carts_router)

ws_router.include_router(auth_ws_router)
