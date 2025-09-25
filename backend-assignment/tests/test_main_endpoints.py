from fastapi.testclient import TestClient
from app.main import app
import io, csv

client = TestClient(app)

def test_endpoints_flow():
    # POST /offer
    offer_payload = {
        "name": "AI Outreach Automation",
        "value_props": ["24/7 outreach","6x more meetings"],
        "ideal_use_cases": ["B2B SaaS mid-market"],
        "icp_industries": ["B2B SaaS"]
    }
    r = client.post("/offer", json=offer_payload)
    assert r.status_code == 200

    # Prepare CSV for leads
    rows = [["name","role","company","industry","location","linkedin_bio"],
            ["Ava Patel","Head of Growth","FlowMetrics","B2B SaaS","India","Experienced growth leader"]]
    csvfile = io.StringIO()
    writer = csv.writer(csvfile)
    writer.writerows(rows)
    csvfile.seek(0)

    files = {"file": ("leads.csv", csvfile.getvalue(), "text/csv")}
    r = client.post("/leads/upload", files=files)
    assert r.status_code == 200
    assert r.json().get("count",0) == 1

    # Run scoring (should succeed even without OPENAI key)
    r = client.post("/score")
    assert r.status_code == 200
    results = r.json()
    assert isinstance(results, list)
    assert len(results) == 1
    item = results[0]
    assert "name" in item and "intent" in item and "score" in item
