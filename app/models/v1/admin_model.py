from pydantic import BaseModel


class AdminDeleteRequest(BaseModel):
    uid: str
    key: str