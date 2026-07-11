"""
LLM çıktı sözleşmesi. Gemini'nin `response_schema` parametresi bu modellerden
türetilir, böylece model yalnızca bu şekle uyan JSON döndürebilir.
Ayrıca Task 2.3 kapsamında YÖK Atlas üniversite verileriyle zenginleştirilmiştir.
"""

from pydantic import BaseModel, Field
from typing import Optional


class UniversityItem(BaseModel):
    universite_adi: str = Field(..., description="Üniversitenin adı")
    fakulte: Optional[str] = Field(None, description="Fakülte adı")
    taban_puan: Optional[float] = Field(None, description="YÖK Atlas taban puanı")
    siralama: Optional[int] = Field(None, description="YÖK Atlas başarı sıralaması")
    kontenjan: Optional[int] = Field(None, description="Bölüm kontenjanı")


class DepartmentSuggestion(BaseModel):
    bolum: str = Field(..., description="Standart YÖK Atlas bölüm adı, ör. 'Psikoloji'")
    uyum_skoru: int = Field(..., ge=0, le=100, description="Profille uyum yüzdesi")
    gerekce: str = Field(..., description="Baskın kişilik tiplerine dayanan 1-2 cümlelik gerekçe")
    universiteler: list[UniversityItem] = Field(
        default=[], 
        description="YÖK Atlas veritabanından çekilen üniversite listesi"
    )


class AnalysisResult(BaseModel):
    holland_kodu: str = Field(..., description="Kullanıcının baskın 3 harfli Holland kodu, ör. 'IAS'")
    profil_ozeti: str = Field(..., description="Kullanıcının kişilik profilinin 2-3 cümlelik özeti")
    onerilen_bolumler: list[DepartmentSuggestion] = Field(
        ..., min_items=5, max_items=5, description="Uyum skoruna göre azalan sırada tam 5 bölüm önerisi"
    )


class UniversityDetail(BaseModel):
    university_name: str
    quota: int
    last_min_score: float
    last_min_rank: int


class DetailedDepartmentMatch(BaseModel):
    department_code: str
    department_name: str
    uyum_skoru: int
    gerekce: str
    universities: list[UniversityDetail]
