from fastapi import FastAPI
from PostTranscriptRequest_schema import PostTranscriptRequest
from TranscriptListItem_schema import TranscriptListItem
from PostTranscriptResponse_schema import PostTranscriptResponse
from TechnicalEvaluationRequest_schema import TechnicalEvaluationRequest
from GetTechnicalResponse_schema import GetTechnicalResponse
from TechnicalEvaluationResponse_schema import TechnicalEvaluationResponse
import interviewer

tags_metadata = [

]

app = FastAPI(openapi_tags=tags_metadata)

@app.get("/", )
async def health_check():
    return "The health check is successful! See the documentation at: /docs"


@app.post("/transcript", response_model=PostTranscriptResponse)
async def post_transcript(req: PostTranscriptRequest):
    status, response = interviewer.generate_question(req.competence, req.transcript)
    return {
        "status": status,
        "response": response
    }