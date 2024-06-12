from pydantic import BaseModel

class TranscriptListItem(BaseModel):
    question: str 
    answer: str
