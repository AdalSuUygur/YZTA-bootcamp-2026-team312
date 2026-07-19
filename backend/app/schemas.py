"""
LLM ve API cikti sozlesmeleri.

Iki katmanli sema:
  1. AnalysisResult / DepartmentSuggestion — Gemini'nin dogrudan uretmesi
     gereken HAM cikti (Task 1.2). `response_schema` olarak llm_service.py'de
     kullanilir.
  2. UniversityDetail / DetailedDepartmentMatch / EnrichedAnalysisResult —
     Task 2.2/2.3 kapsaminda (1)'in uzerine YOK Atlas veritabani verisi
     eklenerek olusturulan ZENGINLESTIRILMIS nihai cikti. main.py bunu
     donuyor (response_model).
"""

from pydantic import BaseModel, Field

from app.department_codes import DepartmentCode


class DepartmentSuggestion(BaseModel):
    department_code: DepartmentCode = Field(
        ..., description="Sabit bolum kodu sozlugunden (department_codes.py) secilecek kod"
    )
    bolum: str = Field(..., description="Standart YOK Atlas bolum adi, or. 'Psikoloji'")
    uyum_skoru: int = Field(..., ge=0, le=100, description="Profille uyum yuzdesi")
    gerekce: str = Field(..., description="Baskin kisilik tiplerine dayanan 1-2 cumlelik gerekce")


class AnalysisResult(BaseModel):
    """Gemini'den dogrudan gelen HAM cikti (universite verisi icermez)."""

    holland_kodu: str = Field(..., description="Kullanicinin baskin 3 harfli Holland kodu, or. 'IAS'")
    profil_ozeti: str = Field(..., description="Kullanicinin kisilik profilinin 2-3 cumlelik ozeti")
    onerilen_bolumler: list[DepartmentSuggestion] = Field(
        ..., min_items=5, max_items=5, description="Uyum skoruna gore azalan sirada tam 5 bolum onerisi"
    )


class UniversityDetail(BaseModel):
    """Task 2.2 — atlas_service.py'nin SQLite'tan dondurdugu satir."""

    university_name: str
    quota: int
    last_min_score: float
    last_min_rank: int


class DetailedDepartmentMatch(BaseModel):
    """Task 2.3 — bir bolum onerisi + o bolumu veren MVP universiteleri."""

    department_code: str
    department_name: str
    uyum_skoru: int
    gerekce: str
    universities: list[UniversityDetail] = Field(
        default_factory=list,
        description="YOK Atlas veritabanindan cekilen, last_min_rank ASC sirali universite listesi",
    )


class EnrichedAnalysisResult(BaseModel):
    """POST /api/v1/test/submit tarafindan donulen NIHAI zenginlestirilmis yanit."""

    holland_kodu: str
    profil_ozeti: str
    onerilen_bolumler: list[DetailedDepartmentMatch] = Field(..., min_items=5, max_items=5)
