from pydantic import BaseModel, Field
from typing import Any


class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        description="Text or question provided by the user"
    )


class QuizRequest(TextRequest):
    count: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Number of quiz questions"
    )


class QuizQuestion(BaseModel):
    question: str
    options: list[str]
    correct_answer: str
    explanation: str


class QuizResponse(BaseModel):
    questions: list[QuizQuestion]


class APIResponse(BaseModel):
    success: bool
    result: Any