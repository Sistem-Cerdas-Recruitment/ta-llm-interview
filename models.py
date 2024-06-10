from pydantic import BaseModel
from typing import List, Annotated, Optional
from fastapi import Query
# from enum import Enum

# class AllowedValues(str, Enum):
#     value1 = "value1"
#     value2 = "value2"
#     value3 = "value3"

class TranscriptListItem(BaseModel):
    role: Annotated[str, Query(regex="^(assistant|user)$")] 
    content: str

class PostTranscriptRequest(BaseModel):
    competence: str
    transcript: List[TranscriptListItem] = []

class PostTranscriptResponse(BaseModel):
    status: bool
    response: str