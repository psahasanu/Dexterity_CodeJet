import re
from docx import Document

from jobs import JOB_DATABASE


# ============================================================
# RESUME TEXT EXTRACTION
# ============================================================

def extract_resume_text(file_path):
    """
    Extract text from a .docx resume.
    """

    try:
        document = Document(file_path)

        paragraphs = []

        for paragraph in document.paragraphs:
            text = paragraph.text.strip()

            if text:
                paragraphs.append(text)

        # Also read tables, because many resumes store
        # education/skills inside tables.
        for table in document.tables:
            for row in table.rows:
                for cell in row.cells:
                    text = cell.text.strip()

                    if text:
                        paragraphs.append(text)

        return "\n".join(paragraphs)

    except Exception as exc:
        raise RuntimeError(
            f"Could not read resume: {exc}"
        )


# ============================================================
# EXPERIENCE PARSING
# ============================================================

def extract_years_of_experience(resume_text):
    """
    Try to determine the candidate's total professional experience.
    """

    text = resume_text.lower()

    patterns = [
        r"(\d+(?:\.\d+)?)\s*\+?\s*years?\s+(?:of\s+)?experience",
        r"experience\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*\+?\s*years?",
    ]

    values = []

    for pattern in patterns:
        matches = re.findall(pattern, text)

        for match in matches:
            try:
                values.append(float(match))
            except ValueError:
                pass

    if values:
        return max(values)

    # Student/fresher fallback
    fresher_words = [
        "fresher",
        "fresh graduate",
        "recent graduate",
        "student",
        "undergraduate",
        "entry level",
    ]

    if any(word in text for word in fresher_words):
        return 0.0

    return 0.0


# ============================================================
# JOB EXPERIENCE REQUIREMENT
# ============================================================

def parse_experience_requirement(experience_string):
    """
    Convert:
        0-1 years  -> 0
        1-3 years  -> 1
        5-8 years  -> 5
        8+ years   -> 8

    We use the LOWER bound as the minimum required experience.
    """

    text = experience_string.lower()

    plus_match = re.search(
        r"(\d+(?:\.\d+)?)\s*\+",
        text
    )

    if plus_match:
        return float(plus_match.group(1))

    range_match = re.search(
        r"(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)",
        text
    )

    if range_match:
        return float(range_match.group(1))

    single_match = re.search(
        r"(\d+(?:\.\d+)?)",
        text
    )

    if single_match:
        return float(single_match.group(1))

    return 0.0


# ============================================================
# SKILL NORMALIZATION
# ============================================================

def normalize_text(text):
    """
    Normalize text so that skill matching is more reliable.
    """

    text = text.lower()

    replacements = {
        "c plus plus": "c++",
        "cplusplus": "c++",
        "c sharp": "c#",
        "js": "javascript",
        "ts": "typescript",
        "postgres": "postgresql",
        "power bi": "powerbi",
        "machine-learning": "machine learning",
        "deep-learning": "deep learning",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


def skill_present(skill, resume_text):
    """
    Check whether a required skill appears in the resume.
    """

    skill_normalized = normalize_text(skill)
    resume_normalized = normalize_text(resume_text)

    # Exact phrase match first
    if skill_normalized in resume_normalized:
        return True

    # Word-based fallback
    words = skill_normalized.split()

    if len(words) > 1:
        return all(
            word in resume_normalized
            for word in words
        )

    return False


# ============================================================
# FIND JOB
# ============================================================

def get_job(category, job_title):
    """
    Find a job from JOB_DATABASE.
    """

    category_jobs = JOB_DATABASE.get(category, [])

    for job in category_jobs:

        if job["title"].lower() == job_title.lower():
            return job

    return None


# ============================================================
# ELIGIBILITY ANALYSIS
# ============================================================

def check_eligibility(category, job_title, resume_path):

    job = get_job(category, job_title)

    if not job:
        return {
            "success": False,
            "error": "Job not found in database."
        }

    resume_text = extract_resume_text(resume_path)

    if not resume_text.strip():
        return {
            "success": False,
            "error": "The resume appears to be empty."
        }

    # --------------------------------------------------------
    # SKILLS
    # --------------------------------------------------------

    required_skills = job.get("requirements", [])

    matched_skills = []
    missing_skills = []

    for skill in required_skills:

        if skill_present(skill, resume_text):
            matched_skills.append(skill)

        else:
            missing_skills.append(skill)

    # --------------------------------------------------------
    # EXPERIENCE
    # --------------------------------------------------------

    candidate_experience = extract_years_of_experience(
        resume_text
    )

    required_experience = parse_experience_requirement(
        job.get("experience", "0 years")
    )

    experience_gap = max(
        0,
        required_experience - candidate_experience
    )

    experience_met = (
        candidate_experience >= required_experience
    )

    # --------------------------------------------------------
    # SCORE
    # --------------------------------------------------------

    total_requirements = len(required_skills)

    if total_requirements > 0:
        skill_score = (
            len(matched_skills) /
            total_requirements
        )
    else:
        skill_score = 1.0

    # Skills = 70%
    # Experience = 30%

    experience_score = (
        1.0 if experience_met else
        min(
            candidate_experience /
            required_experience,
            1.0
        ) if required_experience > 0 else 1.0
    )

    final_score = (
        skill_score * 70
        +
        experience_score * 30
    )

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    if (
        final_score >= 80
        and not missing_skills
        and experience_met
    ):
        status = "Eligible"

    elif final_score >= 40:
        status = "Partially Eligible"

    else:
        status = "Not Eligible"

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    return {
        "success": True,

        "status": status,

        "score": round(final_score, 1),

        "job": job["title"],

        "category": category,

        "matched_requirements": matched_skills,

        "missing_requirements": missing_skills,

        "candidate_experience": candidate_experience,

        "required_experience": required_experience,

        "experience_gap": experience_gap,

        "experience_requirement": job["experience"],

        "total_requirements": total_requirements,

        "matched_count": len(matched_skills),

        "message": (
            "Candidate meets the major requirements."
            if status == "Eligible"
            else
            "Candidate meets some requirements but "
            "needs additional qualifications."
            if status == "Partially Eligible"
            else
            "Candidate currently does not meet enough "
            "of the required qualifications."
        )
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("===== DEXTERITY JOB ELIGIBILITY ENGINE =====")

    print("\nAvailable categories:")

    for category in JOB_DATABASE:
        print(" -", category)

    category = input("\nEnter category: ").strip()

    if category not in JOB_DATABASE:
        print("Invalid category.")
        raise SystemExit

    print("\nAvailable jobs:")

    for job in JOB_DATABASE[category]:
        print(" -", job["title"])

    job_title = input("\nEnter job title: ").strip()

    resume_path = input(
        "\nEnter path to .docx resume: "
    ).strip()

    result = check_eligibility(
        category,
        job_title,
        resume_path
    )

    print("\n===== RESULT =====")

    if not result["success"]:
        print("ERROR:", result["error"])

    else:
        print("Job:", result["job"])
        print("Status:", result["status"])
        print("Score:", result["score"], "/ 100")

        print(
            "\nMatched requirements:"
        )

        for item in result["matched_requirements"]:
            print("  ✓", item)

        print(
            "\nMissing requirements:"
        )

        for item in result["missing_requirements"]:
            print("  ✗", item)

        print(
            "\nCandidate experience:",
            result["candidate_experience"],
            "years"
        )

        print(
            "Required experience:",
            result["experience_requirement"]
        )

        if result["experience_gap"] > 0:
            print(
                "Additional experience needed:",
                result["experience_gap"],
                "years"
            )