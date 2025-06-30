from app.models.user_model import registerRequest
from app.repository.user_repository import enter_user_details_into_DB


async def insert_user_service(registerData: registerRequest, user: dict[str, str]):
    return await enter_user_details_into_DB(registerData,user)