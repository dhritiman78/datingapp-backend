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
    interests: Optional[List[str]] = []  #

class loginRequest(BaseModel):
    email: str
    password: str