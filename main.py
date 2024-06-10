from fastapi import FastAPI
from mangum import Mangum
from PostTranscriptRequest_schema import PostTranscriptRequest
from TranscriptListItem_schema import TranscriptListItem
from PostTranscriptResponse_schema import PostTranscriptResponse
from interviewer import generate_question

app = FastAPI()

# handler = Mangum(app)

@app.get("/", )
async def health_check():
    return "The health check is successful! See the documentation at: /docs"


@app.post("/transcript", response_model=PostTranscriptResponse)
async def post_transcript(req: PostTranscriptRequest):
    status, response = generate_question(req.competence, req.transcript)
    return {
        "status": status,
        "response": response
    }
