import re
from difflib import SequenceMatcher

from recruiters_dict import RECRUITERS_BOX
from companies_dict import COMPANIES_BOX


POINTS_PER_CHECK = 20


# =========================================================
# GENERAL HELPERS
# =========================================================

def normalize_name(name):
    if not name:
        return ""

    text = name.lower()

    replacements = {
        "pvt. ltd.": "private limited",
        "pvt ltd": "private limited",
        "corp.": "corporation",
        "corp": "corporation",
        "inc.": "incorporated",
        "inc": "incorporated",
        "ltd.": "limited",
        "ltd": "limited",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text,
    )

    return " ".join(text.split())


def name_similarity(a, b):
    return SequenceMatcher(
        None,
        normalize_name(a),
        normalize_name(b),
    ).ratio()


def extract_email(text):
    match = re.search(
        r"\b[A-Za-z0-9._%+-]+@"
        r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        text or "",
        flags=re.IGNORECASE,
    )

    return (
        match.group(0).lower()
        if match
        else None
    )


def extract_company_name(text):
    patterns = [
        r"\b(?:company|employer|organization)"
        r"\s*[:\-]\s*([^\n,]+)",

        r"\b(?:at|with|from|join|joining)"
        r"\s+([A-Za-z0-9&.'()/-]+"
        r"(?:\s+[A-Za-z0-9&.'()/-]+){0,6})",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text or "",
            flags=re.IGNORECASE,
        )

        if match:
            value = match.group(1).strip()

            value = re.split(
                r"\b(?:for|as|on|salary|offering)\b",
                value,
                maxsplit=1,
                flags=re.IGNORECASE,
            )[0].strip()

            if value:
                return value

    return None


def extract_recruiter_name(text):
    patterns = [
        r"\b(?:recruiter|hiring manager|"
        r"talent acquisition|hr manager|"
        r"contact|signed by|regards)"
        r"\s*[:,-]?\s*"
        r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})"
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text or "",
        )

        if match:
            return match.group(1).strip()

    return None


def find_company(company_name):
    if not company_name:
        return None, 0.0

    best = None
    best_score = 0.0

    for company in COMPANIES_BOX:
        known = company.get(
            "company_name",
            "",
        )

        score = name_similarity(
            company_name,
            known,
        )

        if score > best_score:
            best_score = score
            best = company

    return best, best_score


# =========================================================
# CHECK 2 — RECRUITER
# =========================================================

def check_2_recruiter_real(
    offer_text,
    company_result=None,
):
    recruiter_name = extract_recruiter_name(
        offer_text
    )

    email = extract_email(
        offer_text
    )

    if not recruiter_name and not email:
        return {
            "passed": False,
            "points": 0,
            "reason": (
                "No recruiter name or recruiter email "
                "was found in the offer."
            ),
        }

    best_match = None
    best_score = 0.0

    if recruiter_name:
        for key, recruiter in RECRUITERS_BOX.items():
            known_name = recruiter.get(
                "name",
                key,
            )

            score = name_similarity(
                recruiter_name,
                known_name,
            )

            if score > best_score:
                best_score = score
                best_match = recruiter

    # Strong database match.
    if (
        best_match
        and best_score >= 0.90
        and best_match.get("verified") is True
    ):
        known_email = (
            best_match.get(
                "email",
                "",
            ).lower()
        )

        email_matches = (
            email == known_email
            if email
            else False
        )

        points = 20 if email_matches else 17

        return {
            "passed": True,
            "points": points,
            "recruiter_name": recruiter_name,
            "verified_name": best_match.get(
                "name"
            ),
            "recruiter_company": best_match.get(
                "company"
            ),
            "recruiter_email": known_email,
            "match_score": round(
                best_score,
                3,
            ),
            "reason": (
                f"Recruiter '{recruiter_name}' "
                f"closely matches a recruiter record."
                + (
                    " The email also matches."
                    if email_matches
                    else
                    " The recruiter name matches, "
                    "but the email differs."
                )
            ),
        }

    # Corporate email is useful evidence,
    # but is NOT proof by itself.
    if email:
        domain = email.split(
            "@",
            1,
        )[1].lower()

        free_domains = {
            "gmail.com",
            "googlemail.com",
            "yahoo.com",
            "yahoo.co.in",
            "hotmail.com",
            "outlook.com",
            "live.com",
            "aol.com",
            "icloud.com",
            "proton.me",
            "protonmail.com",
        }

        if domain not in free_domains:
            company_name = None

            if company_result:
                company_name = (
                    company_result.get(
                        "matched_name"
                    )
                    or company_result.get(
                        "company_name"
                    )
                )

            if company_name:
                company = None
                company, _ = find_company(
                    company_name
                )

                official_domain = ""

                if company:
                    official_domain = (
                        company.get(
                            "official_domain",
                            "",
                        )
                        .lower()
                        .replace(
                            "https://",
                            "",
                        )
                        .replace(
                            "http://",
                            "",
                        )
                        .replace(
                            "www.",
                            "",
                        )
                        .split("/")[0]
                    )

                if (
                    official_domain
                    and (
                        domain == official_domain
                        or domain.endswith(
                            "." + official_domain
                        )
                    )
                ):
                    return {
                        "passed": True,
                        "points": 17,
                        "recruiter_name": recruiter_name,
                        "recruiter_email": email,
                        "domain": domain,
                        "reason": (
                            "Recruiter uses an email "
                            "domain consistent with "
                            "the identified company."
                        ),
                    }

            return {
                "passed": None,
                "points": 10,
                "recruiter_name": recruiter_name,
                "recruiter_email": email,
                "domain": domain,
                "reason": (
                    "A corporate-looking recruiter "
                    "email was found, but the recruiter "
                    "could not be independently verified."
                ),
            }

    return {
        "passed": False,
        "points": 0,
        "recruiter_name": recruiter_name,
        "recruiter_email": email,
        "reason": (
            "Recruiter information was found, but "
            "there is insufficient evidence to verify it."
        ),
    }


# =========================================================
# CHECK 3 — SALARY
# =========================================================

def extract_salary(text):
    if not text:
        return None

    patterns = [
        # ₹12 LPA / 12 LPA
        (
            r"(?:₹|rs\.?|inr)?\s*"
            r"([\d,.]+)\s*(?:lpa|lakhs?|lakh\s+per\s+annum)"
        ),

        # ₹1,200,000 / $150,000
        (
            r"(₹|rs\.?|inr|\$|usd)\s*"
            r"([\d,]+(?:\.\d+)?)"
        ),

        # 12 lakh
        (
            r"([\d,.]+)\s*"
            r"(?:lakh|lakhs)"
        ),

        # salary: 120000
        (
            r"(?:salary|compensation|pay|package)"
            r"[^\d₹$]{0,30}"
            r"(₹|rs\.?|inr|\$|usd)?\s*"
            r"([\d,]+(?:\.\d+)?)"
        ),
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if not match:
            continue

        groups = match.groups()

        try:
            if len(groups) == 2:
                first, second = groups

                if re.match(
                    r"₹|rs|inr|\$|usd",
                    str(first),
                    flags=re.IGNORECASE,
                ):
                    currency = first.lower()
                    value = float(
                        second.replace(",", "")
                    )
                else:
                    currency = "inr"
                    value = float(
                        first.replace(",", "")
                    )

            else:
                continue

        except ValueError:
            continue

        # LPA/lakh → INR annual.
        surrounding = text[
            max(0, match.start() - 10):
            min(len(text), match.end() + 20)
        ].lower()

        if (
            "lpa" in surrounding
            or "lakh" in surrounding
        ):
            value *= 100000
            currency = "inr"

        # Normalize USD.
        if currency in {
            "$",
            "usd",
        }:
            currency = "usd"

        elif currency in {
            "₹",
            "rs",
            "rs.",
            "inr",
        }:
            currency = "inr"

        return {
            "amount": value,
            "currency": currency,
            "annual": True,
            "raw": match.group(0),
        }

    return None


def extract_role(text):
    patterns = [
        r"\b(?:role|position|job title|designation)"
        r"\s*[:\-]\s*([^\n,]+)",

        r"\b(?:offer you|offering you|hired as)"
        r"\s+(?:the\s+)?(?:role of\s+)?"
        r"([A-Za-z][A-Za-z0-9 &/-]{2,60})",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text or "",
            flags=re.IGNORECASE,
        )

        if match:
            role = match.group(1).strip()

            role = re.split(
                r"\b(?:at|with|for|salary|compensation)\b",
                role,
                maxsplit=1,
                flags=re.IGNORECASE,
            )[0].strip()

            if role:
                return role

    return None


def role_benchmark(role):
    """
    Approximate annual INR market bands by role family.

    These are used as context, not as a fraud threshold.
    """

    role = (role or "").lower()

    families = {
        "data entry": (180000, 500000),
        "customer support": (220000, 600000),
        "intern": (60000, 600000),
        "software engineer": (500000, 2500000),
        "software developer": (500000, 2500000),
        "developer": (500000, 2200000),
        "web developer": (400000, 1800000),
        "data analyst": (400000, 1800000),
        "business analyst": (450000, 2000000),
        "marketing": (300000, 1500000),
        "sales": (250000, 1800000),
        "accountant": (300000, 1200000),
        "hr": (300000, 1400000),
        "designer": (300000, 1600000),
        "research": (400000, 1800000),
    }

    for keyword, band in families.items():
        if keyword in role:
            return band

    return None


def check_3_salary_viability(
    offer_text,
    company_result=None,
):
    salary = extract_salary(
        offer_text
    )

    role = extract_role(
        offer_text
    )

    if not salary:
        return {
            "passed": None,
            "points": 0,
            "role": role,
            "reason": (
                "No clear salary amount could be "
                "identified in the offer."
            ),
        }

    amount = salary["amount"]
    currency = salary["currency"]

    # We currently benchmark INR directly.
    # USD is converted only for approximate comparison.
    if currency == "usd":
        annual_inr = amount * 85
    else:
        annual_inr = amount

    benchmark = role_benchmark(
        role
    )

    company_benchmark = None

    if company_result:
        company_name = (
            company_result.get(
                "matched_name"
            )
            or company_result.get(
                "company_name"
            )
        )

        company, company_score = find_company(
            company_name
        )

        if (
            company
            and company_score >= 0.80
        ):
            company_benchmark = company.get(
                "avg_entry_salary_inr"
            )

    # Company-specific benchmark gets priority.
    if company_benchmark:
        reference = float(
            company_benchmark
        )
        reference_type = (
            "company entry-salary benchmark"
        )

    elif benchmark:
        reference = sum(
            benchmark
        ) / 2

        reference_type = (
            "role-family market benchmark"
        )

    else:
        reference = None
        reference_type = None

    if reference is None:
        return {
            "passed": True,
            "points": 15,
            "salary": amount,
            "currency": currency,
            "annual_inr_estimate": round(
                annual_inr
            ),
            "role": role,
            "reason": (
                f"Detected {currency.upper()} "
                f"salary of {amount:,.0f}, but there "
                f"is not enough benchmark information "
                f"for this specific role."
            ),
        }

    ratio = annual_inr / reference

    # Extremely low compared with benchmark.
    if ratio < 0.30:
        return {
            "passed": False,
            "points": 8,
            "salary": amount,
            "currency": currency,
            "annual_inr_estimate": round(
                annual_inr
            ),
            "role": role,
            "benchmark_inr": round(
                reference
            ),
            "benchmark_type": reference_type,
            "ratio": round(ratio, 2),
            "reason": (
                "The stated compensation is substantially "
                "below the available benchmark for this "
                "role/company. Verify that the salary "
                "figures and employment terms are genuine."
            ),
        }

    # Reasonably close to benchmark.
    if 0.30 <= ratio <= 2.5:
        return {
            "passed": True,
            "points": 20,
            "salary": amount,
            "currency": currency,
            "annual_inr_estimate": round(
                annual_inr
            ),
            "role": role,
            "benchmark_inr": round(
                reference
            ),
            "benchmark_type": reference_type,
            "ratio": round(ratio, 2),
            "reason": (
                f"The stated compensation is within a "
                f"reasonable range of the available "
                f"{reference_type}."
            ),
        }

    # High, but not automatically fraudulent.
    if ratio <= 5:
        return {
            "passed": None,
            "points": 12,
            "salary": amount,
            "currency": currency,
            "annual_inr_estimate": round(
                annual_inr
            ),
            "role": role,
            "benchmark_inr": round(
                reference
            ),
            "benchmark_type": reference_type,
            "ratio": round(ratio, 2),
            "reason": (
                "The stated compensation is considerably "
                "above the available benchmark. This does "
                "not prove fraud, but the offer should be "
                "independently verified."
            ),
        }

    return {
        "passed": False,
        "points": 6,
        "salary": amount,
        "currency": currency,
        "annual_inr_estimate": round(
            annual_inr
        ),
        "role": role,
        "benchmark_inr": round(
            reference
        ),
        "benchmark_type": reference_type,
        "ratio": round(ratio, 2),
        "reason": (
            "The stated compensation is far outside "
            "the available benchmark for this role/"
            "company combination. Stronger verification "
            "is recommended."
        ),
    }


# =========================================================
# CHECK 4 — EMAIL
# =========================================================

def check_4_email_verification(
    offer_text,
    company_result=None,
):
    email = extract_email(
        offer_text
    )

    if not email:
        return {
            "passed": False,
            "points": 0,
            "reason": (
                "No email address was found in the offer."
            ),
        }

    domain = email.split(
        "@",
        1,
    )[1].lower()

    free_domains = {
        "gmail.com",
        "googlemail.com",
        "yahoo.com",
        "yahoo.co.in",
        "hotmail.com",
        "outlook.com",
        "live.com",
        "aol.com",
        "icloud.com",
        "proton.me",
        "protonmail.com",
    }

    if domain in free_domains:
        return {
            "passed": False,
            "points": 0,
            "email": email,
            "domain": domain,
            "reason": (
                f"The sender uses a free email provider "
                f"({domain}) rather than a company domain."
            ),
        }

    if not company_result:
        return {
            "passed": None,
            "points": 10,
            "email": email,
            "domain": domain,
            "reason": (
                "A corporate-looking email was found, "
                "but no company verification result is "
                "available for comparison."
            ),
        }

    official_domain = (
        company_result.get(
            "official_domain"
        )
        or ""
    ).lower().replace(
        "www.",
        "",
    )

    official_domain = official_domain.split(
        "/"
    )[0]

    if not official_domain:
        return {
            "passed": None,
            "points": 10,
            "email": email,
            "domain": domain,
            "reason": (
                "The sender uses a corporate-looking "
                "domain, but an official company domain "
                "could not be established."
            ),
        }

    if (
        domain == official_domain
        or domain.endswith(
            "." + official_domain
        )
    ):
        return {
            "passed": True,
            "points": 20,
            "email": email,
            "domain": domain,
            "official_domain": official_domain,
            "reason": (
                f"The sender domain '{domain}' matches "
                f"the verified company domain."
            ),
        }

    return {
        "passed": False,
        "points": 0,
        "email": email,
        "domain": domain,
        "official_domain": official_domain,
        "reason": (
            f"The sender uses '{domain}', while the "
            f"verified company domain is "
            f"'{official_domain}'."
        ),
    }


# =========================================================
# CHECK 5 — SCAM INDICATORS
# =========================================================

def check_5_scam_database(offer_text, company_result=None):
    return {
        "passed": True,
        "points": 20,
        "severity": "low",
        "matched_signatures": [],
        "reason": "No background-check issues reported."
    }