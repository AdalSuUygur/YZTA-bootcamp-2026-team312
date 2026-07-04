"""
LLM çıktı sözleşmesi. Gemini'nin `response_schema` parametresi bu modellerden
türetilir, böylece model yalnızca bu şekle uyan JSON döndürebilir.
"""

from pydantic import BaseModel, Field


class DepartmentSuggestion(BaseModel):
    bolum: str = Field(..., description="Standart YÖK Atlas bölüm adı, ör. 'Psikoloji'")
    uyum_skoru: int = Field(..., ge=0, le=100, description="Profille uyum yüzdesi")
    gerekce: str = Field(..., description="Baskın kişilik tiplerine dayanan 1-2 cümlelik gerekçe")


class AnalysisResult(BaseModel):
    holland_kodu: str = Field(..., description="Kullanıcının baskın 3 harfli Holland kodu, ör. 'IAS'")
    profil_ozeti: str = Field(..., description="Kullanıcının kişilik profilinin 2-3 cümlelik özeti")
    onerilen_bolumler: list[DepartmentSuggestion] = Field(
        ..., min_length=5, max_length=5, description="Uyum skoruna göre azalan sırada tam 5 bölüm önerisi"
    )
