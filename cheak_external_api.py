import os
import re
import json
from difflib import SequenceMatcher
from urllib.parse import quote
from urllib.request import Request, urlopen

POINTS_PER_CHECK = 20
OPENCORPORATES_URL = "https://api.opencorporates.com/v0.4/companies/search"

ENTITY_SUFFIXES = [
    "Inc", "Inc.", "LLC", "Ltd", "Ltd.", "Limited",
    "Pvt Ltd", "Pvt. Ltd.", "Private Limited",
    "Corp", "Corp.", "Corporation", "GmbH", "PLC",
    "Co.", "LLP", "Group"
]

def _extract_company_name(text: str):
    suffix_pattern = "|".join(
        re.escape(s) for s in sorted(ENTITY_SUFFIXES, key=len, reverse=True)
    )
    pattern = (
        rf"\b([A-Za-z0-9][A-Za-z0-9&.,'()/-]*"
        rf"(?:\s+[A-Za-z0-9][A-Za-z0-9&.,'()/-]*){{0,7}}\s+"
        rf"(?:{suffix_pattern}))\b"
    )
    matches = re.findall(pattern, text or "", flags=re.IGNORECASE)
    return matches[0].strip() if matches else None

def _normalize_name(name: str) -> str:
    name = (name or "").lower()
    replacements = {
        "pvt ltd": "private limited",
        "pvt. ltd.": "private limited",
        "corp.": "corporation",
        "corp": "corporation",
        "inc.": "incorporated",
        "inc": "incorporated",
        "ltd.": "limited",
        "ltd": "limited",
    }
    for old, new in replacements.items():
        name = name.replace(old, new)
    name = "".join(ch if ch.isalnum() or ch.isspace() else " " for ch in name)
    return " ".join(name.split())

def _name_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, _normalize_name(a), _normalize_name(b)).ratio()

def _search_opencorporates(company_name: str):
    token = os.getenv("OPENCORPORATES_API_TOKEN")
    if not token:
        return {"success": False, "error": "OPENCORPORATES_API_TOKEN is not set."}

    params = (
        f"?q={quote(company_name)}"
        f"&order=score&per_page=10&api_token={quote(token)}"
    )
    request = Request(
        OPENCORPORATES_URL + params,
        headers={"User-Agent": "DEXTERITY-JobOfferVerifier/1.0"}
    )

    try:
        with urlopen(request, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
        companies = data.get("results", {}).get("companies", [])
        return {"success": True, "companies": companies}
    except Exception as exc:
        return {"success": False, "error": f"OpenCorporates request failed: {exc}"}

def check_1_company_exists(offer_text: str) -> dict:
    company_name = _extract_company_name(offer_text)

    if not company_name:
        return {
            "passed": False, "points": 0, "company_name": None,
            "reason": "No identifiable company name found in the offer."
        }

    api_result = _search_opencorporates(company_name)

    if not api_result["success"]:
        return {
            "passed": None, "points": 0, "company_name": company_name,
            "reason": api_result["error"]
        }

    companies = api_result["companies"]
    if not companies:
        return {
            "passed": False, "points": 0, "company_name": company_name,
            "reason": f"'{company_name}' was not found in the external company registry."
        }

    best_match = None
    best_score = 0.0
    for item in companies:
        company = item.get("company", {})
        registered_name = company.get("name", "")
        score = _name_similarity(company_name, registered_name)
        if score > best_score:
            best_score = score
            best_match = company

    if best_match and best_score >= 0.80:
        return {
            "passed": True,
            "points": POINTS_PER_CHECK,
            "company_name": company_name,
            "matched_name": best_match.get("name"),
            "jurisdiction": best_match.get("jurisdiction_code"),
            "company_number": best_match.get("company_number"),
            "status": best_match.get("current_status"),
            "registry_url": best_match.get("opencorporates_url"),
            "match_score": round(best_score, 3),
            "reason": f"'{company_name}' matched an external company record."
        }

    return {
        "passed": False,
        "points": 0,
        "company_name": company_name,
        "matched_name": best_match.get("name") if best_match else None,
        "match_score": round(best_score, 3),
        "reason": f"No sufficiently close company-name match was found for '{company_name}'."
    }

def _not_built(name):
    return {
        "passed": None,
        "points": 0,
        "reason": f"{name} is not implemented yet."
    }

def check_2_recruiter_real(offer_text: str) -> dict:
    return _not_built("Recruiter verification")

def check_3_salary_viability(offer_text: str) -> dict:
    return _not_built("Salary and opening viability")

def check_4_email_verification(offer_text: str) -> dict:
    return _not_built("Email verification")

def check_5_scam_database(offer_text: str) -> dict:
    return _not_built("Scam database")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python cheak_external_api.py <input_file>")
        raise SystemExit(1)
    try:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            offer_text = f.read()
    except OSError as exc:
        print(f"Could not read input file: {exc}")
        raise SystemExit(1)

    result = check_1_company_exists(offer_text)
    print(f"Company: {result.get('company_name')}")
    print(f"Passed: {result.get('passed')}")
    print(f"Points: {result.get('points', 0)}/{POINTS_PER_CHECK}")
    print(f"Reason: {result.get('reason')}")
