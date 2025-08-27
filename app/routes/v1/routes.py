from fastapi import APIRouter

from app.routes.v1.user_route import router as user_router
from app.routes.v1.reference_data_route import router as ref_router
from app.routes.v1.discover_route import router as discover_router
from app.routes.v1.relations_route import router as relations_router
from app.routes.v1.posts_route import router as posts_router
from app.routes.v1.admin_route import router as admin_router

router = APIRouter()

router.include_router(user_router, prefix='/user', tags=['User'])
router.include_router(ref_router, prefix='', tags=['Reference'])
router.include_router(discover_router, prefix='/discover', tags=['Discover'])
router.include_router(relations_router, prefix='/relation', tags=['Relations'])
router.include_router(posts_router, prefix='/posts', tags=['Posts'])
router.include_router(admin_router, prefix='/admin', tags=['Admin'])