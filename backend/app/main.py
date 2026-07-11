"""
Task 1.3 ve Task 2.3 — Backend Test API Endpoint'i ve Zenginleştirme.

Frontend'den gelen {question_id, score} listesini kabul eder, bunu
deterministik bir Holland profiline çevirir, LLM servisi ile Gemini'ye 
gönderip 5 bölüm önerisi alır. Ardından Task 2.3 kapsamında her bölüm için
YÖK Atlas veritabanından üniversite puan ve sıralama verilerini ekleyerek
zenginleştirilmiş JSON döndürür.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.llm_service import LLMConfigError, LLMResponseError, analyze_personality
from app.atlas_service import get_universities_by_department  # Task 2.3 servisi
from app.schemas import AnalysisResult

app = FastAPI(
    title="GuideAI API",
    description="Kendini Tanı katmanı için test gönderim ve zenginleştirilmiş bölüm önerisi API'si.",
    version="0.2.0",
)

# Geliştirme aşamasında frontend statik dosyadan çalıştığı için CORS'u serbest bırakıyoruz.
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
    return {"status": "ok", "service": "GuideAI API v0.2.0"}


@app.post("/api/v1/test/submit", response_model=AnalysisResult)
def submit_test(payload: TestSubmitRequest) -> AnalysisResult:
    if not payload.answers:
        raise HTTPException(status_code=400, detail="answers listesi boş olamaz.")

    answers_dict = {item.question_id: item.score for item in payload.answers}

    try:
        # 1. Adım:servisten 5 bölüm önerisini al
        result = analyze_personality(answers_dict)
        
        # 2. Adım (Task 2.3): Önerilen her bölüm için YÖK Atlas verilerini ekle
        for suggestion in result.onerilen_bolumler:
            universiteler = get_universities_by_department(suggestion.bolum, limit=5)
            suggestion.universiteler = universiteler
            
        return result

    except LLMConfigError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except LLMResponseError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Sunucu hatası: {str(exc)}") from exc
