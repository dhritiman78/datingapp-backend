import enum
from datetime import date
from typing import List, Optional

from pydantic import BaseModel, EmailStr

class GenderEnum(str, enum.Enum):
    male = "male"
    female = "female"
    both = "both"
    others = "others"

class registerRequest(BaseModel):
    gender: GenderEnum  # Referencing the GenderEnum class
    dateOfBirth: date  # Using date for consistency with database
    bio: Optional[str] = None  # Correct syntax for Optional field with default None
    avataar: Optional[str] = None  # Correct syntax for Optional field with default None
    preferred_gender: Optional[GenderEnum] = None  # Referencing GenderEnum, and Optional
    school_id: Optional[int] = None  # Made optional as per FastAPI's UserCreate and DB
    programme_id: Optional[int] = None  # Renamed from p_programme_id, made optional
    department_id: Optional[int] = None  # Made optional
    interests: Optional[List[int]] = []  #
    personality: Optional[str] = None
    looking_for: Optional[int] = None

class UpdateRequest(BaseModel):
    name: Optional[str] = None
    gender: Optional[GenderEnum] = None
    dateOfBirth: Optional[date] = None
    bio: Optional[str] = None
    preferred_gender: Optional[GenderEnum] = None
    school_id: Optional[int] = None
    programme_id: Optional[int] = None
    department_id: Optional[int] = None
    interests: Optional[List[int]] = None
    personality: Optional[str] = None
    looking_for: Optional[int] = None

class loginRequest(BaseModel):
    email: str
    password: str

class CustomUserRequest(BaseModel):
    user_id: str
    fields: List[str]