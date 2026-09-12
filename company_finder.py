from universities import PLACEMENT_DATA


def get_universities():
    return sorted(PLACEMENT_DATA.keys())


def get_branches(university):
    if university not in PLACEMENT_DATA:
        return []

    return sorted(PLACEMENT_DATA[university].keys())


def get_placement(university, branch, year="2025"):
    if university not in PLACEMENT_DATA:
        return {
            "success": False,
            "message": "University not found."
        }

    if branch not in PLACEMENT_DATA[university]:
        return {
            "success": False,
            "message": "Branch not found."
        }

    if year not in PLACEMENT_DATA[university][branch]:
        return {
            "success": False,
            "message": "Placement data for this year is not available."
        }

    data = PLACEMENT_DATA[university][branch][year]

    return {
        "success": True,
        "university": university,
        "branch": branch,
        "year": year,
        "highest_package": data["highest_package"],
        "company": data["company"],
        "average_package": data["average_package"]
    }
