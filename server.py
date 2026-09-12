```python
import os
import tempfile

from flask import Flask, request, jsonify, send_from_directory

from python_updated import (
    read_txtfile,
    read_pdffile,
    read_frmurl,
    fetch_offer_from_email,
    run_all_checks,
)

app = Flask(__name__)


def error_response(message, status=400):
    """base.html's JS reads data.detail on errors."""
    return jsonify({"detail": message}), status

@app.route("/")
def serve_ui():
    path = os.path.abspath("base.html")
    print("SERVING BASE.HTML FROM:", path)
    return send_from_directory(".", "base.html")


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/read-txt", methods=["POST"])
def read_txt():
    file = request.files.get("file")

    if not file:
        return error_response("No file uploaded.")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        text = read_txtfile(tmp_path)
        return jsonify({"text": text})
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@app.route("/read-pdf", methods=["POST"])
def read_pdf():
    file = request.files.get("file")

    if not file:
        return error_response("No file uploaded.")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        text = read_pdffile(tmp_path)

        if text.startswith("ERROR:"):
            return error_response(text)

        return jsonify({"text": text})

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@app.route("/read-url", methods=["GET"])
def read_url():
    url = request.args.get("url", "")

    if not url:
        return error_response("No URL provided.")

    text = read_frmurl(url)

    if text.startswith("ERROR:"):
        return error_response(text)

    return jsonify({"text": text})


@app.route("/read-email", methods=["POST"])
def read_email():
    data = request.get_json() or {}

    email_address = data.get("email_address", "")
    app_password = data.get("app_password", "")

    text = fetch_offer_from_email(email_address, app_password)

    if text.startswith("ERROR:"):
        return error_response(text)

    return jsonify({"text": text})


@app.route("/verify", methods=["POST"])
def verify():
    data = request.get_json() or {}
    offer_text = data.get("text", "")

    print("\n========== VERIFY INPUT ==========")
    print(offer_text[:1000])
    print("==================================\n")

    if not offer_text.strip():
        return error_response("No offer text provided.")

    result = run_all_checks(offer_text)
    return jsonify(result)


if __name__ == "__main__":
    print("Starting Dexterity verification backend...")
    print("Backend: http://127.0.0.1:8000")
    print("Health:  http://127.0.0.1:8000/health")

    app.run(
        host="127.0.0.1",
        port=8000,
        debug=False,
        use_reloader=False
    )


