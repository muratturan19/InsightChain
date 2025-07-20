from typing import Dict


def hunterio_lookup(company: str) -> Dict[str, str]:
    """Placeholder lookup via Hunter.io"""
    return {"hunter": f"Contact info for {company}"}


def clearbit_lookup(company: str) -> Dict[str, str]:
    """Placeholder lookup via Clearbit"""
    return {"clearbit": f"Enriched data for {company}"}


def apollo_api(company: str) -> Dict[str, str]:
    """Placeholder lookup via Apollo API"""
    return {"apollo": f"Apollo data for {company}"}
