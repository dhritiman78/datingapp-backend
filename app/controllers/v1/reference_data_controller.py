from app.service.v1.reference_data_service import get_school_service, get_branch_service, get_programme_service


async def get_school_controller():
    return await get_school_service()

async def get_branch_controller():
    return await get_branch_service()

async def get_programme_controller():
    return await get_programme_service()