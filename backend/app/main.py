"""
Task 1.3 — Backend Test API Endpoint'i.

Frontend'den gelen {question_id, score} listesini kabul eder, bunu
scoring.score_answers() ile deterministik bir Holland profiline cevirir,
llm_service.analyze_personality() ile Gemini'ye gonderir ve tam 5 bolum
onerisini JSON olarak doner.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.llm_service import LLMConfigError, LLMResponseError, analyze_personality
from app.schemas import AnalysisResult

app = FastAPI(
    title="GuideAI API",
    description="Kendini Tani katmani icin test gonderim ve bolum onerisi API'si.",
    version="0.1.0",
)

# Gelistirme asamasinda frontend statik dosyadan (file:// veya farkli port)
# calistigi icin CORS'u serbest birakiyoruz. Prod'a cikarken origin kisitlanmali.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnswerItem(BaseModel):
    question_id: int
    score: int


class TestSubmitRequest(BaseModel):
    answers: list[AnswerItem]


@app.get("/")
def read_root() -> dict:
    return {"status": "ok", "service": "GuideAI API"}


@app.post("/api/v1/test/submit", response_model=AnalysisResult)
def submit_test(payload: TestSubmitRequest) -> AnalysisResult:
    if not payload.answers:
        raise HTTPException(status_code=400, detail="answers listesi bos olamaz.")

    answers_dict = {item.question_id: item.score for item in payload.answers}

    try:
        return analyze_personality(answers_dict)
    except LLMConfigError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except LLMResponseError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
