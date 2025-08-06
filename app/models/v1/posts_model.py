from typing import Optional

from pydantic import BaseModel


class GetUserPosts (BaseModel):
    target: Optional[str] = None