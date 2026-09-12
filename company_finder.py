from placement_data import PLACEMENT_DATA


def get_universities():
    """Return all available universities."""
    return sorted(PLACEMENT_DATA.keys())


def get_branches(university):
    """Return all branches available for a university."""
    if university not in PLACEMENT_DATA:
        return []

    return sorted(PLACEMENT_DATA[university].keys())


def get_placement(university, branch, year="2025"):
    """
    Return placement information for the selected
    university, branch and year.
    """

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
        "highest_package": data.get("highest_package"),
        "company": data.get("company", "Not disclosed"),
        "average_package": data.get("average_package")
    }


# Simple testing
if __name__ == "__main__":

    print("Available Universities:")
    for university in get_universities():
        print("-", university)

    print("\nExample:")
    result = get_placement(
        "VIT Vellore",
        "CSE",
        "2025"
    )

    print(result)