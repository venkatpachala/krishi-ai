import os
import json
from typing import List, Optional

try:
    import google.generativeai as genai
except Exception:  # pragma: no cover
    genai = None

SYSTEM_PROMPT = """
You are a Telugu agriculture assistant. Answer in JSON with fields: confidence (0-1), plan {low_risk, standard{text, dosage_units, label_citations}, escalation}, when_not_to_spray, citations, needs_escalation.
"""

def _mock_answer(query: str) -> dict:
    return {
        "confidence": 0.9,
        "plan": {
            "low_risk": "సేంద్రీయ ఎరువు ఉపయోగించండి",
            "standard": {"text": "పెస్టిసైడ్ వాడాలి", "dosage_units": "mL/L", "label_citations": [1]},
            "escalation": ""
        },
        "when_not_to_spray": "వర్షం వస్తే స్ప్రే చేయవద్దు",
        "citations": [{"type":"kb","title":"sample","source":"sample.txt"}],
        "needs_escalation": False
    }

def generate_answer(query: str, context: List[str], image: Optional[str] = None) -> dict:
    if os.getenv("MOCK_LLM", "false").lower() == "true" or genai is None:
        return _mock_answer(query)
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")
    prompt = SYSTEM_PROMPT + "\n" + "\n".join(context) + f"\nUser: {query}"
    resp = model.generate_content(prompt)
    try:
        return json.loads(resp.text)
    except Exception:
        return _mock_answer(query)
