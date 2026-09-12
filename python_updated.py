import os
import re
import imaplib
import email
from urllib.request import Request, urlopen

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

from cheak_external_api import check_1_company_exists

from check_2_to_5 import (
    check_2_recruiter_real,
    check_3_salary_viability,
    check_4_email_verification,
    check_5_scam_database,
)

POINTS_PER_CHECK = 20


def read_txtfile(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as exc:
        return f"ERROR: Could not read TXT file: {exc}"


def read_pdffile(file_path):
    try:
        if PdfReader is None:
            return "ERROR: pypdf is not installed."

        reader = PdfReader(file_path)
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        if not text.strip():
            return "ERROR: No readable text found in PDF."

        return text.strip()

    except Exception as exc:
        return f"ERROR: Could not read PDF: {exc}"


def read_frmurl(url):
    try:
        req = Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        with urlopen(req, timeout=15) as response:
            content = response.read()

        text = content.decode("utf-8", errors="ignore")

        text = re.sub(
            r"<script.*?</script>",
            " ",
            text,
            flags=re.DOTALL | re.IGNORECASE
        )

        text = re.sub(
            r"<style.*?</style>",
            " ",
            text,
            flags=re.DOTALL | re.IGNORECASE
        )

        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    except Exception as exc:
        return f"ERROR: Could not read URL: {exc}"


def fetch_offer_from_email(email_address, app_password):
    if not email_address or not app_password:
        return "ERROR: Email address and app password are required."

    mail = None

    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_address, app_password)

        status, _ = mail.select("INBOX")

        if status != "OK":
            return "ERROR: Could not access mailbox."

        status, messages = mail.search(None, "ALL")

        if status != "OK":
            return "ERROR: Could not search mailbox."

        ids = messages[0].split()

        if not ids:
            return "ERROR: No emails found."

        latest_id = ids[-1]

        status, data = mail.fetch(latest_id, "(RFC822)")

        if status != "OK":
            return "ERROR: Could not read latest email."

        msg = email.message_from_bytes(data[0][1])
        parts = []

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() != "text/plain":
                    continue

                payload = part.get_payload(decode=True)

                if payload:
                    parts.append(
                        payload.decode(
                            "utf-8",
                            errors="ignore"
                        )
                    )
        else:
            payload = msg.get_payload(decode=True)

            if payload:
                parts.append(
                    payload.decode(
                        "utf-8",
                        errors="ignore"
                    )
                )

        text = "\n".join(parts).strip()

        if not text:
            return "ERROR: Latest email contains no readable text."

        return text

    except Exception as exc:
        return f"ERROR: Could not read email: {exc}"

    finally:
        if mail is not None:
            try:
                mail.logout()
            except Exception:
                pass


def run_all_checks(offer_text: str) -> dict:
    if not offer_text or not offer_text.strip():
        return {
            "score": 0,
            "checks": {
                f"check_{i}": {
                    "passed": None,
                    "points": 0,
                    "reason": "No offer text was provided."
                }
                for i in range(1, 6)
            }
        }

    results = {}
    total_score = 0

    try:
        check_1 = check_1_company_exists(offer_text)

        if not isinstance(check_1, dict):
            check_1 = {
                "passed": None,
                "points": 0,
                "reason": "Invalid Check 1 result."
            }

    except Exception as exc:
        check_1 = {
            "passed": None,
            "points": 0,
            "reason": f"Check 1 failed safely: {exc}"
        }

    try:
        points = int(check_1.get("points", 0))
    except (TypeError, ValueError):
        points = 0

    check_1["points"] = max(
        0,
        min(POINTS_PER_CHECK, points)
    )

    check_1.setdefault("passed", None)
    check_1.setdefault("reason", "No reason was provided.")

    results["check_1"] = check_1
    total_score += check_1["points"]

    checks = {
        "check_2": check_2_recruiter_real,
        "check_3": check_3_salary_viability,
        "check_4": check_4_email_verification,
        "check_5": check_5_scam_database,
    }

    for name, function in checks.items():
        try:
            result = function(
                offer_text,
                check_1
            )

            if not isinstance(result, dict):
                result = {
                    "passed": None,
                    "points": 0,
                    "reason": "Invalid check result."
                }

            try:
                points = int(result.get("points", 0))
            except (TypeError, ValueError):
                points = 0

            result["points"] = max(
                0,
                min(POINTS_PER_CHECK, points)
            )

            result.setdefault("passed", None)
            result.setdefault("reason", "No reason was provided.")

            results[name] = result
            total_score += result["points"]

        except Exception as exc:
            results[name] = {
                "passed": None,
                "points": 0,
                "reason": f"Check failed safely: {exc}"
            }

    return {
        "score": max(0, min(100, total_score)),
        "checks": results
    }
