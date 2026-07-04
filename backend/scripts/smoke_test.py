"""
Task 1.2 için uçtan uca duman testi (smoke test).

Çalıştırma:
    cd backend
    pip install -r requirements.txt
    cp .env.example .env   # GEMINI_API_KEY'i doldurun
    python -m scripts.smoke_test

Bu script bir test framework'ü değildir; Task 1.2'nin DoD'sini ("kararlı ve
tutarlı 5 bölüm önerisi") manuel olarak gözle doğrulamak için tasarlanmıştır.
"""

import json
import os

from app.llm_service import LLMConfigError, LLMResponseError, analyze_personality
from app.scoring import score_answers

# Araştırıcı + Artistik ağırlıklı örnek cevap seti: bu iki kategoriye ait
# sorulara +1, geri kalanına 0 (Farketmez) veriyoruz.
_ARASTIRICI_ARTISTIK_SORULARI = {
    1, 3, 4, 8, 10, 11, 17, 22, 34, 39, 41, 47, 48, 68, 71, 80,  # Araştırıcı
    6, 14, 31, 32, 42, 44, 45, 50, 62, 72, 74, 78, 81,            # Artistik
}


def _sample_answers() -> dict[int, int]:
    return {no: (1 if no in _ARASTIRICI_ARTISTIK_SORULARI else 0) for no in range(1, 91)}


def test_scoring() -> None:
    print("=== 1) Deterministik puanlama ===")
    profile = score_answers(_sample_answers())
    print(f"Holland kodu: {profile.code}")
    print(f"Puanlar: {profile.scores}")
    assert profile.code[0] in ("I", "A"), "Beklenen: baskın tip Araştırıcı ya da Artistik olmalı"
    print("OK: baskın tipler beklenen kategorilerle uyumlu.\n")


def test_missing_api_key() -> None:
    print("=== 2) API anahtarı eksikken davranış ===")
    original = os.environ.pop("GEMINI_API_KEY", None)
    try:
        analyze_personality(_sample_answers())
        print("BEKLENMEDİK: hata fırlatılmadı!")
    except LLMConfigError as exc:
        print(f"OK: açıklayıcı hata alındı -> {exc}\n")
    finally:
        if original is not None:
            os.environ["GEMINI_API_KEY"] = original


def test_llm_call(n_runs: int = 3) -> None:
    print(f"=== 3) Gemini çağrısı ({n_runs} tekrar, tutarlılık kontrolü) ===")
    if not os.getenv("GEMINI_API_KEY"):
        print("ATLANDI: GEMINI_API_KEY tanımlı değil (backend/.env oluşturun).\n")
        return

    bolum_setleri = []
    for i in range(n_runs):
        try:
            result = analyze_personality(_sample_answers())
        except LLMResponseError as exc:
            print(f"BAŞARISIZ (deneme {i + 1}): {exc}")
            continue

        bolumler = [b.bolum for b in result.onerilen_bolumler]
        assert len(bolumler) == 5, f"Tam 5 bölüm bekleniyordu, {len(bolumler)} geldi"
        assert len(set(bolumler)) == 5, "Bölüm önerilerinde tekrar var"

        print(f"\n-- Deneme {i + 1} --")
        print(f"Holland kodu: {result.holland_kodu}")
        print(f"Profil özeti: {result.profil_ozeti}")
        print(json.dumps([b.model_dump() for b in result.onerilen_bolumler], ensure_ascii=False, indent=2))
        bolum_setleri.append(set(bolumler))

    if len(bolum_setleri) >= 2:
        ortak = set.intersection(*bolum_setleri)
        print(f"\nTutarlılık: {len(ortak)}/5 bölüm tüm denemelerde ortak çıktı.")


if __name__ == "__main__":
    test_scoring()
    test_missing_api_key()
    test_llm_call()
