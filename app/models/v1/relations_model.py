from typing import Optional, List

from pydantic import BaseModel

class getUserRelations(BaseModel):
    target_uid: str


class SetUserRelations(BaseModel):
    likes: Optional[List[str]] = []
    swipes: Optional[List[str]] = []
    blocks: Optional[List[str]] = []
    unblocks: Optional[List[str]] = []