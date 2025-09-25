from typing import List
from .models import Offer, Lead

_offer: Offer | None = None
_leads: List[Lead] = []

def set_offer(offer: Offer):
    global _offer
    _offer = offer

def get_offer() -> Offer | None:
    return _offer

def add_leads(leads: List[Lead]):
    global _leads
    _leads = leads

def get_leads() -> List[Lead]:
    return _leads

def clear_all():
    global _offer, _leads
    _offer = None
    _leads = []
