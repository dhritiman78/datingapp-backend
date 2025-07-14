from fastapi import APIRouter

from app.routes.v1.user_route import router as user_router
from app.routes.v1.reference_data_route import router as ref_router
from app.routes.v1.discover_route import router as discover_router

router = APIRouter()

router.include_router(user_router, prefix='/user', tags=['User'])
router.include_router(ref_router, prefix='', tags=['Reference'])
router.include_router(discover_router, prefix='/discover', tags=['Discover'])