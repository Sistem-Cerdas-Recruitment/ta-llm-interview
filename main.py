from fastapi import FastAPI
from mangum import Mangum
from models import PostTranscriptRequest, PostTranscriptResponse
from interviewer import generate_question

app = FastAPI()

handler = Mangum(app)

@app.post("/transcript", response_model=PostTranscriptResponse)
async def post_transcript(req: PostTranscriptRequest):
    status, response = generate_question(req.competence, req.transcript)
    return {
        "status": status,
        "response": response
    }