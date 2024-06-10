from pydantic import BaseModel
from typing import List, Annotated
from fastapi import Query

class TranscriptListItem(BaseModel):
    role: Annotated[str, Query(regex="^(assistant|user)$")] 
    content: str

class PostTranscriptRequest(BaseModel):
    competence: str
    transcript: List[TranscriptListItem] = []

class PostTranscriptResponse(BaseModel):
    status: bool
    response: str