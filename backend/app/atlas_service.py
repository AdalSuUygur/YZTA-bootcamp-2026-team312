import sqlite3
import os
from app.schemas import UniversityItem

# Veritabanı dosyasının yolu
DB_PATH = "assets/yok_atlas.db"

def get_universities_by_department(bolum_adi: str, limit: int = 5) -> list[UniversityItem]:
    """
    Verilen bölüm adına göre SQLite veritabanından en iyi üniversiteleri
    taban puana göre azalan sırada çeker ve UniversityItem listesi olarak döner.
    """
    # Eğer veritabanı dosyası yoksa veya bulamazsa boş liste dönüp çökmesini engelliyoruz
    if not os.path.exists(DB_PATH):
        print(f"[Uyarı] Veritabanı dosyası bulunamadı: {DB_PATH}")
        return []

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Kolon isimleriyle erişmek için
        cursor = conn.cursor()
        
        # Bölüm adına göre taban puana göre sıralayıp çeken SQL sorgusu
        # LIKE kullanarak (Örn: "%Bilgisayar Mühendisliği%") eşleşmeleri yakalıyoruz
        query = """
            SELECT universite_adi, fakulte, taban_puan, siralama, kontenjan 
            FROM bolumler 
            WHERE bolum_adi LIKE ? 
            ORDER BY taban_puan DESC 
            LIMIT ?
        """
        
        cursor.execute(query, (f"%{bolum_adi}%", limit))
        rows = cursor.fetchall()
        
        universities = []
        for row in rows:
            universities.append(
                UniversityItem(
                    universite_adi=row["universite_adi"] if "universite_adi" in row.keys() else "Bilinmeyen Üniversite",
                    fakulte=row["fakulte"] if "fakulte" in row.keys() else None,
                    taban_puan=row["taban_puan"] if "taban_puan" in row.keys() else None,
                    siralama=row["siralama"] if "siralama" in row.keys() else None,
                    kontenjan=row["kontenjan"] if "kontenjan" in row.keys() else None
                )
            )
        conn.close()
        return universities

    except Exception as e:
        print(f"[SQL Hatası] '{bolum_adi}' verileri çekilirken hata oluştu: {e}")
        return []
