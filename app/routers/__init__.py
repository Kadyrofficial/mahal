from fastapi import FastAPI

from .v1 import router as v1_router
from .admin import router as administration_router


api = FastAPI(
    title="Mahal",
    version="1.0.0",
    openapi_url="/openapi.json"
)
api.include_router(v1_router)

admin = FastAPI(
    title="Mahal Admin",
    version="1.0.0",
    openapi_url="/openapi.json"
)
admin.include_router(administration_router)
