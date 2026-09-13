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

from eligibility import (
    get_categories,
    get_jobs,
    check_eligibility,
)

from company_finder import (
    get_universities,
    get_branches,
    get_placement,
)


app = Flask(__name__)


# ==========================================================
# CORS
# ==========================================================

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


def error_response(message, status=400):
    return jsonify({"detail": message}), status


# ==========================================================
# BASIC ROUTES
# ==========================================================

@app.route("/")
def serve_ui():
    return send_from_directory(".", "base.html")


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


# ==========================================================
# OFFER VERIFIER
# ==========================================================

@app.route("/read-txt", methods=["POST"])
def read_txt():
    file = request.files.get("file")

    if not file:
        return error_response("No file uploaded.")

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".txt"
    ) as tmp:
        file.save(tmp.name)
        path = tmp.name

    try:
        text = read_txtfile(path)

        if text.startswith("ERROR:"):
            return error_response(text)

        return jsonify({"text": text})

    finally:
        if os.path.exists(path):
            os.remove(path)


@app.route("/read-pdf", methods=["POST"])
def read_pdf():
    file = request.files.get("file")

    if not file:
        return error_response("No file uploaded.")

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as tmp:
        file.save(tmp.name)
        path = tmp.name

    try:
        text = read_pdffile(path)

        if text.startswith("ERROR:"):
            return error_response(text)

        return jsonify({"text": text})

    finally:
        if os.path.exists(path):
            os.remove(path)


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
    data = request.get_json(silent=True) or {}

    email_address = data.get("email_address", "")
    app_password = data.get("app_password", "")

    text = fetch_offer_from_email(
        email_address,
        app_password
    )

    if text.startswith("ERROR:"):
        return error_response(text)

    return jsonify({"text": text})


@app.route("/verify", methods=["POST"])
def verify():
    try:
        data = request.get_json(silent=True) or {}

        offer_text = data.get("text", "")

        if not isinstance(offer_text, str):
            return error_response(
                "Offer text must be a string."
            )

        if not offer_text.strip():
            return error_response(
                "No offer text provided."
            )

        print()
        print("======================================")
        print("       OFFER VERIFICATION")
        print("======================================")
        print("Running verification checks...")
        print()

        result = run_all_checks(offer_text)

        if not isinstance(result, dict):
            return error_response(
                "Verification returned an invalid result.",
                500
            )

        print("Verification completed.")
        print("Score:", result.get("score"))
        print("======================================")
        print()

        return jsonify(result), 200

    except Exception as exc:

        print()
        print("======================================")
        print("          VERIFY ERROR")
        print("======================================")
        print(repr(exc))
        print("======================================")
        print()

        return jsonify({
            "detail": f"Verification backend error: {str(exc)}"
        }), 500


# ==========================================================
# RESUME / JOB ELIGIBILITY
# ==========================================================

@app.route("/job-categories", methods=["GET"])
def job_categories():
    return jsonify({
        "categories": get_categories()
    })


@app.route("/jobs/<category>", methods=["GET"])
def jobs_by_category(category):
    jobs = get_jobs(category)

    if not jobs:
        return error_response(
            "Category not found.",
            404
        )

    return jsonify({
        "category": category,
        "jobs": jobs
    })


@app.route("/analyze-resume", methods=["POST"])
def analyze_resume():
    category = request.form.get("category", "")
    job_title = request.form.get("job", "")
    file = request.files.get("resume")

    if not category:
        return error_response(
            "No category selected."
        )

    if not job_title:
        return error_response(
            "No job selected."
        )

    if not file:
        return error_response(
            "No resume uploaded."
        )

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".docx"
    ) as tmp:
        file.save(tmp.name)
        resume_path = tmp.name

    try:
        result = check_eligibility(
            category,
            job_title,
            resume_path
        )

        return jsonify(result)

    except Exception as exc:
        print("RESUME ERROR:", exc)
        return error_response(str(exc))

    finally:
        if os.path.exists(resume_path):
            os.remove(resume_path)


# ==========================================================
# UNIVERSITY PLACEMENT INTELLIGENCE
# ==========================================================

@app.route("/universities", methods=["GET"])
def universities():
    return jsonify({
        "universities": get_universities()
    })


@app.route("/branches/<path:university>", methods=["GET"])
def branches(university):
    branch_list = get_branches(university)

    if not branch_list:
        return error_response(
            "University not found.",
            404
        )

    return jsonify({
        "university": university,
        "branches": branch_list
    })


@app.route("/placement", methods=["GET"])
def placement():
    university = request.args.get(
        "university",
        ""
    ).strip()

    branch = request.args.get(
        "branch",
        ""
    ).strip()

    year = request.args.get(
        "year",
        "2025"
    ).strip()

    if not university:
        return error_response(
            "University is required."
        )

    if not branch:
        return error_response(
            "Branch is required."
        )

    result = get_placement(
        university,
        branch,
        year
    )

    if not result.get("success"):
        return error_response(
            result.get(
                "message",
                "Placement data unavailable."
            ),
            404
        )

    return jsonify(result)


# ==========================================================
# START SERVER
# ==========================================================

if __name__ == "__main__":

    print()
    print("======================================")
    print("       DEXTERITY BACKEND")
    print("======================================")
    print("Backend:      http://127.0.0.1:8000")
    print("Health:       http://127.0.0.1:8000/health")
    print("Categories    :http://127.0.0.1:8000/job-categories")
    print("Universities: http://127.0.0.1:8000/universities")
    print("Placement:    http://127.0.0.1:8000/placement")
    print("======================================")
    print()

    app.run(
        host="127.0.0.1",
        port=8000,
        debug=False,
        use_reloader=False
    )