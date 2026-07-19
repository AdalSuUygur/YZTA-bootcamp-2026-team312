"""
Task 2.1/2.2 — LLM çıktısı ile YÖK Atlas veri tabanını birbirine bağlayan
kanonik (sabit) bölüm kodu sözlüğü.

Neden gerekli: LLM'e serbest metin bölüm adı ürettirmek (Task 1.2'deki gibi)
veri tabanı eşleştirmesi için güvenilir değildir ("Bilgisayar Mühendisliği"
vs "Bilgisayar Müh." gibi varyasyonlar join'i kırar). Bunun yerine LLM'e
kapalı bir kod listesi (enum) veriyoruz; Gemini'nin response_schema'sı bu
enum'u zorunlu kıldığı için model listenin dışına çıkamaz.

MVP kapsamında (Task 2.1) 10 bölüm × ~24 üniversite ile sınırlı tutuldu.
Yeni bölüm eklemek için: (1) DEPARTMENTS listesine ekle, (2) db/seed.py'de
o kod için üniversite satırları ekle, (3) system_prompt.py'deki listeyi
yeniden üretmek için build_department_catalog() zaten otomatik kullanılıyor.
"""

from enum import Enum

# (code, resmi YÖK Atlas bölüm adı)
DEPARTMENTS: list[tuple[str, str]] = [
    ("bilgisayar_muh", "Bilgisayar Mühendisliği"),
    ("endustri_muh", "Endüstri Mühendisliği"),
    ("makine_muh", "Makine Mühendisliği"),
    ("psikoloji", "Psikoloji"),
    ("sosyoloji", "Sosyoloji"),
    ("rehberlik_pdr", "Rehberlik ve Psikolojik Danışmanlık"),
    ("mimarlik", "Mimarlık"),
    ("istatistik", "İstatistik"),
    ("isletme", "İşletme"),
    ("hukuk", "Hukuk"),
]

CODE_TO_NAME: dict[str, str] = dict(DEPARTMENTS)

# Pydantic/Gemini response_schema için: LLM yalnızca bu değerlerden birini
# üretebilir (structured output enum kısıtı).
DepartmentCode = Enum("DepartmentCode", {code: code for code, _ in DEPARTMENTS}, type=str)


def build_department_catalog() -> str:
    """system_prompt.py içinde LLM'e gösterilecek 'kod -> isim' listesini üretir."""
    return "\n".join(f'- "{code}" -> {name}' for code, name in DEPARTMENTS)
