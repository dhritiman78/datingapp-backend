from fastapi import APIRouter
from app.controllers.reference_data_controller import get_school_controller, get_branch_controller, \
    get_programme_controller

router = APIRouter()

@router.get('/schools', status_code=200)
async def school_route():
    return await get_school_controller()

@router.get('/departments', status_code=200)
async def department_route():
    return await get_branch_controller()

@router.get('/programmes', status_code=200)
async def programme_route():
    return await get_programme_controller()