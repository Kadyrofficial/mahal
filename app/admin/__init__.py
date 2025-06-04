from fastapi import APIRouter

from .authentication.views import router as auth_router
from .users.views import router as users_router


router = APIRouter(prefix="/admin")


router.include_router(auth_router)
router.include_router(users_router)
