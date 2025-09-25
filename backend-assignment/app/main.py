from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import pandas as pd
from io import StringIO, BytesIO
from typing import List
from .models import Offer, Lead, ScoredLead
from .storage import set_offer, add_leads, get_leads, get_offer
from .scoring import rule_score, map_ai_label_to_points
from .ai_client import call_ai_for_intent
from .config import settings

app = FastAPI(title="Lead Intent Scoring Service")

@app.post("/offer")
async def post_offer(offer: Offer):
    set_offer(offer)
    return {"status":"ok", "message":"Offer stored"}

@app.post("/leads/upload")
async def upload_leads(file: UploadFile = File(...)):
    if file.content_type not in ("text/csv", "application/vnd.ms-excel", "text/plain"):
        raise HTTPException(status_code=400, detail="Upload a CSV file")
    content = await file.read()
    try:
        df = pd.read_csv(StringIO(content.decode('utf-8')))
    except Exception:
        df = pd.read_csv(StringIO(content.decode('latin-1')))
    expected = ["name","role","company","industry","location","linkedin_bio"]
    missing = [c for c in expected if c not in df.columns]
    if missing:
        raise HTTPException(status_code=400, detail=f"Missing columns: {missing}")
    leads = [Lead(**{c:str(row.get(c,'')) for c in expected}) for _,row in df.iterrows()]
    add_leads(leads)
    return {"status":"ok", "count": len(leads)}

@app.post("/score")
async def run_scoring():
    offer = get_offer()
    if not offer:
        raise HTTPException(status_code=400, detail="No offer configured. POST /offer first.")
    leads = get_leads()
    results: List[ScoredLead] = []
    for lead in leads:
        rscore = rule_score(lead, offer, settings.ICP_INDUSTRIES)
        ai_label, ai_explanation = call_ai_for_intent(lead, offer)
        ai_points = map_ai_label_to_points(ai_label)
        final_score = max(0, min(100, rscore + ai_points))
        results.append(ScoredLead(**lead.dict(), intent=ai_label, score=int(final_score), reasoning=ai_explanation))
    return results

@app.get("/results")
async def get_results():
    return await run_scoring()

@app.get("/results/export")
async def export_csv():
    results = await run_scoring()
    import csv, io
    si = io.StringIO()
    writer = csv.writer(si)
    writer.writerow(["name","role","company","industry","location","intent","score","reasoning"])
    for r in results:
        writer.writerow([r.name, r.role, r.company, r.industry, r.location, r.intent, r.score, r.reasoning])
    output = si.getvalue().encode('utf-8')
    return StreamingResponse(BytesIO(output), media_type="text/csv",
        headers={"Content-Disposition":"attachment; filename=results.csv"})
