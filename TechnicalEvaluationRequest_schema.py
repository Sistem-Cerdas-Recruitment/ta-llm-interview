from pydantic import BaseModel

class TechnicalEvaluationRequest(BaseModel):
    skill: str
    transcript: str