from fastapi.testclient import TestClient
import os, sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[2]))
from api.main import app
from api.db import init_db, SessionLocal
from api.models import Officer

os.environ["MOCK_LLM"] = "true"

client = TestClient(app)

init_db()


def test_ask_endpoint():
    resp = client.post("/api/ask", json={"query": "బనానా పురుగు"})
    assert resp.status_code == 200
    data = resp.json()
    assert "confidence" in data
    assert "plan" in data


def test_feedback_and_escalate():
    ask = client.post("/api/ask", json={"query": "వాతావరణం", "lat":17.4, "lon":78.5}).json()
    db = SessionLocal()
    db.add(Officer(name="Test", phone="000", lat=17.4, lon=78.5))
    db.commit()
    from api.models import QueryLog
    qid = db.query(QueryLog).order_by(QueryLog.id.desc()).first().id
    esc = client.post("/api/escalate", json={"query_id": qid})
    assert esc.status_code == 200
    fb = client.post("/api/feedback", json={"query_id": 1, "rating": 1})
    assert fb.status_code == 200
