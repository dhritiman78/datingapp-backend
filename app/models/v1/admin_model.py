from pydantic import BaseModel


class AdminUidRequest(BaseModel):
    uid: str