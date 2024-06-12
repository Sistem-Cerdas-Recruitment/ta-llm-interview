from fastapi import FastAPI
from PostTranscriptRequest_schema import PostTranscriptRequest
from TranscriptListItem_schema import TranscriptListItem
from PostTranscriptResponse_schema import PostTranscriptResponse
from TechnicalEvaluationRequest_schema import TechnicalEvaluationRequest
from GetTechnicalResponse_schema import GetTechnicalResponse
from TechnicalEvaluationResponse_schema import TechnicalEvaluationResponse
import interviewer
import technical_interviewer
import technical_evaluator

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

@app.get("/technical", response_model=GetTechnicalResponse,
         description="Get the technical question for the specifed skill. Examples of skill: Java, HTML, etc.",
         response_description="Response is the technical question for the specified skill.",)
async def get_technical_question(skill: str):
    response = technical_interviewer.generate_question(skill)
    return {
        "response": response
    }

@app.post("/technical", response_model=TechnicalEvaluationResponse,
         description="Get the technical interview evaluation for the specifed skill.",
         response_description="Response is the evaluation result, true for success, false for fail.")
async def evaluate_technical(req:   TechnicalEvaluationRequest):
    response = technical_evaluator.generate_evaluation(req.skill, req.transcript)
    return {
        "response": response
    }