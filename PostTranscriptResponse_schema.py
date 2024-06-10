from pydantic import BaseModel

class PostTranscriptResponse(BaseModel):
    status: bool
    response: str