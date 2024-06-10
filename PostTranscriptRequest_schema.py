from pydantic import BaseModel
from typing import List

class PostTranscriptRequest(BaseModel):
    competence: str
    transcript: "List[TranscriptListItem]" = []

from TranscriptListItem_schema import TranscriptListItem

PostTranscriptRequest.model_rebuild()