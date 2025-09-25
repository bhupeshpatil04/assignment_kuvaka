from typing import Tuple
from .models import Lead, Offer
import re

DECISION_MAKER_KEYWORDS = [r"\bHead\b", r"\bVP\b", r"\bDirector\b", r"\bChief\b", r"\bFounder\b", r"\bCEO\b",
    r"\bCRO\b", r"\bCMO\b", r"\bCTO\b", r"\bCPO\b", r"\bPresident\b"]
INFLUENCER_KEYWORDS = [r"\bManager\b", r"\bLead\b", r"\bSenior\b", r"\bOwner\b", r"\bPrincipal\b"]

def role_score(role: str) -> int:
    r = role or ""
    for pat in DECISION_MAKER_KEYWORDS:
        if re.search(pat, r, re.I):
            return 20
    for pat in INFLUENCER_KEYWORDS:
        if re.search(pat, r, re.I):
            return 10
    return 0

def industry_score(lead_industry: str, icp_list: list) -> int:
    if not lead_industry:
        return 0
    li = lead_industry.strip().lower()
    icp_lower = [i.strip().lower() for i in icp_list]
    if li in icp_lower:
        return 20
    for icp in icp_lower:
        if any(token in li for token in icp.split()):
            return 10
    return 0

def completeness_score(lead: Lead) -> int:
    fields = [lead.name, lead.role, lead.company, lead.industry, lead.location, lead.linkedin_bio]
    return 10 if all(f and str(f).strip() for f in fields) else 0

def rule_score(lead: Lead, offer: Offer, global_icp: list) -> int:
    icp = offer.icp_industries or global_icp
    rs = role_score(lead.role) + industry_score(lead.industry, icp) + completeness_score(lead)
    return min(rs, 50)

def map_ai_label_to_points(label: str) -> int:
    label = (label or "").strip().lower()
    if label == "high":
        return 50
    if label == "medium":
        return 30
    return 10
