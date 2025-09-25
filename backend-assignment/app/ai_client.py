import os
from typing import Tuple
from .config import settings
import openai

openai.api_key = settings.OPENAI_API_KEY

PROMPT_TEMPLATE = """
You are given a product/offer and a prospect's profile. Classify the prospect's buying intent as exactly one of: High, Medium, Low.
Requirements:
- Output JSON only containing keys: "intent" and "explanation".
- Use product use-cases and value props to reason.

Product/Offer:
Name: {offer_name}
Value props: {value_props}
Ideal use cases: {ideal_use_cases}

Prospect:
Name: {lead_name}
Role: {role}
Company: {company}
Industry: {industry}
Location: {location}
LinkedIn Bio: {bio}
"""

def call_ai_for_intent(lead, offer) -> Tuple[str, str]:
    if not settings.OPENAI_API_KEY:
        return "Low", "No AI key configured; defaulting to Low."

    prompt = PROMPT_TEMPLATE.format(
        offer_name=offer.name,
        value_props=", ".join(offer.value_props),
        ideal_use_cases=", ".join(offer.ideal_use_cases),
        lead_name=lead.name,
        role=lead.role,
        company=lead.company,
        industry=lead.industry,
        location=lead.location,
        bio=lead.linkedin_bio or ""
    )

    try:
        resp = openai.ChatCompletion.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role":"system","content":"You are a helpful sales-relevance classifier."},
                      {"role":"user","content":prompt}],
            max_tokens=200,
            temperature=0.0
        )
        text = resp.choices[0].message.content.strip()
        import json, re
        json_text = text
        m = re.search(r"\{.*\}", text, re.S)
        if m:
            json_text = m.group(0)
        parsed = json.loads(json_text)
        return parsed.get("intent","Low"), parsed.get("explanation","")
    except Exception as e:
        return "Low", f"AI call failed: {str(e)}"
