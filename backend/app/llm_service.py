"""
Gemini çağrı katmanı — Task 1.2'nin çalıştırılabilir kısmı.

Task 1.4 (API endpoint'i) burada tanımlanan `analyze_personality()` fonksiyonunu
çağıracak; bu modül LLM sağlayıcısı detaylarını (google-genai SDK, response_schema,
retry) tek yerde toplayarak endpoint kodunu sağlayıcıdan bağımsız tutar.

Not: Eski `google-generativeai` paketi tamamen EOL olduğu için (bkz. paket
uyarısı) burada Google'ın güncel birleşik SDK'sı `google-genai` kullanılıyor.
"""

import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import ValidationError

from app.prompts.system_prompt import SYSTEM_PROMPT, build_profile_block
from app.schemas import AnalysisResult
from app.scoring import score_answers

load_dotenv()

MODEL_NAME = "gemini-2.5-flash"
# Düşük temperature: aynı profil için tutarlı öneri seti (DoD gereksinimi).
TEMPERATURE = 0.3
MAX_ATTEMPTS = 2


class LLMConfigError(RuntimeError):
    """GEMINI_API_KEY eksik/geçersiz olduğunda fırlatılır."""


class LLMResponseError(RuntimeError):
    """Model, beklenen şemaya (tam 5 bölüm vb.) uyan bir çıktı üretemediğinde fırlatılır."""


def _get_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise LLMConfigError(
            "GEMINI_API_KEY tanımlı değil. backend/.env dosyasını "
            "backend/.env.example üzerinden oluşturup anahtarınızı girin."
        )
    return genai.Client(api_key=api_key)


def _call_once(client: genai.Client, profile) -> AnalysisResult:
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=build_profile_block(profile),
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=AnalysisResult,
            temperature=TEMPERATURE,
        ),
    )
    return AnalysisResult.model_validate_json(response.text)


def analyze_personality(answers: dict[int, int]) -> AnalysisResult:
    """
    Kullanıcının ham cevaplarından (soru_no -> deger) başlayıp:
      1. Deterministik RIASEC profilini çıkarır (scoring.score_answers),
      2. Sistem promptu + profil ile Gemini'yi çağırır,
      3. Şemaya (tam 5 bölüm) uymayan yanıtı bir kez tekrar dener.

    Başarısız olursa LLMConfigError / LLMResponseError fırlatır.
    """
    profile = score_answers(answers)
    client = _get_client()

    last_error: Exception | None = None
    for _ in range(MAX_ATTEMPTS):
        try:
            return _call_once(client, profile)
        except (ValidationError, ValueError) as exc:
            last_error = exc

    raise LLMResponseError(
        f"Model {MAX_ATTEMPTS} denemede de geçerli bir AnalysisResult üretemedi: {last_error}"
    )
