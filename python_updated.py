import os
import re
import urllib.request
from bs4 import BeautifulSoup

from cheak_external_api import check_1_company_exists

def get_file_text():
    print("Paste your job offer text here:")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines)

def read_txtfile(file_path: str) -> str:
    if not os.path.exists(file_path):
        return "Error: File does not exist."
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="cp1252", errors="replace") as file:
            return file.read()

def read_pdffile(pdf_path: str) -> str:
    try:
        from pypdf import PdfReader
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text.strip()
    except ImportError:
        return "Error: Run 'python -m pip install pypdf' to parse PDF files."
    except Exception as exc:
        return f"Error reading PDF: {exc}"

def read_frmurl(url: str) -> str:
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            html_content = response.read().decode("utf-8", errors="ignore")
        soup = BeautifulSoup(html_content, "html.parser")
        for script in soup(["script", "style"]):
            script.extract()
        return re.sub(r"\s+", " ", soup.get_text(separator=" ")).strip()
    except Exception as exc:
        return f"Error fetching URL: {exc}"

def fetch_offer_from_email(email_address: str, app_password: str,
                           imap_server: str = "imap.gmail.com"):
    import imaplib
    import email
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(email_address, app_password)
        mail.select("inbox")
        status, messages = mail.search(None, '(SUBJECT "Offer")')
        if status != "OK" or not messages or not messages[0]:
            mail.logout()
            return "No job offer emails found."

        email_ids = messages[0].split()
        latest_id = email_ids[-1]
        status, msg_data = mail.fetch(latest_id, "(RFC822)")
        if status != "OK":
            mail.logout()
            return "Could not fetch the latest email."

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            payload = part.get_payload(decode=True)
                            mail.logout()
                            return (payload or b"").decode("utf-8", errors="ignore")
                else:
                    payload = msg.get_payload(decode=True)
                    mail.logout()
                    return (payload or b"").decode("utf-8", errors="ignore")

        mail.logout()
        return "Could not extract offer text from the email."
    except Exception as exc:
        return f"Error reading email: {exc}"

def check_input_file(file_path: str) -> dict:
    extension = os.path.splitext(file_path)[1].lower()
    if extension == ".txt":
        offer_text = read_txtfile(file_path)
    elif extension == ".pdf":
        offer_text = read_pdffile(file_path)
    else:
        return {"passed": None, "points": 0,
                "reason": "Supported input files are .txt and .pdf."}

    if offer_text.startswith("Error:"):
        return {"passed": None, "points": 0, "reason": offer_text}
    return check_1_company_exists(offer_text)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python python_updated.py <input_file>")
    else:
        result = check_input_file(sys.argv[1])
        print("\n=== Company Verification ===")
        print(f"Passed: {result.get('passed')}")
        print(f"Points: {result.get('points', 0)}/20")
        print(f"Reason: {result.get('reason', '')}")
