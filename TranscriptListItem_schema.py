from pydantic import BaseModel
from typing import Annotated
from fastapi import Query

class TranscriptListItem(BaseModel):
    role: Annotated[str, Query(regex="^(assistant|user)$")] 
    content: str
