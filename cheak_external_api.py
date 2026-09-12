import html
import re
from difflib import SequenceMatcher
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen

from companies_dict import COMPANIES_BOX

POINTS_PER_CHECK = 20

ENTITY_SUFFIXES = [
    "Private Limited",
    "Pvt. Ltd.",
    "Pvt Ltd",
    "Limited",
    "Ltd.",
    "Ltd",
    "Corporation",
    "Corp.",
    "Corp",
    "Incorporated",
    "Inc.",
    "Inc",
    "LLC",
    "LLP",
    "GmbH",
    "PLC",
    "Company",
    "Co.",
    "Co",
    "Group",
]


# =========================================================
# TEXT / NAME HELPERS
# =========================================================

def normalize_name(name):
    if not name:
        return ""

    text = name.lower()

    replacements = {
        "pvt. ltd.": "private limited",
        "pvt ltd": "private limited",
        "private ltd": "private limited",
        "corp.": "corporation",
        "corp": "corporation",
        "inc.": "incorporated",
        "inc": "incorporated",
        "ltd.": "limited",
        "ltd": "limited",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return " ".join(text.split())


def name_similarity(a, b):
    a = normalize_name(a)
    b = normalize_name(b)

    if not a or not b:
        return 0.0

    return SequenceMatcher(None, a, b).ratio()


def extract_company_name(text):
    if not text:
        return None

    patterns = [
        r"\b(?:company|employer|organization)\s*[:\-]\s*([^\n,]+)",
        r"\b(?:at|with|from|join|joining)\s+"
        r"([A-Za-z0-9&.'()/-]+(?:\s+[A-Za-z0-9&.'()/-]+){0,6})",
    ]

    candidates = []

    for pattern in patterns:
        for match in re.finditer(
            pattern,
            text,
            flags=re.IGNORECASE,
        ):
            value = match.group(1).strip()

            value = re.split(
                r"\b(?:for|as|on|offering|with a salary|salary)\b",
                value,
                maxsplit=1,
                flags=re.IGNORECASE,
            )[0].strip()

            if value:
                candidates.append(value)

    # Prefer names containing a business suffix.
    for candidate in candidates:
        normalized = normalize_name(candidate)

        if any(
            suffix.lower() in normalized
            for suffix in [
                "limited",
                "private limited",
                "corporation",
                "incorporated",
                "llc",
                "llp",
                "gmbh",
                "plc",
            ]
        ):
            return candidate

    if candidates:
        return candidates[0]

    # Last-resort search for known local company names.
    lower_text = text.lower()

    for company in COMPANIES_BOX:
        known = company.get("company_name", "")

        if known and known.lower() in lower_text:
            return known

    return None


def find_local_company(company_name):
    if not company_name:
        return None, 0.0

    best_match = None
    best_score = 0.0

    for company in COMPANIES_BOX:
        known_name = company.get("company_name", "")

        if not known_name:
            continue

        score = name_similarity(
            company_name,
            known_name,
        )

        if score > best_score:
            best_score = score
            best_match = company

    return best_match, best_score


# =========================================================
# WEB SEARCH
# =========================================================

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 "
    "(KHTML, like Gecko) "
    "Chrome/139.0 Safari/537.36"
)


def search_google(company_name):
    query = quote(
        f'"{company_name}" official company website'
    )

    url = (
        "https://www.google.com/search"
        f"?q={query}&num=10"
    )

    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept-Language": "en-US,en;q=0.9",
        },
    )

    try:
        with urlopen(
            request,
            timeout=10,
        ) as response:
            page = response.read().decode(
                "utf-8",
                errors="ignore",
            )

    except Exception:
        return []

    page = html.unescape(page)

    results = []

    # Current/older Google result structures.
    patterns = [
        r'<a[^>]+href="/url\?q=([^"&]+)[^"]*"[^>]*>(.*?)</a>',
        r'<a[^>]+href="(https?://[^"]+)"[^>]*>(.*?)</a>',
    ]

    for pattern in patterns:
        matches = re.findall(
            pattern,
            page,
            flags=re.IGNORECASE | re.DOTALL,
        )

        for raw_url, raw_title in matches:
            parsed = urlparse(raw_url)

            if parsed.netloc.lower().endswith(
                "google.com"
            ):
                continue

            title = re.sub(
                r"<[^>]+>",
                " ",
                raw_title,
            )

            title = re.sub(
                r"\s+",
                " ",
                title,
            ).strip()

            if not title:
                continue

            results.append(
                {
                    "title": title,
                    "url": raw_url,
                    "snippet": "",
                }
            )

    return unique_results(results)[:10]


def search_duckduckgo(company_name):
    query = quote(
        f'"{company_name}" official company website'
    )

    url = (
        "https://html.duckduckgo.com/html/"
        f"?q={query}"
    )

    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
        },
    )

    try:
        with urlopen(
            request,
            timeout=10,
        ) as response:
            page = response.read().decode(
                "utf-8",
                errors="ignore",
            )

    except Exception:
        return []

    results = []

    pattern = (
        r'class="result__a"[^>]+href="([^"]+)"'
        r'[^>]*>(.*?)</a>'
    )

    for raw_url, raw_title in re.findall(
        pattern,
        page,
        flags=re.IGNORECASE | re.DOTALL,
    ):
        title = re.sub(
            r"<[^>]+>",
            " ",
            raw_title,
        )

        title = re.sub(
            r"\s+",
            " ",
            title,
        ).strip()

        if title:
            results.append(
                {
                    "title": title,
                    "url": raw_url,
                    "snippet": "",
                }
            )

    return unique_results(results)[:10]


def unique_results(results):
    unique = []
    seen = set()

    for result in results:
        url = result.get("url", "").strip()

        if not url or url in seen:
            continue

        seen.add(url)
        unique.append(result)

    return unique


# =========================================================
# WEB EVIDENCE
# =========================================================

def domain_matches_company(domain, company_name):
    if not domain or not company_name:
        return False

    domain = domain.lower().replace("www.", "")

    company_words = re.findall(
        r"[a-z0-9]+",
        normalize_name(company_name),
    )

    if not company_words:
        return False

    domain_text = domain.replace(".", " ")

    # Require at least one meaningful company word.
    meaningful = [
        word
        for word in company_words
        if len(word) >= 4
        and word not in {
            "limited",
            "private",
            "corporation",
            "incorporated",
            "company",
            "group",
        }
    ]

    return any(
        word in domain_text
        for word in meaningful
    )


def score_web_evidence(company_name, results):
    if not results:
        return {
            "score": 0.0,
            "best_result": None,
            "official_domain": None,
        }

    best_score = 0.0
    best_result = None

    for result in results:
        title = result.get("title", "")
        url = result.get("url", "")
        snippet = result.get("snippet", "")

        parsed = urlparse(url)
        domain = parsed.netloc.lower().replace(
            "www.",
            "",
        )

        score = 0.0

        title_score = name_similarity(
            company_name,
            title,
        )

        if title_score >= 0.85:
            score += 0.55
        elif title_score >= 0.70:
            score += 0.40
        elif title_score >= 0.50:
            score += 0.25

        if domain_matches_company(
            domain,
            company_name,
        ):
            score += 0.30

        combined = (
            f"{title} {snippet}"
        ).lower()

        if any(
            word in combined
            for word in [
                "official",
                "careers",
                "about us",
                "corporate",
                "investor",
            ]
        ):
            score += 0.10

        score = min(score, 1.0)

        if score > best_score:
            best_score = score
            best_result = result

    official_domain = None

    if best_result:
        official_domain = urlparse(
            best_result.get("url", "")
        ).netloc.lower()

        official_domain = official_domain.replace(
            "www.",
            "",
        )

    return {
        "score": round(best_score, 3),
        "best_result": best_result,
        "official_domain": official_domain,
    }


# =========================================================
# CHECK 1
# =========================================================

def check_1_company_exists(offer_text):
    company_name = extract_company_name(
        offer_text
    )

    if not company_name:
        return {
            "passed": False,
            "points": 0,
            "company_name": None,
            "reason": (
                "No identifiable company name "
                "was found in the offer."
            ),
        }

    local_match, local_score = find_local_company(
        company_name
    )

    results = search_google(
        company_name
    )

    search_source = "Google"

    if not results:
        results = search_duckduckgo(
            company_name
        )
        search_source = "DuckDuckGo"

    evidence = score_web_evidence(
        company_name,
        results,
    )

    web_score = evidence["score"]

    # Strong web evidence.
    if web_score >= 0.75:
        return {
            "passed": True,
            "points": 20,
            "company_name": company_name,
            "matched_name": (
                local_match.get("company_name")
                if local_match and local_score >= 0.80
                else company_name
            ),
            "official_domain": (
                evidence["official_domain"]
            ),
            "local_database_match": (
                local_match is not None
                and local_score >= 0.80
            ),
            "match_score": web_score,
            "search_source": search_source,
            "search_results": results[:5],
            "reason": (
                f"Strong public-web evidence was found "
                f"for '{company_name}'."
            ),
        }

    # Strong local + moderate web evidence.
    if (
        local_match
        and local_score >= 0.90
        and web_score >= 0.45
    ):
        return {
            "passed": True,
            "points": 20,
            "company_name": company_name,
            "matched_name": local_match.get(
                "company_name"
            ),
            "official_domain": local_match.get(
                "official_domain"
            ),
            "local_database_match": True,
            "match_score": round(
                max(
                    local_score,
                    web_score,
                ),
                3,
            ),
            "search_source": search_source,
            "search_results": results[:5],
            "reason": (
                f"'{company_name}' closely matches "
                f"a local company record and has "
                f"supporting web evidence."
            ),
        }

    # Moderate evidence.
    if web_score >= 0.50:
        return {
            "passed": True,
            "points": 10,
            "company_name": company_name,
            "matched_name": (
                local_match.get("company_name")
                if local_match and local_score >= 0.80
                else None
            ),
            "official_domain": (
                evidence["official_domain"]
            ),
            "local_database_match": (
                local_match is not None
                and local_score >= 0.80
            ),
            "match_score": web_score,
            "search_source": search_source,
            "search_results": results[:5],
            "reason": (
                f"Some public-web evidence was found "
                f"for '{company_name}', but it is not "
                f"strong enough for full points."
            ),
        }

    return {
        "passed": False,
        "points": 0,
        "company_name": company_name,
        "matched_name": (
            local_match.get("company_name")
            if local_match and local_score >= 0.80
            else None
        ),
        "official_domain": (
            local_match.get("official_domain")
            if local_match and local_score >= 0.80
            else None
        ),
        "local_database_match": (
            local_match is not None
            and local_score >= 0.80
        ),
        "match_score": web_score,
        "search_source": search_source,
        "search_results": results[:5],
        "reason": (
            f"Insufficient public-web evidence was "
            f"found for '{company_name}'."
        ),
    }