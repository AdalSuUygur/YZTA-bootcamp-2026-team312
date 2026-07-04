"""
Holland (RIASEC) Mesleki Tercih Envanteri - deterministik puanlama.

Bu modül LLM'e hiç dokunmaz: aynı cevaplar her zaman aynı profili üretir.
Kararlılık/tutarlılık (DoD) bu katmanda garanti edilir; LLM yalnızca bu
profili yorumlayıp bölüm önerisi üretir (bkz. prompts/system_prompt.py).
"""

import json
from pathlib import Path

from pydantic import BaseModel

# assets/questions.json -> repo_root/assets/questions.json
_QUESTIONS_PATH = Path(__file__).resolve().parents[2] / "assets" / "questions.json"

# Türkçe kişilik tipi adı -> RIASEC harfi
TYPE_TO_LETTER = {
    "Gerçekçi": "R",
    "Araştırıcı": "I",
    "Artistik": "A",
    "Sosyal": "S",
    "Girişimci": "E",
    "Geleneksel": "C",
}


class HollandProfile(BaseModel):
    """score_answers() çıktısı; prompt bunun üzerinden kurulur."""

    scores: dict[str, int]          # Türkçe tip adı -> toplam puan
    ranked_types: list[str]         # yüksekten düşüğe Türkçe tip adları
    code: str                        # baskın 3 tipin RIASEC harfleri, ör. "IAS"
    dominant_types: list[str]        # "Tip: belirgin özellikler" (ilk 3 tip)


def _load_questions() -> dict[str, list[dict]]:
    with open(_QUESTIONS_PATH, encoding="utf-8") as f:
        return json.load(f)


def score_answers(answers: dict[int, int]) -> HollandProfile:
    """
    answers: {soru_no: deger} — deger questions.json'daki secenekler.deger
    ile aynı ölçekte olmalı (Hoşlanırım=1, Farketmez=0, Hoşlanmam=-1).

    Cevabı olmayan sorular 0 (Farketmez) sayılır.
    """
    data = _load_questions()
    questions = data["sorular"]
    types_meta = {t["isim"]: t for t in data["kisilikTipleri"]}

    scores = {isim: 0 for isim in types_meta}
    for soru in questions:
        deger = answers.get(soru["no"], 0)
        scores[soru["kategori"]] += deger

    ranked = sorted(scores, key=lambda isim: scores[isim], reverse=True)
    code = "".join(TYPE_TO_LETTER[isim] for isim in ranked[:3])

    dominant_types = [
        f"{isim}: {types_meta[isim]['belirginOzellikler']}" for isim in ranked[:3]
    ]

    return HollandProfile(
        scores=scores,
        ranked_types=ranked,
        code=code,
        dominant_types=dominant_types,
    )
