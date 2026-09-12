def run_all_checks(offer_text: str) -> dict:
    if not offer_text or not offer_text.strip():
        return {
            "score": 0,
            "checks": {
                f"check_{i}": {
                    "passed": None,
                    "points": 0,
                    "reason": "No offer text was provided.",
                }
                for i in range(1, 6)
            },
        }

    results = {}
    total_score = 0

    # -----------------------------------------------------
    # CHECK 1 FIRST
    # -----------------------------------------------------

    try:
        check_1 = check_1_company_exists(
            offer_text
        )

        if not isinstance(check_1, dict):
            check_1 = {
                "passed": None,
                "points": 0,
                "reason": "Invalid Check 1 result.",
            }

    except Exception as exc:
        check_1 = {
            "passed": None,
            "points": 0,
            "reason": f"Check 1 failed safely: {exc}",
        }

    check_1["points"] = max(
        0,
        min(
            POINTS_PER_CHECK,
            int(check_1.get("points", 0)),
        ),
    )

    results["check_1"] = check_1
    total_score += check_1["points"]

    # -----------------------------------------------------
    # CHECKS 2–5
    # -----------------------------------------------------

    check_functions = {
        "check_2": check_2_recruiter_real,
        "check_3": check_3_salary_viability,
        "check_4": check_4_email_verification,
        "check_5": check_5_scam_database,
    }

    for check_name, check_function in check_functions.items():
        try:
            result = check_function(
                offer_text,
                check_1,
            )

            if not isinstance(result, dict):
                result = {
                    "passed": None,
                    "points": 0,
                    "reason": (
                        "Check returned an invalid result."
                    ),
                }

            try:
                points = int(
                    result.get("points", 0)
                )
            except (
                TypeError,
                ValueError,
            ):
                points = 0

            points = max(
                0,
                min(
                    POINTS_PER_CHECK,
                    points,
                ),
            )

            result["points"] = points

            if "passed" not in result:
                result["passed"] = None

            if "reason" not in result:
                result["reason"] = (
                    "No reason was provided."
                )

            results[check_name] = result
            total_score += points

        except Exception as exc:
            results[check_name] = {
                "passed": None,
                "points": 0,
                "reason": (
                    f"Check failed safely: {exc}"
                ),
            }

    return {
        "score": max(
            0,
            min(100, total_score),
        ),
        "checks": results,
    }