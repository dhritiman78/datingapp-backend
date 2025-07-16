from typing import Optional, List

from pydantic import BaseModel, Field


class searchData(BaseModel):
    search_parameter: str

class ByIdRequest(BaseModel):
    user_id: int
    fields: Optional[List[str]] = None

class ByUidRequest(BaseModel):
    user_uid: str
    fields: Optional[List[str]] = None

# Model for a user's custom fields
class UserCustomFields(BaseModel):
    id: Optional[int] = Field(None, description="The unique ID of the user.")
    uid: Optional[str] = Field(None, description="The unique identifier (UID) of the user.")
    first_name: Optional[str] = Field(None, description="The first name of the user.")
    last_name: Optional[str] = Field(None, description="The last name of the user.")
    email: Optional[str] = Field(None, description="The email address of the user.")
    phone_number: Optional[str] = Field(None, description="The phone number of the user.")
    school_id: Optional[int] = Field(None, description="The ID of the school the user belongs to.")
    programme_id: Optional[int] = Field(None, description="The ID of the programme the user is enrolled in.")
    department_id: Optional[int] = Field(None, description="The ID of the department the user belongs to.")
    school_name: Optional[str] = Field(None, description="The name of the school.")
    school_code: Optional[str] = Field(None, description="The code of the school.")
    programme_name: Optional[str] = Field(None, description="The name of the programme.")
    programme_code: Optional[str] = Field(None, description="The code of the programme.")
    department_name: Optional[str] = Field(None, description="The name of the department.")
    department_code: Optional[str] = Field(None, description="The code of the department.")
    interests: List[int] = Field([], description="A list of interest IDs associated with the user.")

    class Config:
        # Allow population by field names (e.g., from database columns)
        from_attributes = True