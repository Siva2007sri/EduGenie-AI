from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from schemas import TextRequest, QuizRequest, APIResponse
from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0",
)


app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory=str(__import__("pathlib").Path(__file__).resolve().parent / "templates"))

# Fix Jinja2 cache issue with Python 3.14
templates.env.cache = None


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html"
    )


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "application": "EduGenie"
    }


@app.post("/qa", response_model=APIResponse)
async def qa(request: TextRequest):
    result = answer_question(request.text)
    return APIResponse(
        success=True,
        result=result
    )


@app.post("/explain", response_model=APIResponse)
async def explain(request: TextRequest):
    result = explain_concept(request.text)
    return APIResponse(
        success=True,
        result=result
    )


@app.post("/quiz", response_model=APIResponse)
async def quiz(request: QuizRequest):
    result = generate_quiz(
        request.text,
        request.count
    )
    return APIResponse(
        success=True,
        result=result
    )


@app.post("/summarize", response_model=APIResponse)
async def summarize(request: TextRequest):
    result = summarize_text(request.text)
    return APIResponse(
        success=True,
        result=result
    )


@app.post("/learn/recommendations", response_model=APIResponse)
async def learning_recommendations(request: TextRequest):
    result = get_learning_recommendations(request.text)
    return APIResponse(
        success=True,
        result=result
    )