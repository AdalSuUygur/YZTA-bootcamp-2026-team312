"""
Task 1.3 + Task 2.3 — Backend Test API Endpoint'i ve Zenginlestirme.

Uctan uca akis (Task 2.3'te tarif edildigi gibi):
  1. Frontend'den gelen {question_id, score} listesi Holland profiline
     cevrilir (scoring.py).
  2. Profil Gemini'ye gonderilir, tam 5 department_code + gerekce doner
     (llm_service.py -> AnalysisResult).
  3. Her department_code, atlas_service.py araciligiyla YOK Atlas
     veritabaninda aranir; ilgili universiteler last_min_rank ASC sirayla
     cekilir (Task 2.2).
  4. AI gerekceleri ile SQL'den gelen resmi veriler tek bir semada
     (EnrichedAnalysisResult) birlestirilip 200 OK ile donulur.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.llm_service import LLMConfigError, LLMResponseError, analyze_personality
from app.services.atlas_service import get_universities_by_code
from app.schemas import DetailedDepartmentMatch, EnrichedAnalysisResult

app = FastAPI(
    title="GuideAI API",
    description="Kendini Tanı katmanı için test gönderim ve zenginleştirilmiş bölüm önerisi API'si.",
    version="0.3.0",
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
    return {"status": "ok", "service": "GuideAI API v0.3.0"}


@app.post("/api/v1/test/submit", response_model=EnrichedAnalysisResult)
def submit_test(payload: TestSubmitRequest) -> EnrichedAnalysisResult:
    if not payload.answers:
        raise HTTPException(status_code=400, detail="answers listesi boş olamaz.")

    answers_dict = {item.question_id: item.score for item in payload.answers}

    try:
        # Adım 1-2: Holland profili + Gemini'den 5 department_code önerisi
        result = analyze_personality(answers_dict)
    except LLMConfigError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except LLMResponseError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    try:
        # Adım 3-4: Her öneriyi YÖK Atlas verisiyle zenginleştir
        enriched_departments = [
            DetailedDepartmentMatch(
                department_code=suggestion.department_code.value,
                department_name=suggestion.bolum,
                uyum_skoru=suggestion.uyum_skoru,
                gerekce=suggestion.gerekce,
                universities=get_universities_by_code(suggestion.department_code.value),
            )
            for suggestion in result.onerilen_bolumler
        ]
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Üniversite verisi zenginleştirilirken hata oluştu: {exc}") from exc

    return EnrichedAnalysisResult(
        holland_kodu=result.holland_kodu,
        profil_ozeti=result.profil_ozeti,
        onerilen_bolumler=enriched_departments,
    )
