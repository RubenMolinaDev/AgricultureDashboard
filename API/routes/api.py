from fastapi import APIRouter
from src.endpoints import countries, cereal, agriculture

router = APIRouter()

#### ROUTES ####

router.include_router(countries.router, prefix="/countries", tags=["Countries"])
router.include_router(cereal.router, prefix="/cereal", tags=["Cereal"])
router.include_router(agriculture.router, prefix="/agriculture", tags=["Agriculture"])
