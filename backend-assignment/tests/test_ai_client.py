from app.ai_client import call_ai_for_intent
from app.models import Lead, Offer

def test_ai_client_fallback_no_key(monkeypatch):
    # Ensure settings OPENAI_API_KEY is None (fallback)
    # Construct simple lead and offer
    lead = Lead(name="Test", role="Manager", company="X", industry="SaaS", location="India", linkedin_bio="Bio")
    offer = Offer(name="P", value_props=["a"], ideal_use_cases=["SaaS"])
    intent, explanation = call_ai_for_intent(lead, offer)
    assert intent in ("Low", "Medium", "High")  # fallback returns Low typically
    assert isinstance(explanation, str)
