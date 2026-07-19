"""
Task 2.2 — AI ciktisi (department_code) ile YOK Atlas verilerini eslestiren
SQL servisi.

DoD:
  - department_code alan girdi olarak alindiginda o bolume sahip TUM MVP
    universitelerini last_min_rank ASC sirayla dondurmeli.
  - Bolum veritabaninda hic bulunamazsa uygulama COKMEMELI, bos liste []
    donerek graceful degradation saglamali.
"""

from app.db.database import get_session
from app.db.models import YokAtlasData
from app.schemas import UniversityDetail


def get_universities_by_code(department_code: str) -> list[UniversityDetail]:
    """
    Verilen department_code icin YOK Atlas veritabanindan universiteleri
    basari siralamasina (en iyiden en kotuye) gore cekip doner.

    Veritabani dosyasi yoksa, tablo hazir degilse veya baska bir SQL hatasi
    olusursa uygulamayi cokertmeden bos liste doner.
    """
    try:
        with get_session() as session:
            rows = (
                session.query(YokAtlasData)
                .filter(YokAtlasData.department_code == department_code)
                .order_by(YokAtlasData.last_min_rank.asc())
                .all()
            )
            return [
                UniversityDetail(
                    university_name=row.university_name,
                    quota=row.quota,
                    last_min_score=row.last_min_score,
                    last_min_rank=row.last_min_rank,
                )
                for row in rows
            ]
    except Exception as exc:  # tablo/DB henuz olusturulmamis olabilir
        print(f"[Uyarı] '{department_code}' için üniversite verisi çekilemedi: {exc}")
        return []
