"""
Task 2.1 — Database Seeding.

DoD: "departments.db dosyasi yerelde basariyla olusmali ve icinde MVP
verileri yer almali."

ONEMLI NOT: Asagidaki puan/siralama/kontenjan degerleri resmi YOK Atlas'tan
kazinmis GERCEK veri DEGILDIR — ham kaynak dosya (tablo4_01082025d (2).xls)
ekip icinde henuz paylasilmadigi icin MVP'yi calisir durumda tutmak amaciyla
gercekci ARALIKLARDA elle hazirlanmis ornek (seed) veridir. Ham veri elde
edildiginde extract_data.py + bu dosyadaki SEED_DATA, gercek YOK Atlas
kayitlariyla degistirilmelidir.

Calistirma:
    cd backend
    python -m app.db.seed
"""

from app.db.database import get_session, init_db
from app.db.models import YokAtlasData

# department_code, department_name, university_name, quota, last_min_score, last_min_rank
SEED_DATA: list[tuple[str, str, str, int, float, int]] = [
    # --- bilgisayar_muh ---
    ("bilgisayar_muh", "Bilgisayar Mühendisliği", "Boğaziçi Üniversitesi", 100, 545.32, 2100),
    ("bilgisayar_muh", "Bilgisayar Mühendisliği", "İstanbul Teknik Üniversitesi (İTÜ)", 120, 542.31, 3200),
    ("bilgisayar_muh", "Bilgisayar Mühendisliği", "Orta Doğu Teknik Üniversitesi (ODTÜ)", 150, 538.77, 4100),
    ("bilgisayar_muh", "Bilgisayar Mühendisliği", "İhsan Doğramacı Bilkent Üniversitesi", 80, 520.10, 6800),
    ("bilgisayar_muh", "Bilgisayar Mühendisliği", "Yıldız Teknik Üniversitesi", 130, 498.45, 10200),
    ("bilgisayar_muh", "Bilgisayar Mühendisliği", "Sakarya Üniversitesi", 90, 421.60, 38000),

    # --- endustri_muh ---
    ("endustri_muh", "Endüstri Mühendisliği", "Boğaziçi Üniversitesi", 90, 520.44, 5600),
    ("endustri_muh", "Endüstri Mühendisliği", "İstanbul Teknik Üniversitesi (İTÜ)", 110, 505.18, 7400),
    ("endustri_muh", "Endüstri Mühendisliği", "Orta Doğu Teknik Üniversitesi (ODTÜ)", 130, 498.90, 9100),
    ("endustri_muh", "Endüstri Mühendisliği", "Sabancı Üniversitesi", 60, 480.25, 15800),
    ("endustri_muh", "Endüstri Mühendisliği", "Kocaeli Üniversitesi", 100, 402.15, 42000),

    # --- makine_muh ---
    ("makine_muh", "Makine Mühendisliği", "İstanbul Teknik Üniversitesi (İTÜ)", 140, 495.60, 9800),
    ("makine_muh", "Makine Mühendisliği", "Orta Doğu Teknik Üniversitesi (ODTÜ)", 150, 488.32, 11200),
    ("makine_muh", "Makine Mühendisliği", "Yıldız Teknik Üniversitesi", 160, 460.75, 19500),
    ("makine_muh", "Makine Mühendisliği", "Gazi Üniversitesi", 120, 415.20, 34000),
    ("makine_muh", "Makine Mühendisliği", "Erciyes Üniversitesi", 100, 375.40, 55000),

    # --- psikoloji ---
    ("psikoloji", "Psikoloji", "Boğaziçi Üniversitesi", 60, 505.80, 8200),
    ("psikoloji", "Psikoloji", "Koç Üniversitesi", 50, 495.30, 9700),
    ("psikoloji", "Psikoloji", "Hacettepe Üniversitesi", 90, 460.55, 16400),
    ("psikoloji", "Psikoloji", "Ankara Üniversitesi", 100, 430.10, 26000),
    ("psikoloji", "Psikoloji", "Ege Üniversitesi", 80, 405.25, 37500),

    # --- sosyoloji ---
    ("sosyoloji", "Sosyoloji", "Boğaziçi Üniversitesi", 40, 460.20, 17800),
    ("sosyoloji", "Sosyoloji", "Orta Doğu Teknik Üniversitesi (ODTÜ)", 60, 445.60, 21500),
    ("sosyoloji", "Sosyoloji", "Ankara Üniversitesi", 90, 390.30, 48000),
    ("sosyoloji", "Sosyoloji", "İstanbul Üniversitesi", 100, 375.10, 58000),

    # --- rehberlik_pdr ---
    ("rehberlik_pdr", "Rehberlik ve Psikolojik Danışmanlık", "Hacettepe Üniversitesi", 70, 470.40, 14200),
    ("rehberlik_pdr", "Rehberlik ve Psikolojik Danışmanlık", "Marmara Üniversitesi", 100, 435.75, 24800),
    ("rehberlik_pdr", "Rehberlik ve Psikolojik Danışmanlık", "Gazi Üniversitesi", 90, 415.60, 32000),
    ("rehberlik_pdr", "Rehberlik ve Psikolojik Danışmanlık", "Ondokuz Mayıs Üniversitesi", 80, 385.20, 47000),

    # --- mimarlik ---
    ("mimarlik", "Mimarlık", "İstanbul Teknik Üniversitesi (İTÜ)", 100, 470.80, 15600),
    ("mimarlik", "Mimarlık", "Orta Doğu Teknik Üniversitesi (ODTÜ)", 90, 455.30, 19200),
    ("mimarlik", "Mimarlık", "Yıldız Teknik Üniversitesi", 110, 425.60, 27500),
    ("mimarlik", "Mimarlık", "Selçuk Üniversitesi", 70, 380.40, 46000),

    # --- istatistik ---
    ("istatistik", "İstatistik", "Orta Doğu Teknik Üniversitesi (ODTÜ)", 60, 460.90, 16800),
    ("istatistik", "İstatistik", "Hacettepe Üniversitesi", 80, 420.35, 29500),
    ("istatistik", "İstatistik", "Ankara Üniversitesi", 90, 390.60, 44000),
    ("istatistik", "İstatistik", "Dokuz Eylül Üniversitesi", 70, 370.20, 52000),

    # --- isletme ---
    ("isletme", "İşletme", "Boğaziçi Üniversitesi", 80, 500.50, 8900),
    ("isletme", "İşletme", "Koç Üniversitesi", 60, 490.20, 10100),
    ("isletme", "İşletme", "Marmara Üniversitesi", 150, 430.70, 26500),
    ("isletme", "İşletme", "Sakarya Üniversitesi", 120, 390.10, 45000),

    # --- hukuk ---
    ("hukuk", "Hukuk", "İstanbul Üniversitesi", 200, 520.90, 6200),
    ("hukuk", "Hukuk", "Ankara Üniversitesi", 180, 510.40, 7500),
    ("hukuk", "Hukuk", "Marmara Üniversitesi", 220, 470.60, 15400),
    ("hukuk", "Hukuk", "Selçuk Üniversitesi", 150, 420.30, 31000),
]


def seed() -> None:
    init_db()
    with get_session() as session:
        # Idempotent: her seferinde temizleyip yeniden yaz (tekrar tekrar
        # calistirildiginda satirlarin katlanmasini engeller).
        session.query(YokAtlasData).delete()

        rows = [
            YokAtlasData(
                department_code=code,
                department_name=name,
                university_name=uni,
                quota=quota,
                last_min_score=score,
                last_min_rank=rank,
            )
            for code, name, uni, quota, score, rank in SEED_DATA
        ]
        session.add_all(rows)
        session.commit()

        print(f"[OK] {len(rows)} satır seed edildi -> {session.bind.url}")


if __name__ == "__main__":
    seed()
