from app.scoring import role_score, industry_score, completeness_score, rule_score
from app.models import Lead, Offer

def make_lead(**kwargs):
    defaults = dict(
        name="A",
        role="Head of Growth",
        company="FlowMetrics",
        industry="B2B SaaS",
        location="India",
        linkedin_bio="Experienced growth leader"
    )
    defaults.update(kwargs)
    return Lead(**defaults)

def test_role_score():
    assert role_score("Head of Growth") == 20
    assert role_score("VP Sales") == 20
    assert role_score("Marketing Manager") == 10
    assert role_score("Intern") == 0

def test_industry_score():
    icp = ["B2B SaaS","Fintech"]
    assert industry_score("B2B SaaS", icp) == 20
    assert industry_score("SaaS platform", icp) == 10
    assert industry_score("Healthcare", icp) == 0

def test_completeness_score():
    lead = make_lead()
    assert completeness_score(lead) == 10
    lead2 = make_lead(linkedin_bio="")
    assert completeness_score(lead2) == 0

def test_rule_score_combined():
    lead = make_lead()
    offer = Offer(name="X", value_props=["a"], ideal_use_cases=["B2B SaaS"])
    rs = rule_score(lead, offer, ["B2B SaaS"])
    assert rs == 50
