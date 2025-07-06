from fastapi import APIRouter

from app.routes.v1.user_route import router as user_router
from app.routes.v1.reference_data_route import router as ref_router

router = APIRouter()

router.include_router(user_router, prefix='/user', tags=['User'])
router.include_router(ref_router, prefix='', tags=['Reference'])